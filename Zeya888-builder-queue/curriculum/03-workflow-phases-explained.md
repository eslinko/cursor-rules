# Модуль 3 — Фазы workflow P0–PA–P8 (для человека)

**Operative SSOT:** [`../core/workflow.md`](../core/workflow.md) §PA + §P1–P8 · полные промпты: [`../core/workflow-legacy.md`](../core/workflow-legacy.md)  
**Контекст:** [`00-guide-for-humans.md`](./00-guide-for-humans.md)

Каждая секция — *что происходит* и *роль архитектора*. Промпты для вставки — только в workflow.

**Два skill:** [`builder-session/SKILL.md`](../../../../.cursor/skills/builder-session/SKILL.md) — процесс (pkg, verify, фазы); **execution skill** — язык проекта (`python-pro`, `react-expert`, …) из [`profiles.yaml`](../specs/profiles.yaml), резолв в builder-session §Execution skill resolution. Workflow-промпты универсальны; стек не зашит в §P1–P8.

---

## P0 — Onboarding (Phase 0)

**Что происходит:** новый чат, [`session-starter.md`](../core/session-starter.md), чтение profiles/pipeline/index/pkg без изменения кода.

**Архитектор:** выбирает проект и подтверждает SSOT на диске.  
**Не делать:** execution до явной фазы.

**Operative:** модуль [`01-first-session.md`](./01-first-session.md).

---

## PA — Intake Analysis (перед P1)

**Что происходит:** сырой или неполный intake-файл (requirement, epic, backlog story) доводится до **Builder-ready** формы — метаданные, verified state, AC, стиль как у соседей в папке. Интерактивное интервью на decision points; gap-to-code при секциях verified state.

**Архитектор:** отдельный Studio-чат (Plan/Ask); фиксирует решения **в файле на диске**, не в чате.  
**Typical mistake:** смешать PA с P1 (shape + decompose в одном сообщении) или с P3 (код до canonical intake).

**Skip PA:** файл уже canonical (напр. готовый REQ-41 vs сырой REQ-42).

**Operative:** workflow §PA.1–PA.3 · human context: [`06-architect-studio-and-p1-intakes.md`](./06-architect-studio-and-p1-intakes.md).

**Не путать с P4:** P4 — audit **после** execution; PA — shaping **до** P1.

---

## P1 — Plan (три входа)

P1 **только планирует**: EPIC/STORY/tasks, pkg, index. **Предпосылка:** intake прошёл PA или уже canonical. P1 не проводит интервью черновика.

**Handoff после Studio (PA):** decision tree — [`06-architect-studio-and-p1-intakes.md`](./06-architect-studio-and-p1-intakes.md).

### P1.1 — `input_mode=epic_story`

**Что происходит:** вход — файл эпика. Stories и AC берутся **только из текста эпика**, не придумываются. Для каждой story — task-папки по [`task-standard.md`](../../task-standard.md). Создаётся immutable pkg с `epic_file` и `story_groups`. Обновляется bullrun index.

**Архитектор:** guardrails scope — что в эпике, то и в backlog execution.  
**Typical mistake:** новые stories «от себя» вне эпика.

**Operative:** workflow §P1.1.

### P1.2 — `input_mode=requirement`

**Что происходит:** вход — **canonical** REQ-файл (после PA.2, если был черновик). Найти существующий эпик → stories → tasks → pkg.

**Архитектор:** перед P1.2 при сыром REQ — **PA.2** в Studio; reuse эпиков в P1.  
**Typical mistake:** P1.2 на сыром REQ-42 без PA; новый EPIC-M2-99 на каждый REQ.

**Operative:** workflow §P1.2.

### P1.3 — `input_mode=backlog_story` (типично identity или spa)

**Что происходит:** вход — story из `backlog-stories/`. Materialize epic (если нет), pipeline story, deep task decomposition, pkg `epic_story_tree`, sync index. Backlog-файл не удаляется. Epic/task naming — operator contract §6.

**Архитектор:** intake одной story без полного epic-decompose всего домена.  
**Typical mistake:** смешать с P1.1/P1.2 в одной волне без команды; `python-pro` в spa (нужен `react-expert` из profile).

**Operative:** workflow §P1.3 · [`identity-operator-contract.md`](../contracts/identity-operator-contract.md) §6 · [`spa-operator-contract.md`](../contracts/spa-operator-contract.md) §6.

---

## P2 — Build window

**Что происходит:** из корня workspace — `$verifyCmd`, затем **один** режим `--write-build-window` (story-key, flat, gim-slice). В stdout — `$buildWindowFile`, `cursor_attach:`.

**Архитектор:** выбирает **границу** одной сессии.  
**Не делать:** править окно как SSOT; execution в том же сообщении.

**Operative:** workflow §P2, модуль [`02-first-package-and-window.md`](./02-first-package-and-window.md).

---

## P3 — Execute

**Что происходит:** attach `@$planFile` (`.cursor/plans/*_builder.plan.md`) + `@$buildWindowFile`. Шаг 0 verify. Очередь — YAML default (immutable pkg). README из окна по порядку; bullrun-start + run-task.

**Архитектор:** контролирует verify и scope окна; не переписывает очередь в чате.  
**Typical mistake:** «следующий таск» из памяти, не из `--list`/pkg.

**Operative:** workflow §P3, operator contracts per project.

---

## P4 / P4b — External audit

**Что происходит:** оператор вставляет промпт в **Claude.ai / Claude Code** (не второй Cursor execution). Жёсткий audit по **фактическому коду** vs story/REQ. Findings с paths; без implementation. Отчёт в `{project}/docs/analysis/`.

**Архитектор:** интерпретирует severity, решает P5 vs точечный override.  
**Не делать:** fix gaps в том же audit-промпте.

**P4b:** второй проход audit до P5, если нужен двойной контроль (workflow §P4).

**Operative:** workflow §P4.

---

## P5 — Gap scaffold only

**Что происходит:** по audit report — triage disposition + scaffold только для **TASKED**. **Без кода и pytest.**

**Disposition (workflow §P5):** каждый gap → `CLOSED` | `TASKED` | `WAIVED reason=…`. Working-doc / Info-out-of-DoD → `WAIVED`, не silent ignore. У каждого WAIVED — `follow_up` (`none` | `TASKED-later` | `new_story→PA.3` | `doc-task` | `deferred-INDEX`). AskQuestion только при кандидате в новый скоуп (out-of-DoD / operator / кластер).

**Порог (workflow §P5)** — только TASKED:
- TASKED ≤3, ≤5 README paths, тот же эпик → safe-override `run_mode=…` в plan;
- иначе → scaffold + черновик pkg, `activation: none`, отдельная P1 для current.yaml;
- TASKED = 0 → `activation: none` + disposition table + bullrun note.

**Архитектор:** проектирует gap closure wave, не пишет fix.  
**Typical mistake:** «закрой gaps кодом» в P5; «игнорируй» без строки WAIVED; WAIVED без `follow_up`.

**Operative:** workflow §P5.

---

## P6 — Execute после P5

**Что происходит:** если задан `run_mode` — исполняется **только** numbered list из plan safe-override (build window из YAML не обязателен). Иначе — повтор P2 (verify + window) + P3 по YAML.

**Архитектор:** явно включает override или возвращает YAML default после wave.  
**Typical mistake:** оставить override навсегда вместо pkg.

**Operative:** workflow §P6.

---

## P7 — Re-audit

**Что происходит:** external re-audit по disposition table из P5. `WAIVED` не требует правок; wave complete = 0 OPEN и 0 incomplete TASKED. Stop-rule `WAVE_STALLED_NO_DELTA` при пустом delta vs pass N−1. На stalled: обязательный AskQuestion, если `follow_up` пустой/неясен; иначе принять map из P5 без повторного interview.

**Архитектор:** gate перед P8; не крутить P5→P7 на Low/Info WAIVED без delta.  
**Typical mistake:** считать «правки не подтверждены» fail wave, когда actionable set был пуст / все WAIVED; уйти со stalled без follow_up.  
Product Story Done ≠ empty OPEN gap-list.

**Operative:** workflow §P7.

---

## P8 — Commits

**Что происходит:** commits по scope anchor (REQ / STORY / EPIC). feat → test → docs. По умолчанию **не** коммитить `docs/tasks/**`, BULLRUN, acceptance-verification, run-summary. Push только по запросу.

**Архитектор:** git hygiene и граница «код vs task docs».

**Operative:** workflow §P8, [`git-commit.md`](../../git-commit.md).

---

## Wave checkpoint (между stories)

**Что происходит:** короткое сообщение с `@skill`, `@rule`, active pkg, build window, явной фазой и `$verifyCmd` — сброс контекста прошлой story без потери SSOT.

**Operative:** workflow §«Wave checkpoint».

---

## Карта «когда какую фазу»

| Ситуация | Фаза |
|----------|------|
| Новый чат, первый раз в проекте | P0 |
| Новый эпик / REQ / backlog story | P1 |
| Есть pkg, нужно окно для Cursor | P2 |
| Окно готово, писать код | P3 |
| Story закрыта, нужен взгляд со стороны | P4 |
| Есть gaps, нужны task-и, не код | P5 |
| Gaps описаны, чинить | P6 |
| Проверить fixes | P7 |
| Волна принята | P8 |

## Дальше

[`04-cli-and-contracts-explained.md`](./04-cli-and-contracts-explained.md)
