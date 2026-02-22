## 📅 2025-11-15 — План: усиление @run-task.mdc (one‑pass + прозрачные логи)

### 🧭 Контекст
- Сделать @run-task.mdc “само‑документирующимся”: лог каждой фазы (Understanding → Knowledge → Acceptance → Planning → Implementation → Validation → Retrospective) прямо в диалоге.
- Выполнение “одним заходом” без пауз, кроме явных Decision Points.

### ✅ План реализации
1) Runtime Parameters (новый раздел)
   - execution_mode: one_pass (default)
   - stop_policy: decision_only (default)
   - verbosity: normal (normal|brief|debug)
   - summary_every: itemy (itemy|phase)

2) Logging Policy (новый раздел)
   - Маркеры: “[RUN-TASK] Start/Complete ItemY: <name>”
   - Формат фазы: заголовок → 1–3 bullets контекста → Outcome → Next step
   - Сворачивать длинные артефакты в ссылки/референсы

3) Decision Gate (новый раздел)
   - Триггеры: конфликт требований, опасные/необратимые действия, неясные интерфейсы
   - Выводить: Summary, Technical options (риски/стоимость), Conceptual options (продукт/процесс), My recommendation, Required input (A/B/C)
   - no_decision_required → не останавливаемся

4) Обновить описание 7 фаз
   - Для каждой: “What to log” + “Outcome” (условие перехода)

5) Инварианты честности
   - No fantasy: ссылки на код/доки или пометка assumption
   - Validation обязательна; на провале — fix или Decision Gate

6) Примеры запуска
   - “execute ItemY 'X' using @run-task.mdc with {execution_mode: one_pass, stop_policy: decision_only, verbosity: normal}”

### ⚠️ Риски
- Избыточная вербозность → управлять verbosity и summary_every
- Нежелательные паузы → stop_policy=decision_only

### 📌 Следующие шаги
- Внести правки в @run-task.mdc по пунктам 1–6.
- Протестировать на одном ItemY: логи фаз читаемы, Decision Gate отображается корректно.