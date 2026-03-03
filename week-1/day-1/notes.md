# Week 1 - Day 1

## Core Concepts

### 1. Next-Token Prediction & Logits → Decoding

**How LLMs generate text:**

1. Model receives tokenized input
2. For each position, model outputs **logits** (raw scores for all possible next tokens)
3. Logits are converted to **probabilities** using softmax
4. A token is **sampled** based on these probabilities (controlled by temperature/top-p)
5. Selected token is **decoded** back to text and added to output
6. Process repeats until stopping condition

**Example:** Given "The cat sat on the", model assigns probabilities:

- "mat" = 0.45
- "floor" = 0.30
- "chair" = 0.15
- etc.

### 2. Why Models Hallucinate

#### Root cause: Optimization target ≠ truth

LLMs are trained to predict the next most _plausible_ token, not the next most _truthful_ token.

- ✅ Trained on: statistical patterns in text (what words typically follow other words)
- ❌ Not trained on: factual accuracy or verifying truth

**Result:** The model can confidently generate fluent, grammatically correct text that is completely false.

**Example:** If asked about a fake person, the model might generate a plausible-sounding biography because it's optimizing for "what would a biography look like" rather than "is this person real."

### 3. Common Terms

**System Prompt:**

- Instructions given to the model that set its behavior/role
- Processed before user input
- Examples: "You are a helpful assistant", "You are a Python expert"
- Can override user intent if conflicts arise

**Instruction Tuning:**

- Fine-tuning process where models learn to follow instructions
- Trained on (instruction, response) pairs
- Makes models better at following commands rather than just completing text
- Trade-off: models optimized for following instructions, not necessarily for truth

**Temperature:**

- Controls randomness in token selection
- Low (0-0.3): deterministic, focused
- High (0.8-1.0): creative, diverse, more hallucination risk

**Top-p (nucleus sampling):**

- Limits token selection to top X% probability mass
- Example: top_p=0.9 means "only sample from tokens that make up 90% of probability"
- Provides more stable diversity control than temperature alone

### 4. Tokens vs Words & BPE Intuition

**Tokens ≠ Words:**

- Common words = 1 token ("cat", "the")
- Uncommon words = multiple tokens ("antidisestablishmentarianism" → 5+ tokens)
- Subwords = 1 token ("ing", "un")

**BPE (Byte-Pair Encoding) — How vocabularies are built:**

Starting corpus: `"the cat sat on the mat"`

1. **Initialize:** Each character is a token: `[t, h, e, c, a, s, o, n, m]`
2. **Find most frequent pair:** "t" + "h" appears twice → merge into "th"
3. **Update vocabulary:** `[th, e, c, a, s, o, n, m]` + merge rule `("t", "h") → "th"`
4. **Repeat:** Next most frequent is "th" + "e" → merge into "the"
5. **Continue** until vocabulary reaches target size (e.g., 50k tokens)

**Result:** Model learns common subword patterns that minimize token count for frequent text.

### 5. Why JSON/Code/URLs/Multilingual Text Explode Tokens

**Common patterns:**

| Text Type        | Why Token Count Increases                                                                 |
| ---------------- | ----------------------------------------------------------------------------------------- |
| **JSON**         | Braces `{}`, quotes `""`, commas create separate tokens; keys fragment                    |
| **Code**         | Operators (`::`, `->`, `==`), special chars, indentation not in natural language vocab    |
| **URLs**         | Slashes `/`, percent-encoding `%20`, domain fragments rarely seen together                |
| **Multilingual** | Non-English scripts (Arabic, Chinese, Hindi) trained on less data → smaller subword units |
| **Emojis**       | Encoded as multiple bytes → split into many tokens by byte-level BPE                      |

**Example from our tokenization comparison:**

- `"Hello"` = 1 token (common English)
- `"مرحبا"` (Arabic "hello") = 3-5 tokens (less common in training data)
- `"https://example.com/api?key=123"` = 15+ tokens (special chars fragment)

**Bottom line:** Token count depends on how similar your text is to the model's training data.

## LLM behavior cheatsheet

Implemented a prompt experiment with three decoding settings to understand how temperature affects LLM outputs.

Findings

- Temperature 0 gives consistent, deterministic and accurate outputs.

- Temperature 0.7 provides the best balance.

- Temperature 1 increases creativity and hallucination but reduces reliability.

- Structured outputs (JSON/code) break more often at high temperature.

Efficient usage could be:

| Use case        | Temperature |
| --------------- | ----------- |
| Code generation | 0–0.2       |
| API/JSON        | 0           |
| Explanations    | 0.5–0.7     |
| Brainstorming   | 0.8–1       |

## Prompt experiment (10 prompts x 3 temps)

- Script: run [week-1/day-1/temperature_experiment.py](week-1/day-1/temperature_experiment.py)
- Outputs: `prompt_runs.md` (generated in this folder)
- Settings: temperature = 0, 0.7, 1.0 with top_p = 1.0

## Tokenization comparison (30 strings x 2 tokenizers)

- Script: run [week-1/day-1/tokenize_compare.py](week-1/day-1/tokenize_compare.py)
- Outputs: `tokenization_comparison.csv`, `tokenization_comparison.md`
- Model A: `cl100k_base` (tiktoken)
- Model B: `gpt2` (GPT2TokenizerFast)

### Tokens

Here’s a **clear, concise, interview-ready version** of your explanation:

---

## Tokens in LLMs — Concise Summary

**Tokens = the units of text an LLM understands.**
They are numeric representations of words or parts of words.

### 🔹 Encoding & Decoding

- **Encoding:** Text → tokens → numbers
- **Decoding:** Numbers → tokens → readable text

### 🔹 LLM Flow

1. Input text is **tokenized**
2. Model **processes tokens**
3. Model generates **output tokens**
4. Tokens are **decoded into text**

### 🔹 What you are billed for

- **Input tokens:** prompt + chat history + system instructions + tools
- **Output tokens:** model’s response
  💡 Both are charged (often at different rates).

---

## 🔹 How tokens are created

Tokenizers learn from a large text corpus and build a **vocabulary of common patterns**:

1. Start with **characters**
2. Add frequent **character groups** (e.g., `TH`, `HE`, `AT`)
3. Add **whole words** if common (e.g., `THE`)

This is why tokens can be:

- a character
- part of a word
- a full word

---

## 🔹 Vocabulary size effect

Larger vocabulary → **fewer tokens per word** → more efficient processing.

Example for **“understanding”**:

- Small vocab → many tokens
- Large vocab → fewer tokens

---

## 🔹 Rare / made-up words

Uncommon words aren’t in the vocabulary → split into **many smaller tokens**
➡️ more tokens → higher cost.

---

## 🔹 Cost optimization tip

Design prompts that:

- are shorter
- produce shorter outputs
  → fewer tokens → cheaper.

## Logits

Logits are the final numerical outputs of the model, which are transformed into probabilities of picking a new token.
OR
Logits = raw scores for each possible next token before softmax converts them into probabilities.

In simple terms, when a large language model (LLM) generates text, it assigns:

- **Logit Value:** A single number representing the model's prediction for how likely a specific token is to be the next token in a sequence.
- **Token:** A piece of a word, a whole word, or a punctuation mark – the basic units that the LLM processes.
- **50,257 Numbers:** This refers to the size of the LLM's vocabulary. The LLM is predicting which of these 50,257 tokens is most likely to come next.
- **Vector:** A list of numbers. In this case, it's a list of 50,257 logit values.
- **Associated with each input token:** For every token the LLM processes as input, it generates one of these vectors as output.

**In simpler terms:**

Imagine the LLM is reading a sentence. After reading each word (token), it tries to guess the next word. It does this by assigning a score (logit value) to every word in its vocabulary (all 50,257 of them). The list of all those scores (the vector) is the LLM's prediction for what comes next, based on the current word it just read.

The statement "if your text has 5 tokens, then the final output of the model will be a matrix of size 5x50257" means that for an input text sequence of 5 tokens, the model produces an output matrix where:

- The number of rows is equal to the number of tokens in the input text (5 in this case).
- The number of columns is 50257, which likely represents the size of the model's vocabulary (the number of unique words or sub-word units the model can recognize and output).

Therefore, each row in the 5x50257 matrix can be interpreted as a probability distribution over the vocabulary for a specific token in the input sequence.

## Temperature and Top P Parameters in LLMs

Temperature and Top P (nucleus sampling) are two fundamental parameters that govern the behaviour of AI language models. These parameters act as levers, allowing users to adjust the creativity and predictability of AI outputs.

- **Temperature** controls the randomness or "creativity" of the model's outputs. A lower temperature results in more predictable and focused responses, while a higher temperature encourages more diverse and potentially creative outputs.
- **Top P** or **nucleus sampling**, determines the range of tokens the model considers when generating each word. It allows for a balance between diversity and quality in the output, often providing more nuanced control than temperature alone.

Understanding these parameters is crucial for anyone seeking to tailor AI outputs to meet specific requirements, whether that be creativity, precision, or a balance of both.
