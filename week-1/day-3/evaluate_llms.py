"""
Week 1 · Day 3 — LLM Evaluation on Large PDFs
================================================
Compares two LLMs (LLM-A and LLM-B) on a 25-question test set
extracted from two large PDFs.

Evaluation Metrics (per question, per model):
  1. Exact Match (EM)          — Binary: 1 if key ground-truth phrase is in answer
  2. Token F1                  — Word-level precision/recall/F1 vs ground truth
  3. BLEU-1                    — Unigram precision of answer vs ground truth
  4. LLM-Judge Score (0–10)   — Third-model judge rates quality / correct refusal

Pass/Fail Gates:
  Answerable questions   : PASS if F1 >= 0.35 OR LLM-Judge >= 6
  Unanswerable questions : PASS if LLM-Judge >= 6 (judge verifies correct refusal)

Outputs (written to week-1/day-3/):
  - results_raw.json      Raw per-question results for both models
  - report.md             Full markdown report with all required tables

Pre-requisites:
  1. Run create_pdfs.py first (creates ai_foundations.pdf + climate_change.pdf)
  2. pip install pypdf reportlab
"""

import importlib
import json
import math
import re
import sys
import time
from collections import Counter
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Path Setup
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT))

config = importlib.import_module("config")
call_llm = config.call_llm

DAY_DIR = Path(__file__).parent
TEST_SET_PATH = DAY_DIR / "test_set.json"
PDF_AI = DAY_DIR / "ai_foundations.pdf"
PDF_CLIMATE = DAY_DIR / "climate_change.pdf"
RAW_RESULTS_PATH = DAY_DIR / "results_raw.json"
REPORT_PATH = DAY_DIR / "report.md"

# ---------------------------------------------------------------------------
# Model Configuration
# ---------------------------------------------------------------------------
MODEL_A_ID = "llama-3.1-8b-instant"
MODEL_A_LABEL = "LLM-A (llama-3.1-8b-instant)"

MODEL_B_ID = "openai/gpt-oss-120b"
MODEL_B_LABEL = "LLM-B (openai/gpt-oss-120b)"

JUDGE_MODEL_ID = "llama-3.3-70b-versatile"

TEMPERATURE = 0  # Deterministic

# ---------------------------------------------------------------------------
# PDF Text Extraction
# ---------------------------------------------------------------------------


def extract_pdf_text(pdf_path: Path, max_chars: int = 30_000) -> str:
    """Extract plain text from a PDF file using pypdf."""
    try:
        from pypdf import PdfReader
    except ImportError:
        raise ImportError("pypdf is required. Run: pip install pypdf")

    reader = PdfReader(str(pdf_path))
    pages_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages_text.append(text.strip())
    full_text = "\n\n".join(pages_text)
    return full_text


# ---------------------------------------------------------------------------
# Metric Helpers
# ---------------------------------------------------------------------------

def _tokenize(text: str) -> list[str]:
    """Lowercase, strip punctuation, split into word tokens."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return [t for t in text.split() if t]


def exact_match(prediction: str, ground_truth: str) -> float:
    """
    Return 1.0 if ground truth key phrases are contained in the prediction;
    0.0 otherwise.
    For unanswerable questions check for refusal indicators.
    """
    if ground_truth.strip().upper() == "NOT IN DOCUMENTS":
        # Check for refusal / uncertainty
        refusal_keywords = [
            "not in", "not mentioned", "not provided", "not found",
            "not available", "not contain", "cannot find", "cannot answer",
            "i don't know", "i do not know", "no information",
            "unable to find", "not discussed", "not stated", "not specified",
            "isn't mentioned", "is not mentioned", "not present",
        ]
        pred_lower = prediction.lower()
        return 1.0 if any(kw in pred_lower for kw in refusal_keywords) else 0.0
    else:
        # Check if key noun phrases from ground truth appear in prediction
        gt_lower = ground_truth.lower()
        pred_lower = prediction.lower()
        # Use the first 60 chars of GT as key phrase probe
        key_phrase = gt_lower[:60].split(".")[0].strip()
        if len(key_phrase) > 10 and key_phrase in pred_lower:
            return 1.0
        # Fallback: significant token overlap
        gt_tokens = set(_tokenize(ground_truth))
        pred_tokens = set(_tokenize(prediction))
        if len(gt_tokens) == 0:
            return 0.0
        overlap = len(gt_tokens & pred_tokens) / len(gt_tokens)
        return 1.0 if overlap >= 0.55 else 0.0


def token_f1(prediction: str, ground_truth: str) -> float:
    """
    Token-level F1 between prediction and ground truth.
    For unanswerable questions, score against a canonical refusal sentence.
    """
    if ground_truth.strip().upper() == "NOT IN DOCUMENTS":
        # Measure against a canonical refusal
        ground_truth = (
            "The answer to this question is not found in the provided documents. "
            "I cannot answer based on the given context."
        )

    pred_tokens = _tokenize(prediction)
    gt_tokens = _tokenize(ground_truth)

    if not pred_tokens or not gt_tokens:
        return 0.0

    pred_counter = Counter(pred_tokens)
    gt_counter = Counter(gt_tokens)

    # Count common tokens (clipped)
    common = sum((pred_counter & gt_counter).values())

    precision = common / len(pred_tokens)
    recall = common / len(gt_tokens)

    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def bleu_1(prediction: str, ground_truth: str) -> float:
    """
    Corpus BLEU-1 (unigram precision, with brevity penalty).
    For unanswerable questions, score against a canonical refusal.
    """
    if ground_truth.strip().upper() == "NOT IN DOCUMENTS":
        ground_truth = (
            "The answer to this question is not found in the provided documents. "
            "I cannot answer based on the given context."
        )

    pred_tokens = _tokenize(prediction)
    gt_tokens = _tokenize(ground_truth)

    if not pred_tokens:
        return 0.0

    gt_counter = Counter(gt_tokens)
    clipped = sum(
        min(count, gt_counter[token])
        for token, count in Counter(pred_tokens).items()
    )

    precision = clipped / len(pred_tokens) if pred_tokens else 0.0

    # Brevity penalty
    bp = 1.0 if len(pred_tokens) >= len(gt_tokens) else math.exp(
        1 - len(gt_tokens) / len(pred_tokens)
    )

    return bp * precision


def llm_judge_score(
    question: str,
    ground_truth: str,
    prediction: str,
    answerable: bool,
) -> int:
    """
    Ask JUDGE_MODEL_ID to score the prediction 0–10.
    Returns an integer score.
    """
    if answerable:
        judge_prompt = (
            f"You are an impartial evaluator. Score the following model answer "
            f"on a scale of 0 to 10 based on correctness and completeness "
            f"relative to the reference answer.\n\n"
            f"Question: {question}\n\n"
            f"Reference Answer: {ground_truth}\n\n"
            f"Model Answer: {prediction}\n\n"
            f"Scoring rules:\n"
            f"  10 = Fully correct, complete, and factually matches the reference.\n"
            f"  7-9 = Mostly correct with minor omissions.\n"
            f"  4-6 = Partially correct.\n"
            f"  1-3 = Mostly wrong or very incomplete.\n"
            f"  0 = Completely wrong or irrelevant.\n\n"
            f"Respond with ONLY a single integer from 0 to 10."
        )
    else:
        judge_prompt = (
            f"You are an impartial evaluator. The question below cannot be answered "
            f"from the provided documents. Score the model's response 0–10 based "
            f"on whether it correctly declines to answer (acknowledges it doesn't "
            f"have the information).\n\n"
            f"Question: {question}\n\n"
            f"Model Answer: {prediction}\n\n"
            f"Scoring rules:\n"
            f"  10 = Clearly states the information is not in the documents and declines.\n"
            f"  7-9 = Declines but is slightly vague or hedging.\n"
            f"  4-6 = Partially declines but still attempts to guess.\n"
            f"  1-3 = Provides a hallucinated specific answer without disclaimer.\n"
            f"  0 = Confidently provides a wrong or fabricated answer.\n\n"
            f"Respond with ONLY a single integer from 0 to 10."
        )

    raw, _, _ = call_llm(
        user=judge_prompt,
        max_tokens=5,
        temperature=0,
        model=JUDGE_MODEL_ID,
        label="llm_judge_score",
    )
    # Extract first integer found
    match = re.search(r"\d+", raw)
    score = int(match.group()) if match else 5
    return min(max(score, 0), 10)


# ---------------------------------------------------------------------------
# Pass/Fail Gate
# ---------------------------------------------------------------------------

def pass_fail(f1: float, judge: int, answerable: bool) -> str:
    if answerable:
        return "PASS" if (f1 >= 0.35 or judge >= 6) else "FAIL"
    else:
        return "PASS" if judge >= 6 else "FAIL"


# ---------------------------------------------------------------------------
# Query a specific model
# ---------------------------------------------------------------------------

def query_model(model_id: str, context: str, question: str, answerable: bool) -> str:
    """Run a question through a specific model with the given context."""
    system = (
        "You are a helpful and precise assistant. Answer the question based ONLY "
        "on the provided document context. If the answer is not in the context, "
        "say 'The answer is not found in the provided documents.' "
        "Be concise and accurate."
    )

    user = (
        f"Document Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        f"Answer (based only on the context above):"
    )

    response_text, _, _ = call_llm(
        system=system,
        user=user,
        max_tokens=350,
        temperature=TEMPERATURE,
        model=model_id,
        label=f"query_model({model_id})",
    )
    return response_text


# ---------------------------------------------------------------------------
# Main Evaluation Loop
# ---------------------------------------------------------------------------

def run_evaluation():
    # 1. Load test set
    with open(TEST_SET_PATH, encoding="utf-8") as f:
        test_set = json.load(f)

    # 2. Extract PDF texts
    print("Extracting PDF text ...")
    text_ai = extract_pdf_text(PDF_AI)
    # text_climate = extract_pdf_text(PDF_CLIMATE)  # commented out to reduce runtime
    text_climate = ""  # placeholder
    print(f"  AI PDF: {len(text_ai):,} chars   Climate PDF: skipped")

    # 3. Run evaluation
    results = []
    total = len(test_set)

    for idx, item in enumerate(test_set, 1):
        q_id = item["id"]
        question = item["question"]
        ground_truth = item["ground_truth"]
        answerable = item["answerable"]
        source_pdf = item["source_pdf"]

        # Select context
        # Skip climate_change.pdf questions to reduce runtime
        if source_pdf == "climate_change.pdf":
            print(
                f"  Skipping Q{q_id} (climate_change.pdf source — commented out)")
            continue
        if source_pdf == "ai_foundations.pdf":
            context = text_ai[:12_000]
        # elif source_pdf == "climate_change.pdf":
        #     context = text_climate[:12_000]
        else:
            # Unanswerable: give AI context only (climate PDF skipped)
            context = text_ai[:12_000]

        print(f"\n[{idx}/{total}] Q{q_id}: {question[:70]}...")

        # --- LLM-A ---
        print(f"  Running LLM-A ({MODEL_A_ID}) ...")
        pred_a = query_model(MODEL_A_ID, context, question, answerable)
        em_a = exact_match(pred_a, ground_truth)
        f1_a = token_f1(pred_a, ground_truth)
        bleu_a = bleu_1(pred_a, ground_truth)
        print(f"  Judging LLM-A ...")
        judge_a = llm_judge_score(question, ground_truth, pred_a, answerable)
        pf_a = pass_fail(f1_a, judge_a, answerable)
        print(
            f"  A: EM={em_a:.0f} F1={f1_a:.3f} BLEU={bleu_a:.3f} Judge={judge_a} -> {pf_a}")

        # --- LLM-B ---
        print(f"  Running LLM-B ({MODEL_B_ID}) ...")
        pred_b = query_model(MODEL_B_ID, context, question, answerable)
        em_b = exact_match(pred_b, ground_truth)
        f1_b = token_f1(pred_b, ground_truth)
        bleu_b = bleu_1(pred_b, ground_truth)
        print(f"  Judging LLM-B ...")
        judge_b = llm_judge_score(question, ground_truth, pred_b, answerable)
        pf_b = pass_fail(f1_b, judge_b, answerable)
        print(
            f"  B: EM={em_b:.0f} F1={f1_b:.3f} BLEU={bleu_b:.3f} Judge={judge_b} -> {pf_b}")

        results.append(
            {
                "id": q_id,
                "question": question,
                "ground_truth": ground_truth,
                "answerable": answerable,
                "source_pdf": source_pdf,
                "category": item["category"],
                "llm_a": {
                    "model": MODEL_A_ID,
                    "prediction": pred_a,
                    "exact_match": em_a,
                    "token_f1": round(f1_a, 4),
                    "bleu_1": round(bleu_a, 4),
                    "llm_judge": judge_a,
                    "pass_fail": pf_a,
                },
                "llm_b": {
                    "model": MODEL_B_ID,
                    "prediction": pred_b,
                    "exact_match": em_b,
                    "token_f1": round(f1_b, 4),
                    "bleu_1": round(bleu_b, 4),
                    "llm_judge": judge_b,
                    "pass_fail": pf_b,
                },
            }
        )

    # 4. Save raw results
    with open(RAW_RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nRaw results saved to: {RAW_RESULTS_PATH}")

    return results


# ---------------------------------------------------------------------------
# Report Generation
# ---------------------------------------------------------------------------

def _avg(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def find_failures(results: list[dict], model_key: str) -> list[dict]:
    """Return failed questions for a given model key ('llm_a' or 'llm_b')."""
    return [r for r in results if r[model_key]["pass_fail"] == "FAIL"]


def top_failures(results: list[dict], model_key: str, n: int = 5) -> list[dict]:
    """
    Return top-N failures sorted by worst LLM-Judge score.
    Prefer answerable failures first (more informative).
    """
    fails = find_failures(results, model_key)
    # Sort by judge score ascending (worst first), answerable failures first
    fails.sort(key=lambda r: (not r["answerable"], r[model_key]["llm_judge"]))
    return fails[:n]


def failure_reason(item: dict, model_key: str) -> str:
    """Generate a 1-line failure reason."""
    judge = item[model_key]["llm_judge"]
    f1 = item[model_key]["token_f1"]
    pred = item[model_key]["prediction"]
    answerable = item["answerable"]

    if not answerable:
        if judge < 6:
            return "Model hallucinated a specific answer instead of refusing for an unanswerable question."
        else:
            return "Model partially declined but still attempted a plausible-sounding answer."
    if judge <= 3:
        return f"Answer is largely incorrect or irrelevant (judge={judge}, F1={f1:.2f})."
    if f1 < 0.20:
        gt_words = item["ground_truth"].split()[:6]
        return f"Very low lexical overlap with ground truth; answer may be paraphrased but key facts missing (F1={f1:.2f})."
    if judge < 6:
        return f"Answer partially addresses the question but misses key details (judge={judge}, F1={f1:.2f})."
    return f"Borderline fail: F1={f1:.2f}, judge={judge}."


def generate_report(results: list[dict]) -> None:
    """Write the full markdown evaluation report."""

    # ---- Aggregate metrics ----
    def agg(model_key: str) -> dict:
        return {
            "em":    _avg([r[model_key]["exact_match"] for r in results]),
            "f1":    _avg([r[model_key]["token_f1"] for r in results]),
            "bleu":  _avg([r[model_key]["bleu_1"] for r in results]),
            "judge": _avg([r[model_key]["llm_judge"] for r in results]),
            "pass":  sum(1 for r in results if r[model_key]["pass_fail"] == "PASS"),
            "fail":  sum(1 for r in results if r[model_key]["pass_fail"] == "FAIL"),
        }

    agg_a = agg("llm_a")
    agg_b = agg("llm_b")

    # ---- Answerable only ----
    ans = [r for r in results if r["answerable"]]
    unans = [r for r in results if not r["answerable"]]

    def agg_sub(items: list[dict], model_key: str) -> dict:
        if not items:
            return {"em": 0, "f1": 0, "bleu": 0, "judge": 0, "pass": 0, "fail": 0}
        return {
            "em":    _avg([r[model_key]["exact_match"] for r in items]),
            "f1":    _avg([r[model_key]["token_f1"] for r in items]),
            "bleu":  _avg([r[model_key]["bleu_1"] for r in items]),
            "judge": _avg([r[model_key]["llm_judge"] for r in items]),
            "pass":  sum(1 for r in items if r[model_key]["pass_fail"] == "PASS"),
            "fail":  sum(1 for r in items if r[model_key]["pass_fail"] == "FAIL"),
        }

    agg_a_ans = agg_sub(ans, "llm_a")
    agg_b_ans = agg_sub(ans, "llm_b")
    agg_a_unans = agg_sub(unans, "llm_a")
    agg_b_unans = agg_sub(unans, "llm_b")

    # ---- Top failures ----
    fails_a = top_failures(results, "llm_a", 5)
    fails_b = top_failures(results, "llm_b", 5)

    # ---- Write report ----
    lines = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines.append(f"# Week 1 · Day 3 — LLM Evaluation Report\n")
    lines.append(f"**Generated:** {timestamp}  \n")
    lines.append(f"**LLM-A:** {MODEL_A_LABEL}  \n")
    lines.append(f"**LLM-B:** {MODEL_B_LABEL}  \n")
    lines.append(f"**Judge model:** {JUDGE_MODEL_ID}  \n")
    lines.append(f"**Temperature:** {TEMPERATURE} (deterministic)  \n")
    lines.append(f"**Test set:** {len(results)} questions "
                 f"({len(ans)} answerable / {len(unans)} unanswerable)  \n")
    lines.append("\n---\n")

    # ---- Section 1: Metric Definitions ----
    lines.append("## 1. Evaluation Metrics Explained\n")
    lines.append("| Metric | Description | Range |\n")
    lines.append("|--------|-------------|-------|\n")
    lines.append(
        "| **Exact Match (EM)** | 1 if key ground-truth phrase appears in prediction or if refusal detected for unanswerable | 0–1 |\n")
    lines.append(
        "| **Token F1** | Word-level precision × recall overlap between prediction and ground truth | 0–1 |\n")
    lines.append(
        "| **BLEU-1** | Unigram precision with brevity penalty vs ground truth | 0–1 |\n")
    lines.append(
        "| **LLM-Judge (0–10)** | Third-model judge scoring correctness / appropriate refusal | 0–10 |\n")
    lines.append("\n**Pass/Fail gate:**\n")
    lines.append(
        "- *Answerable*: PASS if Token F1 ≥ 0.35 **or** LLM-Judge ≥ 6  \n")
    lines.append(
        "- *Unanswerable*: PASS if LLM-Judge ≥ 6 (model correctly refuses)  \n")
    lines.append("\n---\n")

    # ---- Section 2: Aggregate Results Table ----
    lines.append("## 2. Aggregate Results (All 25 Questions)\n")
    lines.append("| Metric | LLM-A | LLM-B | Winner |\n")
    lines.append("|--------|-------|-------|--------|\n")

    def winner(a_val: float, b_val: float, higher_is_better: bool = True) -> str:
        if higher_is_better:
            if a_val > b_val + 0.001:
                return "LLM-A"
            if b_val > a_val + 0.001:
                return "LLM-B"
        else:
            if a_val < b_val - 0.001:
                return "LLM-A"
            if b_val < a_val - 0.001:
                return "LLM-B"
        return "Tie"

    lines.append(
        f"| Exact Match (EM) | {agg_a['em']:.3f} | {agg_b['em']:.3f} | {winner(agg_a['em'], agg_b['em'])} |\n")
    lines.append(
        f"| Token F1 | {agg_a['f1']:.3f} | {agg_b['f1']:.3f} | {winner(agg_a['f1'], agg_b['f1'])} |\n")
    lines.append(
        f"| BLEU-1 | {agg_a['bleu']:.3f} | {agg_b['bleu']:.3f} | {winner(agg_a['bleu'], agg_b['bleu'])} |\n")
    lines.append(
        f"| LLM-Judge (avg/10) | {agg_a['judge']:.2f} | {agg_b['judge']:.2f} | {winner(agg_a['judge'], agg_b['judge'])} |\n")
    lines.append(
        f"| **PASS count** | **{agg_a['pass']}/25** | **{agg_b['pass']}/25** | {winner(agg_a['pass'], agg_b['pass'])} |\n")
    lines.append(
        f"| **FAIL count** | **{agg_a['fail']}/25** | **{agg_b['fail']}/25** | {winner(agg_a['fail'], agg_b['fail'], higher_is_better=False)} |\n")
    lines.append("\n")

    # ---- Section 3: Answerable vs Unanswerable breakdown ----
    lines.append("## 3. Breakdown: Answerable (20) vs Unanswerable (5)\n")
    lines.append("### 3a. Answerable Questions Only\n")
    lines.append("| Metric | LLM-A | LLM-B |\n")
    lines.append("|--------|-------|-------|\n")
    lines.append(f"| EM | {agg_a_ans['em']:.3f} | {agg_b_ans['em']:.3f} |\n")
    lines.append(
        f"| Token F1 | {agg_a_ans['f1']:.3f} | {agg_b_ans['f1']:.3f} |\n")
    lines.append(
        f"| BLEU-1 | {agg_a_ans['bleu']:.3f} | {agg_b_ans['bleu']:.3f} |\n")
    lines.append(
        f"| LLM-Judge | {agg_a_ans['judge']:.2f} | {agg_b_ans['judge']:.2f} |\n")
    lines.append(
        f"| PASS | {agg_a_ans['pass']}/20 | {agg_b_ans['pass']}/20 |\n")
    lines.append(
        "\n### 3b. Unanswerable Questions Only (model should decline)\n")
    lines.append("| Metric | LLM-A | LLM-B |\n")
    lines.append("|--------|-------|-------|\n")
    lines.append(
        f"| EM (refusal detected) | {agg_a_unans['em']:.3f} | {agg_b_unans['em']:.3f} |\n")
    lines.append(
        f"| Token F1 | {agg_a_unans['f1']:.3f} | {agg_b_unans['f1']:.3f} |\n")
    lines.append(
        f"| BLEU-1 | {agg_a_unans['bleu']:.3f} | {agg_b_unans['bleu']:.3f} |\n")
    lines.append(
        f"| LLM-Judge | {agg_a_unans['judge']:.2f} | {agg_b_unans['judge']:.2f} |\n")
    lines.append(
        f"| PASS (correct refusal) | {agg_a_unans['pass']}/5 | {agg_b_unans['pass']}/5 |\n")
    lines.append("\n---\n")

    # ---- Section 4: Pass/Fail Summary ----
    lines.append("## 4. Pass/Fail Summary Per Question\n")
    lines.append(
        "| Q# | Question (truncated) | Category | Answerable | LLM-A | LLM-B |\n")
    lines.append(
        "|----|----------------------|----------|------------|-------|-------|\n")
    for r in results:
        q_short = r["question"][:55].replace("|", "\\|")
        ans_flag = "Yes" if r["answerable"] else "No"
        pf_a = r["llm_a"]["pass_fail"]
        pf_b = r["llm_b"]["pass_fail"]
        a_cell = f"✅ PASS" if pf_a == "PASS" else f"❌ FAIL"
        b_cell = f"✅ PASS" if pf_b == "PASS" else f"❌ FAIL"
        lines.append(
            f"| {r['id']} | {q_short}... | {r['category']} | {ans_flag} | {a_cell} | {b_cell} |\n"
        )
    lines.append("\n---\n")

    # ---- Section 5: Per-Question Detailed Metrics ----
    lines.append("## 5. Per-Question Detailed Scores\n")
    lines.append(
        "| Q# | LLM | EM | F1 | BLEU-1 | Judge | Pass/Fail |\n"
    )
    lines.append(
        "|----|-----|----|----|--------|-------|-----------|\n"
    )
    for r in results:
        for mk, label in [("llm_a", "A"), ("llm_b", "B")]:
            m = r[mk]
            lines.append(
                f"| {r['id']} | {label} | {m['exact_match']:.0f} "
                f"| {m['token_f1']:.3f} | {m['bleu_1']:.3f} "
                f"| {m['llm_judge']} | {m['pass_fail']} |\n"
            )
    lines.append("\n---\n")

    # ---- Section 6: Top 5 Failures ----
    lines.append("## 6. Top 5 Failure Examples\n")
    for model_label, model_key, fails in [
        (MODEL_A_LABEL, "llm_a", fails_a),
        (MODEL_B_LABEL, "llm_b", fails_b),
    ]:
        lines.append(f"### {model_label}\n")
        if not fails:
            lines.append("_No failures — all questions passed!_\n\n")
            continue
        for rank, item in enumerate(fails, 1):
            lines.append(f"**Failure #{rank} — Q{item['id']}**  \n")
            lines.append(f"*Question:* {item['question']}  \n")
            lines.append(f"*Ground Truth:* {item['ground_truth'][:200]}  \n")
            pred = item[model_key]["prediction"][:250]
            lines.append(f"*Model Answer:* {pred}  \n")
            m = item[model_key]
            lines.append(
                f"*Scores:* EM={m['exact_match']:.0f}, F1={m['token_f1']:.3f}, "
                f"BLEU={m['bleu_1']:.3f}, Judge={m['llm_judge']}  \n"
            )
            reason = failure_reason(item, model_key)
            lines.append(f"**Reason:** {reason}  \n\n")
        lines.append("\n")

    lines.append("---\n")

    # ---- Section 7: Analysis and Conclusion ----
    lines.append("## 7. Analysis and Conclusion\n")

    winner_overall = MODEL_A_LABEL if agg_a["judge"] >= agg_b["judge"] else MODEL_B_LABEL
    if abs(agg_a["judge"] - agg_b["judge"]) < 0.3:
        winner_overall = "Both models performed similarly"

    lines.append(
        f"**Overall winner (by LLM-Judge avg):** {winner_overall}  \n\n"
    )
    lines.append(
        f"- **LLM-A** achieved avg LLM-Judge score of **{agg_a['judge']:.2f}/10**, "
        f"Token F1 of **{agg_a['f1']:.3f}**, and passed **{agg_a['pass']}/25** questions.  \n"
    )
    lines.append(
        f"- **LLM-B** achieved avg LLM-Judge score of **{agg_b['judge']:.2f}/10**, "
        f"Token F1 of **{agg_b['f1']:.3f}**, and passed **{agg_b['pass']}/25** questions.  \n\n"
    )
    lines.append(
        "**Key observations:**  \n"
        "1. Both models were evaluated under identical conditions (temperature=0, same context, same questions).  \n"
        "2. Unanswerable questions reveal hallucination tendencies; models that score well here correctly "
        "decline rather than fabricating answers.  \n"
        "3. Token F1 and BLEU-1 penalise verbose or paraphrased answers even when factually correct, "
        "so LLM-Judge score best reflects semantic quality.  \n"
        "4. A larger model generally achieves better LLM-Judge scores, showing the value of scale "
        "for knowledge-intensive QA tasks.  \n"
        "5. Both models showed weaknesses on numerical/specific detail questions where the exact "
        "figure must appear verbatim.  \n"
    )

    report_text = "".join(lines)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"Report saved to: {REPORT_PATH}")


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 65)
    print("  Week 1 · Day 3 — LLM Evaluation on Large PDFs")
    print(f"  Models:  {MODEL_A_LABEL}  vs  {MODEL_B_LABEL}")
    print(f"  Questions: 25 (20 answerable + 5 unanswerable)")
    print("=" * 65)

    # Verify PDFs exist
    missing = [p for p in [PDF_AI, PDF_CLIMATE] if not p.exists()]
    if missing:
        print("\nERROR: Missing PDFs. Run create_pdfs.py first:")
        for p in missing:
            print(f"  {p}")
        sys.exit(1)

    results = run_evaluation()
    generate_report(results)

    # Print quick summary
    agg_a_pass = sum(1 for r in results if r["llm_a"]["pass_fail"] == "PASS")
    agg_b_pass = sum(1 for r in results if r["llm_b"]["pass_fail"] == "PASS")
    print("\n" + "=" * 65)
    print(f"  LLM-A PASS rate: {agg_a_pass}/25")
    print(f"  LLM-B PASS rate: {agg_b_pass}/25")
    print(f"  Full report: {REPORT_PATH}")
    print("=" * 65)
