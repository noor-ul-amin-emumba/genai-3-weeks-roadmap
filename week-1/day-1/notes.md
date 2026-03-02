# Week 1 - Day 1

Implemented a prompt experiment with three decoding settings to understand how temperature affects LLM outputs.

## LLM behavior cheatsheet

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

## Tokens in LLMs — Concise Summary

**Tokens = the units of text an LLM understands.**
They are numeric representations of words or parts of words.

**Encoding & Decoding**

- **Encoding:** Text → tokens → numbers
- **Decoding:** Numbers → tokens → readable text

**LLM Flow**

1. Input text is **tokenized**
2. Model **processes tokens**
3. Model generates **output tokens**
4. Tokens are **decoded into text**

**What you are billed for**

- **Input tokens:** prompt + chat history + system instructions + tools
- **Output tokens:** model’s response
  💡 Both are charged (often at different rates).

---

**How tokens are created**

Tokenizers learn from a large text corpus and build a **vocabulary of common patterns**:

1. Start with **characters**
2. Add frequent **character groups** (e.g., `TH`, `HE`, `AT`)
3. Add **whole words** if common (e.g., `THE`)

This is why tokens can be:

- a character
- part of a word
- a full word

---

**Vocabulary size effect**

Larger vocabulary → **fewer tokens per word** → more efficient processing.

Example for **“understanding”**:

- Small vocab → many tokens
- Large vocab → fewer tokens

---

**Rare / made-up words**

Uncommon words aren’t in the vocabulary → split into **many smaller tokens**
➡️ more tokens → higher cost.

---

**Cost optimization tip**

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
