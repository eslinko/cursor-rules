# Модуль 3 — Фазы workflow P0–P8 (для человека)

**Operative SSOT:** [`../core/workflow.md`](../core/workflow.md) · полные промпты: [`../core/workflow-legacy.md`](../core/workflow-legacy.md)  
**Контекст:** [`00-guide-for-humans.md`](./00-guide-for-humans.md)

Каждая секция — *что происходит* и *роль архитектора*. Промпты для вставки — только в workflow.

---

## P0 — Onboarding (Phase 0)

**Что происходит:** новый чат, [`session-starter.md`](../core/session-starter.md), чтение profiles/pipeline/index/pkg без изменения кода.

**Архитектор:** выбирает проект и подтверждает SSOT на диске.  
**Не делать:** execution до явной фазы.

**Operative:** модуль [`01-first-session.md`](./01-first-session.md).

---

## P1 — Plan (три входа)

P1 **только планирует**: EPIC/STORY/tasks, pkg, index. Без pytest, без merge в main.

**Как выбрать intake после Architect Studio:** decision tree и handoff — [`06-architect-studio-and-p1-intakes.md`](./06-architect-studio-and-p1-intakes.md).

### P1.1 — `input_mode=epic_story`

**Что происходит:** вход — файл эпика. Stories и AC берутся **только из текста эпика**, не придумываются. Для каждой story — task-папки по [`task-standard.md`](../../task-standard.md). Создаётся immutable pkg с `epic_file` и `story_groups`. Обновляется bullrun index.

**Архитектор:** guardrails scope — что в эпике, то и в backlog execution.  
**Typical mistake:** новые stories «от себя» вне эпика.

**Operative:** workflow §P1.1.

### P1.2 — `input_mode=requirement`

**Что происходит:** вход — REQ-файл. Сначала **найти существующий эпик** по домену (index + `epics/`), не создавать параллельный дубль. Requirement → story(ies) внутри эпика → tasks → pkg.

**Архитектор:** reuse эпиков — системная целостность домена.  
**Typical mistake:** новый EPIC-M2-99 на каждый REQ.

**Operative:** workflow §P1.2.

### P1.3 — `input_mode=backlog_story` (типично identity)

**Что происходит:** вход — story из `backlog-stories/`. Materialize epic (если нет), pipeline story, deep task decomposition, pkg `epic_story_tree`, sync index. Backlog-файл не удаляется.

**Архитектор:** intake одной story без полного epic-decompose всего домена.  
**Typical mistake:** смешать с P1.1/P1.2 в одной волне без команды.

**Operative:** workflow §P1.3, [`identity-operator-contract.md`](../contracts/identity-operator-contract.md) §4.

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

**Что происходит:** по audit report — **только** scaffold gap tasks, index, опционально safe-override в plan. **Без кода и pytest.**

**Порог (workflow §P5):**
- мало gaps (≤3, ≤5 README paths, тот же эпик) → safe-override `run_mode=…` в plan;
- иначе → scaffold + черновик pkg, `activation: none`, отдельная P1 для current.yaml.

**Архитектор:** проектирует gap closure wave, не пишет fix.  
**Typical mistake:** «закрой gaps кодом» в P5.

**Operative:** workflow §P5.

---

## P6 — Execute после P5

**Что происходит:** если задан `run_mode` — исполняется **только** numbered list из plan safe-override (build window из YAML не обязателен). Иначе — повтор P2 (verify + window) + P3 по YAML.

**Архитектор:** явно включает override или возвращает YAML default после wave.  
**Typical mistake:** оставить override навсегда вместо pkg.

**Operative:** workflow §P6.

---

## P7 — Re-audit

**Что происходит:** external re-audit — каждый gap из P5 проверен по коду на закрытие.

**Архитектор:** gate перед P8; решает, нужна ли ещё волна.

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
