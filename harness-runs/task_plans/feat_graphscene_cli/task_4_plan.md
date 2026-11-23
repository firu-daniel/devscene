### Task 4 — Document the `graphscene` command line in `graphscene/README.md`

**Goal:** Make `graphscene/README.md` describe what Tasks 1, 2 and 3 built:

- the README rows for the widened walk codec, the new `adapters/check_json.py` and the new `facade/cli.py`, which `.claude/context/graphscene.md` → `## What accompanies a new module` requires;
- the `facade` row of `## The layers`;
- a new `## The command line` section for a host that is not written in Python.

**Depends on:** Task 1, Task 2 and Task 3.

- **Task 1** adds two functions to `graphscene/src/graphscene/adapters/walk_json.py`. `step_document(step)` returns a `Step`'s JSON object: an action encoded as the walk-state document encodes `pending`, or `{"kind": "refused", "reason": …}`. `resume_from_json(text)` decodes `{"round", "number", "records"}` into a `RoundResume`. Neither is public.
- **Task 2** adds `graphscene/src/graphscene/adapters/check_json.py` with `check_document(error)`, which encodes a `GraphError` (or `None`) as the check document `{"stage", "violations": [{"path", "check", "reason"}]}`, `check` set only for stage `static`. It is not public.
- **Task 3** adds `graphscene/src/graphscene/facade/cli.py` with `main` (not public) and the console script `graphscene = "graphscene.facade.cli:main"` in `graphscene/pyproject.toml`. It provides the commands `check <graph>`, `start <graph> <state> [--entry] [--resume <file>] [--answer <predicate>=true|false …]`, `next <graph> <state> --outcome … [--node] [--detail] [--answer …]` and `current <graph> <state>`, and prints only documents the two `adapters` modules encode.

This task documents those as they are and changes no code. If a sentence below disagrees with the code Tasks 1–3 landed, the code wins: read `cli.py`'s docstring and the *"The rule:"* of `walk_json.py` and `check_json.py` before writing.

### Targets

- `graphscene/README.md`

**Work:**

- [ ] `## What it is`, the `src/graphscene/adapters/` row.
  - Change the `walk_json.py` entry to name all four functions: `state_to_json` and `state_from_json`, a `WalkState`'s JSON form; `step_document`, a walk step's JSON form; `resume_from_json`, the round-resume document. Keep *"not public"*.
  - Add a `check_json.py` entry: `check_document`, a `GraphError`'s JSON form, the check document the command line prints; *"not public"*, in the wording the `walk_json.py` entry uses.
- [ ] `## What it is`, the `src/graphscene/facade/` row. Add `cli.py`: `main`, the `graphscene` command line (`check`, `start`, `next`, `current`); not public. Use the *"not public"* wording the `engine` and `adapters` rows use (`.claude/context/graphscene.md` → `## Naming and layout`).
- [ ] `## The layers` table, the `facade` row's *Holds* cell. Add *"and the `graphscene` command line, the one module that writes output"*. Leave the bullets below the table unchanged: they already say a thin command-line entry point goes in `facade` and is the one place that may write output.
- [ ] A new section `## The command line`, placed after `## The boundary` and before `## Running the toolchain`. It states:
  - **Who it is for:** a host not written in Python, or a shell script. It reads no configuration.
  - **The four commands, their arguments, and the two JSON documents.**
    - The check document, `{"stage", "violations": [{"path", "check", "reason"}]}`. `check` is set only for stage `static`, from the check id the reason opens with.
    - The step document, the walk-state document's encoding of an action or `{"kind": "refused", "reason"}`.
    - Both are printed as one ASCII-only line on stdout, and both are encoded in `adapters` (`check_json.py`, `walk_json.py`), not by the command module.
  - **Predicate answers:** only through repeated `--answer <predicate>=true|false`. An unanswered predicate is refused by the walk, never guessed.
  - **The exit contract:** `0` / `1` / `2` / `3` / `4`, each with its meaning. For `4`, the stderr line `graphscene: <message>` and an empty stdout.
  - **How it is run.** Show each command in its own fenced block, one command per line (`harness-runs/lessons.md` → `## Adopter-facing documentation`, the first lesson):
    - `uv run --frozen --no-sync --project graphscene graphscene check <graph>` from the repository root, once the package environment is provisioned. The section says the console script is installed by `bash scripts/python-service.sh provision`.
    - A worked `start` / `next` pair over `tests/fixtures/flow_graph/valid_generic.json`.
  - **One sentence on the toolchain wrapper.** `scripts/python-service.sh run` is not a route to the command, because its row names no console script and its exit mapping would collapse `1`–`4` into `1`.

**Verification:**

- Every command, flag, field name and exit code in the new section matches `graphscene/src/graphscene/facade/cli.py` as Task 3 landed it, and the check document's description matches `graphscene/src/graphscene/adapters/check_json.py` as Task 2 landed it, read off the modules' docstrings and argparse definitions, not this plan.
- Each runnable command in the README sits in its own fenced block, one command per line.
- The `walk_json.py`, `check_json.py` and `cli.py` README entries all carry *"not public"*, matching `graphscene/tests/test_public_surface.py` → `_EXPECTED`, which none of their names joins.
  - **Deviations from plan:** Evidence downgrade: the README's `uv run --frozen --no-sync --project graphscene graphscene check …` line was not executed. The direct `uv run` call was refused by the permission layer (don't-ask mode). That line rests on two things. First, reading `scripts/python-service.sh`, where the wrapper exports `UV_PROJECT_ENVIRONMENT="$repo_root/$1/.venv"`, the same location uv uses by default for `--project graphscene`. Second, `graphscene/pyproject.toml`, which declares `graphscene = "graphscene.facade.cli:main"`. The worked `check` / `start` / `next` / `current` sequence over `graphscene/tests/fixtures/flow_graph/valid_generic.json` was run through `main` with `bash scripts/python-service.sh --package graphscene probe harness-runs/scratch/task4_cli_walk.py <fixture>`. The results were: `check` printed `{"stage": null, "violations": []}` and exited 0. `start` printed a `dispatch` of `draft` and exited 0. `next --outcome done` with no answer printed `{"kind": "refused", "reason": "the host cannot answer predicate 'stage_disabled' for node 'edit_check'"}` and exited 3. `next --outcome done --answer stage_disabled=false` printed a `set` for `review_round` and exited 0.
