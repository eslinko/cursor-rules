# Workflow: Requirement → Pipeline → Audit

Операторский playbook для Zeya888 Builder Queue. Детали YAML/CLI — в `[input-package-spec.md](../specs/input-package-spec.md)`, `[queue-manual.md](../cli/queue-manual.md)`.

**Нужны полные промпты PA, P1–P8 (self-contained), P4/P7 audit целиком, таблица «экономия токенов», wave checkpoint с деталями?** → `[workflow-legacy.md](./workflow-legacy.md)` (нумерация legacy может отличаться — см. заголовки фаз).

## Переменные пайплайна

Оператор задаёт `**builder_project`** (`gateway` | `gpt` | `identity` | …) в [starter](./session-starter.md) или в wave checkpoint.


| Переменная                | Подстановка                                                                                                                                                                                                       |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$builderProject`         | `gateway` / `gpt` / …                                                                                                                                                                                             |
| `$verifyCmd`              | `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project $builderProject --verify`                                                                                                  |
| `$verifyDatesCmd`         | `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project $builderProject --verify --check-dates`                                                                                    |
| `$printUtcNowCmd`         | `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --print-utc-now`                                                                                                                     |
| `$inputMode`              | `requirement`                                                                                                                                                                                                     |
| `$requirementDoc`         | файл требования (для `input_mode=requirement`)                                                                                                                                                                    |
| `$epicFile`               | файл эпика (для `input_mode=epic_story`)                                                                                                                                                                          |
| `$storyFile`              | для `input_mode=backlog_story` — готовая story из `backlog-stories/` (напр. `doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-*.md`); для `input_mode=epic_story` — опционально одна story внутри эпика |
| `$backlogIndex`           | опционально для `input_mode=backlog_story`: `doge-identity-service/docs/tasks/backlog-stories/INDEX.md` (порядок/зависимости; не подменяет AC story)                                                              |
| `$planFile`               | см. `plan_file` в `[profiles.yaml](../specs/profiles.yaml)`                                                                                                                                                       |
| `$tasksRoot`              | см. `tasks_dir` в profiles                                                                                                                                                                                        |
| `$storyKey`               | ключ story (gateway), напр. `STORY-M2-14-07`                                                                                                                                                                      |
| `$buildWindowFile`        | путь к `*-cursor-build-window--*.md` в `run-reports/*-build-windows/` (строка `build_window_file:` в stdout после P2; для Cmd+click — `build_window_abs:`)                                                        |
| `$buildWindowCmd`         | см. §P2 — флаги `--write-build-window` для `$builderProject`                                                                                                                                                      |
| `$auditReport`            | `{focus_project}/docs/analysis/*.md`                                                                                                                                                                              |
| `$artifactKind`           | `requirement`                                                                                                                                                                                                     |
| `$intakeDraft`            | сырой или неполный intake-файл (может совпадать с `$requirementDoc` / `$epicFile` / `$storyFile` при refine-in-place)                                                                                             |
| `$etalonDir`              | папка эталонов стиля: `…/requirements/`, `$tasksRoot/epics/`, `…/backlog-stories/` — см. profiles и §PA                                                                                                           |
| `$intakeArtifact`         | **выход PA** — canonical file на диске (= `$requirementDoc`                                                                                                                                                       |
| `$currentPointer`         | `current_pointer` в profiles (напр. `spa-active-package.current.yaml`)                                                                                                                                            |
| `$executionSkillPrimary`  | `execution_skill_primary` в profiles (напр. `python-pro`, `react-expert`)                                                                                                                                         |
| `$executionSkillPath`     | `execution_skill_path` в profiles — путь к execution SKILL.md                                                                                                                                                     |
| `$executionSkillDeclared` | строка для task README: `Skill declared: $executionSkillPrimary` (или fallback из profile / README таска)                                                                                                         |
| `$p13Appendix`            | operator contract §6/§7 P1.3 (`spa` / `identity` / `scripts`) — epic naming, materialize rules                                                                                                                    |




### Профили (быстрая таблица)


|               | `gateway`                                    | `gpt`                                       |
| ------------- | -------------------------------------------- | ------------------------------------------- |
| `$planFile`   | `.cursor/plans/Gateway_builder.plan.md`      | `.cursor/plans/GPT_builder.plan.md`         |
| `$tasksRoot`  | `doge-complaints-gateway/docs/tasks`         | `GPT UI/docs/analysis/tasks`                |
| Окно по story | `--write-build-window --story-key $storyKey` | часто `--window-flat-start` / `--gim-slice` |
| Bullrun index | `$tasksRoot/bullrun-launch-index.md`         | то же                                       |



|                 | `identity` (epic-first / backlog intake)                                                                                      |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `$planFile`     | `.cursor/plans/ID_builder.plan.md`                                                                                            |
| `$tasksRoot`    | `doge-identity-service/docs/tasks`                                                                                            |
| `$epicFile`     | напр. `doge-identity-service/docs/tasks/epics/EPIC-IDS-01-scaffold-config-launch.md`                                          |
| `$storyFile`    | напр. `doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-AUTHCORE-01-profile-and-me.md` (`input_mode=backlog_story`) |
| `$backlogIndex` | `doge-identity-service/docs/tasks/backlog-stories/INDEX.md`                                                                   |
| Окно по story   | `--write-build-window --story-key STORY-IDS-01-02`                                                                            |
| Окно весь эпик  | `--write-build-window --window-flat-start 1 --window-flat-end K` (`K` из `--list`)                                            |
| Pipeline        | `doge-identity-service/docs/tasks/ids-epic-execution-pipeline.md`                                                             |



|                        | `spa` (doc-gap backlog / legacy DASH)                                                                                     |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `$planFile`            | `.cursor/plans/Spa_builder.plan.md`                                                                                       |
| `$tasksRoot`           | `spa-app/docs/tasks`                                                                                                      |
| `$storyFile`           | напр. `spa-app/docs/tasks/backlog-stories/STORY-SPA-G1-gateway-endpoint-alignment.md` (`input_mode=backlog_story`)        |
| `$backlogIndex`        | `spa-app/docs/tasks/backlog-stories/INDEX.md`                                                                             |
| Окно flat              | `--write-build-window --window-flat-start 1 --window-flat-end K` (`K` из `--list`)                                        |
| Pipeline               | `spa-app/docs/tasks/spa-story-execution-pipeline.md`                                                                      |
| `$uiVisualPipelineDoc` | `docs/methodology/Zeya888-builder-queue/guides/spa-ui-visual-pipeline.md` — полный SSOT UI-0..UI-3                        |
| `$uiPipelineDoc`       | `spa-app/docs/tasks/spa-story-execution-pipeline.md` §UI task hard gates; copy-paste P3 UI — workflow §P3 spa UI appendix |



|                 | `scripts` (Web3 / Node.js infrastructure)                                                               |
| --------------- | ------------------------------------------------------------------------------------------------------- |
| `$planFile`     | `.cursor/plans/Scripts_builder.plan.md`                                                                 |
| `$tasksRoot`    | `scripts/docs/tasks`                                                                                    |
| `$storyFile`    | напр. `scripts/docs/tasks/backlog-stories/STORY-SCR-01-web3-connection.md` (`input_mode=backlog_story`) |
| `$backlogIndex` | `scripts/docs/tasks/backlog-stories/INDEX.md`                                                           |
| Окно по story   | `--write-build-window --story-key STORY-SCR-01-01`                                                      |
| Окно flat       | `--write-build-window --window-flat-start 1 --window-flat-end K` (`K` из `--list`)                      |
| Pipeline        | `scripts/docs/tasks/scripts-story-execution-pipeline.md`                                                |
| Intake docs     | `scripts/docs/runtime-infrastructure/README.md` (shaping only, не очередь)                              |


---



## Базовый маршрут

1. **Phase 0** — onboarding ([session-starter.md](./session-starter.md))
2. **PA — Intake Analysis** (если черновик сырой; skip если `$intakeArtifact` уже canonical) → `$intakeArtifact` на диске
3. **P1 — Plan** (P1.1  P1.2  P1.3) — EPIC/STORY/tasks + pkg → `$planFile`
4. **Plan → Package** — immutable `pkg-*.yaml` + `*-active-package.current.yaml`
5. **P2 — Build window** — `$verifyCmd` затем `--write-build-window …` → `$buildWindowFile`
6. **P3 — Execution** — `@$planFile` + `@$buildWindowFile`, шаг 0, Режим A
7. **P4 — Audit** → `$auditReport`
8. **P5 — Gap scaffold** — task folders; YAML default не ломать
9. **P6 — Execute gaps** · **P7 — Re-audit**
10. **P8 — Finalize** — `[git-commit.md](../git-commit.md)`

---



## Предпосылка: Phase 0

В начале project-чата вставьте [session-starter.md](./session-starter.md) с `builder_project: …` и дождитесь **Onboarding summary**.

Без Phase 0 — сначала starter, затем фазы ниже.

### Skill и rule


| Механизм | Файл                                        |
| -------- | ------------------------------------------- |
| Skill    | `.cursor/skills/builder-session/SKILL.md`   |
| Rule     | `.cursor/rules/builder-operator-habits.mdc` |
| Analysis | `.cursor/rules/analysis.mdc`                |


Rule подмешивается при работе в `doge-complaints-gateway/`**,** `GPT UI/`, `doge-identity-service/`**,** `spa-app/`, `scripts/`**.

### Wave checkpoint

```text
Wave checkpoint — $storyKey (builder_project: $builderProject)
@.cursor/skills/builder-session/SKILL.md @.cursor/rules/builder-operator-habits.mdc
@$tasksRoot/*-active-package.current.yaml
@$buildWindowFile
Фаза: P3 (укажи PA|P1|P2|P3|P4|…; PA = intake shaping; P2 = только build window)
Сбрось контекст прошлой story. $verifyCmd перед execution.
```

---



## Короткие промпты (после Phase 0)

**Якорь Builder (P1+):** `@.cursor/skills/builder-session/SKILL.md` + `@.cursor/rules/builder-operator-habits.mdc`  
**Execution skill (P1 decompose / P3 code):** резолв по builder-session → `$executionSkillPath` из profiles; task README overrides profile.  
**Якорь PA:** `@.cursor/rules/analysis.mdc` (skill/rule опционально; без pkg и без P3)

**Skip PA:** если `$intakeArtifact` уже canonical — метаданные, AC, verified state по стилю соседних файлов в `$etalonDir` (ориентир: `[REQ-41](../../../GPT UI/docs/requirements/REQ-41-trigger-observability-audit-trail.md)` vs сырой `[REQ-42](../../../GPT UI/docs/requirements/REQ-42.md)`).

### PA — Intake Analysis (перед P1)

**Режим:** Analysis / shaping only — без pkg, без task README, без P3, без `$verifyCmd` pkg.  
**Выход:** запись `$intakeArtifact` на диск → handoff «PA завершён → P1.x, @file».


| Фаза            | Когда                 | Вопрос                       | Выход             |
| --------------- | --------------------- | ---------------------------- | ----------------- |
| **PA**          | До P1                 | Черновик → canonical intake? | `$intakeArtifact` |
| Gap (внутри PA) | Секции verified state | Код vs целевое?              | paths в intake    |
| **P4**          | После P3              | Код vs AC/pkg?               | `$auditReport`    |


Рекомендуется **отдельный Studio-чат** (Plan/Ask). Human layer: `[curriculum/06-architect-studio-and-p1-intakes.md](../curriculum/06-architect-studio-and-p1-intakes.md)`.

#### PA.1 — Epic shaping

```text
@.cursor/rules/analysis.mdc

PA Intake Analysis. builder_project: $builderProject.
artifact_kind=epic. @$intakeDraft (или @$epicFile при refine-in-place)
Эталон стиля: @$etalonDir (= $tasksRoot/epics/ — соседние EPIC-*.md)

Целевое состояние: canonical epic для P1.1 — Goal, Stories, AC, out of scope, метаданные как у эталонов.

1) Прочитать @$intakeDraft и 1–2 соседних epic из $etalonDir — сравнить глубину и структуру.
2) Интерактивное интервью на каждом decision point: человеческий язык, расшифровка терминов.
   Протокол Other: если оператор задаёт уточняющий вопрос — сначала ответ, затем повтор или адаптация вопроса.
3) Секции «текущее состояние» / verified-by-code — только facts с paths (grep/read); без assumptions.
4) Записать результат в @$intakeArtifact (= @$epicFile). Analysis only — без pkg, без task README, без P3.
5) Handoff: «PA.1 завершён → P1.1 input_mode=epic_story. @$epicFile»
```



#### PA.2 — Requirement shaping

```text
@.cursor/rules/analysis.mdc

PA Intake Analysis. builder_project: $builderProject.
artifact_kind=requirement. @$intakeDraft (или @$requirementDoc при refine-in-place)
Эталон стиля: @$etalonDir (gateway: doge-complaints-gateway/docs/requirements/; gpt: GPT UI/docs/requirements/REQ-*.md)

Целевое состояние: canonical requirement для P1.2 — метаданные, verified current state, целевое состояние, AC, dependencies/парные REQ по стилю эталонов.

1) Прочитать @$intakeDraft и 1–2 соседних requirement из $etalonDir.
2) Интерактивное интервью на decision points; Other-протокол (см. PA.1).
3) Verified state — только из кода/instructions с paths (analysis.mdc).
4) Записать в итоговый файл (добавить нейминг по общему стилю) => @$requirementDoc. Analysis only.s
5) Handoff: «PA.2 завершён → P1.2 input_mode=requirement. @$requirementDoc»

мышление @ai-2-web3-bootstrap/.cursor/rules/analysis.mdc 
```



#### PA.3 — Backlog story shaping

```text
@.cursor/rules/analysis.mdc

PA Intake Analysis. builder_project: $builderProject (типично identity или spa).
artifact_kind=backlog_story. @$intakeDraft (или @$storyFile при refine-in-place)
Эталон: backlog-stories/ + опционально @$backlogIndex

Целевое состояние: canonical backlog story для P1.3 — Meta, Scope, AC, «Точки в коде», «Вне scope» по стилю STORY-IDS-* эталонов.

1) Прочитать @$intakeDraft и 1–2 соседних story из backlog-stories/.
2) Интерактивное интервью; gap-to-code с paths для «Точки в коде»; Other-протокол (см. PA.1).
3) Записать @$intakeArtifact (= @$storyFile). Analysis only — без pkg, без pipeline story, без P3.
4) Handoff: «PA.3 завершён → P1.3 input_mode=backlog_story. @$storyFile»
```

Полные self-contained промпты PA: `[workflow-legacy.md](./workflow-legacy.md)` §PA.

### P1 — Plan

**Предпосылка (все P1.x):** `$intakeArtifact` прошёл PA или уже canonical. P1 **не** проводит интервью и **не** нормализует стиль сырого черновика.

## P1.1 (Epic, обязательный порядок):

```text
@.cursor/skills/builder-session/SKILL.md
@.cursor/rules/builder-operator-habits.mdc
@.cursor/rules/analysis.mdc

P1 Plan mode. builder_project: $builderProject.
input_mode=epic_story. @$epicFile

Нужно сделать декомпозию строго из содержимого эпика:
1) взять Stories из текста эпика (внутренние разделы Story/Acceptance Criteria) как единственный источник;
2) не придумывать новые Stories вне эпика и не менять формулировки AC;
3) для каждой Story подготовить task-папки и README по @docs/methodology/task-standard.md; в README: $executionSkillDeclared (по builder-session);
4) сформировать immutable pkg (@docs/methodology/Zeya888-builder-queue/specs/input-package-spec.md) с корректным `epic_file` и `story_groups`;
5) синхронизировать @$tasksRoot/bullrun-launch-index.md и указатель active package.

Требование analysis.mdc: каждый claim подтверждать путём к файлу. Plan only — без execution.
В конце: таблица Story -> task -> файлы -> статус + список созданных/изменённых путей.

Artifact dates: см. §P1 appendix (artifact dates) — $printUtcNowCmd перед pkg/gate; после scaffold $verifyDatesCmd.

```



## P1.2 (Requirement, обязательный порядок):

```text
@.cursor/skills/builder-session/SKILL.md
@.cursor/rules/builder-operator-habits.mdc
@.cursor/rules/analysis.mdc

1) Вход только @$requirementDoc.
2) Обязательно найти подходящий существующий эпик в @$tasksRoot/epics и bullrun-launch-index.md (по домену/scope requirement); не стартовать с произвольной story.
3) На базе requirement создать 1+ Story внутри выбранного эпика (и task-папки внутри story), без создания параллельного дублирующего эпика если текущий эпик подходит.
4) Материал requirement внедрять в Story/Task артефакты как source-of-truth: AC, scope, ограничения; в task README: $executionSkillDeclared (по builder-session).
5) Обновить pkg (immutable) и индекс; pkg формировать в формате, совместимом с input-package-spec.md (`epic_story_tree` или `epic_decompose_pending` по состоянию); в отчёте явно показать mapping `requirement -> epic -> story -> tasks`.

помни про то что таски внутри стори, чтобы была понятная вложенная структура
и эпик подбери из существующих

По skill: Plan only — без execution. Все claims с путями к файлам (analysis.mdc). В конце — список созданных/изменённых путей.

Artifact dates: см. §P1 appendix (artifact dates) — $printUtcNowCmd перед pkg/gate; после scaffold $verifyDatesCmd.
```



## P1.3 (Backlog story, обязательный порядок):

```text
@.cursor/skills/builder-session/SKILL.md
@.cursor/rules/builder-operator-habits.mdc
@.cursor/rules/analysis.mdc
@$storyFile=

P1 Plan mode. builder_project: $builderProject (типично identity или spa).
input_mode=backlog_story. @$storyFile
Опционально для сверки зависимостей: @$backlogIndex
Epic/task naming и materialize: $p13Appendix (operator contract §6 для spa или identity).

1) Вход — только @$storyFile. AC, Scope, «Вне scope», «Точки в коде» брать из файла; не придумывать новые stories/AC и не менять формулировки.
2) Epic из Meta.Epic story — по $p13Appendix (materialize в @$tasksRoot/epics/, строка в bullrun-launch-index).
3) Materialize pipeline story: @$tasksRoot/epics/<EPIC>/stories/<STORY-KEY>/STORY-*.md — перенести AC/scope из backlog verbatim; decision_ref → @$storyFile + источники из Meta.
4) Глубокая декомпозиция в task-папки (@docs/methodology/task-standard.md):
   - каждый пункт Scope → 1+ atomic task (implement/fix/tests);
   - каждый AC → traceability в task AC/DoD;
   - финальный task — story acceptance-verification; story gate — `[story-acceptance-gate-template.md](../templates/story-acceptance-gate-template.md)`;
   - naming task-папок — по $p13Appendix;
   - каждый README: Purpose, Code Facts (verify exists), AC/DoD, Where to change, Verification commands;
   - $executionSkillDeclared (по builder-session / profiles.yaml).
   Ориентир глубины: мелкая story 3–4 tasks; средняя 4–6; крупная cleanup 5–7. Запрет: один task на всю story, если Scope содержит 3+ независимых изменений в коде.
5) Immutable pkg (@docs/methodology/Zeya888-builder-queue/specs/input-package-spec.md):
   - input_kind: epic_story_tree;
   - epic_file → materialized epic;
   - story_groups: одна группа = STORY-KEY из backlog, paths = все task README по порядку;
   - обновить $currentPointer (из profiles).
6) Синхронизировать @$tasksRoot/bullrun-launch-index.md (story row, task table, «Актуальная точка»).
7) Backlog-файл @$storyFile не удалять; в pipeline-story указать source: backlog-stories/…

Не смешивать в этой волне с input_mode=requirement|epic_story без явной команды оператора.
Plan only — без execution. Claims с путями (analysis.mdc).
В конце: mapping `backlog_story -> epic -> story -> tasks -> pkg paths` + список созданных/изменённых путей.

Artifact dates: см. §P1 appendix (artifact dates) — $printUtcNowCmd перед pkg/gate; после scaffold $verifyDatesCmd.
```

--- P1 appendix: artifact dates (обязательно при создании pkg / gate / run-summary) ---

```text
Перед записью дат выполни из корня workspace:
  $printUtcNowCmd
Используй ТОЛЬКО значения из stdout (utc_now, utc_date, pkg_filename_date, run_summary_prefix).
Запрещено: выдумывать дату, T12:00:00Z без live-run, дата раньше gate зависимостей.
pkg: created_at = utc_now; имя pkg-NNNNNN-<pkg_filename_date>-slug.yaml.
story-acceptance-gate Date: — только после live pytest + --verify в ЭТОЙ сессии.
После scaffold: $verifyDatesCmd (при FAIL — исправить до handoff P2).
SSOT: guides/builder-artifact-dates.md
```

--- P1 appendix: UX mockup brief (spa visual/mixed story only) ---

```text
Если story затрагивает UI (Scope: BoardPage, components/, mockup, drawer, FilterPanel, SearchInput и т.п.) или ui_scope ∈ {visual, mixed}:

После materialize pipeline story + task README + pkg создай один файл рядом с pipeline story:

  @$tasksRoot/epics/<EPIC>/stories/<STORY-KEY>/STORY-UX-MOCKUP-BRIEF.md

Содержимое — готовый промпт для отдельного UX-диалога (не для разработки). Пиши от второго лица («Ты UX-специалист…»), чтобы оператор мог скопировать файл целиком в новый чат.

Структура файла (обязательно):

1) **Роль и задача** — UX/UI spec writer для spa-app; цель: mockup *-spec.md для P3 @mockup:, без кода.
2) **Контекст story** — verbatim из pipeline story: Meta, Зачем, Scope, Вне scope, UI-relevant AC (не перефразировать AC).
3) **Code facts** — таблица «зона UI | файл | что сейчас»; только проверенные пути (analysis.mdc, read/grep).
4) **Уже есть** — ссылки на существующие mockup-NN-*-spec.md, которые можно extends; viewport 1536×1024; UI routes (/#/board и т.д.).
5) **Что нарисовать / описать** — таблица screen/state | описание | must/should; минимум default + 1 interactive state; mobile — если в Scope/AC.
6) **Deliverables** — каталог `spa-app/docs/UX/mockups/<epic-folder>/`; имя `mockup-NN-<slug>-spec.md`; структура как mockup-01-dashboard-main-spec.md (layout, tokens, components, states, selectors/data-testid).
7) **Handoff** — блок copy-paste для P3:
   @mockup: spa-app/docs/UX/mockups/...
8) **Checklist DoD** — каждый UI AC покрыт; selectors для puppeteer; нет противоречий «Вне scope»; operator gate «принято» до P3.

Правила:
- Plan only: в P1 не создавать сами mockup spec PNG/файлы — только STORY-UX-MOCKUP-BRIEF.md.
- Если ui_scope: none / story без DOM — appendix skip, файл не создавать.
- В конце P1 отчёта: путь к brief + «следующий шаг: отдельный UX-чат по STORY-UX-MOCKUP-BRIEF.md → затем P2/P3».
```



### P2 — Build window (`$buildWindowFile`)

Из **корня workspace** `DOGEstonia/` (не из `GPT UI/` или `doge-complaints-gateway/` — иначе Python не найдёт скрипт). После P1, когда `*-active-package.current.yaml` указывает на нужный `pkg-*.yaml`:

1. `$verifyCmd` — при `FAIL` стоп.
2. Сгенерировать окно (ровно **один** режим из таблицы):


| `$builderProject` | Команда (подставьте `$storyKey` / диапазон по `--list`)                                                                                                                                                                                                                                                    |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gateway`         | `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --write-build-window --window-flat-start 1 --window-flat-end 5``--write-build-window --story-key $storyKey` **или** `--window-flat-start 1 --window-flat-end K`                                           |
| `gpt`             | `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gpt --write-build-window --window-flat-start 1 --window-flat-end 5` (или `--gim-slice GIM-102,GIM-103` для среза по GIM)                                                                                            |
| `identity`        | `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --window-flat-start 1 --window-flat-end K``--write-build-window --story-key STORY-IDS-01-02` **или** `--window-flat-start 1 --window-flat-end K` (в зависимости от active pkg и выбранного `input_mode`) |
| `spa`             | `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project spa --write-build-window --window-flat-start 1 --window-flat-end K` (`K` из `--list`; `task_list_linear` после P1.3)                                                                                                |
| `scripts`         | `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project scripts --write-build-window --window-flat-start 1 --window-flat-end K``--write-build-window --story-key $storyKey`                                                                                               |


1. В stdout после `ok build-window`: `**build_window_abs:`** / `**vscode_file_uri:`** — открыть из терминала (Cmd+click); `**quick_open_basename:`** или `**quick_open_pointer:`** (`latest-cursor-build-window.md` в `*-active-packages/`) — для **Cmd+P**; `**cursor_attach:`** — для P3. Symlink обновляется при каждой генерации. **Не** вставлять путь в Go-to-File целиком — `GPT UI/…` обрезается до `UI/docs/…`.
2. Опционально: `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project $builderProject --list` — сверить номера README с окном.

Детали флагов: `[queue-manual.md](../cli/queue-manual.md)` §2–3.

```text
@.cursor/skills/builder-session/SKILL.md
@.cursor/rules/builder-operator-habits.mdc

P2 Build window only. builder_project: $builderProject.
В терминале из корня workspace: $verifyCmd; затем команда --write-build-window (см. workflow P2).
Зафиксируй $buildWindowFile из stdout (`build_window_file:` или `cursor_attach:`). Без execution тасков.
```



### P3 — Execute

```text
@.cursor/skills/builder-session/SKILL.md
@.cursor/rules/builder-operator-habits.mdc

P3 Execute. builder_project: $builderProject. @$planFile + @$buildWindowFile
Ref: input_mode=requirement -> @$requirementDoc; input_mode=epic_story -> @$epicFile / @$storyFile; input_mode=backlog_story -> @$storyFile
По skill/rule: шаг 0 — $verifyCmd из корня workspace; при FAIL — стоп. Загрузить @$executionSkillPath перед code changes (task README `Skill declared` overrides profile). Очередь YAML default (immutable pkg не переписывать). Все README из окна по порядку; bullrun-start + run-task; полные артефакты тасков. Claims из кода, не из памяти чата.

P3 appendix (dates): gate/run-summary `Date:` — только post live-run; `$verifyDatesCmd` перед story Done.
```



### P3 — Execute (spa UI appendix)

Только `builder_project: spa` — для pkg с visual/mixed tasks: copy-paste блок ниже **вместо** базового P3. Build window для spa **автоматически** вставляет этот блок (см. `builder_resolve_queue.py --write-build-window`). Детали — `$uiVisualPipelineDoc`; hard gates — `$uiPipelineDoc`.

```text
@.cursor/skills/builder-session/SKILL.md
@.cursor/rules/builder-operator-habits.mdc
@.cursor/rules/analysis.mdc

P3 Execute. builder_project: spa. @$planFile + @$buildWindowFile
Ref: input_mode=requirement -> @$requirementDoc; input_mode=epic_story -> @$epicFile / @$storyFile; input_mode=backlog_story -> @$storyFile
По skill/rule: шаг 0 — $verifyCmd из корня workspace; при FAIL — стоп.
Шаг 0b (spa visual pkg, после verify):
  cd spa-app && npx puppeteer browsers install chrome   # если test:ui: Could not find Chrome
  cd spa-app && npm run <puppeteer_gate-from-anchor-task>   # напр. test:ui:filters
Стоп при FAIL шага 0b — до UI-2 implement visual tasks. Chrome: spa-app/docs/runtime-docs/frontend-run-and-environment.md §8.
Загрузить @$executionSkillPath перед code changes (task README `Skill declared` overrides profile). Очередь YAML default (immutable pkg не переписывать). Все README из окна по порядку; bullrun-start + run-task; полные артефакты тасков. Claims из кода, не из памяти чата.

--- UI Visual Pipeline (spa; story-anchor model) ---
ui_gate: auto
@mockup: spa-app/docs/UX/mockups/mockup-01-dashboard-main-spec.md
@mockup: spa-app/docs/UX/mockups/mockup-10-dashboard-filter-status-spec.md
@mockup: spa-app/docs/UX/mockups/mockup-13-dashboard-filter-reset-spec.md

Правила ui_gate:
- auto (default) — pipeline по ui_scope/ui_complexity в task README, ui_anchor, или эвристике Scope
- off — skip UI pipeline (doc-only / ui_scope: none)

Story-anchor (один на story wave):
- Anchor task (ui_anchor: true или первый ui_scope: visual) — полный UI-0..UI-1 в task-folder
- Dependent visual tasks — extends ui-mockup: <anchor>/ui-mockup-spec.md; UI-0 skip; UI-3 partial при смене DOM
- Story gate — acceptance-verification §UI + anchor ui-baseline/post-implement/*.png

Anchor task (до UI-2 implement):
UI-0 Baseline (MCP primary): npm run dev (spa-app :4173) → MCP user-puppeteer navigate + screenshot → ui-baseline/ (1536x1024); ui-baseline/README.md
UI-1 Target mockup: @mockup → ui-mockup-spec.md; иначе AskQuestion → ui-mockup-spec.md от baseline → STOP human gate (принято/исправить)
UI-2 Implement: run-task + react-expert (после gate)
UI-3 Verify: npm test + npm run <puppeteer_gate> (обязательно) + post-implement PNG; acceptance-verification §UI

STOP (hard):
- Story Done запрещён без story-gate acceptance §UI + post-implement PNG (anchor)
- UI-2 запрещён без human gate на ui-mockup-spec.md (Path B) или @mockup refs (Path A)
- Retroactive exception — только retroactive_closure в ui-baseline/README.md + operator sign-off / run_mode=spa_*_ui_audit_*; не default path

SSOT: @$uiVisualPipelineDoc; @$uiPipelineDoc

--- UI screenshots delivery (mandatory) ---
ui_screenshot_root: <anchor-task-folder>/ui-baseline/
ui_screenshot_states: all M123 states A|B|C|D (или перечислить из ui-mockup-spec)
viewport: 1536x1024

Правила capture:
1. UI-0 (ДО UI-2): ui-baseline/pre-implement/<state>-<slug>-1536x1024.png + ui-baseline/README.md (route, selectors, utc)
2. UI-3 (ПОСЛЕ implement): ui-baseline/post-implement/<state>-<slug>-1536x1024.png для КАЖДОГО state
3. Сохранять ТОЛЬКО в папку anchor task story (не /tmp, не tests/output)
4. Имена: kebab-case, префикс state (not-supported, form, joined, error)
5. Способ: node script в spa-app/tests/puppeteer/ ИЛИ MCP user-puppeteer — но output path = ui_screenshot_root

Hard deliverable в конце P3 (обязательный блок ответа):

## UI Screenshots
| State | Phase | File |
|-------|-------|------|
| A | post-implement | @spa-app/docs/tasks/.../ui-baseline/post-implement/not-supported-....png |
| B | post-implement | @spa-app/docs/tasks/.../ui-baseline/post-implement/form-....png |
| ... | ... | ... |

+ ссылка на ui-mockup-spec.md и acceptance §UI
STOP story Done если post-implement PNG для anchor state A отсутствует на диске (ls verify).
```

Примечания (не в copy-paste): `@mockup:` — 0..N строк; без них — UI-1 Path B (interview). Doc-only pkg: `ui_gate: off`. Build window должен содержать этот блок (CLI auto-inject). Dry-run: SEARCH-03 P3.

### P4 — Claude external (cross-audit)

Оператор вставляет в **Claude.ai / Claude Code** (не второй Cursor-чат):

```text
проведи жесткий аудит по фактическому коду отностельно исполнения $стори или req

и актуализируй каждый таск и стори в отчете

выбрать из:
doge-complaints-gateway/docs/tasks/bullrun-launch-index.md
doge-identity-service/docs/tasks/bullrun-launch-index.md
spa-app/docs/tasks/bullrun-launch-index.md
GPT UI/docs/analysis/tasks/bullrun-launch-index.md
scripts/docs/tasks/bullrun-launch-index.md

мышление @.cursor/rules/analysis.mdc  

Правила: только проверяемые claims с путями; регрессии; gaps с severity + как закрыть.
Не предлагай реализацию — только findings.

по итогу отчет в анализ зоне текущего проекта (*/docs/analysis)
```

Перед **P5**: если нужен двойной аудит — выполнить P4b до scaffold.

Если gaps точечные и небольшие — оформить в project-specific builder plan подраздел
`Явно прописанный safe-override (<wave>)` (по образцу GPT), где:

- override включается только по явной метке `run_mode=...`;
- default остаётся YAML SSOT;
- список путей в override — нумерованный и проверяемый, без выдумывания.



### P5 — Plan: Gap scaffold only

```text
@.cursor/skills/builder-session/SKILL.md
@.cursor/rules/builder-operator-habits.mdc
@.cursor/rules/analysis.mdc
$planFile=

P5 Plan mode — scaffold only. builder_project: $builderProject. @$auditReport (гапы временной рабочей документации (не runtime, perssistent) игнорируй)
По skill/rule: не выполняй код и pytest; не закрывай gap implementation. Gap → task-папки (@docs/methodology/task-standard.md), @$tasksRoot/bullrun-launch-index.md; YAML остаётся режимом по умолчанию для P3.

Порог P5 (override в `$planFile` vs новый pkg):
- safe-override в plan: gaps ≤ 3, README paths ≤ 5, 0 новых story folders, тот же эпик (post-audit).
- иначе: scaffold task-папок + черновик pkg + `activation: none`; отдельная P1 для обновления current.yaml.

Если порог override: добавь/обнови в `$planFile` подраздел `Явно прописанный safe-override (<wave>)` с:
1) `run_mode=<wave_name>`,
2) нумерованным списком `README.md` (каждый path — exists на диске),
3) правилом: при `run_mode` исполняется **только** этот список, без смены active pkg.
P5 checklist: уникальный run_mode; нет мёртвых run_mode без секции; gap-таблица; `activation: run_mode=…` или `activation: none`.
P5 appendix (dates): новые gap-task gates — те же правила дат (§P1 appendix artifact dates); $printUtcNowCmd после live verify.
В конце: таблица `gap -> task -> файлы -> status`. Claims с путями к файлам.
```



### P6 — Builder после P5

**Не** нажимать **Build / Execute plan** на `$planFile` — Cursor откроет «домашний» чат из локального registry ([fixed-builder-plan-execution.md](../guides/fixed-builder-plan-execution.md)). Copy-paste промпт ниже в **текущий** project-чат (`builder_project` уже задан в Phase 0).

Перед запуском (оператор): в `$planFile` оставить только актуальный §«Явно прописанный safe-override»; убрать устаревшие волны.

#### P6 — Execute (safe-override, `run_mode=<wave_name>`)

Когда после P5 в плане есть §safe-override с нумерованным списком `README.md` — **источник очереди только этот список**; build window из YAML не обязателен; **не** менять `*-active-package.current.yaml`.

```text
@.cursor/skills/builder-session/SKILL.md
@.cursor/rules/builder-operator-habits.mdc
@.cursor/rules/analysis.mdc

run_mode=<wave_name>
builder_project: $builderProject
@$planFile
@<first-readme-from-plan-safe-override-list>

P6 Execute — gap closure only; immutable active pkg unchanged (см. §safe-override в @$planFile).
По skill/rule: шаг 0 — $verifyCmd из корня workspace (контроль default pkg, не смена current); при FAIL — стоп.
Загрузить @$executionSkillPath перед code changes (task README `Skill declared` overrides profile).
Исполнять **только** numbered list из §safe-override @$planFile — **строго по порядку** в плане (не по frontmatter todos).
После **каждого** закрытого gap-task: sync @$tasksRoot/bullrun-launch-index.md + backlog INDEX при наличии; bullrun-start + run-task; acceptance-verification-*.md.
Claims из кода, не из памяти чата. Не редактировать @$planFile без явной команды оператора.

P6 appendix (dates): gate/run-summary `Date:` — только post live-run; $verifyDatesCmd перед закрытием story/gap wave.
```

**Подстановка оператором:**

| Поле | Откуда |
|------|--------|
| `<wave_name>` | Метка из §safe-override, напр. `capy01_audit_followup` |
| `<first-readme-from-plan-safe-override-list>` | **Первый** path из нумерованного списка §safe-override (порядок P6 — как в плане, напр. t08 → t09 → t07) |
| Следующие таски | Новое сообщение с `@<next-readme>` или чекпоинт «следующий в очереди: …/README.md» |

**Пример (scripts, CAPY-01 audit):**

```text
run_mode=capy01_audit_followup
builder_project: scripts
@.cursor/plans/Scripts_builder.plan.md
@scripts/docs/tasks/epics/EPIC-SCR-01-capybara/stories/STORY-SCR-CAPY-01-sweep-balance-to-parent/task-scr-capybara-t08-audit-l2-zero-amount-distinction/README.md

P6 Execute — gap closure only; pkg-000002 unchanged
```

#### P6 — Execute (без `run_mode`, YAML default)

Если оператор **не** задал `run_mode` в сообщении — стандартная очередь из active pkg:

1. Повторить **P2** (`$verifyCmd` + `--write-build-window` → `$buildWindowFile`).
2. Copy-paste **P3** с `@$planFile` + `@$buildWindowFile`.

### P7 — Claude: Re-audit

```text
правки по gap-листу выполнены
проведи подробный re-audit по закрытию каждого gap по фактическому коду
@.cursor/rules/analysis.mdc
```



### P8 — Commits

```text
@.cursor/skills/builder-session/SKILL.md
@.cursor/rules/builder-operator-habits.mdc
@docs/methodology/git-commit.md

Commits для scope anchor (`REQ-XX`, `EPIC/STORY` или `STORY-IDS-*` из backlog intake — по input_mode).
feat → test → docs; не коммить: docs/tasks/**, BULLRUN, acceptance-verification, run-summary без явной команды; push не делать.

```

---



## Чек-лист перед запуском

- `*-active-package.current.yaml` → нужный `pkg-*.yaml`
- `$verifyCmd` → `ok N paths`
- `$buildWindowFile` соответствует активному pkg
- Не смешаны override-run и YAML default
- В execution: `$planFile` + `$buildWindowFile`



## Анти-ошибки

- Запуск без verify → сначала `$verifyCmd`
- Окно устарело → перегенерировать `--write-build-window`
- Override как постоянный режим → вернуть YAML default
- Claims «по памяти» → analysis.mdc
- P1 на сыром черновике → сначала PA; P1 не shape intake
- PA смешан с P3 → разделить чаты (Studio PA vs Builder P1+)
- Build / Execute plan на `*_builder.plan.md` → Cursor откроет «домашний» чат из локального registry, не активный project-чат; для fixed plans — только @attach + workflow §P3/P6 ([fixed-builder-plan-execution.md](../guides/fixed-builder-plan-execution.md))



## Старт сессии

- [session-starter.md](./session-starter.md)
- [queue-manual.md](../cli/queue-manual.md)
- [input-package-spec.md](../specs/input-package-spec.md)
- [git-commit.md](../../git-commit.md)

