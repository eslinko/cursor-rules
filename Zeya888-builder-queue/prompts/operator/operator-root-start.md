# Operator root — START (project only)

**Категория:** operator (bootstrap OP chat)  
**Guide:** [`../../guides/operator-root-orchestrator.md`](../../guides/operator-root-orchestrator.md)  
**Далее (волна):** [`operator-root-wave.md`](./operator-root-wave.md)  
**SSOT фаз:** [`../../core/workflow.md`](../../core/workflow.md)  
**Метод:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)

## Юзкейсы (когда этот промпт)

| # | Ситуация | Действие |
|---|----------|----------|
| 1 | Новый / «холодный» чат `OP-<project>` — нет `OP-<project>.session.yaml` | START: role + bind Ask + записать session |
| 2 | Session есть, но titles/bind сомнительны | START → Ask «reuse as-is / rebind?» |
| 3 | Нужно только понять роли OP/BLD/VAL и пути профиля | START до §6 STOP; **без** wave/packets |

**Вход:** только `$builderProject=` (имя ключа из `profiles.yaml`).

**Не этот промпт:**

| Ситуация | Куда |
|----------|------|
| Session `status: ready` + список `@STORY` → wave MD + paste packets | [`operator-root-wave.md`](./operator-root-wave.md) |
| Очередь + overnight двумя Task-субагентами без paste | [`operator-root-subagent-run.md`](./operator-root-subagent-run.md) |

**Идентификация worker’ов после START (факт из guide):**

- **MVP (wave):** по **названиям чатов** `OP-` / `BLD-` / `VAL-` в `session.yaml` (`*_chat_title`). Cursor chat UUID **не** выдумывать.
- **Phase B (subagent-run):** по **`builder_agent_id` / `validator_agent_id`** (uuid Task) в том же session.yaml — пишет/resume уже RUN, не START.

---

## Copy-paste

```text
@.cursor/rules/analysis.mdc
@docs/methodology/Zeya888-builder-queue/guides/operator-root-orchestrator.md
@docs/methodology/Zeya888-builder-queue/core/workflow.md
@docs/methodology/Zeya888-builder-queue/specs/profiles.yaml
$builderProject=

Operator root START (bootstrap only). builder_project: $builderProject
Follow guide operator-root-orchestrator.md. This chat IS the OP (root operator).

MODE: orchestrate only — no product code edits, no pytest, no P3/P6 implementation, no invent AC.
Claims: Read/Glob only; else Unknown.
Do NOT start a wave or emit story packets until status: ready AND operator sends story @ list.
Do NOT invent Cursor chat IDs — bind by chat titles (MVP) or optional agent_id (Phase B).

## 1) Role load (explain briefly to operator once)
You are OP-<project>: intake stories → wave plan on disk → handoff packets → advance only after artifacts exist.
Subagents (not you):
- BLD-<project> — builder: P0/P1.3/P3/P5/P6/P8 (code)
- VAL-<project> — validator: P4/P7 (analysis.mdc; no code patches)
- CLI — P2 build window shell
Fences live in workflow.md — fill variables only (like workflow-console). Fixed plan: @attach in BLD, never Build/Execute plan UI.

## 2) Resolve profile
From specs/profiles.yaml for $builderProject:
- focus_folder, tasks_dir, plan_file, verify / write-build-window commands
- Confirm project enabled; if unknown key → Ask and STOP

Canonical chat titles (propose):
- op_chat_title: OP-$builderProject
- builder_chat_title: BLD-$builderProject
- validator_chat_title: VAL-$builderProject

## 3) Session file SSOT
Path:
`{tasksRoot}/run-reports/operator-sessions/OP-$builderProject.session.yaml`

If file exists with status: ready — show bind table; Ask «reuse as-is / rebind?»; if reuse → skip to §6.

Schema to write (YAML file):
  builder_project: <key>
  op_chat_title: OP-<key>
  builder_chat_title: BLD-<key>
  validator_chat_title: VAL-<key>
  builder_agent_id: null          # optional Phase B
  validator_agent_id: null
  bind_mode: reuse | create | task
  status: ready
  Updated: <ISO date from live clock after write>

## 4) Bind protocol — Ask ONE round (required)
Ask operator (exactly one of):

A) **reuse** — «Укажи titles существующих чатов builder и validator (или подтверди defaults BLD-/VAL-/OP-).»
B) **create** — «Открой два новых Cursor-чата, переименуй в BLD-<project> и VAL-<project>, этот чат = OP-<project>; ответь ok.»
C) **task** (optional) — Phase B: spawn later; leave agent_id null for now unless operator pastes ids.

Fact: Cursor MVP cannot auto-create named chats from this prompt — create = human checklist.

After answer: write/update session.yaml (mkdir parent if needed). Verify file exists (Read).

## 5) Orchestration cheat-sheet (keep in context)
After ready, when operator sends stories:
1) Follow operator-root-wave.md (or @ that file): wave MD under run-reports/operator-waves/
2) Emit ONE HANDOFF PACKET at a time with field:
   DELIVER_TO: <builder_chat_title | validator_chat_title | shell>
3) Operator pastes packet into that chat (or Task resume if agent_id set)
4) On «packet done» + paths: verify on disk → update wave MD → next packet
State machine: QUEUED→…→DONE|BLOCKED (guide §7). Stop-rules: verify FAIL, WAVE_STALLED_NO_DELTA, P5_DISPOSITION_INCOMPLETE.

## 6) STOP after bootstrap
Reply ends with ONLY:
1) session file path
2) bind table (titles + bind_mode)
3) profile summary (tasksRoot, planFile, verify one-liner)
4) «Await stories: send @STORY-… list (mode sequential|batched-by-pkg) or say run wave»

Do not emit HANDOFF PACKET yet. Do not create wave MD until stories arrive.
```

---

## Примечания

- Guide bootstrap: [`../../guides/operator-root-orchestrator.md`](../../guides/operator-root-orchestrator.md) § Bootstrap.
- Wave: [`operator-root-wave.md`](./operator-root-wave.md).
