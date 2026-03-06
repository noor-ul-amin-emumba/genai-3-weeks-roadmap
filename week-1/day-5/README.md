# Day-5: Profile RAG (LangChain + Chroma + Groq)

This project builds a beginner-friendly RAG pipeline for your resume/profile.
A user can ask questions about you, and the system answers from resume context.

## What You Will Learn

- `Document Loader`: how PDF text is loaded into LangChain documents.
- `Chunking`: why large text is split into smaller pieces, and which chunking strategy is best when.
- `Embeddings`: how text becomes vectors (numbers).
- `Vector DB (Chroma)`: how vectors are stored and searched.
- `Retriever`: how top relevant chunks are selected, and retrieval strategies explained.
- `LLM (Groq via LangChain)`: how final answers are generated from retrieved context.

## Project Files

- `settings.py`: all config values and paths.
- `utils.py`: small helper checks.
- `ingest.py`: index pipeline (load -> split -> embed -> store).
- `chatbot.py`: query pipeline (retrieve -> prompt -> answer).
- `requirements.txt`: dependencies for this day.
- `.env.example`: environment variable template.

## RAG Pipeline Flow

1. `Indexing phase` (`ingest.py`)

- Load your resume PDF.
- Split it into chunks using `RecursiveCharacterTextSplitter`.
- Convert each chunk into an embedding vector.
- Store vectors in persistent `Chroma` DB.

1. `Query phase` (`chatbot.py`)

- Convert user query into embedding.
- Retrieve top `k` similar chunks from Chroma.
- Send the chunks + question to Groq model.
- Return grounded answer.

## Setup

1. Install dependencies:

```bash
pip install -r week-1/day-5/requirements.txt
```

1. Create env file:

```bash
copy week-1\day-5\.env.example week-1\day-5\.env
```

1. Add your Groq key in `week-1/day-5/.env`:

```env
GROQ_API_KEY=your_real_key
```

## Run

1. Build index:

```bash
python week-1/day-5/ingest.py
```

1. Start chatbot:

```bash
python week-1/day-5/chatbot.py
```

- **Normal mode** (no context shown):

  ```bash
  python week-1/day-5/chatbot.py
  ```

- **Learning mode** (show retrieved chunks per query):

  ```bash
  python week-1/day-5/chatbot.py --show-context
  ```

  The `--show-context` flag displays:
  - All retrieved chunks with their similarity scores
  - Visual bars showing retrieval confidence
  - Interpretation guidelines (scores > 0.7 = high quality)
  - Helps you understand and debug retrieval quality

1. Ask questions like:

- "What are Noor's key skills?"
- "What projects has Noor worked on?"
- "What is Noor's education background?"

---

## Strategy Guide

### Chunking Strategy: Recursive Character Splitting

**Strategy Used:** `RecursiveCharacterTextSplitter` with overlapping chunks.

**How it works:**

1. Splits text recursively by a list of separators: `["\n\n", "\n", " ", ""]`
2. Tries each separator in order; if text is too large, moves to the next finer separator.
3. Maintains `CHUNK_OVERLAP` characters between consecutive chunks (default: 120).
4. Ensures semantic boundaries are respected (paragraphs before sentences before words).

**Why this strategy?** It balances semantic coherence with chunk size, respecting natural boundaries in your resume while maintaining context overlap.

#### Chunking Techniques Explained

| Technique                   | How it works                                            | When to use                                 | Pros                                    | Cons                         |
| --------------------------- | ------------------------------------------------------- | ------------------------------------------- | --------------------------------------- | ---------------------------- |
| **Fixed-Size Chunking**     | Split text every N characters with fixed overlap        | Simple use cases, uniform text              | Fast, predictable                       | Can break mid-sentence       |
| **Recursive Chunking**      | Split hierarchically by separators (para → sent → word) | **Our choice** - General documents, resumes | Respects structure, semantic boundaries | Slightly slower              |
| **Sentence-Based Chunking** | Split by sentence boundaries (`.`, `!`, `?`)            | Documents with clear sentences              | Semantically coherent                   | Varies greatly in chunk size |
| **Section-Based Chunking**  | Split by document structure (headings, sections)        | Technical docs, long-form articles          | Perfect for structured content          | Requires parsing structure   |
| **Token-Based Chunking**    | Split by token count (LLM tokenizer)                    | LLM-aware apps                              | Respects context window                 | Requires tokenizer           |

**Tuning parameters in `.env`:**

- `CHUNK_SIZE=800`: target size per chunk (characters)
- `CHUNK_OVERLAP=120`: overlap between chunks (maintains context)

**Try this:** If the chatbot misses details, increase `CHUNK_OVERLAP` to 200-300 to capture more context.

---

### Retrieval Strategy: Similarity Search (Vector Search)

**Strategy Used:** Cosine Similarity Search with top-k retrieval.

**How it works:**

1. Converts user query to embedding vector using the same model as chunks.
2. Computes cosine similarity between query vector and all chunk vectors.
3. Returns top `K` chunks with highest similarity scores (default: `K=4`).
4. Passes these chunks to the LLM as context.

**Why this strategy?** It's the most common RAG approach—fast, semantic, and works well with dense embeddings.

#### Retrieval Strategies Explained

| Strategy                             | How it works                                           | When to use                            | Pros                         | Cons                        |
| ------------------------------------ | ------------------------------------------------------ | -------------------------------------- | ---------------------------- | --------------------------- |
| **Similarity Search (Vector)**       | **Our choice** - Embed query, find nearest vectors     | General RAG, semantic matching         | Fast, semantic, simple       | Requires good embeddings    |
| **BM25 (Keyword)**                   | Full-text search with TF-IDF scoring                   | Keyword-heavy content, recall focus    | Great for exact terms, cheap | Misses paraphrasing         |
| **Hybrid Search**                    | Combine vector + BM25 results                          | Mixed keyword/semantic queries         | Balanced recall & relevance  | More complex                |
| **MMR (Maximal Marginal Relevance)** | Retrieve similar chunks, then diversify                | When you want different viewpoints     | Reduces redundancy           | Slower than pure similarity |
| **Re-ranking**                       | First retrieve top-k, then re-rank with a better model | Production RAG systems                 | Higher quality results       | Expensive (extra LLM calls) |
| **Metadata Filtering**               | Combine vector search + metadata filters               | Filtered searches (date, author, etc.) | Precise filtering            | Need metadata annotations   |

**Tuning parameter in `.env`:**

- `TOP_K=4`: number of chunks to retrieve (default: 4 is good for most resumes)

**Try this:**

- If you get too generic answers, lower `TOP_K` to 2-3 for more focused context.
- If you miss details, raise `TOP_K` to 6-8 for broader context.

---

## Notes for Learning

- If answers are weak, tune `CHUNK_SIZE`, `CHUNK_OVERLAP`, and `TOP_K` in `.env`.
- Re-run `ingest.py` after updating resume or chunk settings.
- This project uses Groq only for generation. Embeddings are local via sentence-transformers.
- **Experiment:** Try changing chunking strategy by modifying the separators in `ingest.py` line 44.
