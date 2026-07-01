# STORY-UX-MOCKUP-BRIEF — <STORY-KEY>

> **Назначение:** вход для **отдельного UX-диалога** (до P3 Execute с UI). Агент-UX пишет mockup spec-файлы; оператор переносит пути в P3 `@mockup:`.
> **Создаётся в:** P1.3 (Plan) при materialize visual/mixed story + pkg.
> **Не путать с:** `ui-mockup-spec.md` в task-folder (UI-1, после baseline в P3).

---

## Meta

| Поле | Значение |
|------|----------|
| **Story key** | `<STORY-KEY>` |
| **Parent epic** | `<EPIC-FILE path>` |
| **Pkg** | `<pkg-NNNNNN.yaml>` |
| **Pipeline story** | `<path to STORY-*.md in epics/.../stories/>` |
| **Backlog source** | `<path to backlog-stories/STORY-*.md>` |
| **ui_scope** | `visual` \| `mixed` |
| **ui_complexity** | `standard` \| `complex` \| `trivial` |
| **UI routes** | `/#/board` [, `/#/issue/:id`, …] |
| **Viewport** | `1536×1024` (desktop канон EPIC-03) |
| **Anchor task (pkg)** | `<task-spa-*-tNN-* path>` — shell task с `ui_anchor: true` |
| **puppeteer_gate (ожидаемый)** | `test:ui:filters` \| `test:ui:board-shell` \| … |

---

## Роль агента (UX-диалог)

Ты **UX/UI специалист** для spa-app. Твоя задача — **не писать код**, а подготовить **target mockup specifications** для последующей реализации в Builder Queue P3 (UI Visual Pipeline).

**Принципы:**

- Опирайся только на факты из этого brief, pipeline story и перечисленных code/mockup refs (**analysis.mdc**).
- Каждый экран/state — отдельный `mockup-NN-<slug>-spec.md` (или delta-spec, если extends глобальный mockup).
- Структура spec — как эталон [mockup-01-dashboard-main-spec.md](../../../../spa-app/docs/UX/mockups/initiation/mockup-01-dashboard-main-spec.md): layout-метрики, токены, компоненты, states, selectors для puppeteer.
- Если зона UI уже покрыта глобальным mockup — укажи **extends** и опиши только **дельту** story.

---

## Контекст story (verbatim из pipeline)

### Зачем (1–3 предложения)

<из pipeline story>

### Scope — что меняется в UI

<bullet list из Scope; каждый пункт с путём к файлу кода, если есть>

### Вне scope

<из pipeline story>

### Acceptance Criteria (UI-relevant)

<чеклист AC, влияющих на визуал / интеракции>

### Решения / decision refs

<ссылки на analysis, CTO interview, D-S* — если есть>

---

## Что уже есть (не выдумывать заново)

### Глобальные mockup SSOT (extends кандидаты)

| Mockup | Путь | Что покрывает |
|--------|------|---------------|
| mockup-01 | `spa-app/docs/UX/mockups/initiation/mockup-01-dashboard-main-spec.md` | Board shell, toolbar, kanban |
| … | … | … |

### Текущая реализация (code facts)

| Компонент / зона | Файл | Что сейчас на экране |
|------------------|------|----------------------|
| … | `spa-app/src/...` | … |

### Зависимости от других story

<напр. SEARCH-03 зависит от SEARCH-02 panel shell — размещение SearchInput>

---

## Задание UX-диалога (deliverables)

Создай **N** mockup spec-файла(ов) в каталоге:

`spa-app/docs/UX/mockups/<epic-folder>/`

(или `spa-app/docs/UX/mockups/initiation/` если story продолжает EPIC-03 board)

### Обязательные экраны / states

| # | Screen / state | Описание | Приоритет |
|---|----------------|----------|-----------|
| 1 | Default | … | must |
| 2 | … expanded / open | … | must |
| 3 | Empty / no results | … | should |
| 4 | Mobile / narrow | … | if D-S7 or Scope |
| 5 | Error / loading | … | if AC требует |

### На каждый spec-файл

- **Имя:** `mockup-NN-<slug>-spec.md` (следующий свободный NN в эпике).
- **Секции:** что фиксирует; layout-метрики; токены; компонентный состав; states; **selectors** (`data-testid` / role / aria для puppeteer); связь с AC.
- **Extends:** если дельта — явная ссылка на базовый mockup-NN.
- **Не включать:** implementation notes, JSX, API-контракты gateway.

### Вопросы оператору (если блокер)

Задай **1–2 раунда** AskQuestion только если Scope не покрывает: placement, mobile behavior, empty states, copy/i18n placeholders.

---

## Handoff → P3 Execute (spa UI appendix)

После UX-диалога оператор фиксирует пути в P3:

```text
@mockup: spa-app/docs/UX/mockups/<folder>/mockup-NN-....md
```

И в anchor task README (materialize / update):

```markdown
- **extends mockup:** mockup-NN-<slug>-spec.md [, …]
```

**Gate:** P3 visual implement **не стартовать**, пока оператор не подтвердил mockup specs («принято») или не приложил `@mockup:` в P3.

---

## Checklist UX-диалога (Definition of Done)

- [ ] Каждый UI-relevant AC покрыт хотя бы одним state в spec(s)
- [ ] Layout-метрики и viewport согласованы с EPIC-03 (`1536×1024`)
- [ ] Selectors перечислены для будущего `puppeteer_gate`
- [ ] Нет противоречий с «Вне scope» pipeline story
- [ ] Пути к созданным spec-файлам перечислены в §Handoff ниже

### Созданные файлы (заполнить по итогу UX-диалога)

| Файл | Покрывает |
|------|-----------|
| | |
