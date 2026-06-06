# Модуль 2 — Package и build window

## Цель

Понять связь `pkg-*.yaml` → `--verify` → `--write-build-window`.

## Шаги

1. Прочитать [`../specs/input-package-spec.md`](../specs/input-package-spec.md) §0–§4 (контракт очереди).
2. Запустить verify из корня workspace:

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```

3. При успехе — build window (пример gateway):

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway \
  --write-build-window --story-key STORY-M2-14-01
```

4. Открыть stdout: `build_window_abs:` / `cursor_attach:`.

## Проверка

- `ok N paths` — все пути pkg существуют на диске
- Build window файл создан в `run-reports/*-build-windows/`

## Ошибки

| Симптом | Действие |
|---------|----------|
| FAIL verify | Исправить пути в pkg YAML |
| story_key not found | Точное совпадение ключа в pkg |

## Дальше

P2 в [`../core/workflow.md`](../core/workflow.md), execution — `.cursor/plans/*_builder.plan.md` + build window.
