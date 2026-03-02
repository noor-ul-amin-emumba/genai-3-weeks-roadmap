# Tokenization Comparison

Generated: 2026-03-02T16:27:05.187848+00:00

Model A: cl100k_base

Model B: gpt2

| # | String | Model A | Model B | Delta |
|---|--------|---------|---------|-------|
| 1 | def hello_world(): return 'hello' | 9 | 13 | 4 |
| 2 | SELECT * FROM users WHERE email LIKE '%@example.com'; | 12 | 14 | 2 |
| 3 | Ich liebe maschinelles Lernen und Urdu: میں سیکھ رہا ہوں. | 31 | 41 | 10 |
| 4 | 你好吗 | 4 | 6 | 2 |
| 5 | Here is a long URL: https://example.com/path/to/resource?query=tokenization&lang=de&utm_source=newsletter&utm_medium=email&utm_campaign=2026q1 | 37 | 48 | 11 |
| 6 | JSON: {"user":{"id":12345,"roles":["admin","editor"]},"active":true} | 21 | 22 | 1 |
| 7 | Emoji test: 😀🚀🔥✨🌍 | 15 | 18 | 3 |
| 8 | C++ template: std::vector<std::string> v; | 13 | 14 | 1 |
| 9 | Markdown: **bold** _italic_ `code` [link](https://a.co) | 19 | 22 | 3 |
| 10 | Numbers: 12345678901234567890 | 10 | 11 | 1 |
| 11 | Email: first.last+tag@example.co.uk | 9 | 13 | 4 |
| 12 | IPV6: 2001:0db8:85a3:0000:0000:8a2e:0370:7334 | 32 | 28 | 4 |
| 13 | Regex: ^[A-Za-z0-9_]+$ | 12 | 17 | 5 |
| 14 | Shell: export PATH=/usr/local/bin:$PATH | 10 | 13 | 3 |
| 15 | Math: E=mc^2 and π ≈ 3.14159 | 16 | 16 | 0 |
| 16 | Tabs and spaces aligned | 6 | 9 | 3 |
| 17 | Whitespace collapse? maybe | 6 | 12 | 6 |
| 18 | XML: <note><to>Tove</to><from>Jani</from></note> | 19 | 22 | 3 |
| 19 | YAML: key: value list: - a - b | 16 | 18 | 2 |
| 20 | CSV: id,name,score 1,Alice,98 2,Bob,87 | 18 | 20 | 2 |
| 21 | SQL with emojis: INSERT INTO logs(msg) VALUES('ok 😀'); | 14 | 20 | 6 |
| 22 | Arabic only: مرحبا كيف حالك | 15 | 20 | 5 |
| 23 | Hindi: मुझे मशीन लर्निंग पसंद है | 30 | 46 | 16 |
| 24 | Deutsch umlaut: Fußgänger überqueren | 12 | 17 | 5 |
| 25 | Mixed scripts: English 中文 日本語 한국어 | 14 | 25 | 11 |
| 26 | URL encoded: https://example.com/search?q=hello%20world%20%F0%9F%9A%80 | 27 | 30 | 3 |
| 27 | Code comment: // TODO: refactor; // FIXME: bug | 12 | 15 | 3 |
| 28 | Path: C:\Program Files\MyApp\app.exe | 12 | 13 | 1 |
| 29 | Quoted JSON: {"text":"He said, \"hello\""} | 14 | 14 | 0 |
| 30 | Long JSON array: [1,2,3,4,5,6,7,8,9,10] | 25 | 25 | 0 |

## 5 Surprises (largest deltas)

1. Hindi: मुझे मशीन लर्निंग पसंद है
   - Model A: 30 | Model B: 46
   - Why: Different vocabularies merge or split common substrings differently.

2. Here is a long URL: https://example.com/path/to/resource?query=tokenization&lang=de&utm_source=newsletter&utm_medium=email&utm_campaign=2026q1
   - Model A: 37 | Model B: 48
   - Why: URLs fragment into many sub-tokens due to slashes, punctuation, and percent-encoding.

3. Mixed scripts: English 中文 日本語 한국어
   - Model A: 14 | Model B: 25
   - Why: CJK characters often map to individual tokens, raising counts quickly.

4. Ich liebe maschinelles Lernen und Urdu: میں سیکھ رہا ہوں.
   - Model A: 31 | Model B: 41
   - Why: Arabic/Urdu script usually breaks into shorter sub-tokens, increasing counts.

5. Whitespace collapse? maybe
   - Model A: 6 | Model B: 12
   - Why: Different vocabularies merge or split common substrings differently.

