# Builder Queue — дисциплина дат артефактов

> **CLI:** `builder_resolve_queue.py --print-utc-now` · `--verify --check-dates`  
> **Grandfather:** [`specs/date-gate-grandfather.txt`](../specs/date-gate-grandfather.txt)  
> **Шаблоны:** [`templates/story-acceptance-gate-template.md`](../templates/story-acceptance-gate-template.md) · [`templates/pkg-scaffold-snippet.yaml`](../templates/pkg-scaffold-snippet.yaml)

## Источник «сегодня»

**Единственный канон для агента:** stdout `--print-utc-now` или дата Run Reports Registry **той же** P1/P3-сессии после live-run.

**Запрещено:** даты из training cutoff, copy-paste из других pkg, «круглые» `T12:00:00Z` / `T14:00:00Z` без live-run, дата раньше gate зависимостей.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --print-utc-now
```

## Правила по типам артефактов

| Артефакт | Поле | Правило |
|----------|------|---------|
| `pkg-*.yaml` | `created_at` | UTC ISO; дата = scaffold-сессия; время из `--print-utc-now` |
| `pkg-*.yaml` | имя файла | `pkg-NNNNNN-YYYYMMDD-slug.yaml` — `YYYYMMDD` = date-part `created_at` |
| `story-acceptance-gate-*.md` | `Date:` | После live pytest + `--verify`; ≥ `pkg.created_at`; ≥ max dependency gate dates |
| `acceptance-verification-*.md` | `Date:` | То же |
| `run-summary-*.md` | имя + metadata | `run-summary-YYYYMMDD-HHMM` из `--print-utc-now` |
| `bullrun-launch-index.md` | gate PASS / P1 / P3 | Дата сессии; не раньше dependency rows |

## Иерархия дат (temporal contract)

```
gate Date(story S) >= date(created_at(pkg(S)))
gate Date(S) >= gate Date(each dependency of S)
date(created_at(pkg(S))) >= gate Date(each dependency of S)   # если deps уже Done
```

## CLI verify

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
python3 ... --verify --check-dates --strict-dates   # remediation: allowlist ignored
```

| Режим | Поведение |
|-------|-----------|
| Default `--check-dates` | FAIL для pkg с `created_at` ≥ `DATE_GATE_INTRODUCED`; WARN для pkg из grandfather allowlist |
| `--strict-dates` | FAIL для всех нарушений, allowlist игнорируется |
| Только WARN (allowlist) | exit 0 + сводка в stdout |
| Есть FAIL | exit 1 — стоп P2/P3 |

**`DATE_GATE_INTRODUCED`:** `2026-06-20` (методология 1.4.6). Новые pkg не могут быть в allowlist.

## Remediation legacy

По образцу GW-L10N-02: секция `Remediation:` + re-verify; **не** переименовывать immutable pkg filename. После remediation — удалить строку из `date-gate-grandfather.txt`.

См. [`specs/date-gate-remediation-checklist.md`](../specs/date-gate-remediation-checklist.md).
