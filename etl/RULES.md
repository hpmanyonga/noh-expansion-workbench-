# RULES — etl/

> Scripts that transform inputs to outputs, plus logs. Reproducible, documented, and safe.

---

## What belongs here

- Data cleaning and transformation scripts.
- Pipeline definitions and orchestration configs.
- Data validation and quality check scripts.
- De-identification scripts.
- Run logs produced by ETL scripts.

## What does not belong here

- Raw input data (go in `inputs/`).
- Final model or analysis code (go in `src/`).
- Schema definitions (go in `schemas/`).
- Hardcoded paths outside this repo.
- Secrets, API keys, tokens, or passwords.
- PHI or patient identifiers of any kind.

## Standards

- Every script must have a header comment stating:
  - Purpose
  - Input file(s) and expected format
  - Output file(s) and format
  - Author and date
- Scripts must never hardcode paths outside the repo — use relative paths or config variables.
- Never write PHI or patient identifiers into any output file.
- De-identification must happen before any data is written to `inputs/` or `outputs/`.
- Scripts must be idempotent where possible (safe to run more than once).
- Every script must write its output to `outputs/` using the date-prefix naming convention.
- Every script must produce a validation summary on completion, stating:
  - Input row count
  - Output row count
  - Any rows dropped and why
  - Pass/fail status

## Naming convention

- Use `lowercase_with_underscores`.
- Add date prefix when relevant: `YYYY-MM-DD_name.ext`
- Name scripts by what they do: `clean_intake_data.py`, `deduplicate_sites.py`.

## Before adding a script

- [ ] Header comment is complete (purpose, inputs, outputs, author, date).
- [ ] No hardcoded paths outside the repo.
- [ ] No secrets, keys, or tokens in the script or config.
- [ ] No PHI written to any output.
- [ ] Script writes output to `outputs/` with date prefix.
- [ ] Script produces a validation summary (row counts, drops, pass/fail).
- [ ] Script tested with synthetic data.
- [ ] Filename follows naming convention.
