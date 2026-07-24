# Identity Builder — operator contract

> **Plan (read-only unless operator asks):** [`.cursor/plans/ID_builder.plan.md`](../../../.cursor/plans/ID_builder.plan.md)  
> **Propagation:** [builder-session/SKILL.md](../../../.cursor/skills/builder-session/SKILL.md) · [builder-operator-habits.mdc](../../../.cursor/rules/builder-operator-habits.mdc) · [session-starter.md](../core/session-starter.md)

Три process-reminder правила из frontmatter `ID_builder.plan.md` + §4 `input_mode` / §5 P4 — исполняются агентом на **каждой** сессии `builder_project: identity`. P1 промпты — только [workflow.md](../core/workflow.md); не дублировать в plan.

---

## 1. `resolve-start-from-index` — старт только из индекса + active pkg

**Перед** batch-run, Build window или P3 Execute:

**Fixed plan:** `@attach` [`.cursor/plans/ID_builder.plan.md`](../../../.cursor/plans/ID_builder.plan.md) + workflow §P3/P6 в **этом** чате — **не** Build / Execute plan на файле ([fixed-builder-plan-execution.md](../guides/fixed-builder-plan-execution.md)).

1. Прочитать [`doge-identity-service/docs/tasks/bullrun-launch-index.md`](../../../doge-identity-service/docs/tasks/bullrun-launch-index.md) §«Актуальная точка» и §«Epic registry».
2. Прочитать [`identity-active-package.current.yaml`](../../../doge-identity-service/docs/tasks/identity-active-package.current.yaml) → `package_file`.
3. Из корня workspace:  
   `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify`  
   При `FAIL` — **стоп** (не выдумывать очередь).
4. Следующий эпик / волну / override брать **только** из индекса или явной команды оператора (`run_mode=…` из plan §safe-override).

**Запрещено:**

- Создавать или исполнять эпики вне префикса `EPIC-IDS-*` в `doge-identity-service/docs/tasks/epics/`.
- Брать порядок задач из устаревшего текста плана, если он расходится с индексом и `--list`.

---

## 2. `treat-missing-epic-as-not-decomposed` — эпик без индекса = не декомпозирован

Если файл `EPIC-IDS-NN-*.md` существует в `docs/tasks/epics/`, но в `bullrun-launch-index.md` **нет** строки в §Epic registry с task queue (или статус «не декомпозирован»):

- Считать эпик **не декомпозированным**.
- **Не** начинать P3 Execute по story/task из этого эпика.
- Запустить **P1** + [`@.cursor/commands/bullrun-epic-decompose.md`](../../../.cursor/commands/bullrun-epic-decompose.md): story folders, task README, immutable `pkg-*.yaml`, обновление индекса.

**Backlog story (отдельный случай):** если эпик **ещё не в pipeline** (`docs/tasks/epics/`), но story лежит в `docs/tasks/backlog-stories/` — это **не** P3 Execute и **не** полный `bullrun-epic-decompose` целого эпика. Использовать **P1.3** (`input_mode=backlog_story`): materialize epic + pipeline story + deep tasks + pkg ([workflow.md](../core/workflow.md) §P1.3).

Пример: эпик без строки в §Epic registry с task queue (или пометка «не декомпозирован») → только decompose. **EPIC-IDS-06** после P1 2026-06-02 — декомпозирован (`pkg-000008`, 15 tasks); post-audit gaps — override `run_mode=epic_ids_06_audit_2026_06_02`, не новый pkg.

---

## 3. `sync-index-after-each-task` — индекс в той же итерации

После **каждого** закрытого task (🟢 Done / acceptance) или story gate:

1. Обновить статус строки в `bullrun-launch-index.md` (task table или gap queue).
2. Обновить package [`backlog-stories/*/INDEX.md`](../../../doge-identity-service/docs/tasks/backlog-stories/) и root [`backlog-stories/INDEX.md`](../../../doge-identity-service/docs/tasks/backlog-stories/INDEX.md).
3. Пересчитать [`identity-backlog-dashboard.md`](../../../doge-identity-service/docs/tasks/identity-backlog-dashboard.md) (derived snapshot; см. [backlog-dashboard-maintenance.md](../workflow/backlog-dashboard-maintenance.md)).
4. При необходимости — §«Актуальная точка» (следующая story, override, epic gate).
5. Не откладывать синхронизацию на «конец сессии».

Артефакты таска (`acceptance-verification-*.md`, `run-summary`) **не** заменяют индекс.

---

## 4. `pick-input-mode-explicitly` — один режим входа на сессию

Оператор в **первом** сообщении сессии указывает **один** режим:

| `input_mode` | Якорь P1/P3/P4 | Когда |
|--------------|----------------|-------|
| `epic_story` | `@$epicFile` (`EPIC-IDS-*.md`) | Волна по готовому эпику, pkg `epic_story_tree` |
| `requirement` | `@$requirementDoc` (`docs/requirements/NN-*.md`) | Новая фича / gap по REQ |
| `backlog_story` | `@$storyFile` (`docs/tasks/backlog-stories/STORY-IDS-*.md`); опц. `@$backlogIndex` | Intake одной готовой story в pipeline (P1.3); epic materialize если нет в `epics/` |
| `run_mode=epic_ids_06_audit_2026_06_02` (и др. из plan) | audit gap task README (5× EPIC-IDS-06) | P3 по [`epic-ids-06-audit-2026-06-02.md`](../../../doge-identity-service/docs/analysis/epic-ids-06-audit-2026-06-02.md); **не** менять `pkg-000008` |

**Запрещено** смешивать в одном pkg без явного решения оператора: requirement-AC, epic-only AC и backlog-story AC.

Override-волна (`run_mode=epic_ids_*_audit_*` / `*_reaudit_*`) — отдельный режим: только нумерованный список из `ID_builder.plan.md` §safe-override; `input_mode=epic_story` **не** подменяет `run_mode`.

---

## Session checklist (Phase 0 / после Build)

```markdown
## Identity session resolve

- verify: ok N paths (pkg-000008 …)
- index: bullrun-launch-index §Актуальная точка
- active pkg: identity-active-package.current.yaml → pkg-000008
- input_mode: epic_story | requirement | backlog_story | run_mode=epic_ids_06_audit_2026_06_02 (оператор, один на сессию)
- next work: <из индекса или run_mode list, не из памяти>
- EPIC-IDS-06 audit: F1–F5 ⚪ если run_mode=epic_ids_06_audit_2026_06_02
```

---

## SSOT order (identity)

1. `run_mode` override list (если оператор явно указал)  
2. Active `identity-active-packages/pkg-*.yaml` + `--verify`  
3. `bullrun-launch-index.md` + `backlog-stories/INDEX.md` + package `INDEX.md`  
4. `identity-backlog-dashboard.md` (derived)  
5. **Epic mode:** `EPIC-IDS-*.md` · **Requirement mode:** `docs/requirements/` → эпик по ссылкам/индексу · **Backlog mode:** `backlog-stories/` → после P1.3 pipeline story в `epics/`  
6. Task `README.md` + acceptance-verification

---

## 5. Аудит P4 / P4b (якоря по `input_mode`)

Отчёты: `doge-identity-service/docs/analysis/`. Мышление: `@.cursor/rules/analysis.mdc`. Промпты — [workflow.md](../core/workflow.md) §P4 / §P4b.

| Режим | Cursor P4 | Claude P4b (external) |
|-------|-----------|------------------------|
| `requirement` | Факт-код vs `$requirementDoc` + AC | workflow §P4b (anchor=requirement) |
| `epic_story` | Факт-код vs AC Stories в `$epicFile` | workflow §P4b (anchor=epic/story) |
| `backlog_story` | Факт-код vs AC в `@$storyFile` | workflow §P4b (anchor=backlog story) |
| `run_mode=…` (audit override) | Факт-код vs findings в audit report + AC тасков override-списка | workflow §P4b по audit report |

Build plan (`ID_builder.plan.md`) **не** содержит таблицу P4 — только эта секция и workflow.

---

## 6. P1.3 `backlog_story` (identity appendix)

Используется с [workflow.md](../core/workflow.md) §P1.3 (`$p13Appendix` для `builder_project: identity`).

| Параметр | Значение |
|----------|----------|
| Epic prefix | `EPIC-IDS-*` |
| Materialize path | `doge-identity-service/docs/tasks/epics/` |
| Pipeline story | `epics/<EPIC>/stories/<STORY-KEY>/STORY-*.md` |
| Task naming | `task-ids-NN-YY-tNN-<slug>/README.md` |
| Active pointer | `identity-active-package.current.yaml` |
| Execution skill | `python-pro` |

**Epic materialize (из backlog Meta.Epic):**

- EPIC уже в `epics/` → использовать.
- EPIC только в `backlog-stories/EPIC-*.md` → materialize `EPIC-IDS-NN-*.md` (следующий свободный номер) + bullrun.
- EPIC только «в коде» (AUTH-CORE/OAUTH/EID) → `EPIC-IDS-NN-<slug>.md` по Meta + runtime-docs из «Парадигма-якорь»; не дублировать EPIC-IDS-01..06.

**Пример:** `STORY-IDS-EID-01` → `EPIC-IDS-09` / `pkg-000015`.

