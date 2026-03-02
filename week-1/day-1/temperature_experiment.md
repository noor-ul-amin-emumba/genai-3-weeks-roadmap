# Prompt Runs

Model: llama-3.3-70b-versatile

Settings:
- temp_0: temperature=0.0, top_p=1.0
- temp_0_7: temperature=0.7, top_p=1.0
- temp_1: temperature=1.0, top_p=1.0

## Prompt 1

**Prompt:** Explain why the sky is blue in 2 sentences.

**temp_0:**

The sky appears blue because of a phenomenon called Rayleigh scattering, where shorter wavelengths of light, such as blue and violet, are scattered more than longer wavelengths by the Earth's atmosphere. As a result, our eyes perceive the scattered blue light as the dominant color of the sky, making it appear blue to us.

**temp_0_7:**

The sky appears blue because of a phenomenon called Rayleigh scattering, where shorter wavelengths of light (like blue and violet) are scattered more than longer wavelengths by the tiny molecules of gases in the atmosphere. This scattering effect gives the sky its blue color, as our eyes perceive the scattered blue light from all directions.

**temp_1:**

The sky appears blue because of a phenomenon called Rayleigh scattering, where shorter wavelengths of light, such as blue and violet, are scattered more than longer wavelengths by the Earth's atmosphere. This scattering of blue light in all directions is what gives the sky its blue color, as it reaches our eyes from all parts of the atmosphere.

## Prompt 2

**Prompt:** Write a haiku about city rain.

**temp_0:**

Raindrops on pavement
City streets shine wet and grey
Urban calm descends

**temp_0_7:**

Raindrops on pavement
City streets in misty gray
Urban calm descends

**temp_1:**

Raindrops on pavement
City lights reflected bright
Wet urban delight

## Prompt 3

**Prompt:** Give 5 concise tips for debugging Python code.

**temp_0:**

1. Use `print()` statements to track variable values.
2. Run code in a debugger like `pdb`.
3. Check for typos and syntax errors.
4. Test small code sections separately.
5. Use `try-except` blocks to catch exceptions.

**temp_0_7:**

1. Use `print()` for variable checks.
2. Run with `python -i` for interactive debugging.
3. Utilize `pdb` for step-by-step debugging.
4. Check logs and error messages.
5. Use a debugger like PyCharm's built-in tool.

**temp_1:**

1. Use print() statements to track variables.
2. Run code in a debugger like pdb.
3. Check error messages for line numbers.
4. Test small code segments separately.
5. Use a linter to catch syntax errors.

## Prompt 4

**Prompt:** Summarize the story of Cinderella in 1 sentence.

**temp_0:**

Cinderella, a mistreated young woman, attends a royal ball with the help of a fairy godmother and captures the heart of a prince, ultimately escaping her difficult life.

**temp_0_7:**

Cinderella, a kind and mistreated young woman, attends a royal ball with the help of a fairy godmother and captures the heart of a prince, ultimately escaping her difficult life with her evil stepmother and stepsisters.

**temp_1:**

Cinderella, a young girl mistreated by her stepmother and stepsisters, attends a royal ball with the help of a fairy godmother and captures the heart of a prince, ultimately leading to their marriage.

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
  "title": "Exploring Europe",
  "tags": ["travel", "adventure", "europe"],
  "score": 4.5
}
```

**temp_0_7:**

```json
{
  "title": "Exploring Europe",
  "tags": ["travel", "adventure", "europe"],
  "score": 4.5
}
```

**temp_1:**

```json
{
  "title": "Exploring Europe",
  "tags": ["travel", "europe", "adventure"],
  "score": 4.5
}
```

## Prompt 7

**Prompt:** Provide a SQL query to list the top 3 customers by total revenue.

**temp_0:**

```sql
SELECT customer_name, SUM(revenue) AS total_revenue
FROM sales
GROUP BY customer_name
ORDER BY total_revenue DESC
LIMIT 3;
```

**temp_0_7:**

```sql
SELECT customer_name, SUM(order_total) as total_revenue
FROM orders
GROUP BY customer_name
ORDER BY total_revenue DESC
LIMIT 3;
```

**temp_1:**

```sql
SELECT customer_name, SUM(order_total) AS total_revenue
FROM orders
GROUP BY customer_name
ORDER BY total_revenue DESC
LIMIT 3;
```

## Prompt 8

**Prompt:** List 3 risks of deploying LLMs in financial workflows.

**temp_0:**

1. Data bias and inaccuracies
2. Regulatory non-compliance
3. Cybersecurity vulnerabilities

**temp_0_7:**

1. Data bias and inaccuracy
2. Regulatory non-compliance
3. Cybersecurity vulnerabilities

**temp_1:**

1. Data leakage and security breaches.
2. Model bias and discriminatory outcomes.
3. Regulatory non-compliance and auditing challenges.

## Prompt 9

**Prompt:** Suggest 3 catchy product names for an eco-friendly water bottle.

**temp_0:**

1. HydraGreen
2. EcoSip
3. AquaPure

**temp_0_7:**

1. HydraGreen
2. EcoSip
3. AquaPure

**temp_1:**

1. EcoHydrate
2. GreenSip
3. AquaPure

## Prompt 10

**Prompt:** Explain the difference between precision and recall in 2 sentences.

**temp_0:**

Precision measures the proportion of true positives among all predicted positive instances, while recall measures the proportion of true positives among all actual positive instances. In other words, precision is about avoiding false positives, and recall is about detecting all actual positives.

**temp_0_7:**

Precision measures the accuracy of positive predictions, while recall measures the proportion of actual positives that are correctly identified. A model with high precision but low recall is precise but misses many actual positives, whereas a model with high recall but low precision is sensitive but prone to false positives.

**temp_1:**

Precision measures the accuracy of positive predictions, or the proportion of true positives among all predicted positives. Recall measures the completeness of positive predictions, or the proportion of true positives among all actual positives, highlighting the difference between what was predicted and what actually existed.

