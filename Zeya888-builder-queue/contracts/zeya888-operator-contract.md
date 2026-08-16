# Zeya888 Builder — operator contract

> **Plan (read-only unless operator asks):** [`.cursor/plans/Zeya888_builder.plan.md`](../../../.cursor/plans/Zeya888_builder.plan.md)  
> **Propagation:** [builder-session/SKILL.md](../../../.cursor/skills/builder-session/SKILL.md) · [builder-operator-habits.mdc](../../../.cursor/rules/builder-operator-habits.mdc) · [session-starter.md](../core/session-starter.md)

Process-reminder правила для `builder_project: zeya888` (WordPress/PHP в `zeya888.me/`). P1/PA промпты — только [workflow.md](../core/workflow.md); не дублировать в plan.

---

## 1. `resolve-start-from-index` — старт только из индекса + active pkg

**Перед** batch-run, Build window или P3 Execute:

**Fixed plan:** `@attach` [`.cursor/plans/Zeya888_builder.plan.md`](../../../.cursor/plans/Zeya888_builder.plan.md) + workflow §P3/P6 в **этом** чате — **не** Build / Execute plan на файле ([fixed-builder-plan-execution.md](../guides/fixed-builder-plan-execution.md)).

1. Прочитать [`zeya888.me/docs/tasks/bullrun-launch-index.md`](../../../zeya888.me/docs/tasks/bullrun-launch-index.md) §«Актуальная точка».
2. Прочитать [`zeya888-active-package.current.yaml`](../../../zeya888.me/docs/tasks/zeya888-active-package.current.yaml) → `package_file`, `activation`.
3. Из корня workspace:  
   `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project zeya888 --verify`  
   При `FAIL` — **стоп**; запустить **P1.3** (после авторства `STORY-ZEYA-BUG-*`), не выдумывать очередь.
4. Следующую волну брать **только** из индекса, pkg/`--list`, или явной команды (`run_mode=…` из plan §safe-override).

**Запрещено:**

- Брать порядок из памяти или исполнять raw audit findings без materialized story + task `README.md` + pkg.
- Invent `STORY-ZEYA-BUG-*` / epics без фактов audit.
- Публиковать exploit/PoC или attack procedures ([BUG-STORY-SCHEMA.md](../../../zeya888.me/docs/tasks/backlog-stories/BUG-STORY-SCHEMA.md)).
- Смешивать zeya888 work с другими `builder_project` без явной команды.

---

## 2. `treat-missing-epic-as-not-decomposed` — эпик без task queue = не декомпозирован

Если `EPIC-ZEYA-*` появится в `zeya888.me/docs/tasks/epics/`, но в bullrun **нет** Builder Queue task queue:

- Считать эпик **не декомпозированным**.
- **Не** начинать P3 Execute.
- Запустить **P1.1** + [`bullrun-epic-decompose.md`](../../../.cursor/commands/bullrun-epic-decompose.md) или **P1.3** для backlog story.

**Primary intake:** **P1.3** `backlog_story` — keys `STORY-ZEYA-BUG-*` per [BUG-STORY-SCHEMA.md](../../../zeya888.me/docs/tasks/backlog-stories/BUG-STORY-SCHEMA.md) from [backdoor-audit-2026-08-14.md](../../../zeya888.me/docs/backdoor-audit-2026-08-14.md).

---

## 3. `sync-index-after-each-task` — индекс в той же итерации

После **каждого** закрытого task или story gate (и при **emit / добавлении** новых `STORY-ZEYA-BUG-*`):

1. Обновить `bullrun-launch-index.md` и [`backlog-stories/INDEX.md`](../../../zeya888.me/docs/tasks/backlog-stories/INDEX.md).
2. Обновить §«Актуальная точка».
3. Recount [`zeya888-mvp-dashboard.md`](../../../zeya888.me/docs/tasks/zeya888-mvp-dashboard.md): Summary / By package / Remaining (keys = links) / §Now / `Updated` / `Last change` — только с диска (см. [backlog-dashboard-maintenance.md](../workflow/backlog-dashboard-maintenance.md)).
4. Не откладывать sync на конец сессии.

---

## 4. `pick-input-mode-explicitly` — один режим входа на сессию

| `input_mode` | Якорь P1/P3/P4 | Когда (zeya888) |
|--------------|----------------|-----------------|
| `backlog_story` | `@$storyFile` (`STORY-ZEYA-BUG-*`); опц. `@$backlogIndex` | **Primary:** после авторства story из audit |
| `requirement` | `@$requirementDoc` (situation/audit docs) | Инкремент по audit/context |
| `epic_story` | `@$epicFile` (`EPIC-ZEYA-*`) | Когда эпик materialize |
| `run_mode=…` | audit gap list из `Zeya888_builder.plan.md` §safe-override | Post-audit; **не** менять active pkg |

**Bootstrap marker t00:** methodology only — **не** P3 product work на marker.

**PA (до P1):** workflow §PA — shaping; без pkg и без P3.

---

## 5. Date discipline (artifact dates)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --print-utc-now
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project zeya888 --verify --check-dates
```

SSOT: [`guides/builder-artifact-dates.md`](../guides/builder-artifact-dates.md).

---

## Session checklist

```markdown
## Zeya888 session resolve

- verify: ok N paths | FAIL (→ author STORY + P1.3 first)
- check-dates: ok / WARN / FAIL
- index: bullrun-launch-index §Актуальная точка
- active pkg: zeya888-active-package.current.yaml → pkg-…
- input_mode: backlog_story | requirement | epic_story | run_mode=… (один)
- stack: WordPress (PHP); skill wordpress-pro (fallback php-pro)
- next work: <из --list или backlog INDEX, не из памяти>
- forbidden: exploit/PoC, invent findings
```

---

## SSOT order (zeya888)

1. `run_mode` override list (если оператор явно указал)  
2. Active `zeya888-active-packages/pkg-*.yaml` + `--verify`  
3. `bullrun-launch-index.md` + `backlog-stories/INDEX.md`  
4. **Backlog:** `backlog-stories/` + schema · **Audit/context:** `zeya888.me/docs/backdoor-audit-*.md`, `situation-context-*.md` (intake, не очередь)  
5. Task `README.md` + acceptance-verification

Pipeline: [`zeya888-story-execution-pipeline.md`](../../../zeya888.me/docs/tasks/zeya888-story-execution-pipeline.md).

---

## 6. Аудит P4 / P7 (якоря по `input_mode`)

Отчёты: `zeya888.me/docs/analysis/` (создать при необходимости). Мышление: `@.cursor/rules/analysis.mdc`. Промпты — [workflow.md](../core/workflow.md) §P4 / §P7 (P5 auto-decide disposition + follow_up; без AskQuestion).

| Режим | Cursor P4 | External re-audit |
|-------|-----------|-------------------|
| `backlog_story` | Факт-код/снимок vs AC в `@$storyFile` | workflow §P4 |
| `requirement` | Факт vs `$requirementDoc` + AC | workflow §P4 |
| `epic_story` | Факт vs AC Stories в `$epicFile` | workflow §P4 |
| `run_mode=…` | Findings + AC тасков override | workflow §P7 |

Build plan **не** содержит таблицу P4 — только эта секция и workflow.

---

## 7. P1.3 `backlog_story` (zeya888 appendix)

Используется с [workflow.md](../core/workflow.md) §P1.3 (`$p13Appendix` для `builder_project: zeya888`).

| Параметр | Значение |
|----------|----------|
| Epic prefix (target) | `EPIC-ZEYA-*` (when materialize) |
| Story prefix | `STORY-ZEYA-BUG-*` |
| Materialize path | `zeya888.me/docs/tasks/epics/` (after P1) |
| Execution skill | `wordpress-pro` (`execution_skill_primary`); fallback `php-pro` |
| Schema | [`BUG-STORY-SCHEMA.md`](../../../zeya888.me/docs/tasks/backlog-stories/BUG-STORY-SCHEMA.md) |
| Audit SSOT | [`backdoor-audit-2026-08-14.md`](../../../zeya888.me/docs/backdoor-audit-2026-08-14.md) |
| Context | [`situation-context-2026-08-14.md`](../../../zeya888.me/docs/situation-context-2026-08-14.md) |

**hasUxPipeline:** false — не spa UI-0..UI-3.

**Forbidden in stories/tasks:** exploit PoC, attack procedures, unverified Floou→zeya888 transfer.
