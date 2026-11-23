### Task 3 — Add the `graphscene` command line in `facade` and declare its console script

**Goal:** Add `graphscene/src/graphscene/facade/cli.py`, the thin command line over the library: `check`, `start`, `next` and `current`, with the JSON output and the exit contract the story index's `## Context` states. Declare it as the console script `graphscene` in `graphscene/pyproject.toml`.

**Depends on:** Task 1 and Task 2, which own every wire form this module prints or reads. This task calls them exactly as follows and re-encodes nothing:

- **Task 1**, `graphscene/src/graphscene/adapters/walk_json.py`:
  - `step_document(step: Step) -> dict[str, object]` returns the step document. For an action, that is the action's encoding inside the walk-state document. For a refusal, it is `{"kind": "refused", "reason": <text>}`.
  - `resume_from_json(text: str) -> RoundResume` decodes `{"round": str, "number": int, "records": [{"gate", "outcome", "detail"}]}` and raises `ValueError("<path>: <reason>")` on a malformed document.
- **Task 2**, `graphscene/src/graphscene/adapters/check_json.py`:
  - `check_document(error: GraphError | None) -> dict[str, object]` returns the check document: `{"stage": None, "violations": []}` for `None`; otherwise `{"stage": error.stage, "violations": [{"path", "check", "reason"}, …]}`, with the static check-id split already applied and `path` verbatim (`""` for the root).

`graphscene/README.md` is **Task 4's**: this task adds the module's opening docstring but not its README row or the README's command-line section.

**Where this module may reach.** `facade` may import `adapters`, `engine`, `model` and the standard library (`graphscene/README.md` → `## The layers`). Import each name from its defining module, never from the package root (`graphscene/src/graphscene/__init__.py` → *"no module inside the package imports from the package root"*):

- `load_graph_file` from `graphscene.facade.loading`;
- `Walker` from `graphscene.engine.walker`;
- `FileStateStore` from `graphscene.adapters.state_file`, `step_document` and `resume_from_json` from `graphscene.adapters.walk_json`, and `check_document` from `graphscene.adapters.check_json`;
- `GraphError` from `graphscene.model.errors`.

Use only the standard library besides (`argparse`, `json`, `pathlib`, `sys`, `typing`). Never name a `devscene`-prefixed module or the harness's configuration file (`graphscene/tests/test_boundary.py` → `scan`). `main` stays out of `__all__`, and the README marks it *"not public"* (Task 4).

### Targets

- `graphscene/src/graphscene/facade/cli.py` (new): the command line.
- `graphscene/pyproject.toml`: a `[project.scripts]` table, `graphscene = "graphscene.facade.cli:main"`.
- `graphscene/tests/facade/test_cli.py` (new): the module's own suite.

**Work:**

- [ ] `cli.py`: the opening docstring, `main`, and the `check` command.
  - **Docstring.** It opens with what the module owns, then *"The rule:"*: every command prints one ASCII-only JSON document on stdout, and the exit contract is 0 / 1 / 2 / 3 / 4 as the story index's `## Context` states. It names `graphscene.adapters.check_json` and `graphscene.adapters.walk_json` as the owners of every document it prints, and says this module encodes none itself. It ends with *"Deliberately not covered:"*:
    - `RoundResume` validity, which is `Walker.start`'s;
    - configuration, which the CLI reads none of;
    - platforms without `fcntl`, which `FileStateStore` does not cover;
    - DevScene's `key: value` wire, which is #418's.
  - **`main`.** `main(argv: Sequence[str] | None = None, *, stdout: TextIO | None = None, stderr: TextIO | None = None) -> int`. `None` streams resolve to `sys.stdout` / `sys.stderr` at call time.
    - Use an `argparse.ArgumentParser` subclass whose `_print_message` writes to the injected streams and whose `exit` / `error` raise a module-private exception instead of `SystemExit`. `main` turns usage into return value `2` with argparse's usage text on the injected stderr. `--help` goes to the injected stdout and returns `0`.
    - End the module with `if __name__ == "__main__": raise SystemExit(main())`.
  - **`check <graph>`.** Call `load_graph_file(Path(graph))`. On success print `check_document(None)` with exit `0`; on `GraphError` print `check_document(error)` with exit `1`. This module does not build the violation objects or split any reason: both are `check_document`'s (Task 2).
- [ ] `cli.py`: the walk commands. Each loads `<graph>` exactly as `check` does, and on a `GraphError` prints `check_document(error)` with exit `1` before touching `<state>`. Then it builds `Walker(graph, FileStateStore(Path(state)), host)`.
  - **`start <graph> <state> [--entry <node>] [--resume <file>] [--answer …]`** calls `walker.start(entry, resume=…)`. `--resume` is read as UTF-8 and decoded with `resume_from_json`.
  - **`next <graph> <state> --outcome <outcome> [--node <node>] [--detail <text>] [--answer …]`** calls `walker.next(outcome, node, detail)`.
  - **`current <graph> <state>`** calls `walker.current()` with a host that answers every predicate `None`. `current` arrives nowhere, so it never asks.
  - **`--answer <predicate>=true|false`** may repeat. The host is a small module-private class satisfying `PredicateHost` structurally (`graphscene/src/graphscene/model/walk_state.py` → `PredicateHost`). It answers by predicate name for every node, as `graphscene/tests/facade/test_walking.py` → `DictHost` does, and returns `None` for a predicate no flag names.
    - The value is exactly `true` or `false`.
    - Any other value, a missing `=`, an empty predicate name, or the same predicate given twice is a usage error, exit `2`.
  - **Output.** Print `step_document(step)`. Exit `3` when the step is a `Refused`, otherwise `0`.
- [ ] `cli.py`: output and environment failures.
  - Every document is written as `json.dumps(document)` with the default `ensure_ascii=True`, followed by `"\n"`, so a lone surrogate (argv bytes Python decoded with `surrogateescape`) or a non-ASCII name never raises on write.
  - Catch exactly `OSError`, `ValueError` and `TimeoutError` around reading the resume file and around the walker call. `GraphError` is a `ValueError`, so catch it first, at the load. Turn each into one stderr line `graphscene: <message>` with exit `4` and nothing on stdout. These are:
    - a missing graph, state directory or resume file;
    - `FileStateStore.read`'s *"`<state>`: …"* malformed-state `ValueError`;
    - `resume_from_json`'s `ValueError`;
    - `FileStateStore.lock`'s `TimeoutError`.
  - Anything else propagates with its traceback: it is a defect, not an anticipated failure. That mirrors the shape `.claude/context/conventions.md` → `## Output, logging and errors` gives the Python backend.
- [ ] `graphscene/pyproject.toml`: add `[project.scripts]` with `graphscene = "graphscene.facade.cli:main"`, placed after `[project]`'s `dependencies`. `[project] dependencies` is untouched, so neither `graphscene/uv.lock` nor `devscene-flow-host`'s lock moves (`.claude/context/conventions.md` → `## The layers`, the lock bullet). Do not re-lock.
- [ ] `graphscene/tests/facade/test_cli.py`.
  - **Header.** Open with *"The rule this file exists to enforce"* (`.claude/context/conventions.md` → `## The testing bar`). Say why this facade suite names `graphscene.facade.cli` rather than importing from `graphscene`: the command's Python entry is deliberately not public, and its real caller is a process. State that every expected value is hand-written from reading `valid_generic.json`, the `static_negative_*.json` / `schema_negative_*.json` fixtures and the library's refusal texts, never taken from the command's output. The check document's own cases are `graphscene/tests/adapters/test_check_json.py`'s (Task 2); this suite checks that the command prints it and exits as the contract says.
  - **Calling convention.** Cases call `main([...], stdout=io.StringIO(), stderr=io.StringIO())` and plant state files under `tmp_path`.
  - **`check`.**
    - `valid_generic.json` → exit 0, `{"stage": null, "violations": []}`.
    - One `static_negative_*.json` → exit 1, `stage` `"static"`, its one violation with `check` split off.
    - One `schema_negative_*.json` → exit 1, `check` `null`.
    - A file planted under `tmp_path` that is not JSON → stage `"parse"`, path `""`.
    - A missing file → exit 4, the `graphscene: ` stderr line and empty stdout.
  - **A walk.**
    - `start` on `valid_generic.json` → exit 0 and the `draft` dispatch.
    - `next --outcome done` without `--answer` → exit 3 and `{"kind": "refused", "reason": "the host cannot answer predicate 'stage_disabled' for node 'edit_check'"}` (`graphscene/src/graphscene/engine/transitions.py`, the `cannot answer predicate` refusal).
    - The same `next` with `--answer stage_disabled=false` → exit 0 and the round's dispatch set.
    - `current` re-prints the saved pending action.
    - After the walk, `tmp_path` holds only the state file and its `.lock` sibling.
  - **Refusals and environment failures.**
    - `--entry` of a non-entry → exit 3 with the walker's exact refusal.
    - `current` before any `start` → exit 3, `"no walk has started"`.
    - A malformed state file → exit 4.
    - A malformed `--resume` file → exit 4 naming its path.
    - A valid `--resume` into `review_round` → exit 0.
    - A walk command on a `static_negative_*.json` graph → exit 1, the check document on stdout, and no state file under `tmp_path`.
  - **Usage.**
    - `--answer stage_disabled=maybe` → exit 2.
    - A duplicate `--answer` → exit 2.
    - No sub-command → exit 2.
    - `--help` → exit 0 on stdout.
  - **ASCII output.** `start --entry` given `"\udcff"` → exit 3, and the stdout text is ASCII and carries `\\udcff`.
  - **Declaration.** Read `graphscene/pyproject.toml` (built off `__file__`) with `tomllib` and assert `[project.scripts]["graphscene"] == "graphscene.facade.cli:main"`. It reads one fixed file, so it is not a tree-reading test and owes no `treeGuards` entry.
  - **Subprocess.** Run `[sys.executable, "-m", "graphscene.facade.cli", "check", <valid_generic.json>]` with `cwd=tmp_path`. Assert exit 0 and the exact stdout line, proving the module writes to the real stdout as a process.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/facade/test_cli.py` passes.
- `cli.py` contains no `print(` without an explicit `file=` naming an injected stream, and no direct `sys.stdout` / `sys.stderr` write outside the `None`-default resolution in `main`.
- `cli.py`'s imports are the standard library plus the defining modules named in this file's "Where this module may reach", and it re-implements no wire form. Its only use of the JSON forms is calling `check_document`, `step_document` and `resume_from_json`: it builds no `"violations"` object, contains no `partition(": ")` / `split(": "` of a reason, and encodes no action.
- `graphscene/uv.lock` is unchanged in the diff.

- **Deviations from plan:**
  - `cli.py` imports four more names than the "Where this module may reach" list gives, each from its defining `model` module, which `facade` may import (`.claude/context/graphscene.md` → `## The internal layers`): `Refused` and `Step` from `graphscene.model.walk_actions` (the exit-3 test and `_walk`'s return type), `RoundResume` from `graphscene.model.walk_state` and `FlowGraph` from `graphscene.model.flow_graph` (annotations). No wire form is built from them.
  - `resume_from_json`'s `ValueError` carries a path inside the document, not the file's path. To meet "a malformed `--resume` file → exit 4 naming its path", `cli.py` prefixes it with the file path as `<file>: <error>`, the way `FileStateStore.read` prefixes the state path. A non-UTF-8 resume file (`UnicodeDecodeError`, also a `ValueError`) is reported the same way.
  - The `--help` case asserts exit 0 and usage text on stdout. Argparse's help text is not compared verbatim.
