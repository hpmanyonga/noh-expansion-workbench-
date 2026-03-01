# RULES — finance/

> Unit economics, pricing logic, and payment flows. Numbers must be traceable.

---

## What belongs here

- Unit economics models (cost per visit, revenue per site, etc.).
- Pricing logic and fee schedules.
- Payment flow definitions.
- Budget templates and forecasts.
- Break-even and scenario analyses.

## What does not belong here

- Analytical or statistical models (go in `models/`).
- Raw data (go in `inputs/`).
- Generated reports (go in `outputs/`).
- Signed financial agreements (go in `legal/`).

## Standards

- Every number must have a source, date, and assumptions noted.
- Every KPI must state: denominator, time window, population, and site.
- No unlabeled percentages.
- Use synthetic or aggregated data — no patient-level financials with identifiers.
- Version files when assumptions change significantly.

## Naming convention

- Use `lowercase_with_underscores`.
- Add date prefix when relevant: `YYYY-MM-DD_name.ext`
- One concept per file.

## Before adding a file

- [ ] All numbers have documented sources.
- [ ] Assumptions are stated explicitly.
- [ ] No PHI or patient-level identifiers included.
- [ ] Filename follows naming convention.
