"""Build the Chroma vector database from the resume PDF.

RAG Index Phase:
1) Load documents
2) Chunk documents (Recursive Character Splitting Strategy)
3) Create embeddings
4) Store vectors in Chroma

CHUNKING STRATEGY USED: Recursive Character Splitting with Overlap

RecursiveCharacterTextSplitter works by:
1. Trying to split text by a hierarchy of separators: ["\\n\\n", "\\n", " ", ""]
2. Starts with the "largest" separator (paragraphs) and recursively moves to smaller
   separators if chunks are still too large.
3. Automatically maintains semantic boundaries (respects sentence/paragraph structure).
4. Overlaps consecutive chunks by CHUNK_OVERLAP characters to preserve context.

Why use Recursive Chunking?
- Balances semantic coherence with chunk size control.
- Respects natural document structure (paragraphs before sentences).
- Prevents mid-sentence/word splitting that breaks meaning.
- Works well for unstructured text like resumes.

Alternative chunking strategies available:
- FIXED_SIZE: Split every N chars (simple, fast, may break mid-sentence)
- SENTENCE_BASED: Split per sentence (semantic, but highly variable size)
- SECTION_BASED: Split by document structure/headings (best for structured docs)
- TOKEN_BASED: Split by LLM token count (respects context window limits)

Configurable in settings.py:
- CHUNK_SIZE: Target characters per chunk (default: 800)
- CHUNK_OVERLAP: Characters overlapped between chunks (default: 120)
"""

from __future__ import annotations

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from settings import (
    CHROMA_DIR,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    RESUME_PATH,
)
from utils import require_file


class ResumeIndexer:
    """Creates and persists a vector store from the resume file.

    INDEXING PHASE STRATEGY:

    This class orchestrates the entire indexing pipeline:
    1. LOAD: PyPDFLoader reads resume PDF and extracts text
    2. CHUNK: RecursiveCharacterTextSplitter breaks text into overlapping chunks
    3. EMBED: HuggingFaceEmbeddings converts chunks to dense vectors
    4. STORE: Chroma persists vectors and metadata to local disk

    Output: A searchable vector database in chroma_db/ directory

    Typical flow:
        indexer = ResumeIndexer()
        indexer.run()  # Loads PDF -> chunks -> embeds -> stores

    After indexing, chatbot.py can load and query without re-indexing.
    Re-run indexer.py whenever your resume changes or chunk settings are tuned.
    """

    def __init__(self) -> None:
        """Initialize embedder (lazy-loads model on first use).

        Uses HuggingFaceEmbeddings with sentence-transformers/all-mpnet-base-v2:
        - Lightweight model (~22M parameters)
        - Fast inference (~100 embeddings/sec on CPU)
        - 384-dimensional vectors (good semantic quality)
        - Pre-trained on diverse NLI and retrieval tasks

        This same model will be used in chatbot.py for query embedding,
        ensuring query and document embeddings are in the same vector space.
        """
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    def load_documents(self):
        require_file(RESUME_PATH)
        loader = PyPDFLoader(str(RESUME_PATH))
        docs = loader.load()
        print(f"Loaded {len(docs)} PDF page(s) from: {RESUME_PATH.name}")
        return docs

    def load_web_documents(self, url):
        """Load documents from a web page URL.

        This method is not used in the current indexing pipeline but can be
        useful for future extensions where you want to index online content
        instead of (or in addition to) a local PDF.

        Uses WebBaseLoader to fetch and parse the web page content into
        LangChain Document objects. The same chunking and embedding logic
        can then be applied to these documents.

        Args:
            url: The URL of the web page to load
        Returns:
            List of Document objects containing the web page content
        """

        loader = WebBaseLoader(url)
        docs = loader.load()
        print(f"Loaded {len(docs)} document(s) from URL: {url}")
        return docs

    def split_documents(self, docs):
        """Split documents into chunks using Recursive Character Splitting.

        CHUNKING STRATEGY: RecursiveCharacterTextSplitter

        Splits text hierarchically by separators in order: ["\\n\\n", "\\n", " ", ""]
        - First tries to split by double newline (paragraphs)
        - If chunk is still too large, recursively tries single newline (sentences)
        - Then space (words), then character as fallback
        - This ensures semantic boundaries are respected
        - Consecutive chunks overlap by CHUNK_OVERLAP chars for context continuity

        Args:
            docs: List of LangChain Document objects from PyPDFLoader

        Returns:
            List of split Document chunks with metadata preserved
        """
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", " ", ""],
        )
        chunks = splitter.split_documents(docs)
        print(
            f"Created {len(chunks)} chunk(s) with size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP}"
        )
        return chunks

    def build_vector_store(self, chunks) -> Chroma:
        """Build and persist vector store from chunks.

        EMBEDDING & STORAGE STRATEGY:

        Embedding Model: Sentence Transformers (sentence-transformers/all-mpnet-base-v2)
        - Lightweight, fast embedding model (only 22M parameters)
        - Converts text chunks into 384-dimensional dense vectors
        - These vectors capture semantic meaning of text
        - Enables cosine similarity search in vector space

        Vector Store: Chroma (Local Persistent Database)
        - Stores embeddings and original text locally on disk
        - Supports semantic similarity search
        - Can be reloaded from disk without re-computing embeddings
        - Better for development/learning; Pinecone/Weaviate for production

        Args:
            chunks: List of split Document objects

        Returns:
            Chroma vector store (also persists to CHROMA_DIR)
        """
        # Recreate index each time so changes to the resume are reflected immediately.
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=str(CHROMA_DIR),
            collection_name=COLLECTION_NAME,
        )
        print(f"Saved Chroma DB in: {CHROMA_DIR}")
        return vector_store

    def run(self) -> None:

        # docs = self.load_web_documents(
        #     "https://my-portfolio-alpha-ashen-31.vercel.app/")

        docs = self.load_documents()
        chunks = self.split_documents(docs)
        # print chunks with metadata for debugging
        for i, chunk in enumerate(chunks):  # Print first 3 chunks
            print(f"\nChunk {i+1}:")
            # Print first 200 chars
            print(f"Text: {chunk.page_content}")
            print(f"Metadata: {chunk.metadata}")
        self.build_vector_store(chunks)
        print("Indexing complete. You can now run chatbot.py")


if __name__ == "__main__":
    ResumeIndexer().run()
