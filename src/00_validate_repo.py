"""checks required files/folders exist"""

"""
00_validate_repo.py

Checks if required files exist and prints messages in the required format.
"""

import os

REQUIRED_FILES = [
    "data/reviews_clean.jsonl",
    "personas/personas_manual.json",
    "spec/spec_auto.md",
    "tests/tests_hybrid.json"
]

print("Checking repository structure...")

for file in REQUIRED_FILES:
    if os.path.exists(file):
        print(f"{file} found")

print("Repository validation complete")