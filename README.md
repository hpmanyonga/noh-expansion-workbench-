# NOH Expansion Workbench

> Code, models, templates, and documentation to support Network One Health growth and site expansion.
> Work here focuses on repeatable operating assets, clean data handling, and audit-ready outputs.

---

## Table of Contents

1. [Non-Negotiables](#non-negotiables)
2. [How to Start a Session](#how-to-start-a-session)
3. [Folder Map](#folder-map)
4. [Naming Rules](#naming-rules)
5. [Working Agreements](#working-agreements)
6. [Next Tasks](#next-tasks)

---

## Non-Negotiables

> **These rules apply to every file, every session, without exception.**

- No patient identifiers.
- No secrets — no API keys, tokens, passwords, or credentials.
- Use synthetic or aggregated data only.

---

## How to Start a Session

1. Open Terminal.
2. Navigate to this project folder:
   ```bash
   cd ~/Desktop/my-project
   ```
3. Start Claude Code:
   ```bash
   claude
   ```
4. First prompt to Claude:
   ```
   Read CLAUDE.md and REPO_RULES.md, summarize repo state in 7 bullets, propose next 3 tasks.
   ```

---

## Folder Map

| Folder         | Contents                                                                 |
|----------------|--------------------------------------------------------------------------|
| `src/`         | Source code only                                                         |
| `tests/`       | Tests only                                                               |
| `inputs/`      | De-identified raw inputs only                                            |
| `outputs/`     | Generated artifacts only — use date prefix in filenames                  |
| `docs/`        | Specs and notes                                                          |
| `templates/`   | Reusable templates for documents, emails, and reports                    |
| `models/`      | Assumptions, calculators, and scenario definitions                       |
| `finance/`     | Unit economics, pricing logic, and payment flows                         |
| `dashboards/`  | Power BI notes, measures, and data dictionary                            |
| `etl/`         | Data cleaning and transformation scripts                                 |
| `schemas/`     | Column definitions and validation rules                                  |
| `governance/`  | SOPs, controls, and audit checklists                                     |
| `legal/`       | Templates only — no signed documents                                     |
| `sales/`       | Pitch scripts, objection handling, and meeting notes                     |
| `ops/`         | Site launch checklists, staffing models, and training plans              |
| `risk/`        | Risk register, controls mapping, and quality metrics definitions         |
| `sites/`       | One folder per site with local configs, launch plan, and KPIs            |
| `archive/`     | Old versions — read only                                                 |

---

## Naming Rules

- Use `lowercase_with_underscores` for all filenames.
- Use date prefix when relevant: `YYYY-MM-DD_name.ext`
- One concept per file.

---

## Working Agreements

Claude must:

- Ask before installing any dependency.
- Ask before creating new top-level folders.
- Never run `sudo`.
- Never delete files unless explicitly instructed.
- Show files changed and commands run after every task.

---

## Next Tasks

- [ ] Create `BRAND_RULES.md`.
- [ ] Add a `RULES.md` inside `inputs/`, `outputs/`, `models/`, `finance/`, `legal/`, and `governance/`.
- [ ] Add first real project under `src/` with tests and a small synthetic dataset.
