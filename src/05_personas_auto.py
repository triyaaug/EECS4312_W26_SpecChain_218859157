"""Combined Step 4.1 + 4.2: Review Grouping + Persona Generation"""
import json
from groq import Groq

# -------------------------
# CONFIG
# -------------------------
API_KEY = "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"  # replace with your valid Groq API key
REVIEW_CLEAN_FILE = "../data/reviews_clean.jsonl"
REVIEW_GROUPS_FILE = "../data/review_groups_auto.json"
PERSONAS_FILE = "../personas/personas_auto.json"
MAX_SAMPLE = 100  # to avoid token limits

client = Groq(api_key=API_KEY)

# -------------------------
# STEP 4.1: AUTOMATIC REVIEW GROUPING
# -------------------------
with open(REVIEW_CLEAN_FILE, "r", encoding="utf-8") as f:
    reviews = [json.loads(line) for line in f]

sample_reviews = reviews[:MAX_SAMPLE]

# Format reviews for the prompt
formatted_reviews = [
    {"reviewId": r["reviewId"], "content": r["content"]}
    for r in sample_reviews
]

prompt_group_reviews = f"""
You are given user reviews from a meditation app (Headspace).

Group these reviews into 5 meaningful categories based on common themes.

Each group must include:
- group_id (G1, G2, G3, G4, G5)
- theme (short description)
- review_ids (list of reviewId values)

IMPORTANT: Return only valid JSON. No explanations, no extra text, no markdown, no comments.

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

# Call Groq API to generate review groups
response_groups = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[{"role": "user", "content": prompt_group_reviews}],
    temperature=0.2
)

result_text = response_groups.choices[0].message.content.strip()

# Remove ``` if Groq wraps output in codeblock
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
    print("JSON parsing failed for review groups. Saving raw output instead.")
    review_groups = {"raw_output": result_text}

# Save Step 4.1 output
with open(REVIEW_GROUPS_FILE, "w", encoding="utf-8") as f:
    json.dump(review_groups, f, indent=4)

print(f"Step 4.1 complete: review groups saved to {REVIEW_GROUPS_FILE}")

# -------------------------
# STEP 4.2: AUTOMATIC PERSONA GENERATION
# -------------------------
# Persona prompt template
prompt_personas_template = """
You are given groups of user reviews for a meditation app.

For each group, create a structured persona object. Each persona must:
- Have a 'name' equal to the group's 'theme'.
- Include the 'group_id' it was derived from.
- Include a 'summary' that captures the key characteristics and needs of users in this group.
- Include 'key_reviews', which is a list of some representative reviews from this group.

Return ONLY valid JSON. Do not include any explanations or extra text.

Groups:
{groups}

Return personas in this format:
{{
  "personas": [
    {{
      "group_id": "G1",
      "name": "...",
      "summary": "...",
      "key_reviews": ["review text 1", "review text 2"]
    }}
  ]
}}
"""

# Only include a subset of reviews for each group to avoid token limit
for g in review_groups.get("groups", []):
    g["review_texts"] = [
        next((r["content"] for r in sample_reviews if r["reviewId"] == rid), "")
        for rid in g["review_ids"][:10]  # up to 10 reviews per group
    ]

prompt_personas = prompt_personas_template.format(groups=json.dumps(review_groups.get("groups", []), indent=2))

# Call Groq API to generate personas
response_personas = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[{"role": "user", "content": prompt_personas}],
    temperature=0.2
)

result_text_personas = response_personas.choices[0].message.content.strip()

# Remove ``` if Groq wraps output in codeblock
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
    print("JSON parsing failed for personas. Saving raw output instead.")
    personas_json = {"raw_output": result_text_personas}

# Save Step 4.2 output
with open(PERSONAS_FILE, "w", encoding="utf-8") as f:
    json.dump(personas_json, f, indent=4)

print(f"Step 4.2 complete: personas saved to {PERSONAS_FILE}")