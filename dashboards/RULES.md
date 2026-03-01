# RULES — dashboards/

> Power BI measures, data dictionary, and export schemas.

---

## What belongs here

- Power BI report definitions and layout notes.
- DAX measures and calculated column definitions.
- Data dictionary and field descriptions.
- Dashboard design specs and wireframes.
- Refresh schedules and connection documentation.

## What does not belong here

- Raw extracts or input data (go in `inputs/`).
- Row-level clinical data of any kind.
- Patient identifiers or PHI.
- ETL or transformation scripts (go in `etl/`).
- Generated report exports (go in `outputs/`).
- Schema definitions (go in `schemas/`).

## Standards

- Every measure must include: definition, denominator, time window, and data source.
- No unlabeled percentages or calculated fields without documentation.
- Use de-identified or synthetic data for any screenshots or examples.
- Document refresh cadence and data connection for every dashboard.

## Naming convention

- Format: `YYYY-MM-DD_<site>_<topic>.md` or `.csv`
- Examples:
  - `2026-03-01_nairobiwest_intake_measures.md`
  - `2026-03-01_all_sites_data_dictionary.csv`
- One dashboard or concept per file.

## Before adding a file

- [ ] Measures and fields are documented.
- [ ] No PHI or patient identifiers in screenshots or examples.
- [ ] Data source and refresh schedule noted.
- [ ] Filename follows naming convention.
