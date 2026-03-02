
import re
from datetime import datetime, timezone
from pathlib import Path

import tiktoken
from transformers import GPT2TokenizerFast

MODEL_A = "cl100k_base"
MODEL_B = "gpt2"

ENC_A = tiktoken.get_encoding(MODEL_A)
TOKENIZER_B = GPT2TokenizerFast.from_pretrained(MODEL_B)

STRINGS = [
    "def hello_world():\n    return 'hello'",
    "SELECT * FROM users WHERE email LIKE '%@example.com';",
    "Ich liebe maschinelles Lernen und Urdu: میں سیکھ رہا ہوں.",
    "你好吗",
    "Here is a long URL: https://example.com/path/to/resource?query=tokenization&lang=de&utm_source=newsletter&utm_medium=email&utm_campaign=2026q1",
    "JSON: {\"user\":{\"id\":12345,\"roles\":[\"admin\",\"editor\"]},\"active\":true}",
    "Emoji test: 😀🚀🔥✨🌍",
    "C++ template: std::vector<std::string> v;",
    "Markdown: **bold** _italic_ `code` [link](https://a.co)",
    "Numbers: 12345678901234567890",
    "Email: first.last+tag@example.co.uk",
    "IPV6: 2001:0db8:85a3:0000:0000:8a2e:0370:7334",
    "Regex: ^[A-Za-z0-9_]+$",
    "Shell: export PATH=/usr/local/bin:$PATH",
    "Math: E=mc^2 and \u03c0 \u2248 3.14159",
    "Tabs\tand\tspaces\taligned",
    "Whitespace    collapse?    maybe",
    "XML: <note><to>Tove</to><from>Jani</from></note>",
    "YAML: key: value\nlist:\n  - a\n  - b",
    "CSV: id,name,score\n1,Alice,98\n2,Bob,87",
    "SQL with emojis: INSERT INTO logs(msg) VALUES('ok \U0001F600');",
    "Arabic only: مرحبا كيف حالك",
    "Hindi: मुझे मशीन लर्निंग पसंद है",
    "Deutsch umlaut: Fu\u00dfg\u00e4nger \u00fcberqueren",
    "Mixed scripts: English 中文 日本語 한국어",
    "URL encoded: https://example.com/search?q=hello%20world%20%F0%9F%9A%80",
    "Code comment: // TODO: refactor; // FIXME: bug",
    "Path: C:\\Program Files\\MyApp\\app.exe",
    "Quoted JSON: {\"text\":\"He said, \\\"hello\\\"\"}",
    "Long JSON array: [1,2,3,4,5,6,7,8,9,10]",
]


def count_tokens_a(text: str) -> int:
    return len(ENC_A.encode(text))


def count_tokens_b(text: str) -> int:
    try:
        encoded = TOKENIZER_B.encode(text, add_special_tokens=False)
        return len(encoded)
    except Exception as e:
        print(
            f"Warning: Failed to encode with GPT2 for text: {text[:50]}... Error: {e}")
        return 0


def one_line(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def explain(text: str) -> str:
    if re.search(r"[\U0001F300-\U0001FAFF]", text):
        return "Emojis often split into multiple tokens in byte-level BPEs."
    if "http" in text:
        return "URLs fragment into many sub-tokens due to slashes, punctuation, and percent-encoding."
    if re.search(r"[\u0600-\u06FF]", text):
        return "Arabic/Urdu script usually breaks into shorter sub-tokens, increasing counts."
    if re.search(r"[\u4E00-\u9FFF]", text):
        return "CJK characters often map to individual tokens, raising counts quickly."
    if "{" in text or "}" in text:
        return "Braces, quotes, and commas create extra tokens in JSON-like text."
    if re.search(r"\d{8,}", text):
        return "Long numbers are often split into chunks rather than single tokens."
    return "Different vocabularies merge or split common substrings differently."


rows = []
for s in STRINGS:
    a = count_tokens_a(s)
    b = count_tokens_b(s)
    rows.append(
        {
            "string": s,
            "string_one_line": one_line(s),
            "model_a": a,
            "model_b": b,
            "delta": abs(a - b),
        }
    )

rows_sorted = sorted(rows, key=lambda r: r["delta"], reverse=True)

out_md = Path(__file__).parent / "tokenization_comparison.md"
with open(out_md, "w", encoding="utf-8", errors="replace") as f:
    f.write("# Tokenization Comparison\n\n")
    f.write(f"Generated: {datetime.now(timezone.utc).isoformat()}\n\n")
    f.write(f"Model A: {MODEL_A}\n\n")
    f.write(f"Model B: {MODEL_B}\n\n")
    f.write("| # | String | Model A | Model B | Delta |\n")
    f.write("|---|--------|---------|---------|-------|\n")
    for idx, r in enumerate(rows, start=1):
        safe_str = r['string_one_line'].encode(
            "utf-8", errors="replace").decode("utf-8")
        f.write(
            f"| {idx} | {safe_str} | {r['model_a']} | {r['model_b']} | {r['delta']} |\n"
        )

    f.write("\n## 5 Surprises (largest deltas)\n\n")
    for idx, r in enumerate(rows_sorted[:5], start=1):
        f.write(f"{idx}. {r['string_one_line']}\n")
        f.write(f"   - Model A: {r['model_a']} | Model B: {r['model_b']}\n")
        f.write(f"   - Why: {explain(r['string'])}\n\n")

print(f"Wrote {out_md}")
