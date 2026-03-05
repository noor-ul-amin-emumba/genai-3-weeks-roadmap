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
- **LLM-B** (`llama3-70b-8192`) — larger, more capable model
- Both run at `temperature=0` for reproducibility

## Observations

- Larger models generally score higher on LLM-Judge but are slower and use more tokens
- Unanswerable questions reveal hallucination tendencies
- Lexical metrics (EM, F1, BLEU) can underestimate quality for paraphrased correct answers
- LLM-as-Judge is the most human-aligned metric but adds cost and latency

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
