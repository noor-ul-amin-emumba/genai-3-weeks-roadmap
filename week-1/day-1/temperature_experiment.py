# import json
import importlib
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2]))

config = importlib.import_module("config")
MODEL = config.MODEL
call_llm = config.call_llm

PROMPTS = [
    "Explain why the sky is blue in 2 sentences.",
    "Write a haiku about city rain.",
    "Give 5 concise tips for debugging Python code.",
    "Summarize the story of Cinderella in 1 sentence.",
    "Translate to Urdu: 'Good morning, how are you?'.",
    "Create a JSON object with keys title, tags, score for a travel blog post.",
    "Provide a SQL query to list the top 3 customers by total revenue.",
    "List 3 risks of deploying LLMs in financial workflows.",
    "Suggest 3 catchy product names for an eco-friendly water bottle.",
    "Explain the difference between precision and recall in 2 sentences.",
]

SETTINGS = [
    {"temperature": 0.0, "top_p": 1.0, "label": "temp_0"},
    {"temperature": 0.7, "top_p": 1.0, "label": "temp_0_7"},
    {"temperature": 1.0, "top_p": 1.0, "label": "temp_1"},
]

SYSTEM_PROMPT = (
    "You are a concise assistant. Keep responses short and direct."
)

results = {
    "model": MODEL,
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "settings": SETTINGS,
    "prompts": [],
}

for prompt in PROMPTS:
    entry = {"prompt": prompt, "responses": {}}
    for setting in SETTINGS:
        content, _, _ = call_llm(
            system=SYSTEM_PROMPT,
            user=prompt,
            max_tokens=200,
            temperature=setting["temperature"],
            top_p=setting["top_p"],
            label=setting["label"],
        )
        entry["responses"][setting["label"]] = content
    results["prompts"].append(entry)

# out_json = Path(__file__).parent / "temperature_experiment.json"
# with open(out_json, "w", encoding="utf-8") as f:
#     json.dump(results, f, ensure_ascii=False, indent=2)

out_md = Path(__file__).parent / "temperature_experiment.md"
with open(out_md, "w", encoding="utf-8") as f:
    f.write("# Prompt Runs\n\n")
    f.write(f"Model: {MODEL}\n\n")
    f.write("Settings:\n")
    for setting in SETTINGS:
        f.write(
            f"- {setting['label']}: temperature={setting['temperature']}, top_p={setting['top_p']}\n"
        )
    f.write("\n")
    for idx, item in enumerate(results["prompts"], start=1):
        f.write(f"## Prompt {idx}\n\n")
        f.write(f"**Prompt:** {item['prompt']}\n\n")
        for setting in SETTINGS:
            label = setting["label"]
            f.write(f"**{label}:**\n\n{item['responses'][label]}\n\n")

# print(f"Wrote {out_json}")
print(f"Wrote {out_md}")
