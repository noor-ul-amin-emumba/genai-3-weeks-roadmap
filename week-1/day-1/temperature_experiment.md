# Prompt Runs

Model: openai/gpt-oss-120b

Settings:
- temp_0: temperature=0.0, top_p=1.0
- temp_0_7: temperature=0.7, top_p=1.0
- temp_1: temperature=1.0, top_p=1.0

## Prompt 1

**Prompt:** Explain why the sky is blue in 2 sentences.

**temp_0:**

The sky appears blue because molecules in Earth’s atmosphere scatter shorter (blue) wavelengths of sunlight more efficiently than longer (red) wavelengths—a phenomenon called Rayleigh scattering. This scattered blue light reaches our eyes from all directions, giving the sky its characteristic color.

**temp_0_7:**

The sky appears blue because molecules in the atmosphere scatter shorter (blue) wavelengths of sunlight more efficiently than longer (red) wavelengths—a phenomenon known as Rayleigh scattering. As a result, more blue light reaches our eyes from all directions, giving the sky its characteristic color.

**temp_1:**

The sky appears blue because molecules in Earth’s atmosphere scatter short‑wavelength (blue) light from the Sun more efficiently than longer‑wavelength (red) light—a process called Rayleigh scattering. This scattered blue light reaches our eyes from all directions, giving the sky its characteristic color.

## Prompt 2

**Prompt:** Write a haiku about city rain.

**temp_0:**

City streets glisten—  
Umbrellas bloom, soft patter,  
Night sighs in gray mist.

**temp_0_7:**

City lights flicker,  
Rain drums on the sidewalk’s skin—  
Night breathes, softened.

**temp_1:**



## Prompt 3

**Prompt:** Give 5 concise tips for debugging Python code.

**temp_0:**

1. **Read the traceback** – Identify the exact line and error type.  
2. **Use `print`/`logging`** – Inspect variable values and program flow.  
3. **Run in a debugger** – Step through code with `pdb` or an IDE.  
4. **Check assumptions** – Verify data types, indices, and external resources.  
5. **Write minimal reproductions** – Isolate the problem in a small, self‑contained script.

**temp_0_7:**

1. **Read the traceback** – Identify the exact line and error type first.  
2. **Add `print`/`logging` statements** – Show variable values and program flow.  
3. **Use a debugger** – Step through code with `pdb` or an IDE’s breakpoints.  
4. **Check assumptions** – Verify data types, lengths, and external resources.  
5. **Write minimal reproductions** – Isolate the problematic code in a small, testable script.

**temp_1:**

- **Read the traceback**: Start at the last line; it points to the exact error location.  
- **Use a debugger**: `python -m pdb script.py` or IDE breakpoints to step through code.  
- **Print intermediate values**: `print()` or `logging.debug()` to inspect variables and flow.  
- **Write small test cases**: Isolate the failing part in a minimal reproducible example.  
- **Check assumptions**: Verify data types, boundaries, and external resources (files, APIs).

## Prompt 4

**Prompt:** Summarize the story of Cinderella in 1 sentence.

**temp_0:**

Cinderella, a mistreated girl aided by a magical fairy godmother, attends a royal ball, wins the prince’s love, and regains her rightful place after the prince discovers her through a lost glass slipper.

**temp_0_7:**

Cinderella, a mistreated orphan, attends a royal ball with magical help, captivates the prince, and is recognized by her lost glass slipper, leading to her escape from her cruel family and a happily‑ever‑after marriage.

**temp_1:**

A mistreated girl, helped by a magical godmother to attend a royal ball, wins the prince’s love, and escapes her abusive family.

## Prompt 5

**Prompt:** Translate to Urdu: 'Good morning, how are you?'.

**temp_0:**

صبح بخیر، آپ کیسے ہیں؟

**temp_0_7:**

صبح بخیر، آپ کیسے ہیں؟

**temp_1:**

صبح بخیر، آپ کیسے ہیں؟

## Prompt 6

**Prompt:** Create a JSON object with keys title, tags, score for a travel blog post.

**temp_0:**

```json
{
  "title": "Exploring the Hidden Gems of Kyoto",
  "tags": ["Japan", "travel", "culture", "food", "photography"],
  "score": 9.4
}
```

**temp_0_7:**

```json
{
  "title": "Exploring the Hidden Gems of Kyoto",
  "tags": ["Japan", "travel", "culture", "food", "photography"],
  "score": 9.4
}
```

**temp_1:**

```json
{
  "title": "Exploring the Hidden Gems of Kyoto",
  "tags": ["Japan", "Kyoto", "Travel", "Culture", "Food"],
  "score": 9.4
}
```

## Prompt 7

**Prompt:** Provide a SQL query to list the top 3 customers by total revenue.

**temp_0:**

```sql
SELECT
    c.customer_id,
    c.customer_name,
    SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM customers      AS c
JOIN orders         AS o  ON o.customer_id = c.customer_id
JOIN order_items    AS oi ON oi.order_id = o.order_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_revenue DESC
LIMIT 3;
```

**temp_0_7:**

```sql
-- Assuming:
--   customers (customer_id, name, …)
--   orders    (order_id, customer_id, order_date, …)
--   order_items (order_id, product_id, quantity, unit_price)

SELECT
    c.customer_id,
    c.name,
    SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM customers      AS c
JOIN orders         AS o  ON o.customer_id = c.customer_id
JOIN order_items    AS oi ON oi.order_id   = o.order_id
GROUP BY c.customer_id, c.name
ORDER BY total_revenue DESC
LIMIT 3;
```

**temp_1:**

```sql
SELECT
    c.customer_id,
    c.customer_name,
    SUM(o.amount) AS total_revenue
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_revenue DESC
LIMIT 3;
```

## Prompt 8

**Prompt:** List 3 risks of deploying LLMs in financial workflows.

**temp_0:**

- **Model bias & inaccurate predictions** – can lead to faulty credit assessments or investment decisions.  
- **Data privacy & regulatory violations** – inadvertent exposure of sensitive financial data may breach GDPR, PCI DSS, etc.  
- **Operational & security vulnerabilities** – adversarial prompts or model drift can cause system failures or fraud exploitation.

**temp_0_7:**

1. **Model Hallucinations** – Generating inaccurate or fabricated data that can lead to erroneous financial decisions.  
2. **Bias & Fairness** – Propagating or amplifying existing biases, potentially causing discriminatory outcomes in credit scoring or lending.  
3. **Regulatory & Compliance Violations** – Failing to meet strict reporting, data‑privacy, and audit requirements, exposing firms to legal penalties.

**temp_1:**

1. **Model bias leading to unfair credit decisions.**  
2. **Incorrect or outdated financial predictions causing monetary loss.**  
3. **Regulatory non‑compliance due to opaque decision‑making.**

## Prompt 9

**Prompt:** Suggest 3 catchy product names for an eco-friendly water bottle.

**temp_0:**

1. **EcoSip**  
2. **GreenFlow Bottle**  
3. **PureTerra Hydrator**

**temp_0_7:**

1. **EcoSip**  
2. **GreenFlow Bottle**  
3. **PurePlanet Hydrator**

**temp_1:**

1. PureSip Eco  
2. GreenFlow Bottle  
3. TerraQuench™

## Prompt 10

**Prompt:** Explain the difference between precision and recall in 2 sentences.

**temp_0:**

Precision measures the proportion of predicted positives that are actually correct, while recall measures the proportion of actual positives that were correctly identified. High precision means few false positives; high recall means few false negatives.

**temp_0_7:**

Precision measures the proportion of retrieved items that are actually relevant, while recall measures the proportion of all relevant items that are successfully retrieved. High precision means few false positives, and high recall means few false negatives.

**temp_1:**

Precision measures the proportion of predicted positive cases that are actually correct, while recall measures the proportion of all actual positive cases that the model successfully identified. High precision means few false positives; high recall means few false negatives.

