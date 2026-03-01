# REPO RULES

> NOH growth and expansion workbench — code, models, templates, and documentation.

---

## Table of Contents

1. [Hard Bans](#hard-bans)
2. [Data Handling](#data-handling)
3. [Folder Discipline](#folder-discipline)
4. [Naming Conventions](#naming-conventions)
5. [Quality Gate](#quality-gate)
6. [Claude Behavior](#claude-behavior)

---

## Hard Bans

> **These rules are non-negotiable. No exceptions.**

- No patient identifiers (names, MRNs, DOBs, or any PHI).
- No secrets — no API keys, passwords, or tokens.
- No signed contracts or sensitive partner documents.

---

## Data Handling

- Use synthetic or aggregated data only.
- If you import extracts, de-identify first and store in `inputs/`.
- Never export row-level clinical data to `outputs/`.

---

## Folder Discipline

| What                  | Where              |
|-----------------------|--------------------|
| Source code           | `src/`             |
| Tests                 | `tests/`           |
| Raw inputs            | `inputs/`          |
| Generated artifacts   | `outputs/`         |
| Specs and docs        | `docs/`            |
| Financial models      | `finance/` or `models/` |
| ETL scripts           | `etl/`             |
| Dashboards            | `dashboards/`      |
| Notebooks             | `notebooks/`       |
| Config files          | `config/`          |
| Schema definitions    | `schemas/`         |
| Governance artifacts  | `governance/`      |
| Templates             | `templates/`       |
| Archived work         | `archive/`         |

---

## Naming Conventions

- Use `lowercase_with_underscores` for all filenames.
- Prefix with date when relevant: `YYYY-MM-DD_name.ext`
- One concept per file — keep files focused and small.

---

## Quality Gate

- After any code change, run the smallest command that proves it works.
- Keep changes small and reversible.
- Update `README.md` when behavior changes.
- Do not merge broken or untested code.

---

## Claude Behavior

- Read `CLAUDE.md` and `REPO_RULES.md` before making any changes.
- Ask before installing dependencies.
- Ask before creating new top-level folders.
- Show files changed and commands run after every task.
- Never commit secrets, PHI, or large binary files.
