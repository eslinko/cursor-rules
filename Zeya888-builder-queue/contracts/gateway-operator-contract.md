# Gateway Builder — operator contract

> **Plan (read-only unless operator asks):** [`.cursor/plans/Gateway_builder.plan.md`](../../../.cursor/plans/Gateway_builder.plan.md)  
> **Propagation:** [builder-session/SKILL.md](../../../.cursor/skills/builder-session/SKILL.md) · [builder-operator-habits.mdc](../../../.cursor/rules/builder-operator-habits.mdc) · [session-starter.md](../core/session-starter.md)

Process-reminder правила для `builder_project: gateway`. P1 промпты — только [workflow.md](../core/workflow.md); не дублировать в plan.

---

## 1. `resolve-start-from-index-and-pkg`

**Перед** batch-run, Build window или P3/P6 Execute:

1. Прочитать [`doge-complaints-gateway/docs/tasks/bullrun-launch-index.md`](../../../doge-complaints-gateway/docs/tasks/bullrun-launch-index.md) §«Актуальная точка».
2. Прочитать [`gateway-active-package.current.yaml`](../../../doge-complaints-gateway/docs/tasks/gateway-active-package.current.yaml) → `package_file`.
3. Из корня workspace:  
   `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify`  
   При `FAIL` — **стоп**.
4. Следующую story/task брать **только** из:
   - нормализованного `pkg-*.yaml` (`--list` / `--print-next`), или
   - явного override в plan (только по команде оператора).

**Запрещено:** порядок из памяти, если расходится с `--list` и индексом.

---

## 2. `story-key-build-window`

Build window для gateway — **по story-key**:

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway \
  --write-build-window --story-key STORY-M2-XX-YY
```

Окно **не SSOT** — перегенерировать после смены pkg.

---

## 3. `sync-index-after-each-story`

После закрытия story (acceptance gate / run-summary):

1. Обновить [`bullrun-launch-index.md`](../../../doge-complaints-gateway/docs/tasks/bullrun-launch-index.md) в **той же** итерации.
2. Не откладывать на конец сессии.

---

## Session checklist

```markdown
## Gateway session resolve

- verify: ok N paths (pkg-0000XX …)
- index: bullrun-launch-index §Актуальная точка
- active pkg: gateway-active-package.current.yaml → pkg-0000XX
- next work: <из --print-next или индекса>
```

---

## SSOT order (Gateway)

1. Active `gateway-active-packages/pkg-*.yaml` + `--verify`  
2. `bullrun-launch-index.md`  
3. `doge-complaints-gateway/docs/requirements/REQ-*.md`  
4. Story / task README + acceptance-verification

Pipeline: [`m2-epic-story-execution-pipeline.md`](../../../doge-complaints-gateway/docs/tasks/m2-epic-story-execution-pipeline.md).
