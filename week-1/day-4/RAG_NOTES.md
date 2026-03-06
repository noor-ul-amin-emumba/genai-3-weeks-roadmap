# RAG (Retrieval-Augmented Generation) Notes

## 1. RAG Flow: Query → Retrieve → Answer

A RAG system works in three stages:

```
User Question
    ↓
[RETRIEVE] Search knowledge base for relevant documents
    ↓
Retrieved Context (top-k chunks)
    ↓
[GENERATE] LLM reads context + question and writes answer
    ↓
Final Answer
```

### Detailed Breakdown:

**Stage 1: Retrieve**

- Convert query to embedding using a fast embedding model (e.g., SentenceTransformer)
- Search vector database for k most similar document chunks
- Rank by cosine similarity score
- Pass top results as context to the LLM

**Stage 2: Generate**

- Combine system prompt + retrieved context + user query
- LLM reads this combined prompt and generates answer
- LLM should only use provided context (instructed not to hallucinate)

**Key advantage:** The LLM can answer questions about documents it never "saw" during training, and answers are grounded in actual text.

---

## 2. Retrieval Failure vs Generation Failure

### Retrieval Failure

**What:** The system fails to find relevant documents for the query.

**Symptoms:**

- Retrieved context is irrelevant or empty
- LLM can't answer because context doesn't contain the answer
- Result: Model correctly says "not in documents" OR gives wrong answer based on bad context

**Cause:**

- Query embedding doesn't match document embeddings (vocabulary mismatch, semantics differ)
- Documents not chunked well (too large/small chunks)
- Low similarity threshold excludes relevant docs
- Knowledge base incomplete (document missing entirely)

**Example:**

- Query: "What is AlphaFold 2?"
- Retrieved: [documents about protein folding in general, but not AlphaFold 2 specifically]
- Result: Wrong or incomplete answer

### Generation Failure

**What:** The correct context is provided, but the LLM fails to use it properly.

**Symptoms:**

- Context IS relevant and contains the answer
- LLM still generates wrong/incomplete answer
- Result: Model wastes good information

**Cause:**

- LLM ignores context and relies on training knowledge (hallucination)
- LLM misinterprets context (reading comprehension failure)
- Prompt is confusing or poorly written
- LLM generates plausible-sounding but false information
- Context is too long and important details buried

**Example:**

- Query: "What is the exact market cap of AI industry in 2024?"
- Retrieved: [5 documents saying "this data not in our documents"]
- LLM Answer: "The global AI market is valued at approximately $500 billion" (HALLUCINATED!)
- Result: Confident but completely wrong

### How to Diagnose:

1. Check retrieved context manually — is it relevant?
2. If YES → Generation failure (LLM failed to use good context properly)
3. If NO → Retrieval failure (system didn't find the right documents)

---

## 3. Why "LLM Answered Confidently But Wrong" Happens

This is called **hallucination** or **confident generation error**.

### Root Causes:

#### A. Model Trained on Internet Data

- LLM trained on vast web text containing contradictory/false information
- LLM learned to generate plausible-sounding text, not necessarily true text
- When uncertain, it defaults to "confident guess"

#### B. Context Ignored or Overridden

```
System: "Answer ONLY based on provided context. Don't make up info."
Context: "This information is not in the documents."
User: "What is X?"
LLM: "X is [something from training data]"  ← Ignored instruction!
```

- LLM sometimes ignores constraints and uses training knowledge
- Stronger training signal > weaker instruction

#### C. Genuinely Ambiguous Context

- Retrieved text is misleading or poorly written
- LLM misreads the context
- LLM fills gaps with "reasonable" but wrong inferences

#### D. Instruction Following Fails

- LLM knows when to refuse (correct behavior exists in training)
- But at inference time, it doesn't activate that knowledge
- Instead defaults to "answer-like" generation

### Example from Our Evaluation:

**Q: "What is the exact market capitalisation of AI industry in 2024?"**

Expected: "The answer is not found in the provided documents."

What might happen:

```
Ground Truth: NOT IN DOCUMENTS
Retrieved Context: [No mention of 2024 AI market cap]
LLM Output: "According to industry analysts, the global AI market
            is projected to reach $500-600 billion by 2024,
            driven by increased enterprise adoption..."

Result: FAIL ❌ (confident, specific, but completely made up)
```

Why?

- LLM trained on thousands of real market analysis reports
- Generating market predictions feels "natural" to the model
- "Refusing to answer" is harder than "generating plausible text"
- No ground truth signal to anchor on → confidence + hallucination

### How to Prevent:

1. **Better Retrieval:** Ensure relevant context is always found
2. **Stronger Prompts:** Use explicit refusal templates
3. **Temperature = 0:** Use deterministic mode (reduces randomness)
4. **Fact Checking:** Post-process answers against retrieved context
5. **Judge Model:** Use third LLM to verify correctness (like we do in evaluation)
6. **Semantic Similarity:** Check if LLM answer actually matches provided context

---

## Summary Table

| Failure Type                | Root Cause                   | Fix                               |
| --------------------------- | ---------------------------- | --------------------------------- |
| **Retrieval Failure**       | Bad query→doc matching       | Better embeddings, chunking       |
| **Generation Failure**      | LLM ignores context          | Better prompts, post-verification |
| **Confident Hallucination** | Training data > instructions | Judge models, temperature tuning  |
