# RULES — outputs/

> Generated artifacts only. Date-prefixed. Never contains row-level clinical data.

---

## What belongs here

- Reports, summaries, and analysis outputs.
- Exported charts, tables, and dashboards.
- Generated templates filled with synthetic or aggregated data.
- Model results and scenario outputs.

## What does not belong here

- Row-level clinical data of any kind.
- Files containing PHI.
- Intermediate working files (keep those in `src/` or `inputs/`).
- Signed legal documents.

## Naming convention

All files in this folder must use a date prefix:

```
YYYY-MM-DD_name.ext
```

Examples:
- `2026-03-01_site_launch_summary.pdf`
- `2026-03-01_unit_economics_v2.xlsx`

## Before saving a file

- [ ] Confirm no row-level clinical data is included.
- [ ] Confirm filename uses date prefix.
- [ ] Add a one-line changelog at the top of generated reports.
- [ ] Get user approval before saving client-facing copy here.

## Hard ban

> **No row-level clinical data. No PHI. No exceptions.**
