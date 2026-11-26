### Task 4 — Make run mode public, document it in the README and drive it end to end as a caller

**Goal:** Make run mode something a host can reach and read about. Export `start_run`, `continue_run` and `RunExit` from `graphscene`. Rewrite `graphscene/README.md`'s sentences and rows that the story index's `## Scope register` assigns to this task. Prove, as a caller importing only from `graphscene`, that the committed graph `valid_generic.json` walks end to end over a real `FileStateStore`.

**Depends on:**
- Task 1: `RunExit: TypeAlias = End | Stop | Interrupt | Halt | Refused`, defined in `graphscene.model.run_control`, and `ExecutionLimits.max_concurrent_dispatches: int = 10`.
- Task 3: `start_run(walker, executor, *, signals, counter, sink, limits, failure_outcome, undelivered_limit=3, entry=None, resume=None) -> RunExit` and `continue_run(walker, executor, *, signals, counter, sink, limits, failure_outcome, undelivered_limit=3, outcome=None) -> RunExit`, both defined in `graphscene.engine.run_loop`.

This task changes neither module's behaviour. It exports and documents them as they are.

### Targets

- `graphscene/src/graphscene/facade/__init__.py`: imports and `__all__`.
- `graphscene/src/graphscene/__init__.py`: imports, `__all__` and the module docstring.
- `graphscene/tests/test_public_surface.py`: `_EXPECTED` and `_DEFINED_IN`.
- `graphscene/README.md`: scope-register rows 1–4.
- `graphscene/tests/facade/test_run_mode.py` (new): run mode driven as a caller.

**Work:**

- [ ] `facade/__init__.py` and `__init__.py`: import `RunExit` from `graphscene.model.run_control`, and `start_run` and `continue_run` from `graphscene.engine.run_loop`. Append `"RunExit"`, `"start_run"`, `"continue_run"` to the **end** of both `__all__` lists, in that order, after `"execute_set"`. `__all__` is compared as a list, so this is the reviewed change (`.claude/context/graphscene.md` → `## The public surface`). In `__init__.py`'s docstring, add one sentence: run mode, `start_run` and `continue_run`, drives a walk end to end through a caller's `Executor`, applying `execute_set` set by set and returning a `RunExit`, while step mode, `Walker`, stays the synchronous route.
- [ ] `test_public_surface.py`: append the three names to `_EXPECTED` in the same order. Add `"RunExit": graphscene.model.run_control`, `"start_run": graphscene.engine.run_loop` and `"continue_run": graphscene.engine.run_loop` to `_DEFINED_IN`, importing `graphscene.engine.run_loop` beside the module's other imports.
- [ ] `graphscene/README.md`, scope-register rows 1–4 and nothing else.
  - **Row 1**, `## What it is` prose: replace *"The run loop that applies the rules is not yet built (#484)."* with a short description of the two modes. Step mode is `Walker`, synchronous, where the host runs each action. Run mode is `start_run` and `continue_run`, `asyncio`, where the engine runs each action through `execute_set`, records each result through the walker, and stops at `End`, `Stop`, `Interrupt`, `Refused` or a `Halt`, returned as a `RunExit`. Also say that at most `ExecutionLimits.max_concurrent_dispatches` runs of a set are in flight, 10 by default.
  - **Row 2**, the `src/graphscene/model/` row: add `RunExit` to `run_control.py`'s list.
  - **Row 3**, the `src/graphscene/engine/` row: add the window to the `set_execution.py` entry, and a `run_loop.py: start_run and continue_run, the run loop …` entry after it.
  - **Row 4**, the `## The layers` `engine` row: add "and the run loop".

  Every adopter-runnable command stays in its own fenced block (`harness-runs/lessons.md` → *Adopter-facing documentation*). This edit adds none.
- [ ] `tests/facade/test_run_mode.py`. The header opens with *"The rule this file exists to enforce"*, and the module imports public names from `graphscene` only. Load `valid_generic.json` through `load_graph_file`, with the path built off `__file__` as `graphscene/tests/facade/test_execution_rules.py` → `_FIXTURE` does. Keep the walk in a `FileStateStore` under `tmp_path`. Use in-test `Signals`, `Counter`, `Rows` and `DictHost`. Run with `backoff_seconds=0` through `asyncio.run`. Every expected literal is hand-written from reading `valid_generic.json` and the script. Cases:
  - `start_run` with `draft: done`, `edit_check: approved` and `stage_disabled=False` returns `End` at `published`, with `reports` `(("edit_check", "approved"),)`.
  - `draft` failing three `infra` attempts with `failure_outcome="crashed"` returns the graph's `Stop` through binding `<halt>`, reason `crash`.
  - STOP raised after `draft`'s set returns `Halt("stop", "stop requested before a set of 1")`. `continue_run` with fresh signals then finishes at `End`, reading the walk back from the same state file.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/test_public_surface.py` passes, with the three names compared in list order and each resolved to its defining module.
- `bash scripts/python-service.sh --package graphscene test tests/facade/test_run_mode.py` passes.
- Re-run the story index's `## Scope register` command entry, `git grep -l -E '#484|run loop|[Ss]tep mode|not yet built' -- '*.md' ':!harness-runs/**' ':!examples/**'`. Every file it prints is a register row. `git grep -n "#484" -- graphscene` prints nothing.
- `git diff -- graphscene/src/graphscene/facade/cli.py graphscene/src/graphscene/engine/walker.py` is empty. Step mode and the command line are unchanged.
