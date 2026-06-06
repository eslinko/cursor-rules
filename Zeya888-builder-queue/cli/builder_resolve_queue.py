#!/usr/bin/env python3
"""
Разворот operative-пакета Zeya888 Builder Queue из YAML (указатель current → pkg).

Запускать из корня workspace (каталог с docs/methodology/Zeya888-builder-queue/specs/profiles.yaml).

  python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
  python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gpt --list
  python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-M2-14-01
  python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gpt --write-build-window --window-flat-start 1 --window-flat-end 3

См. queue-manual.md в этом каталоге.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.request import pathname2url

BUILD_WINDOW_POINTER_NAME = "latest-cursor-build-window.md"


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for depth in (3, 4, 5, 6, 7):
        if depth - 1 >= len(here.parents):
            continue
        cand = here.parents[depth - 1]
        if (cand / "docs" / "methodology" / "Zeya888-builder-queue" / "specs" / "profiles.yaml").is_file():
            return cand
    raise SystemExit(
        "Не найден корень workspace (ожидается docs/methodology/Zeya888-builder-queue/specs/profiles.yaml). "
        "Запускайте скрипт из workspace с установленной методологией Zeya888 Builder Queue."
    )


def _parse_simple_yaml_mapping(text: str) -> dict[str, Any]:
    """Минимальный разбор вложенного mapping для profiles.yaml (stdlib only)."""
    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]
    key_re = re.compile(r"^(\s*)([\w-]+):\s*(.*)$")

    for raw in text.splitlines():
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        m = key_re.match(raw)
        if not m:
            continue
        indent = len(m.group(1))
        key = m.group(2)
        rest = m.group(3).strip()

        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()

        parent = stack[-1][1]

        if rest == "":
            child: dict[str, Any] = {}
            parent[key] = child
            stack.append((indent, child))
            continue

        if rest in ("true", "false"):
            parent[key] = rest == "true"
        elif rest.isdigit():
            parent[key] = int(rest)
        else:
            parent[key] = rest.strip("'\"")

    return root


def _load_profiles(root: Path) -> dict[str, dict[str, Any]]:
    path = root / "docs" / "methodology" / "Zeya888-builder-queue" / "specs" / "profiles.yaml"
    data = _parse_simple_yaml_mapping(path.read_text(encoding="utf-8"))
    projects = data.get("projects")
    if not isinstance(projects, dict):
        raise SystemExit(f"Некорректный {path}: ожидается projects:")
    return projects


@dataclass(frozen=True)
class ProjectProfile:
    key: str
    enabled: bool
    tasks_dir: Path
    tasks_dir_rel: str
    active_packages_dir: Path
    current_pointer: Path
    build_windows_dir: Path
    build_window_prefix: str
    next_readme_path: Path
    pkg_path_prefix: str
    pipeline_doc: Path
    input_package_yaml_key: str
    artifact_kind: str
    build_window_title: str
    default_input_kind: str

    @classmethod
    def from_registry(cls, root: Path, key: str, raw: dict[str, Any]) -> ProjectProfile:
        if not raw.get("enabled", True):
            raise SystemExit(
                f"Профиль '{key}' отключён (enabled: false). "
                "Добавьте spa-active-packages и включите профиль в profiles.yaml."
            )
        tasks_rel = str(raw["tasks_dir"]).replace("\\", "/")
        tasks_dir = root / tasks_rel
        if not tasks_dir.is_dir():
            raise SystemExit(f"Нет каталога tasks для профиля '{key}': {tasks_dir}")
        ap_rel = str(raw["active_packages_dir"])
        bw_sub = str(raw["build_windows_subdir"])
        return cls(
            key=key,
            enabled=True,
            tasks_dir=tasks_dir,
            tasks_dir_rel=tasks_rel,
            active_packages_dir=tasks_dir / ap_rel,
            current_pointer=tasks_dir / str(raw["current_pointer"]),
            build_windows_dir=tasks_dir / bw_sub,
            build_window_prefix=str(raw["build_window_prefix"]),
            next_readme_path=tasks_dir / ap_rel / str(raw["next_readme_dotfile"]),
            pkg_path_prefix=str(raw["pkg_path_prefix"]),
            pipeline_doc=root / str(raw["pipeline_doc"]),
            input_package_yaml_key=str(raw["input_package_yaml_key"]),
            artifact_kind=str(raw["artifact_kind"]),
            build_window_title=str(raw["build_window_title"]),
            default_input_kind=str(raw.get("default_input_kind", "epic_story_tree")),
        )


def _get_profile(root: Path, project_key: str) -> ProjectProfile:
    projects = _load_profiles(root)
    if project_key not in projects:
        known = ", ".join(sorted(projects))
        raise SystemExit(f"Неизвестный --project '{project_key}'. Доступны: {known}")
    return ProjectProfile.from_registry(root, project_key, projects[project_key])


def _parse_pkg_scalar(text: str, key: str) -> str | None:
    for line in text.splitlines():
        s = line.strip()
        if s.startswith(f"{key}:"):
            return s.split(":", 1)[1].strip().strip("'\"")
    return None


def _parse_linear_paths_pkg(text: str, path_prefix: str) -> list[str]:
    lines = text.splitlines()
    paths: list[str] = []
    in_linear = False
    for line in lines:
        if line.strip() == "linear_paths:":
            in_linear = True
            continue
        if not in_linear:
            continue
        if line.strip().startswith("story_groups:"):
            break
        m = re.match(r"^\s+-\s+(.+?)\s*$", line)
        if m:
            p = m.group(1).strip().strip("'\"")
            if p.startswith(path_prefix):
                paths.append(p)
        elif line.strip() and not line.startswith(" ") and not line.startswith("\t"):
            if paths:
                break
    return paths


def _parse_epic_story_tree_pkg(text: str, path_prefix: str) -> list[tuple[str, list[str]]]:
    lines = text.splitlines()
    groups: list[tuple[str, list[str]]] = []
    i = 0
    in_groups = False
    while i < len(lines):
        line = lines[i]
        if not in_groups:
            if line.strip() == "story_groups:":
                in_groups = True
            i += 1
            continue
        m = re.match(r"^-\s+story_key:\s*(.+)\s*$", line)
        if m:
            story = m.group(1).strip().strip("'\"")
            i += 1
            paths: list[str] = []
            if i < len(lines) and lines[i].strip() == "paths:":
                i += 1
                while i < len(lines):
                    pl = lines[i]
                    if re.match(r"^-\s+story_key:\s*", pl):
                        break
                    pm = re.match(r"^\s+-\s+(\S+)\s*$", pl) or re.match(
                        r"^\s+-\s+(.+?)\s*$", pl
                    )
                    if pm:
                        p = pm.group(1).strip().strip("'\"")
                        if p.startswith(path_prefix):
                            paths.append(p)
                        i += 1
                        continue
                    if pl.strip() and not pl.startswith(" ") and not pl.startswith("\t"):
                        break
                    i += 1
            groups.append((story, paths))
            continue
        i += 1
    return groups


def _flatten(groups: list[tuple[str, list[str]]]) -> list[str]:
    out: list[str] = []
    for _, ps in groups:
        out.extend(ps)
    return out


def _resolve_queue(
    text: str, profile: ProjectProfile
) -> tuple[str, list[tuple[str, list[str]]], list[str]]:
    kind = _parse_pkg_scalar(text, "input_kind") or profile.default_input_kind
    if kind == "task_list_linear":
        flat = _parse_linear_paths_pkg(text, profile.pkg_path_prefix)
        return kind, [("linear", flat)], flat
    if kind == "epic_story_tree":
        groups = _parse_epic_story_tree_pkg(text, profile.pkg_path_prefix)
        return kind, groups, _flatten(groups)
    raise SystemExit(f"Неподдерживаемый input_kind: {kind}")


def _read_package_file_pointer(profile: ProjectProfile) -> str:
    cur = profile.current_pointer
    if not cur.is_file():
        raise SystemExit(f"Нет файла указателя: {cur}")
    for line in cur.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("package_file:"):
            return s.split(":", 1)[1].strip().strip("'\"")
    raise SystemExit(f"В {cur} не найдено поле package_file:")


def _select_window_paths(
    groups: list[tuple[str, list[str]]],
    flat: list[str],
    story_key: str | None,
    story_index: int | None,
    flat_start: int | None,
    flat_end: int | None,
) -> tuple[str, str, list[str]]:
    modes = sum(
        1
        for x in (
            story_key is not None,
            story_index is not None,
            flat_start is not None,
        )
        if x
    )
    if modes != 1:
        raise SystemExit(
            "Ровно один режим окна: --story-key … ИЛИ --story-index N ИЛИ --window-flat-start A [--window-flat-end B]"
        )
    if story_key is not None:
        for sk, ps in groups:
            if sk == story_key:
                return ("story_key", sk, ps)
        raise SystemExit(f"story_key не найден в пакете: {story_key}")
    if story_index is not None:
        if story_index < 1 or story_index > len(groups):
            raise SystemExit(f"--story-index вне диапазона 1..{len(groups)}")
        sk, ps = groups[story_index - 1]
        return ("story_index", sk, ps)
    assert flat_start is not None
    if flat_start < 1 or flat_start > len(flat):
        raise SystemExit(f"--window-flat-start вне 1..{len(flat)}")
    end = flat_end if flat_end is not None else flat_start
    if end < flat_start or end > len(flat):
        raise SystemExit(f"--window-flat-end невалиден (диапазон 1..{len(flat)}, end >= start)")
    slice_paths = flat[flat_start - 1 : end]
    title = f"Плоский срез {flat_start}–{end} (как в --list)"
    return ("flat_slice", title, slice_paths)


def _suffix_for_build_window(
    w_mode: str,
    section_title: str,
    flat_start: int | None,
    flat_end: int | None,
) -> str:
    if w_mode == "gim_slice":
        return re.sub(r"[^\w.\-]+", "-", section_title).strip("-") or "gim-slice"
    if w_mode in ("story_key", "story_index"):
        return re.sub(r"[^\w.\-]+", "-", section_title).strip("-") or "story"
    assert flat_start is not None
    end = flat_end if flat_end is not None else flat_start
    return f"flat-{flat_start}-{end}"


def _default_build_window_rel(
    root: Path,
    profile: ProjectProfile,
    w_mode: str,
    section_title: str,
    flat_start: int | None,
    flat_end: int | None,
) -> str:
    suffix = _suffix_for_build_window(w_mode, section_title, flat_start, flat_end)
    p = profile.build_windows_dir / f"{profile.build_window_prefix}--{suffix}.md"
    return p.relative_to(root).as_posix()


def _quote_path_if_needed(path_str: str) -> str:
    if " " in path_str or "\t" in path_str:
        return f'"{path_str}"'
    return path_str


_ARTIFACT_STDOUT_KEYS: dict[str, tuple[str, str, str]] = {
    "build_window": ("ok build-window", "build_window_file", "build_window_abs"),
    "next_readme": (
        "ok next-readme-pointer",
        "next_readme_pointer_file",
        "next_readme_pointer_abs",
    ),
}


def _path_to_file_uri(path: Path) -> str:
    return "file:" + pathname2url(str(path.resolve()))


def _update_build_window_pointer(out_path: Path, profile: ProjectProfile) -> Path:
    """Стабильный symlink в *-active-packages/ — находится в Cmd+P по имени без «GPT UI» в запросе."""
    profile.active_packages_dir.mkdir(parents=True, exist_ok=True)
    pointer = profile.active_packages_dir / BUILD_WINDOW_POINTER_NAME
    rel_target = os.path.relpath(out_path, pointer.parent)
    if pointer.exists() or pointer.is_symlink():
        pointer.unlink()
    pointer.symlink_to(rel_target)
    return pointer


def _emit_artifact_stdout(
    *,
    artifact_kind: str,
    out_path: Path,
    root: Path,
    project_key: str,
    profile: ProjectProfile | None = None,
    attach_rel: str | None = None,
    extra_lines: list[tuple[str, str]] | None = None,
) -> None:
    """Печать путей в stdout: кавычки при пробелах (GPT UI), abs для Cmd+click в терминале."""
    if artifact_kind not in _ARTIFACT_STDOUT_KEYS:
        raise ValueError(f"unknown artifact_kind: {artifact_kind}")
    status, file_key, abs_key = _ARTIFACT_STDOUT_KEYS[artifact_kind]
    rel = out_path.relative_to(root).as_posix()
    abs_path = out_path.resolve().as_posix()
    print(f"{status} (project={project_key})")
    print(f"{file_key}: {_quote_path_if_needed(rel)}")
    print(f"{abs_key}: {_quote_path_if_needed(abs_path)}")
    attach = attach_rel if attach_rel is not None else rel
    print(f"cursor_attach: @{attach}")
    if artifact_kind == "build_window" and profile is not None:
        basename = out_path.name
        within_tasks = out_path.relative_to(profile.tasks_dir).as_posix()
        pointer = _update_build_window_pointer(out_path, profile)
        ptr_rel = pointer.relative_to(root).as_posix()
        ptr_in_ap = pointer.relative_to(profile.active_packages_dir).as_posix()
        print(f"quick_open_basename: {basename}")
        print(f"build_window_within_tasks: {within_tasks}")
        print(f"build_window_pointer: {_quote_path_if_needed(ptr_rel)}")
        print(f"quick_open_pointer: {ptr_in_ap}")
        print(f"vscode_file_uri: {_path_to_file_uri(out_path)}")
        if " " in rel:
            print(
                "hint_quick_open: Cmd+P → quick_open_basename или quick_open_pointer "
                "(не вставляйте путь с «GPT UI» в Go-to-File — обрезается до UI/docs/…)"
            )
    if extra_lines:
        for key, value in extra_lines:
            print(f"{key}: {_quote_path_if_needed(value)}")


def _script_rel_to_repo(root: Path) -> str:
    return Path(__file__).resolve().relative_to(root).as_posix()


def _render_build_window_md(
    *,
    profile: ProjectProfile,
    rel_pkg: str,
    window_mode: str,
    section_title: str,
    paths: list[str],
    regen_cmd: str,
    schema_version: str | None,
    pipeline_md_link: str,
) -> str:
    gen = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    pkg_key = profile.input_package_yaml_key
    lines: list[str] = [
        "---",
        f"generated_utc: {gen}",
        f"builder_project: {profile.key}",
        f"{pkg_key}: {rel_pkg}",
        f"window_mode: {window_mode}",
        f"artifact_kind: {profile.artifact_kind}",
    ]
    if schema_version is not None:
        lines.append(f"pkg_schema_version: {schema_version}")
    lines.append("---")
    lines.extend(
        [
            "",
            f"# {profile.build_window_title}",
            "",
            f"**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `{pkg_key}`. "
            "Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.",
            "",
            "```bash",
            regen_cmd,
            "```",
            "",
        ]
    )
    if profile.key == "gateway":
        lines.extend(
            [
                "После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. "
                f"[`m2-epic-story-execution-pipeline.md`]({pipeline_md_link}) (Gate: Story parent AC, Gate: Epic AC). "
                "Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                f"Исполнение: [`{profile.pipeline_doc.name}`]({pipeline_md_link}) + "
                "`@.cursor/commands/bullrun-start.md` / `run-task.md`.",
                "",
            ]
        )
    lines.extend([f"## {section_title}", ""])
    body = "\n".join(lines)
    for i, p in enumerate(paths, start=1):
        body += f"{i}. `@{p}`\n"
    body += "\n"
    return body


def main() -> None:
    ap = argparse.ArgumentParser(description="Builder Queue YAML → очередь README.md")
    ap.add_argument(
        "--project",
        required=True,
        metavar="KEY",
        help="Ключ профиля из profiles.yaml (gateway, gpt, spa, …)",
    )
    ap.add_argument("--verify", action="store_true", help="Проверить exists для каждого README")
    ap.add_argument("--list", action="store_true", help="Нумерованный список путей")
    ap.add_argument(
        "--export-active-task-path",
        action="store_true",
        help="Одна строка ACTIVE_TASK_PATH=[...] (JSON)",
    )
    ap.add_argument("--skip", type=int, default=0, metavar="N")
    ap.add_argument("--print-next", action="store_true")
    ap.add_argument("--write-next-pointer", action="store_true")
    ap.add_argument("--write-build-window", action="store_true")
    ap.add_argument("--build-window-out", metavar="PATH")
    ap.add_argument("--story-key", metavar="KEY")
    ap.add_argument("--story-index", type=int, metavar="N")
    ap.add_argument("--window-flat-start", type=int, metavar="N")
    ap.add_argument("--window-flat-end", type=int, metavar="N")
    ap.add_argument(
        "--gim-slice",
        metavar="GIM-102,GIM-103",
        help="Срез по плоской очереди (gpt): N ключей = первые N README",
    )
    args = ap.parse_args()
    if not (
        args.verify
        or args.list
        or args.export_active_task_path
        or args.print_next
        or args.write_next_pointer
        or args.write_build_window
    ):
        ap.print_help()
        sys.exit(2)

    root = _repo_root()
    profile = _get_profile(root, args.project)
    rel_pkg = _read_package_file_pointer(profile)
    pkg_path = profile.tasks_dir / rel_pkg
    if not pkg_path.is_file():
        raise SystemExit(f"Нет пакета: {pkg_path}")

    text = pkg_path.read_text(encoding="utf-8")
    _kind, groups, flat = _resolve_queue(text, profile)
    if not flat:
        raise SystemExit("Очередь README пуста (проверьте linear_paths или story_groups).")

    missing = [p for p in flat if not (root / p).is_file()]

    if args.verify:
        if missing:
            print("FAIL missing files:", file=sys.stderr)
            for p in missing:
                print(" ", p, file=sys.stderr)
            sys.exit(1)
        print(f"ok {len(flat)} paths (project={profile.key}, pkg {pkg_path.relative_to(root)})")

    if args.list:
        for n, p in enumerate(flat, start=1):
            print(f"{n:02d}\t{p}")

    if args.export_active_task_path:
        if len(groups) == 1 and groups[0][0] == "linear":
            line = "ACTIVE_TASK_PATH=" + json.dumps(groups[0][1], separators=(",", ":"))
        else:
            grouped = [{"story": sk, "paths": ps} for sk, ps in groups]
            line = "ACTIVE_TASK_PATH=" + json.dumps(grouped, separators=(",", ":"))
        print(line)

    if args.print_next or args.write_next_pointer:
        if args.skip < 0:
            raise SystemExit("--skip must be >= 0")
        if args.skip >= len(flat):
            raise SystemExit(f"--skip {args.skip} out of range (queue length {len(flat)})")
        next_path = flat[args.skip]
        if not (root / next_path).is_file():
            raise SystemExit(f"Next path missing on disk: {next_path}")
        if args.print_next:
            print(next_path)
        if args.write_next_pointer:
            profile.next_readme_path.parent.mkdir(parents=True, exist_ok=True)
            profile.next_readme_path.write_text(next_path + "\n", encoding="utf-8")
            _emit_artifact_stdout(
                artifact_kind="next_readme",
                out_path=profile.next_readme_path,
                root=root,
                project_key=profile.key,
                attach_rel=next_path,
                extra_lines=[("next_readme_path", next_path)],
            )

    if args.write_build_window:
        gim_slice = None
        if args.gim_slice:
            gim_slice = [k.strip() for k in args.gim_slice.split(",") if k.strip()]
        if args.story_key and args.story_index is not None:
            raise SystemExit("Нельзя одновременно --story-key и --story-index")
        if gim_slice and (
            args.story_key is not None
            or args.story_index is not None
            or args.window_flat_start is not None
        ):
            raise SystemExit("--gim-slice несовместим с --story-key / --story-index / --window-flat-*")
        if args.story_key and args.window_flat_start is not None:
            raise SystemExit("Нельзя одновременно --story-key и --window-flat-start")
        if args.story_index is not None and args.window_flat_start is not None:
            raise SystemExit("Нельзя одновременно --story-index и --window-flat-start")
        if (
            args.story_key is None
            and args.story_index is None
            and args.window_flat_start is None
            and gim_slice is None
        ):
            raise SystemExit(
                "С --write-build-window укажите --story-key, --story-index, "
                "--window-flat-start или --gim-slice"
            )
        if args.window_flat_end is not None and args.window_flat_start is None:
            raise SystemExit("--window-flat-end без --window-flat-start")

        if gim_slice is not None:
            win_paths = flat[: len(gim_slice)]
            w_mode, section_title = "gim_slice", f"GIM {','.join(gim_slice)}"
            flat_start, flat_end = None, None
        else:
            w_mode, section_title, win_paths = _select_window_paths(
                groups,
                flat,
                args.story_key,
                args.story_index,
                args.window_flat_start,
                args.window_flat_end,
            )
            flat_start, flat_end = args.window_flat_start, args.window_flat_end

        default_rel = _default_build_window_rel(
            root, profile, w_mode, section_title, flat_start, flat_end
        )
        out_rel = args.build_window_out or default_rel
        out_path = root / out_rel
        out_path.parent.mkdir(parents=True, exist_ok=True)
        missing_win = [p for p in win_paths if not (root / p).is_file()]
        if missing_win:
            print("FAIL build-window: missing README:", file=sys.stderr)
            for p in missing_win:
                print(" ", p, file=sys.stderr)
            raise SystemExit(1)
        rel_pkg_out = str(pkg_path.relative_to(root)).replace("\\", "/")
        script_rel = _script_rel_to_repo(root)
        regen = f"python3 {script_rel} --project {profile.key} --write-build-window"
        if out_rel != default_rel:
            regen += f" --build-window-out {out_rel}"
        if gim_slice is not None:
            regen += f" --gim-slice {args.gim_slice}"
        elif args.story_key:
            regen += f" --story-key {args.story_key}"
        elif args.story_index is not None:
            regen += f" --story-index {args.story_index}"
        else:
            regen += f" --window-flat-start {args.window_flat_start}"
            if args.window_flat_end is not None:
                regen += f" --window-flat-end {args.window_flat_end}"
        sv = _parse_pkg_scalar(text, "schema_version")
        pipeline_md_link = Path(
            os.path.relpath(str(profile.pipeline_doc), str(out_path.parent))
        ).as_posix()
        body = _render_build_window_md(
            profile=profile,
            rel_pkg=rel_pkg_out,
            window_mode=w_mode,
            section_title=section_title,
            paths=win_paths,
            regen_cmd=regen,
            schema_version=sv,
            pipeline_md_link=pipeline_md_link,
        )
        out_path.write_text(body, encoding="utf-8")
        _emit_artifact_stdout(
            artifact_kind="build_window",
            out_path=out_path,
            root=root,
            project_key=profile.key,
            profile=profile,
        )


if __name__ == "__main__":
    main()
