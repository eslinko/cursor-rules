# Operator root — wave plan + handoff packets

**Категория:** operator (root orchestrator)  
**Guide:** [`../../guides/operator-root-orchestrator.md`](../../guides/operator-root-orchestrator.md)  
**START first:** [`operator-root-start.md`](./operator-root-start.md) — presuppose `{tasksRoot}/run-reports/operator-sessions/OP-<project>.session.yaml` (`status: ready`); if missing → run START, then return.  
**SSOT phases:** [`../../core/workflow.md`](../../core/workflow.md) — не дублировать fences; только заполнять переменные  
**Метод:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)

## Юзкейсы (когда этот промпт)

| # | Ситуация | Действие |
|---|----------|----------|
| 1 | В `OP-<project>` уже есть ready session; BLD/VAL чаты открыты/именованы; нужна **очередь stories + handoff** | WAVE: wave MD + один packet за раз → paste |
| 2 | Повторная волна в том же OP-диалоге (те же BLD/VAL titles) | WAVE снова; **не** обязателен новый START, если session ready |
| 3 | Operator сам ведёт BLD/VAL (paste MVP), без overnight Task | WAVE (не subagent-run) |

**Вход:** `builder_project` + `stories: [@…]` + `mode: sequential|batched-by-pkg`.

**Да, реюз существующих worker’ов:** WAVE рассчитан на уже привязанные чаты из session. Идентификация — см. ниже.

**Не этот промпт:**

| Ситуация | Куда |
|----------|------|
| Нет session / холодный OP | сначала [`operator-root-start.md`](./operator-root-start.md) |
| «Задал очередь и ушёл» двумя Task, без paste | [`operator-root-subagent-run.md`](./operator-root-subagent-run.md) |

### Как достоверно идентифицировать BLD/VAL (MVP wave)

| Механизм | Где | Как работает |
|----------|-----|----------------|
| **`*_chat_title`** (канон) | `OP-<project>.session.yaml` | Packet поле `DELIVER_TO: BLD-<project>` / `VAL-<project>` / `shell`. Оператор (или OP) paste в чат с **этим title**. |
| Cursor internal chat UUID | — | **Не** SSOT. START явно: не invent chat IDs. |
| **`*_agent_id`** (Task uuid) | session.yaml (Phase B) | Для WAVE **не** обязателен. Если ids уже есть — опционально Task resume вместо paste ([START](./operator-root-start.md) §5); основной путь WAVE = paste по titles. |

**Итого:** реюзить **можно** (и нужно) — по **именам чатов**, записанным в session при START (`bind_mode: reuse|create`). Имя при создании чата = то, что оператор задал/подтвердил (defaults `BLD-`/`VAL-`), не внутренний id Cursor.

**Запреты root:** code edits, pytest, invent AC, silent advance без path on disk, переписывать полный текст P1–P8 (ссылайся на workflow §).

---

## Copy-paste

```text
@.cursor/rules/analysis.mdc
@docs/methodology/Zeya888-builder-queue/guides/operator-root-orchestrator.md
@docs/methodology/Zeya888-builder-queue/core/workflow.md
builder_project:
stories:
  - @
mode: sequential

Operator root wave (OP chat only). Follow guide operator-root-orchestrator.md.

MODE: orchestrate only — no product code edits, no pytest, no pkg activate unless operator orders.
Claims: only after Read/Glob of paths; else Unknown.
Do NOT paste full P* fences into wave MD — reference workflow.md §P* and fill variables like workflow-console.

## Step 1 — Resolve context
- Require session file from START (path above); Read titles / bind_mode; if absent → STOP and point to operator-root-start.md.
- Read each @$story (AC, package, skill if any).
- Resolve tasksRoot / planFile / profile from specs/profiles.yaml for builder_project.
- List existing active pkg / bullrun «Актуальная точка» if relevant (facts only).

## Step 2 — Write wave plan (materialize plan file)
Create:
`{tasksRoot}/run-reports/operator-waves/wave-<YYYYMMDD>-<slug>.md`
Sections per guide §5 (queue, per-story checklist, artifacts, handoff log, stop-rules).
Story status start = QUEUED → after this file = PLANNED.

## Step 3 — Emit next handoff packet(s)
For the first story (mode=sequential) or batch plan (batched-by-pkg), emit ONE ready packet at a time unless operator asks for full packet list.

Packet schema (guide §6):
### HANDOFF PACKET
packet_id / ROLE / PHASE / builder_project / DELIVER_TO / @files / DONE_WHEN / DO_NOT / RETURN_TO_ROOT
DELIVER_TO = builder_chat_title | validator_chat_title | shell from session.yaml.

Default first packets per story (skip if already Done on disk):
1) ROLE=cli PHASE=P2 — exact shell command from profile verify/write-build-window (or N/A if run_mode-only)
2) ROLE=builder PHASE=P3 — @planFile @buildWindowFile @story; workflow §P3
3) ROLE=validator PHASE=P4 — @$auditReport target path; workflow §P4; analysis.mdc
4) If gaps: builder P5 → builder P6 → validator P7 (loop until wave complete or WAVE_STALLED_NO_DELTA)
5) ROLE=builder PHASE=P8 — git-commit plan; no push unless operator said

If story needs P1.3 materialize first — emit builder P1.3 before P2.

## Step 4 — STOP for operator
After wave MD + current packet:
Handoff: none automatic.
Reply ends with:
1) path to wave MD
2) the single next HANDOFF PACKET (copy-ready)
3) clarifying questions if Unknown blocks routing

Wait for operator: «packet done» + paths, or paste RETURN_TO_ROOT summary.
Then verify paths on disk, update wave MD handoff log + story status, emit next packet.

Do not suggest opening unrelated projects. Do not run Builder/Validator work in this OP chat.
```

---

## Примечания

- Naming: `OP-<project>`, `BLD-<project>`, `VAL-<project>` — guide §3.
- Console mapping — guide §6 table.
- Dashboard recount after wave closes stories — [`../../workflow/backlog-dashboard-maintenance.md`](../../workflow/backlog-dashboard-maintenance.md).
