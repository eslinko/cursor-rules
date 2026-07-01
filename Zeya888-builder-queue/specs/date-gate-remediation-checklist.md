# Date gate — remediation checklist (legacy pkg)

SSOT политики: [`guides/builder-artifact-dates.md`](../guides/builder-artifact-dates.md)

## Когда применять

Pkg в [`date-gate-grandfather.txt`](./date-gate-grandfather.txt) с `--verify --check-dates` → WARN. Remediation закрывает WARN и удаляет строку из allowlist.

## Шаги (на pkg)

1. Live re-verify: pytest + `--verify` в **одной** сессии; `--print-utc-now` для даты.
2. Обновить `story-acceptance-gate-*.md`:
   - `Date:` = дата live verification
   - секция `Remediation:` — что было неверно, что исправлено (образец: GW-L10N-02 gate)
3. Синхронизировать `bullrun-launch-index.md` (gate PASS / P3 execute dates).
4. **Не** переименовывать immutable `pkg-*.yaml` filename.
5. `--verify --check-dates --strict-dates` → ok (или только unrelated legacy WARN).
6. Удалить строку pkg из `date-gate-grandfather.txt`.

## Открытые legacy (gateway)

| pkg | Story | Действие |
|-----|-------|----------|
| 000031 | GW-RC-02 | Gate T06 Date; bullrun T06 vs T07 audit dates |
| 000032 | GW-RC-03 | Gate T05 Date 2026-05-29 → post RC-01/RC-02 |
