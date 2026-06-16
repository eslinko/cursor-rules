---
name: Taxonomy Cycle Builder
overview: "Standalone meta-script для регулярного цикла обновления таксономии меток (gateway + spa-app): TC0–TC7, dry-run gate на бэкфилл, статусы в bullrun/run-reports. SSOT процесса: taxonomy-update-process-ru.md."
todos:
  - id: sync-bullrun-taxonomy
    content: После TC7 обновить секцию Taxonomy Cycles в bullrun-launch-index и run-summary
    status: completed
  - id: never-touch-readiness-tables
    content: Не править REQUIRED_READINESS_TABLES; TC7 включает test_supabase_required_tables.py
    status: completed
  - id: dry-run-backfill-gate
    content: reproject_issue_i18n.py write только после явного go оператора (TC6b)
    status: completed
isProject: false
---

# Taxonomy Cycle Builder

> **Teaching snapshot** — для P3 attach только [`.cursor/plans/Taxonomy_builder.plan.md`](../../../../.cursor/plans/Taxonomy_builder.plan.md). См. [README](./README.md).

Проект: **full monorepo** — `doge-complaints-gateway` (маппинг/бэкфилл) + `spa-app` (переводы).  
Операционный SSOT: [`taxonomy-update-process-ru.md`](/Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/docs/runtime-docs/appendix/taxonomy-update-process-ru.md)  
Схема решений: [`taxonomy-decisions-schema.md`](/Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/docs/runtime-docs/appendix/taxonomy-decisions-schema.md)

## Назначение

Канонический **ручной** meta-script для цикла обновления таксономии меток по телеметрии GW-L10N-03. **Не** pkg-очередь Builder Queue — отдельный plan без `pkg-*.yaml`.

**Триггер:** только явный запуск оператором (нет cron / auto-threshold).

## Поведение при Build / Execute plan (Cursor)

**Default:** весь plan **top-to-bottom** TC0→TC7 в одной сессии.

**`run_mode`:** `run_mode=taxonomy_cycle_<YYYYMMDD>` — тот же порядок фаз; numbered README list **не используется**.

### Шаг 0 — сразу после Build (корень `DOGEstonia/`)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project taxonomy --verify
```

Ожидаемо: `ok taxonomy verify (N paths)`. При `FAIL` — стоп.

### Шаблон первого сообщения в чат

```text
@.cursor/plans/Taxonomy_builder.plan.md
@doge-complaints-gateway/docs/runtime-docs/appendix/taxonomy-update-process-ru.md
Taxonomy cycle TC0–TC7. cycle_id=YYYYMMDD. Claims из кода.
```

---

## Hard rules (из §6.4 taxonomy-update-process-ru)

1. **Запрет** правки [`REQUIRED_READINESS_TABLES`](/Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/src/core/infrastructure/db_supabase.py) — guard [`test_supabase_required_tables.py`](/Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/tests/test_supabase_required_tables.py) в TC7.
2. **Не трогать** форму projection DTO / envelope контракт.
3. **Новая board-метка (а):** только при `new_board_label: true` + явное имя в manifest; иначе **STOP**.
4. **Бэкфилл:** `reproject_issue_i18n.py --dry-run` → лог → **STOP** → write только после явного «go» оператора.
5. **Не коммитить** `docs/tasks/run-reports/taxonomy-cycles/cycle-*` без явной команды оператора.

---

## Фазы meta-script

| Phase | Имя | Авто/человек | Действие |
|-------|-----|--------------|----------|
| **TC0** | Verify | auto | Scripts + plan exist; telemetry route `POST /telemetry/label-misses` в [`asgi_app.py`](/Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/src/core/api/asgi_app.py); optional `.env` для fetch |
| **TC1** | Fetch misses | auto | `python3 scripts/taxonomy_fetch_misses.py --out docs/tasks/run-reports/taxonomy-cycles/cycle-<DATE>/misses-ranked.json` |
| **TC2** | Classify draft | auto | `python3 scripts/taxonomy_classify_candidates.py --in …/misses-ranked.json --out …/taxonomy-decisions.yaml --cycle-id <DATE>` |
| **TC3** | Decision interview | human | AskQuestion по `action: pending`; `(а)` new board только при `new_board_label: true` |
| **TC4** | Apply gateway | auto* | `python3 scripts/taxonomy_apply_gateway.py --manifest …/taxonomy-decisions.yaml` |
| **TC5** | Apply spa i18n | auto* | `python3 scripts/taxonomy_apply_spa_i18n.py --manifest …/taxonomy-decisions.yaml` |
| **TC6a** | Backfill dry-run | auto | `python3 scripts/reproject_issue_i18n.py --dry-run` → `reproject-dry-run.log` |
| **TC6b** | Backfill write | human gate | write без `--dry-run` **только** после «go» |
| **TC7** | Gates + status | auto + spot-check | pytest + npm test; sync bullrun; `run-summary-taxonomy-cycle-<DATE>.md` |

\* TC4/TC5 — после финализации manifest (TC3).

### TC0 — Verify checklist

```bash
cd /Users/eslinko/Development/DOGEstonia
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project taxonomy --verify
test -f doge-complaints-gateway/scripts/taxonomy_fetch_misses.py
test -f doge-complaints-gateway/scripts/taxonomy_classify_candidates.py
test -f doge-complaints-gateway/scripts/taxonomy_apply_gateway.py
test -f doge-complaints-gateway/scripts/taxonomy_apply_spa_i18n.py
rg -n "telemetry/label-misses" doge-complaints-gateway/src/core/api/asgi_app.py
```

### TC1 — Fetch (из `doge-complaints-gateway/`)

```bash
CYCLE=YYYYMMDD
python3 scripts/taxonomy_fetch_misses.py \
  --out docs/tasks/run-reports/taxonomy-cycles/cycle-${CYCLE}/misses-ranked.json
```

### TC2 — Classify

```bash
python3 scripts/taxonomy_classify_candidates.py \
  --in docs/tasks/run-reports/taxonomy-cycles/cycle-${CYCLE}/misses-ranked.json \
  --out docs/tasks/run-reports/taxonomy-cycles/cycle-${CYCLE}/taxonomy-decisions.yaml \
  --cycle-id ${CYCLE}
```

**Heuristic (verified):**
- `miss_count < 3` **или** ключ не `^[a-z][a-z0-9_]{1,48}$` → `ignore`
- ключ уже в `_CANONICAL_TO_SPA_LABEL` **или** в `DOGEIssueLabel` → `translate_only` (spa only)
- иначе → `pending` (интервью)

### TC3 — Interview

- Для каждого `pending`: AskQuestion — `map` / `translate_only` / `ignore` / `new_board_label`
- `new_board_label`: обязательны `new_board_label: true`, `target_label`, переводы или TODO copy
- Обновить `taxonomy-decisions.yaml` (final)

### TC4 — Apply gateway

```bash
python3 scripts/taxonomy_apply_gateway.py \
  --manifest docs/tasks/run-reports/taxonomy-cycles/cycle-${CYCLE}/taxonomy-decisions.yaml
```

### TC5 — Apply spa i18n

```bash
python3 scripts/taxonomy_apply_spa_i18n.py \
  --manifest docs/tasks/run-reports/taxonomy-cycles/cycle-${CYCLE}/taxonomy-decisions.yaml
```

### TC6 — Backfill

```bash
python3 scripts/reproject_issue_i18n.py --dry-run \
  | tee docs/tasks/run-reports/taxonomy-cycles/cycle-${CYCLE}/reproject-dry-run.log
# STOP — operator review
python3 scripts/reproject_issue_i18n.py   # only after explicit go
```

### TC7 — Gates

```bash
cd doge-complaints-gateway && python3 -m pytest -q --ignore=tests/smoke --ignore=tests/integration
cd doge-complaints-gateway && python3 -m pytest -q tests/integration/supabase/test_supabase_dotenv_connectivity.py
cd doge-complaints-gateway && python3 -m pytest -q tests/test_supabase_required_tables.py tests/test_taxonomy_classify_candidates.py
cd spa-app && npm test
```

**Manual spot-check:** `GET /tallinn/issues?labels=<label>` после map/new label.

**Status sync:** обновить секцию **Taxonomy Cycles** в [`bullrun-launch-index.md`](/Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/docs/tasks/bullrun-launch-index.md); создать `run-summary-taxonomy-cycle-<DATE>.md`.

---

## Артефакты цикла

Каталог: `doge-complaints-gateway/docs/tasks/run-reports/taxonomy-cycles/cycle-<YYYYMMDD>/`

| Файл | Фаза |
|------|------|
| `misses-ranked.json` | TC1 |
| `taxonomy-decisions.yaml` | TC2 draft → TC3 final |
| `reproject-dry-run.log` | TC6a |
| `run-summary-taxonomy-cycle-<DATE>.md` | TC7 |

Layout SSOT: [`taxonomy-cycles/README.md`](/Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/docs/tasks/run-reports/taxonomy-cycles/README.md)

---

## Out of scope

- Auto-trigger по порогу / cron
- Rate-limit telemetry (§13 taxonomy-update-process-ru)
- GW-L10N-04 public registry endpoint
- Auto write backfill без human gate (TC6b)
- Новый `DOGEIssueLabel` без `new_board_label: true` в manifest
