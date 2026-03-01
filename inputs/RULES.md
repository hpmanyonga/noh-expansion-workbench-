# RULES — inputs/

> Raw input data only. De-identified before storage. Never export from here.

---

## What belongs here

- De-identified extracts from clinical or operational systems.
- Aggregated data files (no row-level identifiers).
- Synthetic datasets used for testing or modelling.
- Survey exports and intake summaries with no PHI.

## What does not belong here

- Files containing names, phone numbers, ID numbers, or any PHI.
- EMR exports with identifiers.
- WhatsApp exports.
- Free-text clinical notes.
- Signed contracts or partner documents.

## Before adding a file

- [ ] Confirm it contains no patient identifiers.
- [ ] Confirm it is de-identified or synthetic.
- [ ] Use `lowercase_with_underscores` for the filename.
- [ ] Add date prefix if relevant: `YYYY-MM-DD_name.ext`

## Hard ban

> **No PHI. No exceptions.**
