"""runs the full pipeline end-to-end"""

"""

Runs the full automated pipeline:
1. Load and clean dataset (not in automation, not in this file)
2. Generate review groups (4.1)
3. Generate personas (4.2)
4. Generate specifications (4.3)
5. Generate test cases (4.4)
6. Compute metrics (4.5)

"""

import os

def run_script(script_name):
    print(f"\nRunning {script_name}...")
    result = os.system(f"python {script_name}")
    
    if result != 0:
        print(f"Error while running {script_name}. Stopping pipeline.")
        exit(1)
    else:
        print(f"{script_name} completed successfully.")

if __name__ == "__main__":
    
    print("Starting full automated pipeline...\n") 

    # Step 4.1 + 4.2
    # Generates:
    # - data/review_groups_auto.json
    # - personas/personas_auto.json
    run_script("05_personas_auto.py")

    # Step 4.3
    # Generates:
    # - spec/spec_auto.md
    run_script("06_spec_generate.py")

    # Step 4.4
    # Generates:
    # - tests/tests_auto.json
    run_script("07_tests_generate.py")

    # Step 4.5
    # Generates:
    # - metrics/metrics_auto.json
    run_script("08_metrics.py")

    print("\nAll steps completed successfully")