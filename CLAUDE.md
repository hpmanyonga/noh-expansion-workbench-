# CLAUDE OPERATING INSTRUCTIONS

> These instructions govern all Claude activity in this repository.
> Read `REPO_RULES.md` and `BRAND_RULES.md` before starting any task.

---

## Table of Contents

1. [Read First](#read-first)
2. [Scope](#scope)
3. [Non-Negotiables](#non-negotiables)
4. [Metrics Discipline](#metrics-discipline)
5. [Data Classification](#data-classification)
6. [Default Workflow](#default-workflow)
7. [Folder Discipline](#folder-discipline)
8. [Dependencies](#dependencies)
9. [Running Commands](#running-commands)
10. [Approvals Required](#approvals-required)
11. [Outputs](#outputs)

---

## Read First

Before touching any file:

- [ ] Read `REPO_RULES.md`
- [ ] Read `BRAND_RULES.md`
- [ ] Read `README.md` if present

---

## Scope

This repo supports **NOH growth and expansion**.

Outputs include code, models, templates, and documents. All work must be traceable, reproducible, and compliant with the rules below.

---

## Non-Negotiables

> **Stop immediately if any of these are violated. Do not proceed.**

- No patient identifiers of any kind.
- No secrets — no API keys, tokens, passwords, or credentials.
- No signed contracts or sensitive partner documents.
- Use synthetic or aggregated data only.

---

## Metrics Discipline

Every KPI or metric must include all of the following:

| Field         | Description                              |
|---------------|------------------------------------------|
| Denominator   | What is the base population?             |
| Time window   | What period does this cover?             |
| Population    | Which patients, sites, or cohort?        |
| Site          | Which location(s)?                       |
| Data source   | Where did this number come from?         |

- No unlabeled percentages.
- No metrics without a denominator.

---

## Data Classification

**Allowed**
- Synthetic data.
- Aggregated extracts (no row-level identifiers).
- De-identified tables with no free-text clinical notes.

**Not Allowed**
- Names, phone numbers, ID numbers, or any PHI.
- EMR exports with identifiers.
- WhatsApp exports.
- Free-text clinical notes.

---

## Default Workflow

For every task, follow this sequence:

1. **Summarize** — describe current state in 5 bullets.
2. **Plan** — propose a 3-step plan before acting.
3. **Implement** — execute one step at a time.
4. **Verify** — run the smallest command that proves it works.
5. **Report** — list files changed and commands run.

---

## Folder Discipline

| Folder         | Contents                                                        |
|----------------|-----------------------------------------------------------------|
| `src/`         | Source code only                                                |
| `tests/`       | Tests only                                                      |
| `inputs/`      | De-identified raw inputs only                                   |
| `outputs/`     | Generated artifacts only                                        |
| `docs/`        | Specs, notes, and documentation                                 |
| `templates/`   | Client-facing content — must comply with `BRAND_RULES.md`      |
| `finance/`     | Financial models and projections                                |
| `models/`      | Analytical and statistical models                               |
| `etl/`         | ETL scripts and pipeline definitions                            |
| `dashboards/`  | Dashboard definitions and configs                               |
| `notebooks/`   | Jupyter or analysis notebooks                                   |
| `schemas/`     | Data schema definitions                                         |
| `governance/`  | Governance artifacts and policies                               |
| `legal/`       | Legal documents — requires explicit approval to write           |
| `config/`      | Configuration files                                             |
| `archive/`     | Deprecated or historical work                                   |

---

## Dependencies

- Ask before installing any new dependency.
- Prefer the standard library first.
- Document the reason for any new package added.

---

## Running Commands

- Ask before running any command that writes outside the repo.
- Never run `sudo`.
- Never delete files without explicit instruction.
- Never use `--force` or `--no-verify` flags without approval.

---

## Approvals Required

Pause and ask the user before any of the following:

- Installing packages or dependencies.
- Creating new top-level folders.
- Writing into `legal/`.
- Generating client-facing copy in `outputs/`.
- Running destructive commands (`rm`, `drop`, `truncate`, etc.).

---

## Outputs

- Use date prefix for all files in `outputs/`: `YYYY-MM-DD_name.ext`
- Add a one-line changelog at the top of every generated report.
- Never export row-level clinical data to `outputs/`.
