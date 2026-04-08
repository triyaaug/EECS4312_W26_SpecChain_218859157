# EECS4312_W26_SpecChain

## instructions:

How to run this project!

- App name: HeadSpace
- Data collection method: Google Play Scraper

Dataset:

- reviews_raw.jsonl contains the collected reviews.
- reviews_clean.jsonl contains the cleaned dataset.
- Final cleaned dataset: 2335 reviews

Repository Structure:

- data/ contains datasets and review groups
- personas/ contains persona files
- spec/ contains specifications
- tests/ contains validation tests
- metrics/ contains all metric files
- src/ contains executable Python scripts

Exact commands to run pipeline

1. python src/00_validate_repo.py
2. python src/02_clean.py
3. python src/run_all.py
4. Open metrics/metrics_summary.json for comparison results
