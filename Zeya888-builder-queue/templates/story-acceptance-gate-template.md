# Story acceptance gate — <STORY-KEY>

- **Story:** <title>
- **Package:** `pkg-NNNNNN-YYYYMMDD-<slug>.yaml`
- **Result:** PASS | FAIL
- **Date:** <utc_date from --print-utc-now after live verify>

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| … | PASS | … |

## Commands (live verification <utc_date>)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project <gateway|spa|identity|gpt> --verify
# project tests…
```

SSOT дат: [`guides/builder-artifact-dates.md`](../guides/builder-artifact-dates.md)
