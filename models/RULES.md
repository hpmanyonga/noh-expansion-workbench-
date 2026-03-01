# RULES — models/

> Analytical and statistical models. Assumptions explicit. One concept per file.

---

## What belongs here

- Assumptions files and parameter definitions.
- Calculators and scenario models.
- Statistical or ML model definitions.
- Sensitivity analyses and scenario comparisons.

## What does not belong here

- Financial models (go in `finance/`).
- Raw input data (go in `inputs/`).
- Generated outputs (go in `outputs/`).
- Code scripts (go in `src/`).

## Standards

- Every model must document its assumptions explicitly.
- Every metric must state: denominator, time window, population, site, and data source.
- No unlabeled percentages.
- Use synthetic or aggregated data only — no PHI.

## Naming convention

- Use `lowercase_with_underscores`.
- Add date prefix when relevant: `YYYY-MM-DD_name.ext`
- One concept per file.

## Before adding a model

- [ ] Assumptions are documented inside the file.
- [ ] Denominators and time windows are stated.
- [ ] No PHI or row-level clinical data included.
- [ ] Filename follows naming convention.
