"""Ask questions about the resume using a LangChain RAG pipeline.

RAG Query Phase:
1) Retrieve relevant chunks from Chroma (Similarity Search Strategy)
2) Inject chunks into the prompt as context
3) Ask Groq LLM to answer from context only

RETRIEVAL STRATEGY USED: Cosine Similarity Search (Vector Search)

How Similarity Search works:
1. Converts user query into embedding vector (same model as chunks)
2. Computes cosine similarity between query vector and all chunk vectors
3. Ranks chunks by similarity score
4. Returns top K (default: 4) most similar chunks
5. Passes these chunks to LLM as grounded context

Why use Similarity Search?
- Fast O(n) search over embedded vectors
- Captures semantic meaning (not just keywords)
- Works well with dense embeddings
- Simple to implement and understand
- Perfect for learning RAG concepts

Alternative retrieval strategies:
- BM25 (Keyword Search): Full-text TF-IDF scoring (exact terms, cheap)
- Hybrid Search: Combines vector + BM25 (balanced recall & relevance)
- MMR (Maximal Marginal Relevance): Diversifies results (reduces redundancy)
- Re-ranking: Retrieve top-k, then re-rank with better model (expensive)
- Metadata Filtering: Vector search + metadata filters (requires annotations)

Configurable in settings.py:
- TOP_K: Number of chunks to retrieve (default: 4)
- EMBEDDING_MODEL: Which embedding model to use (default: all-MiniLM-L6-v2)

USAGE:
python chatbot.py              # Normal mode (no context shown)
python chatbot.py --show-context  # Show retrieved chunks for each query
"""

from __future__ import annotations

import argparse
from typing import Iterable
import os
import sys

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
import numpy as np

from settings import CHROMA_DIR, COLLECTION_NAME, EMBEDDING_MODEL, GROQ_MODEL, TOP_K


class ResumeRAGChatbot:
    """Simple RAG chatbot for resume/profile Q&A.

    RETRIEVAL STRATEGY: Cosine Similarity Search (Vector Search)

    This chatbot uses similarity search to find relevant resume chunks:
    1. User query is embedded into a 384-d vector
    2. Cosine similarity computed against all chunk vectors in Chroma
    3. Top K most similar chunks are retrieved
    4. These chunks become the context for the LLM
    5. LLM answers using ONLY the provided context (grounded answers)

    Similarity Search is ideal for:
    - Semantic matching (captures paraphrasing)
    - Fast retrieval (O(n) with efficient vector index)
    - Learning RAG fundamentals
    - General-purpose document Q&A

    When to use other strategies:
    - BM25: When you need exact keyword matching
    - MMR: When you want diverse results (different viewpoints)
    - Hybrid: When your data has both semantic and keyword aspects
    - Re-ranking: When you need production-quality results (slower)
    """

    def __init__(self) -> None:
        """Initialize RAG pipeline with retriever and LLM.

        RETRIEVAL SETUP (Similarity Search Strategy):

        1. Embeddings: HuggingFaceEmbeddings (all-MiniLM-L6-v2)
           - Same model used in ingest.py for consistency
           - Converts queries into 384-d vectors

        2. Vector Store: Chroma (loads from disk)
           - Loads previously indexed chunks and embeddings
           - Ready for similarity search

        3. Retriever: Chroma.as_retriever() with k=TOP_K
           - Wraps vector store in a standard LangChain retriever interface
           - search_kwargs={"k": TOP_K} retrieves top K similar chunks
           - Internally computes cosine similarity

        4. LLM: ChatOpenAI (Groq API)
           - Uses Groq's OpenAI-compatible endpoint
           - Model: llama-3.1-8b-instant (fast, 8B params)
           - base_url: https://api.groq.com/openai/v1

        5. Prompt: ChatPromptTemplate
           - Forces LLM to use only provided context
           - Structure: [system prompt with context] + [user question]

        When you call .ask(question), this pipeline orchestrates:
        question -> embed -> retrieve chunks -> inject into prompt -> LLM -> answer
        """
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self.vector_store = Chroma(
            persist_directory=str(CHROMA_DIR),
            embedding_function=self.embeddings,
            collection_name=COLLECTION_NAME,
        )
        self.retriever = self.vector_store.as_retriever(
            search_kwargs={"k": TOP_K})
        self.llm = ChatOpenAI(
            model=GROQ_MODEL,
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1",
        )
        self.prompt = ChatPromptTemplate.from_template(
            """
You are a helpful assistant that answers questions about Noor Ul Amin's profile/resume.
Use ONLY the provided context. If the answer is not present, say you do not know based on the resume.

Context:
{context}

Question:
{question}
""".strip()
        )

    @staticmethod
    def _format_docs(docs: Iterable[Document]) -> str:
        """Format retrieved documents into a context string.

        Takes the Document objects returned by similarity search and joins them
        into a readable context block separated by double newlines.

        The order matters: documents are in order of retrieval (most relevant first),
        and the LLM will read them in this order.

        Args:
            docs: Iterable of LangChain Document objects from retriever

        Returns:
            String with document contents joined by newline separators
        """
        return "\n\n".join(doc.page_content for doc in docs)

    def ask(self, question: str) -> str:
        """Answer a question using retrieval-augmented generation.

        RETRIEVAL FLOW (Similarity Search Strategy):

        1. EMBED: Convert question into vector using HuggingFaceEmbeddings
           - Uses all-MiniLM-L6-v2 model (same as chunk embeddings)
           - Produces 384-dimensional vector

        2. SEARCH: Query Chroma for TOP_K most similar chunks
           - Computes cosine similarity: dot(query, chunk) / norm(query) * norm(chunk)
           - Ranks chunks by similarity score (higher = more relevant)
           - Returns top 4 chunks by default

        3. CONTEXT: Format retrieved chunks as context string
           - Joins chunks with newline separators
           - Maintains order from retrieval (most relevant first)

        4. PROMPT: Inject context + question into prompt template
           - Template: "Use context to answer question"
           - Forces LLM to stay grounded in retrieved context

        5. GENERATE: Call Groq LLM to produce answer
           - Uses llama-3.1-8b instant model (fast, 8B parameters)
           - via ChatOpenAI binding to Groq OpenAI-compatible API

        Args:
            question: User's natural language question

        Returns:
            LLM-generated answer grounded in retrieved resume context

        Note:
            The quality of answers depends on:
            - Chunking quality (CHUNK_SIZE, CHUNK_OVERLAP tuning)
            - Retrieval quality (TOP_K tuning)
            - Vector embedding model quality
            - LLM instructions in prompt template
        """
        docs = self.retriever.invoke(question)
        context = self._format_docs(docs)
        messages = self.prompt.format_messages(
            context=context, question=question)
        response = self.llm.invoke(messages)
        return response.content.strip()

    def retrieve_with_scores(self, question: str) -> tuple[list[Document], list[float]]:
        """Retrieve chunks with similarity scores.

        This method performs similarity search and also computes the exact cosine
        similarity scores for visualization and learning purposes.

        RETRIEVAL LEARNING:
        - Similarity score ranges from 0.0 to 1.0
        - Higher scores = more similar (more relevant to the query)
        - Good threshold for relevance is typically > 0.5
        - If all scores are low, consider tweaking CHUNK_SIZE or EMBEDDING_MODEL

        Args:
            question: User's query

        Returns:
            Tuple of (list of Documents, list of similarity scores)
        """
        # Embed the query
        query_embedding = np.array(self.embeddings.embed_query(question))

        # Get all documents from the vector store
        # Note: We retrieve more chunks with higher k to compute scores
        retriever_with_more = self.vector_store.as_retriever(
            search_kwargs={"k": TOP_K}
        )
        docs = retriever_with_more.invoke(question)

        # Compute similarity scores for each retrieved document
        scores = []
        for doc in docs:
            doc_embedding = np.array(
                self.embeddings.embed_query(doc.page_content))
            # Cosine similarity: (A · B) / (||A|| * ||B||)
            dot_product = np.dot(query_embedding, doc_embedding)
            norm_query = np.linalg.norm(query_embedding)
            norm_doc = np.linalg.norm(doc_embedding)
            similarity = dot_product / \
                (norm_query * norm_doc) if norm_query * norm_doc != 0 else 0.0
            # Normalize to 0-1 range (cosine similarity is already in -1 to 1, but embeddings are positive)
            # converts from [-1, 1] to [0, 1]
            similarity = (similarity + 1) / 2
            scores.append(float(similarity))

        return docs, scores

    def print_retrieved_chunks(self, question: str) -> tuple[list[Document], list[float]]:
        """Print retrieved chunks with similarity scores for visualization.

        LEARNING MODE: Shows exactly which chunks were retrieved and why.

        This helps you understand:
        - Whether the retriever found relevant information
        - How confident the system is (similarity scores)
        - If chunks are too small/large (adjust CHUNK_SIZE)
        - If embedding quality is good (all scores > 0.5?)

        Args:
            question: User's query

        Returns:
            Tuple of (list of Documents, list of similarity scores)
        """
        docs, scores = self.retrieve_with_scores(question)

        print("\n" + "=" * 80)
        print("RETRIEVAL ANALYSIS (Similarity Search Strategy)")
        print("=" * 80)
        print(f"Query: {question}\n")
        print(f"Retrieved {len(docs)} chunks (TOP_K={TOP_K}):\n")

        for i, (doc, score) in enumerate(zip(docs, scores), 1):
            # Visual score bar
            bar_length = 30
            filled = int(bar_length * score)
            bar = "█" * filled + "░" * (bar_length - filled)

            print(f"[Chunk {i}] Similarity: {score:.4f} |{bar}|")
            print(f"From page {doc.metadata.get('page', 'unknown')}:")
            print(
                f"  {doc.page_content[:120]}{'...' if len(doc.page_content) > 120 else ''}")
            print()

        print("=" * 80)
        print("INTERPRETATION:")
        print("- Scores > 0.7: Highly relevant (strong match)")
        print("- Scores 0.5-0.7: Moderately relevant")
        print("- Scores < 0.5: Weakly relevant (may contain noise)")
        if all(s > 0.7 for s in scores):
            print("✓ All chunks are highly relevant. Good retrieval quality!")
        elif any(s < 0.3 for s in scores):
            print(
                "⚠ Some chunks have low relevance. Consider tweaking CHUNK_SIZE or TOP_K.")
        print("=" * 80 + "\n")

        return docs, scores


def main() -> None:
    """Interactive chatbot with optional --show-context flag for retrieval visualization.

    Usage:
        python chatbot.py              # Normal mode
        python chatbot.py --show-context  # Show retrieved chunks per query

    When --show-context is enabled:
    - Retrieved chunks are displayed before each answer
    - Similarity scores show how confident the retriever was
    - Helps you understand and debug retrieval quality
    """
    parser = argparse.ArgumentParser(
        description="Resume RAG chatbot with optional retrieval visualization"
    )
    parser.add_argument(
        "--show-context",
        action="store_true",
        help="Print retrieved chunks and similarity scores for each query"
    )
    args = parser.parse_args()

    print("Resume RAG chatbot is ready. Type 'exit' to quit.")
    if args.show_context:
        print("(--show-context mode: Retrieved chunks will be shown for each query)\n")

    bot = ResumeRAGChatbot()

    while True:
        question = input("\nYou: ").strip()
        if question.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break
        if not question:
            continue

        # Show context if flag is set
        if args.show_context:
            bot.print_retrieved_chunks(question)

        answer = bot.ask(question)
        print(f"Bot: {answer}")


if __name__ == "__main__":
    main()
