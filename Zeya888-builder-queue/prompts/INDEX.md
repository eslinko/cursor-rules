# Useful prompts — index

Каталог **копируемых** промптов вне happy-path PA/P*. Curriculum и contracts **не** дублируют текст промптов — только ссылки сюда или в `core/workflow.md`.

## Taxonomy

| Категория | Когда | Где |
|-----------|-------|-----|
| **architect/** | До PA / cross-project analytics / system map | [`architect/`](./architect/) |
| **operator/** | Root OP bootstrap / wave / subagent overnight | [`operator/`](./operator/) |
| **operator-wave** | P0–P8 + PA.1–PA.3 happy path fences | SSOT: [`../core/workflow.md`](../core/workflow.md) (не мигрировать сюда без явного решения) |
| **housekeeping** | Dashboard focus, git commit plan | см. таблицу ниже |

## architect/

| Prompt | Назначение |
|--------|------------|
| [`architect/cross-project-system-orientation.md`](./architect/cross-project-system-orientation.md) | Read-only STOP: карта 4 проектов + docs analytics + candidates in chat; без PA/P1 handoff |
| [`architect/parent-requirement-to-project-reqs.md`](./architect/parent-requirement-to-project-reqs.md) | Parent → child REQs + link matrix; materialize + mvp-dashboard sync → PA.2 |
| [`architect/req-to-backlog-stories.md`](./architect/req-to-backlog-stories.md) | Non-UI REQ → STORY package (reuse\|new); INDEX + mvp-dashboard sync → P1.3 |
| [`architect/req-to-ui-admin-layers.md`](./architect/req-to-ui-admin-layers.md) | UI REQ → ADMIN-01…06 (always NEW pkg); INDEX + mvp-dashboard sync; STORY via ADMIN-05 |

## operator/

| Prompt | Назначение |
|--------|------------|
| [`operator/operator-root-start.md`](./operator/operator-root-start.md) | OP chat: только `$builderProject=` → role + session bind (reuse\|create\|task) |
| [`operator/operator-root-wave.md`](./operator/operator-root-wave.md) | OP chat: story links → wave MD + handoff packets для BLD/VAL/CLI (MVP paste) |
| [`operator/operator-root-subagent-run.md`](./operator/operator-root-subagent-run.md) | OP chat: `$builderProject` + `$queueSpec` → два субагента overnight (Phase B) |

## operator-wave

Короткие fences: [`../core/workflow.md`](../core/workflow.md). Полные: [`../core/workflow-legacy.md`](../core/workflow-legacy.md). UI copy: [`../tools/workflow-console.html`](../tools/workflow-console.html).

## housekeeping/

| Prompt | Назначение |
|--------|------------|
| [`../workflow/build-scope-dashboard-prompt.md`](../workflow/build-scope-dashboard-prompt.md) | Focus-диалог Layer-2 backlog dashboard (`/build-scope-dashboard`) |
| [`../../git-commit-prompt.md`](../../git-commit-prompt.md) | План коммитов на согласование (корневая methodology) |

## SSOT rules

1. Новые useful prompts **вне** PA/P* → `prompts/<category>/` + строка в этой INDEX.
2. Изменение PA/P* → править `core/workflow.md` (+ console, если fence).
3. Не копировать полный текст промпта в curriculum / operator contracts — thin pointer only.
