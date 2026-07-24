# Backlog dashboard template (per scope)

> **Канон:** один snapshot-файл на **scope of work** (сейчас `mvp`).  
> **Эталоны:** [`gateway-mvp-dashboard.md`](../../../../doge-complaints-gateway/docs/tasks/gateway-mvp-dashboard.md), [`gpt-mvp-dashboard.md`](../../../../GPT%20UI/docs/tasks/gpt-mvp-dashboard.md)  
> **Housekeeping:** [`backlog-dashboard-maintenance.md`](./backlog-dashboard-maintenance.md)  
> **Aggregate:** [`backlog-dashboard-aggregate.md`](../../../../scripts/docs/backlog-dashboard-aggregate.md)  
> **Interview decisions:** 2026-07-24 (GPT vs Gateway format)

Layer-2 snapshot для `npm run dashboard:aggregate`. Не SSOT статусов — derived recount из INDEX / REQ Status / doc-task файлов.

---

## Naming

| Элемент | Формат | Пример |
|---------|--------|--------|
| Файл | `{project}-{scopeId}-dashboard.md` | `gateway-mvp-dashboard.md` |
| Каталог | `{profile}/docs/tasks/` | `doge-complaints-gateway/docs/tasks/` |
| Шапка | `Scope-Id` + `Scope` | `mvp` / `MVP` |

**Legacy:** `*-backlog-dashboard.md` (spa, identity, scripts, capybara) допустим до rename. При создании нового scope — только `{project}-{scopeId}-dashboard.md`.

Redirect stub со старого имени (5–10 строк → ссылка на новый файл) — после миграции.

---

## Обязательные секции

Скелет (копируй и заполни; пустые секции не оставляй — omit, если не применимо):

```markdown
# {Project} · scope dashboard

> **Scope-Id:** mvp
> **Scope:** MVP
> **SSOT:** package INDEX.md · … · requirements/ (если есть)
> **Updated:** YYYY-MM-DD
> **Last change:** одна строка факта (что изменилось)

## Summary

| Metric | Value |
|--------|-------|
| Backlog packages | N |
| Active work items | N |
| Done | N |
| Todo | N |
| Deferred | N |
| **Overall progress (active)** | **P%** `████████████` |

## By package

| Package | Stories | Done | Todo | Deferred | Progress |
|---------|---------|------|------|----------|----------|
| [pkg-name](backlog-stories/pkg-name/INDEX.md) | N | N | N | N | P% `████…` |

## Remaining

| Type | Key | Title | Package/Epic | Status | Priority | Essence |
|------|-----|-------|--------------|--------|----------|---------|
| story | KEY | … | pkg / EPIC | Todo | P1 | Одна фраза: что ещё нужно сделать |

## Requirements Done

| REQ | Title | Evidence |
|-----|-------|----------|
| [REQ-N](../requirements/…) | … | Done — ссылка на epic/pkg/evidence |

## Epic rollup

| Epic | Status | Notes |
|------|--------|-------|
| EPIC-… | Done / In Progress / Todo | Краткая заметка + ссылка на epic md при необходимости |

## Roadmap → 100%

**Текущая точка:** …

| Цель | Знаменатель | Как закрыть |
|------|-------------|-------------|
| **Активные 100%** | done+todo (без deferred) | … |
| **Полные 100%** | + deferred | … |

## §Now

1. …

## §Deferred

- …

## Mermaid — completion

(вставь mermaid pie: Done / Todo по active work items)

## How to refresh

1. Recount из package INDEX / REQ Status / doc-task files (не из памяти).
2. Обновить этот файл.
3. npm run dashboard:aggregate
4. Методика: backlog-dashboard-maintenance.md · этот template
```

### Когда omit секции

| Секция | Omit если |
|--------|-----------|
| Requirements Done | В проекте нет `requirements/` / REQ work items |
| Remaining | Активный остаток пуст — оставь таблицу с одной строкой `_нет_` или заголовок + «пусто» |
| §Deploy / §Retired | Опционально; не часть канона |

**Не включать в канон:** полный разворот всех stories внутри каждого epic; длинный strikethrough build-list.

---

## Правила цифр (denominator)

| Входит в active % | Не входит |
|-------------------|-----------|
| Product stories: Done + Todo | Deferred / post-scope |
| REQ с open/done статусом в scope | Baseline SoT REQ (foundation draft, не open work) |
| Doc-tasks: Done + Todo | Superseded (denominator 0) |
| | Vacant REQ slots без файла |

**Формула progress:**

```
active_total = done + todo
pct = round(100 * done / active_total)   # если active_total = 0 → 100% или N/A
filled = round(12 * done / active_total)  # bar █/░, clamp 0…12
```

**By package:** считает **только product stories** пакета (как раньше). Unified % — только в Summary `Active work items`.

**Essence (Remaining):** одна фраза про суть работы. Ясно человеку; без канцелярита и без метафор.

**Type values:** `story` · `doc-task` · `req` · `bug` (при необходимости).

---

## Agent checklist (focus dialog)

**Полный промпт (собрать с нуля / полный recount):** [`build-scope-dashboard-prompt.md`](./build-scope-dashboard-prompt.md) · команда [`/build-scope-dashboard`](../../../../.cursor/commands/build-scope-dashboard.md). Вход: `$scope=MVP` (+ `$builderProject` из сессии).

Использовать в фокусном диалоге профиля (`gateway`, `gpt`, …), когда закрывается story / меняется REQ / появляется doc-task (короткий sync) **или** по промпту выше (полный build).

1. **Найти файл:** `{docs/tasks}/{project}-{scopeId}-dashboard.md` (`$scopeId` из `$scope`, напр. `MVP` → `mvp`).
2. **Recount только с диска:** package `INDEX.md`, root backlog INDEX, поле Status в REQ, doc-task файлы. Не угадывать Done.
3. **Обновить в одном проходе:**
   - `Updated` + `Last change`
   - Summary (Active work items, Done, Todo, Deferred, progress bar)
   - By package (affected rows)
   - Remaining (убрать закрытое; добавить новое Todo; Essence по факту постановки)
   - Requirements Done — только если закрыли REQ
   - Epic rollup compact (Status/Notes)
   - §Now / §Deferred
4. **Deferred** — в §Deferred и колонка Deferred; **не** в Remaining и **не** в active %.
5. **После правки snapshot:** `npm run dashboard:aggregate`.
6. **Запрещено:** менять статусы без path evidence ([analysis.mdc](../../../../.cursor/rules/analysis.mdc)); править embedded JSON в `backlog-dashboard.html` вручную.

### Минимальный verify

```bash
npm run dashboard:aggregate
# spot-check: accordion проекта, Overall progress (active), Remaining пуст или актуален
```
