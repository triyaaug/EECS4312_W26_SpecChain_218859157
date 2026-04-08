"""Combined Step 4.1 + 4.2: Review Grouping + Persona Generation"""

import json
from groq import Groq

# -------------------------
# CONFIG
# -------------------------
API_KEY = "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"  # replace this
REVIEW_CLEAN_FILE = "../data/reviews_clean.jsonl"
REVIEW_GROUPS_FILE = "../data/review_groups_auto.json"
PERSONAS_FILE = "../personas/personas_auto.json"
MAX_SAMPLE = 100  # avoid token limit

client = Groq(api_key=API_KEY)

# -------------------------
# LOAD REVIEWS
# -------------------------
with open(REVIEW_CLEAN_FILE, "r", encoding="utf-8") as f:
    reviews = [json.loads(line) for line in f]

sample_reviews = reviews[:MAX_SAMPLE]

# Format reviews for prompt
formatted_reviews = [
    {"reviewId": r["reviewId"], "content": r["content"]}
    for r in sample_reviews
]

# -------------------------
# STEP 4.1: GROUP REVIEWS
# -------------------------
prompt_group_reviews = f"""
You are given user reviews from a meditation app (Headspace).

Group these reviews into 5 meaningful categories based on common themes.

Each group must include:
- group_id (G1, G2, G3, G4, G5)
- theme (short description)
- review_ids (list of reviewId values)

IMPORTANT: Return only valid JSON. No explanations, no extra text, no markdown.

Reviews:
{json.dumps(formatted_reviews, indent=2)}

Return ONLY valid JSON in this format:
{{
  "groups": [
    {{
      "group_id": "G1",
      "theme": "...",
      "review_ids": ["id1", "id2"]
    }}
  ]
}}
"""

response_groups = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[{"role": "user", "content": prompt_group_reviews}],
    temperature=0.3
)

result_text = response_groups.choices[0].message.content.strip()

# Clean ``` if present
if result_text.startswith("```"):
    lines = result_text.split("\n")
    if lines[0].startswith("```"):
        lines = lines[1:]
    if lines[-1].strip() == "```":
        lines = lines[:-1]
    result_text = "\n".join(lines)

try:
    review_groups = json.loads(result_text)
except json.JSONDecodeError:
    print("JSON parsing failed for review groups.")
    review_groups = {"groups": []}

# -------------------------
# ADD EXAMPLE REVIEWS (2 per group)
# -------------------------
review_lookup = {r["reviewId"]: r["content"] for r in sample_reviews}

for g in review_groups.get("groups", []):
    example_texts = []
    for rid in g.get("review_ids", [])[:2]:
        if rid in review_lookup:
            example_texts.append(review_lookup[rid])
    g["example_reviews"] = example_texts

# Save review groups
with open(REVIEW_GROUPS_FILE, "w", encoding="utf-8") as f:
    json.dump(review_groups, f, indent=4)

print(f"Step 4.1 complete: saved to {REVIEW_GROUPS_FILE}")

# -------------------------
# STEP 4.2: GENERATE PERSONAS
# -------------------------

# Attach review_texts for persona generation
for g in review_groups.get("groups", []):
    g["review_texts"] = [
        review_lookup.get(rid, "") for rid in g["review_ids"][:10]
    ]

prompt_personas = f"""
You are given grouped user reviews for a meditation app.

For each group, create a persona.

Each persona must include:
- id (P1, P2, etc.)
- name (same as the group theme)
- description (short summary of the user)
- derived_from_group (group_id)
- goals (list)
- pain_points (list)
- context (list)
- constraints (list)
- evidence_reviews (use review_ids)

IMPORTANT: Return ONLY valid JSON.

Groups:
{json.dumps(review_groups.get("groups", []), indent=2)}

Return JSON in this format:
{{
  "personas": [
    {{
      "id": "P1",
      "name": "...",
      "description": "...",
      "derived_from_group": "G1",
      "goals": [],
      "pain_points": [],
      "context": [],
      "constraints": [],
      "evidence_reviews": []
    }}
  ]
}}
"""

response_personas = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[{"role": "user", "content": prompt_personas}],
    temperature=0.3
)

result_text_personas = response_personas.choices[0].message.content.strip()

# Clean ``` if present
if result_text_personas.startswith("```"):
    lines = result_text_personas.split("\n")
    if lines[0].startswith("```"):
        lines = lines[1:]
    if lines[-1].strip() == "```":
        lines = lines[:-1]
    result_text_personas = "\n".join(lines)

try:
    personas_json = json.loads(result_text_personas)
except json.JSONDecodeError:
    print("JSON parsing failed for personas.")
    personas_json = {"personas": []}

# Save personas
with open(PERSONAS_FILE, "w", encoding="utf-8") as f:
    json.dump(personas_json, f, indent=4)

print(f"Step 4.2 complete: saved to {PERSONAS_FILE}")