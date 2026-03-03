"""
Tokenization Comparison
=======================
Tokenizes 30 diverse strings with two different tokenizers and compares
the token counts.

Model A: cl100k_base  (tiktoken — OpenAI GPT-4/3.5 encoding)
Model B: gpt2         (Hugging Face GPT2TokenizerFast)
"""

# import csv
import re
from datetime import datetime, timezone
from pathlib import Path

import tiktoken
from transformers import GPT2TokenizerFast

# ── Models ──────────────────────────────────────────────────────────────────
MODEL_A = "cl100k_base"  # tiktoken encoding name
MODEL_B = "gpt2"         # Hugging Face model id

# Load once — reused for every string (avoids repeated downloads/init)
ENC_A = tiktoken.get_encoding(MODEL_A)
TOKENIZER_B = GPT2TokenizerFast.from_pretrained(MODEL_B)

# ── 30 test strings ─────────────────────────────────────────────────────────
STRINGS = [
    # --- Code ---
    "def hello_world():\n    return 'hello'",
    "SELECT * FROM users WHERE email LIKE '%@example.com';",
    "C++ template: std::vector<std::string> v;",
    "Code comment: // TODO: refactor; // FIXME: bug",
    "Path: C:\\Program Files\\MyApp\\app.exe",

    # --- JSON ---
    '{"user":{"id":12345,"roles":["admin","editor"]},"active":true}',
    '{"text":"He said, \\"hello\\""}',
    "[1,2,3,4,5,6,7,8,9,10]",
    '{"name":"Ali","age":30,"skills":["Python","AI","SQL"]}',
    "YAML: key: value\nlist:\n  - a\n  - b",

    # --- Long URLs ---
    "https://example.com/path/to/resource?query=tokenization&lang=de&utm_source=newsletter&utm_medium=email&utm_campaign=2026q1",
    "https://example.com/search?q=hello%20world%20%F0%9F%9A%80",
    "https://www.example.com/products/category/item?id=12345&ref=chatgpt&utm_source=test",

    # --- Emojis ---
    "Emoji test: \U0001F600\U0001F680\U0001F525\U0001F31D",
    "I love AI \U0001F916\U0001F525\U0001F680",
    "SQL with emoji: INSERT INTO logs(msg) VALUES('ok \U0001F600');",

    # --- Urdu / Deutsch mix ---
    "Ich liebe maschinelles Lernen und Urdu: \u0645\u06CC\u06BA \u0633\u06CC\u06A9\u06BE \u0631\u06C1\u0627 \u06C1\u0648\u06BA\u06D4",
    "\u0645\u062A\u0646 \u0627\u0631\u062F\u0648 \u06A9\u06D2 \u0633\u0627\u062A\u06BE English mix.",
    "\u0622\u067E \u06A9\u06CC\u0633\u06D2 \u06C1\u06CC\u06BA? Ich bin gut.",
    "Deutsch umlaut: Fu\u00DFg\u00E4nger \u00FCberqueren",

    # --- Multilingual ---
    "\u4F60\u597D\u5417",                                     # Chinese
    "Mixed scripts: English \u4E2D\u6587 \u65E5\u672C\u8A9E \uD55C\uAD6D\uC5B4",  # CJK mix
    "Arabic only: \u0645\u0631\u062D\u0628\u0627 \u0643\u064A\u0641 \u062D\u0627\u0644\u0643",
    "Hindi: \u092E\u0941\u091D\u0947 \u092E\u0936\u0940\u0928 \u0932\u0930\u094D\u0928\u093F\u0902\u0917 \u092A\u0938\u0902\u0926 \u0939\u0948",

    # --- Other tricky cases ---
    "Email: first.last+tag@example.co.uk",
    "IPV6: 2001:0db8:85a3:0000:0000:8a2e:0370:7334",
    "Math: E=mc^2 and \u03C0 \u2248 3.14159",
    "Numbers: 12345678901234567890",
    "Markdown: **bold** _italic_ `code` [link](https://a.co)",
    "Regex: ^[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\\.[A-Za-z]$",
]

assert len(STRINGS) == 30, f"Expected 30 strings, got {len(STRINGS)}"


# ── Helpers ──────────────────────────────────────────────────────────────────
def count_tokens_a(text: str) -> int:
    """Token count using tiktoken cl100k_base (OpenAI-style BPE)."""
    return len(ENC_A.encode(text))


def count_tokens_b(text: str) -> int:
    """Token count using GPT-2 tokenizer (Hugging Face)."""
    try:
        return len(TOKENIZER_B.encode(text, add_special_tokens=False))
    except Exception as exc:
        print(f"[WARN] GPT2 encode failed for: {text[:40]!r} — {exc}")
        return 0


def to_one_line(text: str) -> str:
    """Collapse whitespace/newlines for display in a table cell."""
    return re.sub(r"\s+", " ", text).strip()


def surprise_reason(text: str) -> str:
    """Return a short human-readable explanation for why token counts differ."""
    if re.search(r"[\U0001F300-\U0001FAFF]", text):
        return (
            "Emojis are encoded as multiple UTF-8 bytes; GPT-2 maps each byte "
            "to its own token while cl100k_base has merged emoji sequences."
        )
    if re.search(r"[\u4E00-\u9FFF\u3040-\u30FF\uAC00-\uD7AF]", text):
        return (
            "CJK / Korean ideographs often receive a single token in cl100k_base "
            "(trained on more multilingual data) but multiple byte tokens in GPT-2."
        )
    if re.search(r"[\u0600-\u06FF]", text):
        return (
            "Arabic / Urdu text is largely absent from GPT-2's training corpus, "
            "forcing byte-level fallback tokens (1 char → 2-4 tokens)."
        )
    if "http" in text and ("%" in text or "&" in text or "utm" in text):
        return (
            "Long URLs contain percent-encoding (%20), slashes, and query params "
            "that fragment into many small tokens in both tokenizers."
        )
    if "{" in text and "}" in text:
        return (
            "JSON uses braces, quotes, colons, and commas — each is a separate "
            "token, so deeply nested objects produce unexpectedly high counts."
        )
    if re.search(r"\d{10,}", text):
        return (
            "Long integers are split digit-by-digit or into small chunks because "
            "the tokenizer has no 'number' concept beyond its trained patterns."
        )
    if re.search(r"[\u0900-\u097F]", text):
        return (
            "Hindi script has very little coverage in GPT-2's vocabulary, "
            "causing aggressive byte-level splitting."
        )
    return (
        "Different training corpora → different merge rules → same surface text "
        "splits into more or fewer subword units depending on the tokenizer."
    )


# ── Build comparison rows ────────────────────────────────────────────────────
rows = []
for s in STRINGS:
    a = count_tokens_a(s)
    b = count_tokens_b(s)
    rows.append(
        {
            "string": s,
            "display": to_one_line(s),
            "model_a": a,
            "model_b": b,
            "delta": abs(a - b),
        }
    )

top5_surprises = sorted(rows, key=lambda r: r["delta"], reverse=True)[:5]

# ── CSV output ───────────────────────────────────────────────────────────────
# out_csv = Path(__file__).parent / "tokenization_comparison.csv"
# with open(out_csv, "w", newline="", encoding="utf-8") as f:
#     writer = csv.writer(f)
#     writer.writerow(["#", "string", MODEL_A, MODEL_B, "delta"])
#     for idx, r in enumerate(rows, start=1):
#         writer.writerow([idx, r["string"], r["model_a"],
#                         r["model_b"], r["delta"]])

# ── Markdown output ──────────────────────────────────────────────────────────
out_md = Path(__file__).parent / "tokenization_comparison.md"
with open(out_md, "w", encoding="utf-8") as f:
    f.write("# Tokenization Comparison\n\n")
    f.write(f"Generated: {datetime.now(timezone.utc).isoformat()}\n\n")
    f.write(f"**Model A:** `{MODEL_A}` (tiktoken — OpenAI BPE)  \n")
    f.write(f"**Model B:** `{MODEL_B}` (Hugging Face GPT-2 tokenizer)\n\n")

    # Main comparison table
    f.write("## String → Token Count Comparison\n\n")
    f.write(f"| # | String | {MODEL_A} | {MODEL_B} | Δ |\n")
    f.write("|---|--------|-----------|-----------|---|\n")
    for idx, r in enumerate(rows, start=1):
        display = r["display"].replace("|", "\\|")
        f.write(
            f"| {idx} | `{display}` | {r['model_a']} | {r['model_b']} | {r['delta']} |\n"
        )

    # 5 surprises
    f.write("\n---\n\n## 5 Surprises (Largest Token-Count Deltas)\n\n")
    for i, r in enumerate(top5_surprises, start=1):
        display = r["display"].replace("|", "\\|")
        f.write(f"### Surprise {i}\n\n")
        f.write(f"**String:** `{display}`  \n")
        f.write(
            f"**{MODEL_A}:** {r['model_a']} tokens | "
            f"**{MODEL_B}:** {r['model_b']} tokens | "
            f"**Δ = {r['delta']}**\n\n"
        )
        f.write(f"**Why:** {surprise_reason(r['string'])}\n\n")

print(f"Wrote:\n  {out_md}")
