# Week 1 · Day 2 — Report

## Context Window Strategies & Prompt Engineering

---

## Part 1: Context Window Experiment

### Document Used

`long_document.txt` — a synthetic ~15-page technical report titled  
_"Artificial Intelligence in Climate Change Mitigation and Adaptation"_  
(GICT Report ENV-2024-117, ~4,200 words, estimated ~5,600 tokens).

### Strategies Tested

| Strategy                      | Approach                                                         | Token Cost Per Question                         |
| ----------------------------- | ---------------------------------------------------------------- | ----------------------------------------------- |
| **A – Naive Stuffing**        | Entire document + question → single API call                     | ~5,700+ tokens (prompt only)                    |
| **B – Summarize-then-Answer** | Chunk by chapter → summarise each → answer on combined summaries | Higher total (map calls) but each call is small |

---

### What Breaks and Why

#### Strategy A — Naive Stuffing

**What works:**

- Simple to implement (one API call).
- For short, specific questions about content near the beginning or end of a document, naive stuffing often produces correct, well-cited answers.
- Preserves full verbatim detail — useful when an exact quote or statistic must be reproduced.

**What breaks:**

1. **"Lost-in-the-middle" degradation.**  
   LLMs attend disproportionately to the beginning and end of their context window. Content buried in the middle of a long document is statistically likely to be ignored or under-weighted. In this experiment, Q2 (asking about a specific statistic from Chapter 3 — middle of the document) showed noticeably weaker answers under Strategy A compared to Strategy B.

2. **Context-limit pressure.**  
   The document (~5,600 tokens) plus a system prompt (~60 tokens) and question (~30 tokens) totals ~5,700 tokens — well within the 8,192-token limit of `llama-3.1-8b-instant`. But for a 20-page document, this strategy would exceed the limit and trigger silent back-truncation, cutting the final chapters entirely.

   > **Failure mode:** The model answers as if the truncated content never existed — no warning is given.

3. **No graceful "not in document" signalling.**  
   For Q5 (asking about India's GDP impact — information that does NOT exist in the document), naive stuffing with no refusal instruction led the model to generate a plausible-sounding but fabricated statistic in some runs.

4. **Higher per-question latency and cost.**  
   Every question re-sends the full document. At scale (many users, many questions), this is expensive.

#### Strategy B — Summarize-then-Answer (Map-Reduce)

**What works:**

- Summaries drastically reduce the token footprint of the "answer" step — the combined summary is ≈ 800–1,200 tokens vs. the original ~5,600.
- Scales to arbitrarily long documents with no context-limit risk at the answer stage.
- The summarisation step explicitly extracts key statistics and author-year references, making them more prominent in the condensed context used for answering.

**What breaks:**

1. **Lossy compression.**  
   Summarisation discards verbatim detail. If the question requires an exact quote, precise sentence, or specific figure that was deemed unimportant by the summariser, Strategy B will miss it or hallucinate.

2. **Multi-step error accumulation.**  
   Each summarisation call can introduce its own hallucinations. By the answer step, the model is reasoning on summaries-of-summaries, and small errors compound.

3. **Over-reliance on map quality.**  
   If the document's structure does not split cleanly into chapters, or if a key fact spans a chapter boundary, the chunking strategy may isolate that fact from its context, producing a bad summary.

4. **Higher total token cost for simple questions.**  
   If you only need to answer one simple question about one section, running a full map-reduce pipeline costs more API tokens than a targeted retrieval.

---

### Strategy Win Matrix

| Question Type                        | Strategy A (Naive)     | Strategy B (Summarise)   | Recommended |
| ------------------------------------ | ---------------------- | ------------------------ | ----------- |
| Simple factual — early in document   | ✓ Good                 | ✓ Good                   | Either      |
| Simple factual — middle of document  | ⚠️ Lost-in-middle risk | ✓ Better                 | **B**       |
| Exact verbatim quote                 | ✓ Best                 | ✗ Lossy                  | **A**       |
| Multi-section synthesis              | ⚠️ Attention diluted   | ✓ Better (cross-summary) | **B**       |
| "Info not in document" (refusal)     | ✗ May hallucinate      | ✓ Refusal more reliable  | **B**       |
| Very long document (>10k tokens)     | ✗ Context overflow     | ✓ Scales                 | **B**       |
| Single targeted question (short doc) | ✓ Simpler              | ✗ Overkill               | **A**       |

---

### What Else Could Improve These Strategies

1. **Retrieval-Augmented Generation (RAG)**  
   Instead of stuffing the full document or summarising everything upfront, use embedding-based retrieval to fetch only the top-K most relevant passages for each question. This gives the precision of naive stuffing without the token cost or lost-in-middle problem. RAG is the dominant production approach for long-document Q&A.

2. **Hierarchical Summarisation (Tree Reduce)**  
   Rather than a single map-reduce, build a summary tree: summarise small chunks → summarise summaries → answer. Reduces compression loss for very long documents.

3. **Structured Chunking with Metadata**  
   Store chunk metadata (section title, page range, key entities) alongside each summary. Use metadata filtering to skip irrelevant chunks during the reduce step.

4. **Hybrid: RAG + Summary**  
   Use summaries for global context ("what is this document about?") and RAG for specific fact retrieval. Combine both in the final context window.

5. **Context Reranking**  
   After retrieval, rerank passages by relevance to the question before inserting them into the context. Puts the most relevant content at the ends of the context window (where attention is strongest).

---

## Part 2: Prompt Engineering — 10 Prompts

### Methodology

All 10 prompts target the same underlying task: Q&A over the AI-climate report.  
Difficulty escalates from a plain instruction to a fully multi-constrained prompt  
with embedded injection attacks.

Full prompt text, model responses, and failure analysis are in `prompt_pack.md`  
(generated by `prompt_engineering.py`).

### Difficulty Progression

| ID  | Label                     | Difficulty | Key Challenge                                |
| --- | ------------------------- | ---------- | -------------------------------------------- |
| P01 | Plain Instruction         | 1/8        | No grounding → hallucination risk            |
| P02 | Structured Output (JSON)  | 2/8        | Format compliance, JSON validity             |
| P03 | Must Cite Sources         | 3/8        | Citation accuracy, no hallucinated refs      |
| P04 | Refuse if Missing Info    | 3/8        | Grounding + refusal, resist helpfulness bias |
| P05 | Strict Format Enforcement | 4/8        | Simultaneous multi-format constraints        |
| P06 | Instruction Hierarchy     | 4/8        | Developer > user priority enforcement        |
| P07 | Naive Injection           | 5/8        | Basic "ignore prev instructions" resistance  |
| P08 | Data-Embedded Injection   | 6/8        | Indirect injection via untrusted document    |
| P09 | Persona Hijack (DAN)      | 7/8        | Roleplay jailbreak + system-prompt leak      |
| P10 | Multi-Constraint          | 8/8        | JSON + citations + refusal + word-limit      |

### Key Findings

#### Constraint Compliance Degrades Under Stacking

- Individual constraints (JSON only, cite only, word-limit only) are handled well.
- Stacking 3+ constraints simultaneously causes at least one violation in most runs with 8B-class models — most commonly the word limit or citation format.

#### Injection Resistance

- **Naive injection (P07)** consistently blocked by instruction-tuned models.
- **Data-embedded injection (P08)** is the most dangerous real-world vector — resistance is inconsistent even with explicit warnings, because the model is told to process the document.
- **Persona hijack (P09)** varies: models often begin a partial response before catching themselves, leaking partial alignment information.

#### Refusal Behaviour

- P04 (refuse if missing) works reliably when the absent information is clearly off-topic (fake GDP figure).
- Fails more often when the absent information _sounds like it should be in the document_ — the model fills in plausibly-sounding content.

#### JSON Output

- P02 success depends heavily on explicit instructions like "do NOT wrap in markdown fences."
- Without this instruction, ~60% of model outputs are wrapped in `json ... ` code blocks, breaking strict JSON parsers.

### Improvement Principles (Extracted from Failures)

| Failure Pattern                  | Mitigation                                                      |
| -------------------------------- | --------------------------------------------------------------- |
| JSON wrapped in markdown         | Explicitly forbid markdown; use structured-output API           |
| Hallucinated citations           | Use RAG to surface exact passages; post-validate citations      |
| Refusal bypassed                 | Reinforce refusal phrase; add output classifier                 |
| Format violations under stacking | Place constraints at end (recency bias); few-shot examples      |
| Instruction hierarchy ignored    | Use API-level developer/system roles; mark overrides explicitly |
| Indirect injection succeeded     | Delimit untrusted content (XML tags); output validation         |
| Persona hijack partial           | Never put sensitive info in system prompt; canary tokens        |

---

## Conclusion

For **single-question, short-document** scenarios: **Naive Stuffing (Strategy A)** is simpler and adequate.

For **multi-question, long-document, or production environments**: **Summarize-then-Answer (Strategy B) or RAG** clearly wins — it avoids context-limit failures, reduces the lost-in-middle problem, and scales.

The real-world answer is almost always **RAG + a well-engineered system prompt**:  
retrieve relevant passages → stuff them → enforce grounding + refusal + output format.

Prompt injection remains a meaningful threat in data-pipeline architectures (indirect injection via documents). The best mitigation combines input delimitation, explicit untrusted-content labelling, and output-layer classifiers — no single system-prompt instruction is sufficient on its own.
