# BUG-SPA-20260709-001 — Filter chip label truncation on narrow viewport

| Field | Value |
|-------|-------|
| **ID** | `BUG-SPA-20260709-001` |
| **Severity** | P2 |
| **Status** | Inbox (sample — not implemented) |
| **Route** | `/#/board` |
| **Environment** | local |
| **Reporter** | operator (test fixture) |
| **Date** | 2026-07-09 |

### Description

On viewport width &lt; 400px, active filter chips in the filter panel truncate institution names without tooltip; user cannot read full institution label.

### Expected

Per [mockup-10-dashboard-filter-status-spec.md](../../../../spa-app/docs/UX/mockups/initiation/mockup-10-dashboard-filter-status-spec.md): chip shows readable label or ellipsis with `title` tooltip on hover/focus.

### Actual

Chip text cuts mid-word; no `title` attribute; keyboard focus shows no full label.

### Repro steps

1. `cd spa-app && npm run dev`
2. Open `http://localhost:5173/#/board`
3. Apply institution filter with long name (e.g. cross-locale institution string)
4. Resize viewport to 360px width
5. Observe chip in filter toolbar

### Screenshots

| # | File | Caption |
|---|------|---------|
| 1 | `attachments/BUG-SPA-20260709-001/screen-1.png` | *(placeholder — attach on real report)* |

### Code hints

- [`src/components/Filters/Filters.jsx`](../../../../spa-app/src/components/Filters/Filters.jsx)
- [`src/components/Filters/Filters.css`](../../../../spa-app/src/components/Filters/Filters.css)

### Triage outcome

| Field | Value |
|-------|-------|
| Story created | — (sample only) |
| Pkg / wave | Would map to EPIC-SPA-03 / SEARCH follow-up |
| Closed | — |
