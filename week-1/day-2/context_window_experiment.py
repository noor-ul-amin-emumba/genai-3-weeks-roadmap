"""
Week 1 · Day 2 — Context Window Experiment
===========================================
Tests two strategies for handling a long (~15-page) document:

  Strategy A – Naive Stuffing
    Send the entire document + question in one API call.
    Demonstrates the "lost-in-the-middle" degradation and measures
    token usage approaching the context limit.

  Strategy B – Summarize-then-Answer (Map-Reduce)
    1. Split document into chapter-level chunks.
    2. Summarize each chunk independently ("map" step).
    3. Combine summaries into a condensed context ("reduce" step).
    4. Answer the question using only the combined summary.

The script runs both strategies on the same 5 test questions and
writes results to context_window_results.md.
"""

import importlib
import sys
from pathlib import Path

# Add project root to path BEFORE imports (necessary due to hyphenated folder names)
# This allows importing config.py from the root
sys.path.insert(0, str(Path(__file__).parents[2]))

config = importlib.import_module("config")
MODEL = config.MODEL
call_llm = config.call_llm


DOCUMENT_PATH = Path(__file__).parent / "long_document.txt"
OUTPUT_PATH = Path(__file__).parent / "context_window_results.md"

# Approximate token count: ~1 token per 4 characters (rough heuristic)


def approx_tokens(text: str) -> int:
    return len(text) // 4


# ---------------------------------------------------------------------------
# Load document and split into chapters
# ---------------------------------------------------------------------------
def load_document(path: Path) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def split_into_chunks(document: str) -> list[dict]:
    """
    Split the document at chapter/section boundaries marked by
    '==...==' separator lines.  Returns list of {title, content} dicts.
    """
    chunks = []
    current_title = "Preamble"
    current_lines: list[str] = []

    for line in document.splitlines():
        stripped = line.strip()
        if stripped.startswith("=" * 20):
            # Save previous chunk
            if current_lines:
                chunks.append(
                    {
                        "title": current_title,
                        "content": "\n".join(current_lines).strip(),
                    }
                )
                current_lines = []
        elif stripped.startswith("=" * 10):
            pass  # sub-divider, ignore
        else:
            # Check if this line looks like a chapter heading
            if stripped.startswith("CHAPTER") or stripped.startswith("EXECUTIVE") or stripped.startswith("CONCLUSION") or stripped.startswith("REFERENCES"):
                current_title = stripped
                current_lines = []
            else:
                current_lines.append(line)

    # flush last chunk
    if current_lines:
        chunks.append(
            {"title": current_title, "content": "\n".join(
                current_lines).strip()}
        )

    # Remove empty chunks
    return [c for c in chunks if len(c["content"]) > 100]


# ---------------------------------------------------------------------------
# Strategy A – Naive Stuffing
# ---------------------------------------------------------------------------
def strategy_naive(document: str, question: str) -> dict:
    """Send the full document + question in a single API call."""
    system = (
        "You are a careful research assistant. "
        "Answer the question strictly based on the provided document. "
        "Be concise but complete. If the answer is not in the document, say so."
    )
    user = f"DOCUMENT:\n\n{document}\n\n---\n\nQUESTION: {question}"

    approx_prompt_tokens = approx_tokens(system + user)

    try:
        answer, prompt_tok, completion_tok = call_llm(
            system, user, max_tokens=400)
        status = "ok"
        notes = []

        # Detect failure signals
        if "i don't" in answer.lower() or "not mentioned" in answer.lower() or "not provided" in answer.lower():
            notes.append(
                "Model signalled missing info (may be lost-in-the-middle).")
        if len(answer) < 80:
            notes.append(
                "Suspiciously short answer — possible truncation effect.")
        if prompt_tok > 6000:
            notes.append(
                f"WARNING: Actual prompt tokens ({prompt_tok}) "
                "is high — context limit pressure likely."
            )

    except Exception as exc:
        answer = f"[ERROR] {exc}"
        prompt_tok, completion_tok = 0, 0
        status = "error"
        notes = [str(exc)]

    return {
        "strategy": "Naive Stuffing",
        "question": question,
        "answer": answer,
        "prompt_tokens": prompt_tok,
        "completion_tokens": completion_tok,
        "approx_prompt_tokens_estimate": approx_prompt_tokens,
        "status": status,
        "failure_notes": notes,
    }


# ---------------------------------------------------------------------------
# Strategy B – Summarize-then-Answer (Map-Reduce)
# ---------------------------------------------------------------------------
def strategy_summarize(chunks: list[dict], question: str) -> dict:
    """
    Map: summarize each chunk.
    Reduce: combine summaries, then answer the question.
    """
    # --- MAP step ---
    map_system = (
        "You are a technical summariser. "
        "Produce a concise summary (3–5 bullet points) of the section provided. "
        "Preserve key statistics, author names, figures, and technical conclusions."
    )
    summaries = []
    map_tokens_total = 0

    for chunk in chunks:
        user = f"SECTION: {chunk['title']}\n\n{chunk['content']}"
        try:
            summary, p_tok, c_tok = call_llm(map_system, user, max_tokens=200)
            map_tokens_total += p_tok + c_tok
        except Exception as exc:
            summary = f"[SUMMARY ERROR: {exc}]"
        summaries.append(f"### {chunk['title']}\n{summary}")

    combined_summary = "\n\n".join(summaries)

    # --- REDUCE step ---
    reduce_system = (
        "You are a careful research assistant. "
        "Answer the question strictly based on the provided document summaries. "
        "Be concise but complete. Cite the section name when possible. "
        "If the answer is not in the summaries, say so explicitly."
    )
    reduce_user = (
        f"DOCUMENT SUMMARIES:\n\n{combined_summary}\n\n---\n\nQUESTION: {question}"
    )

    approx_reduce_tokens = approx_tokens(reduce_system + reduce_user)

    try:
        answer, p_tok, c_tok = call_llm(
            reduce_system, reduce_user, max_tokens=400)
        total_tokens = map_tokens_total + p_tok + c_tok
        status = "ok"
        notes = []

        if "not mentioned" in answer.lower() or "not provided" in answer.lower():
            notes.append("Summarisation may have dropped the relevant detail.")
        if len(answer) < 80:
            notes.append(
                "Short answer — detail may have been lost during summarisation.")

    except Exception as exc:
        answer = f"[ERROR] {exc}"
        total_tokens = map_tokens_total
        status = "error"
        notes = [str(exc)]

    return {
        "strategy": "Summarize-then-Answer",
        "question": question,
        "answer": answer,
        "total_api_tokens_used": total_tokens,
        "map_chunks": len(chunks),
        "approx_reduce_prompt_tokens": approx_reduce_tokens,
        "combined_summary": combined_summary,
        "status": status,
        "failure_notes": notes,
    }


# ---------------------------------------------------------------------------
# Test questions
# ---------------------------------------------------------------------------
QUESTIONS = [
    # Q1 – factual, detail in early section
    "What percentage reduction in precipitation forecast errors did AI-enhanced "
    "climate models achieve compared to traditional NWP models, and which study "
    "reported this?",

    # Q2 – factual, detail in a middle section (lost-in-middle test)
    "What was the median annual energy production gain achieved by ML-optimised "
    "wind farm layouts according to the meta-analysis cited in the report, and "
    "how many commercial projects were included?",

    # Q3 – factual, detail near the end of the document
    "What are the four specific policy recommendations made in the Conclusion of "
    "the report?",

    # Q4 – multi-section synthesis
    "What are the three main limitations of AI in climate applications as described "
    "in Chapter 6? Provide at least one specific example for each.",

    # Q5 – adversarial: asks for information NOT in the document
    "What is the projected GDP impact of a 2°C warming scenario on India according "
    "to this report?",
]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print(f"Loading document from {DOCUMENT_PATH} ...")
    document = load_document(DOCUMENT_PATH)
    chunks = split_into_chunks(document)

    doc_tokens = approx_tokens(document)
    print(f"Document size: {len(document):,} chars | ~{doc_tokens:,} tokens")
    print(f"Split into {len(chunks)} chunks:")
    for c in chunks:
        print(
            f"  - {c['title'][:60]!r}  ({approx_tokens(c['content'])} tokens)")

    results = []
    total_qs = len(QUESTIONS)

    for idx, question in enumerate(QUESTIONS, start=1):
        print(f"\n[{idx}/{total_qs}] Question: {question}...")

        print("  Running Strategy A (Naive Stuffing)...")
        result_a = strategy_naive(document, question)

        print("  Running Strategy B (Summarize-then-Answer)...")
        result_b = strategy_summarize(chunks, question)

        results.append((result_a, result_b))
        print(f"  A tokens: {result_a['prompt_tokens']} prompt | "
              f"  B total tokens: {result_b.get('total_api_tokens_used', 'N/A')}")

    # -----------------------------------------------------------------------
    # Write results to Markdown
    # -----------------------------------------------------------------------
    write_markdown(results, chunks, document)
    print(f"\nDone! Results written to {OUTPUT_PATH}")


def write_markdown(results, chunks, document):
    doc_tokens = approx_tokens(document)

    lines = [
        "# Context Window Experiment Results",
        "",
        f"**Model:** `{MODEL}`  ",
        f"**Document:** `long_document.txt`  ",
        f"**Document size:** {len(document):,} chars | ~{doc_tokens:,} estimated tokens  ",
        f"**Context window limit (model):** 8,192 tokens  ",
        f"**Chunks (Strategy B):** {len(chunks)}",
        "",
        "---",
        "",
        "## Strategy Descriptions",
        "",
        "| Strategy | Description |",
        "|---|---|",
        "| **A – Naive Stuffing** | Entire document + question sent in one API call. Simple but risks context pressure and 'lost-in-the-middle' degradation. |",
        "| **B – Summarize-then-Answer** | Document chunked by chapter → each chunk summarised (map) → summaries combined → question answered on combined summary (reduce). |",
        "",
        "---",
        "",
    ]

    for idx, (ra, rb) in enumerate(results, start=1):
        lines += [
            f"## Question {idx}",
            "",
            f"> {ra['question']}",
            "",
            "### Strategy A – Naive Stuffing",
            "",
            f"**Status:** `{ra['status']}`  ",
            f"**Prompt tokens (actual):** {ra['prompt_tokens']}  ",
            f"**Estimated prompt tokens:** ~{ra['approx_prompt_tokens_estimate']}  ",
            f"**Completion tokens:** {ra['completion_tokens']}  ",
            "",
            "**Answer:**",
            "",
            ra["answer"],
            "",
        ]
        if ra["failure_notes"]:
            lines += [
                "**Failure / Warning Notes:**",
                "",
            ]
            for note in ra["failure_notes"]:
                lines.append(f"- {note}")
            lines.append("")

        lines += [
            "### Strategy B – Summarize-then-Answer",
            "",
            f"**Status:** `{rb['status']}`  ",
            f"**Total API tokens (map + reduce):** {rb.get('total_api_tokens_used', 'N/A')}  ",
            f"**Map chunks:** {rb['map_chunks']}  ",
            f"**Approx reduce-prompt tokens:** ~{rb['approx_reduce_prompt_tokens']}  ",
            "",
            "**Answer:**",
            "",
            rb["answer"],
            "",
        ]
        if rb["failure_notes"]:
            lines += [
                "**Failure / Warning Notes:**",
                "",
            ]
            for note in rb["failure_notes"]:
                lines.append(f"- {note}")
            lines.append("")

        lines += ["---", ""]

    # Appendix: combined summaries
    lines += [
        "## Appendix – Combined Chapter Summaries (Strategy B Map Output)",
        "",
    ]
    if results:
        # all questions share the same summaries; grab from first result
        lines.append(results[0][1]["combined_summary"])

    lines.append("")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
