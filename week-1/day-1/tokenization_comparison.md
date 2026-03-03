# Tokenization Comparison

Generated: 2026-03-03T05:13:29.380319+00:00

**Model A:** `cl100k_base` (tiktoken — OpenAI BPE)  
**Model B:** `gpt2` (Hugging Face GPT-2 tokenizer)

## String → Token Count Comparison

| # | String | cl100k_base | gpt2 | Δ |
|---|--------|-----------|-----------|---|
| 1 | `def hello_world(): return 'hello'` | 9 | 13 | 4 |
| 2 | `SELECT * FROM users WHERE email LIKE '%@example.com';` | 12 | 14 | 2 |
| 3 | `C++ template: std::vector<std::string> v;` | 13 | 14 | 1 |
| 4 | `Code comment: // TODO: refactor; // FIXME: bug` | 12 | 15 | 3 |
| 5 | `Path: C:\Program Files\MyApp\app.exe` | 12 | 13 | 1 |
| 6 | `{"user":{"id":12345,"roles":["admin","editor"]},"active":true}` | 19 | 20 | 1 |
| 7 | `{"text":"He said, \"hello\""}` | 10 | 10 | 0 |
| 8 | `[1,2,3,4,5,6,7,8,9,10]` | 21 | 21 | 0 |
| 9 | `{"name":"Ali","age":30,"skills":["Python","AI","SQL"]}` | 17 | 19 | 2 |
| 10 | `YAML: key: value list: - a - b` | 16 | 18 | 2 |
| 11 | `https://example.com/path/to/resource?query=tokenization&lang=de&utm_source=newsletter&utm_medium=email&utm_campaign=2026q1` | 31 | 42 | 11 |
| 12 | `https://example.com/search?q=hello%20world%20%F0%9F%9A%80` | 24 | 27 | 3 |
| 13 | `https://www.example.com/products/category/item?id=12345&ref=chatgpt&utm_source=test` | 21 | 30 | 9 |
| 14 | `Emoji test: 😀🚀🔥🌝` | 13 | 16 | 3 |
| 15 | `I love AI 🤖🔥🚀` | 12 | 12 | 0 |
| 16 | `SQL with emoji: INSERT INTO logs(msg) VALUES('ok 😀');` | 14 | 18 | 4 |
| 17 | `Ich liebe maschinelles Lernen und Urdu: میں سیکھ رہا ہوں۔` | 32 | 42 | 10 |
| 18 | `متن اردو کے ساتھ English mix.` | 17 | 22 | 5 |
| 19 | `آپ کیسے ہیں? Ich bin gut.` | 19 | 24 | 5 |
| 20 | `Deutsch umlaut: Fußgänger überqueren` | 12 | 17 | 5 |
| 21 | `你好吗` | 4 | 6 | 2 |
| 22 | `Mixed scripts: English 中文 日本語 한국어` | 14 | 25 | 11 |
| 23 | `Arabic only: مرحبا كيف حالك` | 15 | 20 | 5 |
| 24 | `Hindi: मुझे मशीन लर्निंग पसंद है` | 30 | 46 | 16 |
| 25 | `Email: first.last+tag@example.co.uk` | 9 | 13 | 4 |
| 26 | `IPV6: 2001:0db8:85a3:0000:0000:8a2e:0370:7334` | 32 | 28 | 4 |
| 27 | `Math: E=mc^2 and π ≈ 3.14159` | 16 | 16 | 0 |
| 28 | `Numbers: 12345678901234567890` | 10 | 11 | 1 |
| 29 | `Markdown: **bold** _italic_ `code` [link](https://a.co)` | 19 | 22 | 3 |
| 30 | `Regex: ^[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z]$` | 27 | 41 | 14 |

---

## 5 Surprises (Largest Token-Count Deltas)

### Surprise 1

**String:** `Hindi: मुझे मशीन लर्निंग पसंद है`  
**cl100k_base:** 30 tokens | **gpt2:** 46 tokens | **Δ = 16**

**Why:** Hindi script has very little coverage in GPT-2's vocabulary, causing aggressive byte-level splitting.

### Surprise 2

**String:** `Regex: ^[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z]$`  
**cl100k_base:** 27 tokens | **gpt2:** 41 tokens | **Δ = 14**

**Why:** Different training corpora → different merge rules → same surface text splits into more or fewer subword units depending on the tokenizer.

### Surprise 3

**String:** `https://example.com/path/to/resource?query=tokenization&lang=de&utm_source=newsletter&utm_medium=email&utm_campaign=2026q1`  
**cl100k_base:** 31 tokens | **gpt2:** 42 tokens | **Δ = 11**

**Why:** Long URLs contain percent-encoding (%20), slashes, and query params that fragment into many small tokens in both tokenizers.

### Surprise 4

**String:** `Mixed scripts: English 中文 日本語 한국어`  
**cl100k_base:** 14 tokens | **gpt2:** 25 tokens | **Δ = 11**

**Why:** CJK / Korean ideographs often receive a single token in cl100k_base (trained on more multilingual data) but multiple byte tokens in GPT-2.

### Surprise 5

**String:** `Ich liebe maschinelles Lernen und Urdu: میں سیکھ رہا ہوں۔`  
**cl100k_base:** 32 tokens | **gpt2:** 42 tokens | **Δ = 10**

**Why:** Arabic / Urdu text is largely absent from GPT-2's training corpus, forcing byte-level fallback tokens (1 char → 2-4 tokens).

