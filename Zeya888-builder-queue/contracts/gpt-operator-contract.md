# GPT Builder — operator contract

> **Plan (read-only unless operator asks):** [`.cursor/plans/GPT_builder.plan.md`](../../../.cursor/plans/GPT_builder.plan.md)  
> **Propagation:** [builder-session/SKILL.md](../../../.cursor/skills/builder-session/SKILL.md) · [builder-operator-habits.mdc](../../../.cursor/rules/builder-operator-habits.mdc) · [session-starter.md](../core/session-starter.md)  
> **Local SSOT:** [`GPT-BUILDER-PROCESS-SSOT.md`](../../../GPT UI/docs/analysis/tasks/GPT-BUILDER-PROCESS-SSOT.md)

Три process-reminder правила из frontmatter `GPT_builder.plan.md` — исполняются агентом на **каждой** сессии `builder_project: gpt`. P1 промпты — только [workflow.md](../core/workflow.md); не дублировать в plan.

---

## 1. `resolve-start-item-from-index` — старт из индекса + active pkg

**Перед** batch-run, Build window или P3/P6 Execute:

**Fixed plan:** `@attach` [`.cursor/plans/GPT_builder.plan.md`](../../../.cursor/plans/GPT_builder.plan.md) + workflow §P3/P6 в **этом** чате — **не** Build / Execute plan на файле ([fixed-builder-plan-execution.md](../guides/fixed-builder-plan-execution.md)).

1. Прочитать [`GPT UI/docs/analysis/tasks/bullrun-launch-index.md`](../../../GPT UI/docs/analysis/tasks/bullrun-launch-index.md) §«Актуальная точка» и таблицы волн (GIM-*).
2. Прочитать [`gpt-active-package.current.yaml`](../../../GPT UI/docs/analysis/tasks/gpt-active-package.current.yaml) → `package_file`.
3. Из корня workspace:  
   `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gpt --verify`  
   При `FAIL` — **стоп** (не выдумывать очередь).
4. Следующий таск / волну / override брать **только** из:
   - нормализованного `pkg-*.yaml` (`--list` / `--print-next`), или
   - явного `run_mode=…` из plan §safe-override (см. §4), или
   - первой **⚪** в индексе (режим B — только если нет валидного pkg и пустой `ACTIVE_TASK_PATH`).

**Запрещено:**

- Брать порядок из устаревшего текста плана или памяти, если расходится с `--list` и индексом.
- Переключаться на режим B при непустом валидном pkg до конца пакета.

---

## 2. `treat-missing-epic-as-not-decomposed` — эпик без индекса = не декомпозирован

Если файл `EPIC-M1-NN-*.md` существует в `GPT UI/docs/analysis/tasks/epics/`, но в `bullrun-launch-index.md` **нет** строки в epic registry / GIM-диапазоне с task queue:

- Считать эпик **не декомпозированным**.
- **Не** начинать P3 Execute по story/task из этого эпика.
- Запустить **P1** + [`@.cursor/commands/bullrun-epic-decompose.md`](../../../.cursor/commands/bullrun-epic-decompose.md): story folders, task README, immutable `pkg-*.yaml`, обновление индекса.

**REQ → tasks (типичный GPT P1.2):** новая волна по requirement внутри **существующего** `EPIC-M1-*` — story + nested tasks, новый `pkg-*`, без дубля эпика.

---

## 3. `sync-index-after-each-item` — индекс в той же итерации

После **каждого** закрытого task (🟢 Done / acceptance) или story gate:

1. Обновить статус строки в [`bullrun-launch-index.md`](../../../GPT UI/docs/analysis/tasks/bullrun-launch-index.md) (task table, gap queue, §«Актуальная точка»).
2. При дубле GIM — [`gpt-interview-module1-tasks-index.md`](../../../GPT UI/docs/analysis/tasks/gpt-interview-module1-tasks-index.md).
3. Не откладывать синхронизацию на «конец сессии».

Артефакты таска (`acceptance-verification-*.md`, `run-summary`) **не** заменяют индекс.

---

## 4. Safe-override paths (вне immutable pkg)

Оператор явно задаёт `run_mode=…` — **не** менять `gpt-active-package.current.yaml`.

| `run_mode` | Порядок | Paths (от корня `DOGEstonia/`) |
|------------|---------|--------------------------------|
| `req43_audit_followup` | GIM-185 | 1. `GPT UI/docs/analysis/tasks/epics/EPIC-M1-02-interview-dialogue-experience/stories/STORY-M1-02-11-req43-acceptance-evidence/task-doc-req43-req43-namespace-disambiguation/README.md` |
| `req42_audit_followup` | GIM-181 | 1. `GPT UI/docs/analysis/tasks/epics/EPIC-M1-06-orchestrator-openapi-web2/stories/STORY-M1-06-24-req42-acceptance-evidence/task-doc-req42-req42-namespace-disambiguation/README.md` |
| `req40_audit_followup` | GIM-174 | 1. `GPT UI/docs/analysis/tasks/epics/EPIC-M1-06-orchestrator-openapi-web2/stories/STORY-M1-06-16-req40-evidence-severity-sidecar/task-fix-req40-evidence-summary-flag-nesting/README.md` |
| `req39_audit_followup` | GIM-170 | 1. `GPT UI/docs/analysis/tasks/epics/EPIC-M1-05-issue-normalizer-strict-artifacts/stories/STORY-GM5-11-req39-city-level-canonicalization/task-fix-req39-changelog-version-order/README.md` |
| `req38_audit_followup` | GIM-166 | 1. `GPT UI/docs/analysis/tasks/epics/EPIC-M1-08-label-extraction-axes-controlled-vocabulary/stories/STORY-GM8-17-req38-normalizer-ecosystem-classification/task-fix-req38-anti-collapse-triplet-dedup/README.md` |
| `req36_audit_followup` | GIM-161 → GIM-162 | 1. `GPT UI/docs/analysis/tasks/epics/EPIC-M1-08-label-extraction-axes-controlled-vocabulary/stories/STORY-GM8-12-req36-promote-affected-deep-desired/task-fix-req36-affected-scope-dedup-promotion/README.md` · 2. `GPT UI/docs/analysis/tasks/epics/EPIC-M1-08-label-extraction-axes-controlled-vocabulary/stories/STORY-GM8-13-req36-ecosystem-governance-axes/task-fix-req36-brain-drain-cross-axis-dedup/README.md` |
| `req33_audit_followup` | GIM-147 → GIM-148 | 1. `GPT UI/docs/analysis/tasks/epics/EPIC-M1-08-label-extraction-axes-controlled-vocabulary/stories/STORY-GM8-10-req33-audit-followup-gap-closure/task-fix-req33-multi-axis-per-axis-rule/README.md` · 2. `GPT UI/docs/analysis/tasks/epics/EPIC-M1-08-label-extraction-axes-controlled-vocabulary/stories/STORY-GM8-10-req33-audit-followup-gap-closure/task-fix-req33-traceability-header-l10/README.md` |

Любой другой `run_mode` — только если есть одноимённый § в plan; иначе → YAML default (`pkg-000023`).

---

## Session checklist (Phase 0 / после Build)

```markdown
## GPT session resolve

- verify: ok 3 paths (pkg-000023 …)
- index: bullrun-launch-index §Актуальная точка
- active pkg: gpt-active-package.current.yaml → pkg-000023 (GIM-182…184 🟢)
- run_mode: (оператор) | default pkg queue
- next work: GIM-185 ⚪ via run_mode=req43_audit_followup | или --print-next / первая ⚪ (режим B)
```

---

## SSOT order (GPT)

1. `run_mode` override list (если оператор явно указал)  
2. Active `gpt-active-packages/pkg-*.yaml` + `--verify`  
3. `bullrun-launch-index.md` (+ module1 index)  
4. `GPT UI/docs/requirements/REQ-*.md`  
5. Task `README.md` + acceptance-verification

Skill для артефактов instructions: `@.cursor/skills/openai-custom-gpt-builder/SKILL.md`.
