# Week 1 · Day 3 — Notes

## Topic

Simple evaluation of LLM answers using large PDFs (compare 2 LLMs)

## Learning Objectives

1. How to create a small golden test set (questions + ground truth)
2. How to evaluate LLM outputs with basic pass/fail using quality gates
3. How to compare two LLMs using 4 core evaluation metrics

## Setup

### Step 1 — Install dependencies

```bash
pip install pypdf reportlab
```

### Step 2 — Create the PDFs

```bash
python week-1/day-3/create_pdfs.py
```

This generates two synthetic PDFs in `week-1/day-3/`:

- `ai_foundations.pdf` — 7 chapters on Artificial Intelligence (~5 000 words)
- `climate_change.pdf` — 7 chapters on Climate Change (~5 000 words)

### Step 3 — Run the evaluation

```bash
python week-1/day-3/evaluate_llms.py
```

This will:

- Extract text from both PDFs
- Run all 25 test questions through LLM-A and LLM-B
- Score each answer with 4 metrics + pass/fail
- Write `results_raw.json` and `report.md` to the `week-1/day-3/` folder

## Architecture

```
create_pdfs.py          → Generates ai_foundations.pdf + climate_change.pdf
test_set.json           → 25 questions with ground truth (20 answerable + 5 not)
evaluate_llms.py        → Main evaluation script
  ├── PDF text extraction (pypdf)
  ├── Context selection (per-question, ~12 000 chars)
  ├── LLM-A query  (llama-3.1-8b-instant, temperature=0)
  ├── LLM-B query  (llama3-70b-8192, temperature=0)
  ├── 4 metrics per answer:
  │    ├── Exact Match (EM)
  │    ├── Token F1
  │    ├── BLEU-1
  │    └── LLM-Judge (gemma2-9b-it, 0–10)
  ├── Pass/Fail gate
  └── report.md generation
results_raw.json        → Per-question raw scores (generated at runtime)
report.md               → Final evaluation report (generated at runtime)
```

## Key Concepts Learned

### Golden Test Set

- A curated set of (question, ground-truth-answer) pairs used as the evaluation benchmark
- 20 in-document questions drawn from specific chapters of the PDFs
- 5 unanswerable questions (answer not in either PDF) to test hallucination resistance

### Pass/Fail Quality Gates

- A simple threshold-based check that classifies each model response as PASS or FAIL
- Allows non-technical stakeholders to interpret model quality at a glance
- Gate used: `F1 >= 0.35 OR LLM-Judge >= 6` (answerable), `LLM-Judge >= 6` (unanswerable)

### 4 Core Evaluation Metrics

| Metric           | Strength                    | Weakness                  |
| ---------------- | --------------------------- | ------------------------- |
| Exact Match (EM) | Fast, deterministic         | Penalises paraphrasing    |
| Token F1         | Balances precision & recall | Ignores semantics         |
| BLEU-1           | Standard NLP benchmark      | Brevity bias              |
| LLM-Judge        | Captures semantics & nuance | Non-deterministic, costly |

### Two-Model Comparison

- **LLM-A** (`llama-3.1-8b-instant`) — smaller, faster model
- **LLM-B** (`openai/gpt-oss-120b`) — larger, faster and more capable model
- Both run at `temperature=0` for reproducibility

## Important Document Feeding Strategies

When querying an LLM about a large document (e.g., a 50+ pages PDF), you have to decide _how_ to pass that document to the model. Two common strategies are described below.

---

### Strategy A — Naive Stuffing (Send the Entire Document)

**What it does:** Extract all text from the PDF and paste the entire thing into a single prompt as context or provide the document directly to the LLM (depend on the Model you're using).

**Why it seems attractive:** Simple to implement — no chunking logic, no information loss, the model sees everything. But it often can lead to truncation failures like loss of context at the beginning or end.

**Why it fails on Groq Free Tier:**

Groq free tier enforces a **Tokens Per Minute (TPM)** limit per model. For example, `openai/gpt-oss-120b` allows only **8,000 TPM**. The expanded `ai_foundations.pdf` (69 KB, 32 chapters) produces roughly **14,000–17,000 tokens** of extracted text. Sending it in a single prompt immediately exceeds the TPM limit and returns this error:

```
Request too large for model openai/gpt-oss-120b in organization ...
Limit 8000, Requested 14339, please reduce your message size and try again.
```

Even if the limit were not an issue, most models have a **context window ceiling** (e.g., 8k, 32k, 128k tokens). Stuffing an entire document pushes against that ceiling, leaving little room for the answer.

**Summary of problems with Naive Stuffing:**

| Problem                 | Detail                                                                  |
| ----------------------- | ----------------------------------------------------------------------- |
| TPM exceeded            | Groq free tier rejects requests larger than the per-minute token budget |
| Context window pressure | Large context leaves less room for generation; model may truncate       |
| Higher latency & cost   | More tokens = slower response and higher API cost                       |
| Irrelevant noise        | Unrelated chapters dilute the signal; model may get confused            |

---

### Strategy B — Map-Reduce Summarization

**What it does:** Instead of sending the whole document at once, split it into chapters (chunks), summarise each chunk independently, then combine the summaries and answer the question from the combined summary.

**The two phases:**

```
┌─────────────────────────────────────────────────────────────────┐
│  MAP phase  (one API call per chunk)                            │
│                                                                 │
│  Chapter 1 text  ──► LLM ──► bullet-point summary 1            │
│  Chapter 2 text  ──► LLM ──► bullet-point summary 2            │
│  ...                                                            │
│  Chapter N text  ──► LLM ──► bullet-point summary N            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼  combine all summaries
┌─────────────────────────────────────────────────────────────────┐
│  REDUCE phase  (one final API call)                             │
│                                                                 │
│  Combined summaries + Question  ──► LLM ──► Final Answer        │
└─────────────────────────────────────────────────────────────────┘
```

**Why this works within rate limits:**

- Each individual MAP call sends only **one chapter at a time** (~400–800 tokens), well within the TPM budget.
- Each summary is compressed to 3–5 bullet points (~150–200 tokens).
- The REDUCE call receives only the _summaries_ (not the raw text), so the combined prompt stays small.

**Trade-off:** Information can be lost during the MAP summarisation step. If the answer to a question is a very specific detail that the summariser omits (e.g., a precise figure or statistic buried in a paragraph), the REDUCE step will correctly say the information is not present — even though it was in the original document. This is preferable to hallucinating an answer.

**Implementation:** See `week-1/day-2/context_window_experiment.py` → `strategy_summarize()` function.

---

### Comparison

|                           | Naive Stuffing                       | Map-Reduce Summarization                 |
| ------------------------- | ------------------------------------ | ---------------------------------------- |
| **TPM usage**             | One large request → may exceed limit | Many small requests → stays within limit |
| **Implementation**        | Trivial                              | Moderate (chunking + two-stage calls)    |
| **Information retention** | Full (if fits in context)            | Partial (summarisation may lose details) |
| **Latency**               | Single round-trip                    | Multiple round-trips (MAP + REDUCE)      |
| **Cost**                  | One call                             | Multiple calls (higher total tokens)     |
| **Best suited for**       | Small docs on paid/high-limit tiers  | Large docs on free/rate-limited tiers    |

---

## Observations

- Larger models generally score higher on LLM-Judge but are slower and use more tokens
- Unanswerable questions reveal hallucination tendencies
- Lexical metrics (EM, F1, BLEU) can underestimate quality for paraphrased correct answers
- LLM-as-Judge is the most human-aligned metric but adds cost and latency
- Naive Stuffing is the simplest strategy but breaks under Groq free-tier TPM limits for large PDFs
- Map-Reduce Summarization trades some information fidelity for reliable operation within rate limits

## Files

| File                 | Description                                    |
| -------------------- | ---------------------------------------------- |
| `create_pdfs.py`     | Generates the two knowledge-base PDFs          |
| `test_set.json`      | 25-question golden test set with ground truth  |
| `evaluate_llms.py`   | Main evaluation + scoring + report generation  |
| `notes.md`           | This file                                      |
| `ai_foundations.pdf` | Generated PDF 1 — AI/ML textbook               |
| `climate_change.pdf` | Generated PDF 2 — Climate change report        |
| `results_raw.json`   | Per-question scores (generated at runtime)     |
| `report.md`          | Final evaluation report (generated at runtime) |
