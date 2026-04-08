"""computes metrics: coverage/traceability/ambiguity/testability"""
import json
import os

# File paths
review_groups_file = "../data/review_groups_auto.json"
personas_file = "../personas/personas_auto.json"
spec_file = "../spec/spec_auto.md"
tests_file = "../tests/tests_auto.json"
metrics_file = "../metrics/metrics_auto.json"

# Load review groups
with open(review_groups_file, "r", encoding="utf-8") as f:
    review_groups_data = json.load(f)
review_groups = review_groups_data.get("groups", [])
dataset_size = sum(len(g["review_ids"]) for g in review_groups)

# Load personas
with open(personas_file, "r", encoding="utf-8") as f:
    personas = json.load(f)
persona_count = len(personas)

# Load specifications
requirements = []
with open(spec_file, "r", encoding="utf-8") as f:
    lines = f.readlines()
current_req = {}
for line in lines:
    line = line.strip()
    if line.startswith("# Requirement ID:"):
        if current_req:
            requirements.append(current_req)
        current_req = {"req_id": line.split(":", 1)[1].strip()}
    elif line.startswith("- Description:"):
        current_req["desc"] = line.split(":", 1)[1].strip().strip("[]")
    elif line.startswith("- Source Persona:"):
        current_req["persona"] = line.split(":", 1)[1].strip().strip("[]")
    elif line.startswith("- Traceability:"):
        current_req["trace"] = line.split(":", 1)[1].strip().strip("[]")
    elif line.startswith("- Acceptance Criteria:"):
        current_req["ac"] = line.split(":", 1)[1].strip().strip("[]")
if current_req:
    requirements.append(current_req)
requirements_count = len(requirements)

# Load tests
with open(tests_file, "r", encoding="utf-8") as f:
    tests = json.load(f)
tests_count = len(tests)

# Compute traceability links
traceability_links = sum(1 for r in requirements if r.get("trace"))

# Compute review coverage: fraction of dataset reviews covered by requirements
reviews_in_trace = set(r.get("trace", "") for r in requirements if r.get("trace"))
review_coverage = len(reviews_in_trace) / dataset_size if dataset_size else 0

# Traceability ratio: fraction of requirements linked to a persona
traceability_ratio = sum(1 for r in requirements if r.get("persona")) / requirements_count if requirements_count else 0

# Testability rate: fraction of requirements with at least one test
req_ids_with_tests = set(t["requirement_id"] for t in tests)
testability_rate = sum(1 for r in requirements if r["req_id"] in req_ids_with_tests) / requirements_count if requirements_count else 0

# Ambiguity ratio: simple heuristic, e.g., fraction of requirements with very short description
ambiguity_ratio = sum(1 for r in requirements if len(r.get("desc","")) < 20) / requirements_count if requirements_count else 0

metrics = {
    "pipeline": "automated",
    "dataset_size": dataset_size,
    "persona_count": persona_count,
    "requirements_count": requirements_count,
    "tests_count": tests_count,
    "traceability_links": traceability_links,
    "review_coverage": round(review_coverage, 2),
    "traceability_ratio": round(traceability_ratio, 2),
    "testability_rate": round(testability_rate, 2),
    "ambiguity_ratio": round(ambiguity_ratio, 2)
}

# Save metrics
os.makedirs(os.path.dirname(metrics_file), exist_ok=True)
with open(metrics_file, "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=4)

print(f"Metrics saved in {metrics_file}")