"""generates tests from specs"""
import json
import os

spec_file = "../spec/spec_auto.md"
tests_file = "../tests/tests_auto.json"

requirements = []

with open(spec_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

current_req = {}
field_map = {
    "Requirement ID": "req_id",
    "Description": "desc",
    "Source Persona": "persona",
    "Traceability": "trace",
    "Acceptance Criteria": "ac"
}

for line in lines:
    line = line.strip()
    if line.startswith("# Requirement ID:"):
        if current_req:
            requirements.append(current_req)
        current_req = {"req_id": line.split(":", 1)[1].strip()}
    elif any(line.startswith(f"- {key}:") for key in field_map if key != "Requirement ID"):
        key = next(k for k in field_map if line.startswith(f"- {k}:"))
        value = line.split(":", 1)[1].strip()
        # remove brackets if present
        if value.startswith("[") and value.endswith("]"):
            value = value[1:-1].strip()
        current_req[field_map[key]] = value

# append last requirement
if current_req:
    requirements.append(current_req)

if not requirements:
    print("No requirements found in spec_auto.md. Check the formatting.")
else:
    print(f"Found {len(requirements)} requirements.")
    # Example: generate a dummy test scenario for each requirement
    tests = []
    for i, r in enumerate(requirements, 1):
        tests.append({
            "test_id": f"TEST_{i}",
            "requirement_id": r["req_id"],
            "scenario": f"Validate {r['desc']}",
            "steps": [
                f"Perform the action described in requirement {r['req_id']}"
            ],
            "expected_result": f"Requirement {r['req_id']} is satisfied"
        })

    # save tests
    os.makedirs(os.path.dirname(tests_file), exist_ok=True)
    with open(tests_file, "w", encoding="utf-8") as f:
        json.dump(tests, f, indent=4)

    print(f"Tests saved in {tests_file}")