### Task 12 — Commit through the main checkout's commit wrapper and flip a ledger entry in `host/commit_points.py`

**Goal:** Give the flow host the two side effects every planning hook is built from:

- **a commit point:** one call of the main checkout's `commit-on-branch.sh` in its `--artifact` form, with `--push`;
- **a ledger flip:** `- [ ] <id>.` becomes `- [x] <id>.` in the branch's flow-progress ledger.

They read as `cli/templates/scripts/lib/planning-record-lib.sh` → `prl_artifact_commit` and `prl_ledger_flip`, in the call spelling the autonomous fork gives (`plugin/instructions/task_plan_writing_instructions_autonomous.md` → `## Override 4 — commit the task plan after it converges`, **Commit mechanism**).

**Where this layer stops.** This task never decides which commit a step owes; that is Task 13's (`PlanningHooks`). The wrapper owns three things, and this module re-derives none of them:

- **the subject and the path set of each artifact kind** (`cli/templates/scripts/lib/unit-commit-lib.sh` → `ucl_artifact`);
- **the re-sync of a commit that landed with exit 1** (*"re-synced by the wrapper itself, which exits 0"*);
- **the push.**

The wrapper's path is the caller's input. The run driver (#424) resolves it to `<MAIN_REPO>/<scriptsDir>/commit-on-branch.sh`, because a run copy's wrapper is not trusted (`cli/templates/scripts/lib/planning-driver-lib.sh` header, *"THE WALKER IS THE MAIN CHECKOUT'S"*).

**Depends on:** Task 10, whose `records/ledger.py` declares the ledger's planning literals and owns them:

```python
PLANNING_ENTRIES: Final = ("P1", "P2", "P3")
OPEN_MARK: Final = "- [ ] "
DONE_MARK: Final = "- [x] "
SKIPPED_MARK: Final = "- [-] "
```

An entry's line opens `<mark> + f"{entry}."`. This module imports all four and declares none of its own.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/commit_points.py` (new)
- `devscene-flow-host/tests/test_commit_points.py` (new)

**The contract this task produces.** Task 13 calls it.

```python
from devscene_flow_host.records.ledger import (
    DONE_MARK, OPEN_MARK, PLANNING_ENTRIES, SKIPPED_MARK, ledger_path,
)   # Task 10's; not redeclared here

class CommitPointError(Exception): ...   # one-line message naming the call and its cause

async def commit_artifact(wrapper: Path, worktree: Path, kind: str, *,
                          round_number: int | None = None, entry: str | None = None) -> bool: ...

def flip_ledger_entry(repo_root: Path, state_dir: str, branch: str, entry: str) -> bool: ...
```

**`commit_artifact`** runs one fixed argument vector, with no shell, through `asyncio.create_subprocess_exec`, its working directory `worktree`. The vector is:

```
["bash", str(wrapper), "--repo", str(worktree), "--artifact", kind,
 *(["--round", str(round_number)] if round_number is not None else []),
 *(["--entry", entry] if entry is not None else []),
 "--push"]
```

The wrapper's exit status decides the result:

| Exit | Result |
|---|---|
| `0` | returns `True` (committed) |
| `3` | returns `False` (nothing to commit) |
| anything else | raises `CommitPointError(f"commit-on-branch.sh --artifact {kind} exited {rc}: {cause}")` |

`<cause>` is the last stdout line opening `error: `, with that prefix removed, or `no message` when there is none. stdout and stderr are both captured. The function is cancellable: on `asyncio.CancelledError` it kills the child, awaits it and re-raises.

**`flip_ledger_entry`** works on `records/ledger.py` → `ledger_path(...)`:

- **An `entry` not in `PLANNING_ENTRIES`** raises `ValueError(f"flip_ledger_entry takes P1, P2 or P3, not '{entry}'")`.
- **A missing ledger** raises `RecordError(f"the ledger '{rel}' does not exist")`.
- **An open entry.** The first line opening `OPEN_MARK + f"{entry}."` (`- [ ] <entry>.`) becomes `DONE_MARK + f"{entry}."` (`- [x] <entry>.`) with the rest of the line kept, and the call returns `True`. The file is replaced atomically, through a temporary file in the same directory and `os.replace`, with mode `0o644`.
- **A resolved entry.** If the first matching line opens `DONE_MARK` or `SKIPPED_MARK` + `f"{entry}."` (`[x]` or `[-]`), the file is left untouched and the call returns `False`.
- **No line for the entry** raises `RecordError(f"the ledger '{rel}' carries no {entry} line")`.

`rel` is the ledger's repo-relative path. A flip writes the file only. The `ledger-flip` commit is the caller's next `commit_artifact` call.

**Work:**

- [ ] **`host/commit_points.py`.**
  - **The code.** Implement `CommitPointError`, `commit_artifact` and `flip_ledger_entry` exactly as the contract spells them. Import `ledger_path`, `PLANNING_ENTRIES`, `OPEN_MARK`, `DONE_MARK` and `SKIPPED_MARK` from `records/ledger.py` (Task 10) and `RecordError` from `records/errors.py`. Declare no entry id or mark literal in this module.
  - **The docstring.** Its *"The rule:"* names `prl_artifact_commit` and `prl_ledger_flip`, the fork's call spelling, the exit-status mapping and the atomic replace. Its *"Deliberately not covered"* list names three things: resolving the wrapper path (the caller's), which artifact a step owes (`host/planning_hooks.py`'s), and the wrapper's own subjects, paths, re-sync and push.
- [ ] **`tests/test_commit_points.py` — the commit point.** Open with the header *"The rule this file exists to enforce"*. Plant a fake wrapper under `tmp_path`: a `#!/usr/bin/env bash` script that appends its arguments, one call per line, to a log file beside it, prints a scripted stdout, and exits with a scripted status. Then cover:
  - the exact argument vector for `plan-round --round 2`, for `ledger-flip --entry P1` and for `task-plan`;
  - exit `0` returns `True`, and exit `3` returns `False`;
  - exit `1` with `error: refused` on stdout raises with the exact message;
  - exit `2` with no `error:` line raises with `no message`;
  - a cancelled call leaves no child process. Use a wrapper that sleeps, cancel the task, and assert the child's PID is gone.
- [ ] **`tests/test_commit_points.py` — the ledger flip.** Cover each flip outcome on planted ledgers:
  - an open entry flipped, with the rest of the line kept;
  - an `[x]` entry and a `[-]` entry left byte-identical, returning `False`;
  - a missing line, a missing ledger and an unknown entry, each with its exact message.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_commit_points.py` passes.
- `commit_points.py` builds every argument vector as a list, with no `shell=True` and no string command. Grep the module and find neither.
- `git grep -nE '"P1"|"- \[ \] "|"- \[x\] "|"- \[-\] "' -- devscene-flow-host/src` has no hit outside `records/ledger.py`.

**Deviations from plan:**

- `flip_ledger_entry` also raises `RecordError(f"{path}: not UTF-8 text")` for a ledger that does not decode as UTF-8, the message `records/ledger.py` → `read_planning_marks` already uses. The contract names no outcome for this shape, and `.claude/context/devscene-flow-host.md` → `## Errors` makes `RecordError` the failure for a record not readable as the harness writes it. No test case covers it.
