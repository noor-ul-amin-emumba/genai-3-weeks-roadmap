# Prompt Pack — 10 Prompts with Escalating Difficulty

**Model:** `openai/gpt-oss-120b`  
**Pass rate:** 2/2

## Quick Summary Table

| ID | Label | Difficulty | Pass? | Evaluation |
|---|---|---|---|---|
| P01 | Plain Instruction | 1/8 | ✓ PASS | Free-form OK |
| P02 | Structured Output – JSON Schema | 2/8 | ✓ PASS | Valid JSON |

---

## P01 — Plain Instruction

**Difficulty:** 1/8  
**Result:** ✓ PASS  
**Evaluation:** Free-form OK

**Description:** A bare user-turn question with no system prompt and no document context. Tests what the model knows from pre-training alone. Risk: hallucination, no grounding.

### System Prompt

*(No system prompt — user turn only)*

### User Prompt

```
What are three ways AI is being used to address climate change? Give a brief explanation for each.
```

### Model Response

**1. Climate‑modeling and weather prediction**  
AI‑driven neural networks and other machine learning (ML) techniques can ingest massive volumes of satellite, sensor, and historical climate data to improve the speed and accuracy of climate models. By learning complex, non‑linear relationships in the atmosphere and oceans, AI helps:  

- **Downscale global climate projections** to regional or city‑level resolutions, giving policymakers finer‑grained impact forecasts.  
- **Accelerate forecasting** – ML surrogates can produce results in minutes instead of days, allowing more frequent scenario testing.  
- **Identify early‑warning signals** for extreme events (heatwaves, floods, hurricanes) so communities can prepare and reduce damage.

**2. Optimizing energy systems and reducing emissions**  
AI is being embedded in the planning, operation, and market participation of low‑carbon energy infrastructures:  

- **Smart grids:** Reinforcement‑learning agents balance supply and demand in real time, integrating variable renewables (solar, wind) while minimizing reliance on fossil‑fuel peaker plants.  
- **Building energy management:** AI‑controlled HVAC, lighting, and occupancy sensors cut commercial and residential electricity use by 10‑30 % on average.  
- **Industrial process optimization:** Machine‑learning models predict equipment failures and suggest process tweaks that lower fuel consumption and waste in sectors such as steel, cement, and chemicals.

**3. Enhancing carbon‑removal and ecosystem monitoring**  
AI helps both in removing CO₂ from the atmosphere and in protecting natural carbon sinks:  

- **Carbon capture and storage (CCS) monitoring:** Computer‑vision algorithms analyze drone‑ or satellite‑based imagery to detect leaks in

**Tokens:** 91 prompt + 400 completion

### Known Failure Risk

Model may hallucinate specific statistics or cite non-existent papers because there is no grounding document.

### Improved Version

Attach the grounding document and instruct the model to base answers only on provided content. Add: 'If you are uncertain, say so.'

---

## P02 — Structured Output – JSON Schema

**Difficulty:** 2/8  
**Result:** ✓ PASS  
**Evaluation:** Valid JSON

**Description:** Requires the model to emit a valid JSON object matching a fixed schema. Tests format compliance.

### System Prompt

```
You are a structured data extraction assistant. You MUST respond with ONLY a valid JSON object — no prose, no markdown fences, no extra text — strictly matching this schema:

{
  "topic": "<string>",
  "findings": [
    {
      "finding": "<string>",
      "source_section": "<string>"
    }
  ],
  "confidence": "<high|medium|low>"
}

Use the document below as your source.

DOCUMENT EXCERPT:

ARTIFICIAL INTELLIGENCE IN CLIMATE CHANGE MITIGATION AND ADAPTATION
A Comprehensive Technical and Policy Review
Report No. ENV-2024-117 | Global Institute for Climate Technology (GICT)
Published: September
... [document excerpt truncated for display]
```

### User Prompt

```
Extract the key finding about AI improving renewable energy efficiency from the document.
```

### Model Response

{
  "topic": "Renewable Energy Efficiency",
  "findings": [
    {
      "finding": "Machine-learning-optimized wind-farm layouts have demonstrated 11–18% gains in annual energy yield over conventional design heuristics, based on a meta-analysis of 47 commercial wind projects in Europe (Osei & Lindqvist, 2024).",
      "source_section": "EXECUTIVE SUMMARY"
    }
  ],
  "confidence": "high"
}

**Tokens:** 969 prompt + 216 completion

### Known Failure Risk

Models often wrap JSON in markdown code fences (```json ... ```) or add preamble text, breaking strict JSON parsers. Schema fields may be hallucinated if the detail is not in the excerpt.

### Improved Version

Add explicit instruction: 'Do NOT wrap in markdown. Output raw JSON only.' Use function-calling / structured output API feature if available. Provide a few-shot example of the expected output.

---
