"""generates structured specs from personas"""
import json
from groq import Groq
import os

# Initialize Groq client
client = Groq(api_key="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")

# Paths
persona_file = "../personas/personas_auto.json"
output_md_file = "../spec/spec_auto.md"

# Load personas
with open(persona_file, "r", encoding="utf-8") as f:
    personas = json.load(f)

# Prepare prompt for the LLM
prompt = f"""
You are given the following personas derived from user reviews of a meditation app:

{json.dumps(personas, indent=2)}

Your task is to generate structured system requirements in Markdown. 
For each requirement, include:
- Requirement ID (unique, e.g., FR1, FR2, ...)
- Description of system behavior
- Persona that motivated the requirement
- Traceability to the review group
- Acceptance criteria

Format the output exactly as Markdown using this template:

# Requirement ID: <Requirement ID>
- Description: <system behavior>
- Source Persona: <persona name>
- Traceability: <review group ID>
- Acceptance Criteria: <acceptance criteria>
"""

# Call Groq API
response = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.2
)

# Extract response text
result_text = response.choices[0].message.content.strip()

# Save to Markdown file
os.makedirs(os.path.dirname(output_md_file), exist_ok=True)
with open(output_md_file, "w", encoding="utf-8") as f:
    f.write(result_text)

print(f"Specifications saved in {output_md_file}")