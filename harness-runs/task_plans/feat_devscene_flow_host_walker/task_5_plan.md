### Task 5 — Keep each branch's walk in its own `FileStateStore` under `<stateDir>/.flow_walker_state/`

**Goal:** Give the walk a store keyed by branch, so one branch's walk can never be read for another branch in a checkout where runs on several branches share one `<stateDir>`. The bash walker refuses that case (`flow-walker.sh` → exit 1, *"a flow or branch other than the state's"*). Here it cannot arise. The store for branch `b` is GraphScene's own `FileStateStore`, unchanged, at `<repo_root>/<stateDir>/.flow_walker_state/<quote(b, safe="")>.json`. The story index's `## Context` (**Decisions**, first bullet) gives why the store is keyed by branch, why it is a directory at that path, and which three bash-era assumptions the cutover owns.

**Depends on:** Task 1, which creates `devscene-flow-host/src/devscene_flow_host/host/`. Under that package's rule, this module imports `graphscene` through its public surface only (`from graphscene import FileStateStore`). It takes `state_dir` as an argument, the repo-relative `HarnessConfig.state_dir` that `records.config.read_config` returns (Task 2), and reads no configuration itself.

**Where this layer stops.** This task builds the store and nothing that uses it. Composing it with the predicate host and the graph into a `Walker` is **Task 6's** (`open_walker`). Removing a finished branch's walk, and moving the bash walker's flat file aside at the cutover, are not this branch's.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/store.py` (new)
- `devscene-flow-host/tests/test_store.py` (new)

**Work:**

- [ ] **`host/store.py`.**
  - `STATE_DIRECTORY: Final = ".flow_walker_state"`.
  - `walk_state_path(repo_root: Path, state_dir: str, branch: str) -> Path` returns `repo_root / state_dir / STATE_DIRECTORY / (urllib.parse.quote(branch, safe="") + ".json")`. An empty `branch` raises `ValueError("a walk's branch is empty")`.
  - `walk_store(repo_root: Path, state_dir: str, branch: str, *, lock_timeout: float = 120.0) -> FileStateStore` returns `FileStateStore(walk_state_path(...), lock_timeout=lock_timeout)`. It touches no file: `FileStateStore` creates the directory on its first write or lock.
  - The module docstring's *"The rule:"* says one file per branch, the branch percent-encoded with no safe character, so the encoding is injective and a `/` never makes a subdirectory. Everything the store writes — the state file, its `.lock` sibling and `FileStateStore`'s temporary files — stays inside `<stateDir>/.flow_walker_state/`. Its *"Deliberately not covered:"* list names three things: two branch names that differ only in case, on a case-insensitive filesystem; removing a finished branch's file; and a flat file already at `<stateDir>/.flow_walker_state`, the bash walker's, under which the first write or lock raises an `OSError` that propagates unchanged.
- [ ] **`tests/test_store.py`.** Its docstring opens *"The rule this file exists to enforce"*. Plain `-> None` functions under `tmp_path`, expected paths written as literals:
  - `walk_state_path(tmp_path, "state", "feat_x")` → `tmp_path / "state" / ".flow_walker_state" / "feat_x.json"`; `"feat/x"` → `"feat%2Fx.json"`; `"a%b"` → `"a%25b.json"`; `""` → `ValueError` with its exact message
  - **two branches, two walks.** Build one `WalkState` from `graphscene`'s public types, for example `awaiting="done"` with an `End` as `pending` and empty mappings, and `write` it through `walk_store(tmp_path, "state", "feat/a")`. Then `walk_store(tmp_path, "state", "feat/b").read()` is `None`, and the `feat/a` store's `read()` equals the written state
  - **what is written.** After that write and one `with store.lock():` block, every path under `tmp_path`, walked with `rglob`, is inside `tmp_path / "state" / ".flow_walker_state"`. The set of file names there is exactly `{"feat%2Fa.json", "feat%2Fa.json.lock"}`
  - **a flat file in the way.** With a file already at `tmp_path / "state" / ".flow_walker_state"`, `write` raises an `OSError`, and the file is unchanged byte for byte
  - **Deviations from plan:** In **what is written**, `rglob` also yields `tmp_path / "state"`, the store directory's own ancestor, which cannot be inside it; the test exempts the store directory and its ancestors and asserts every other path is inside `tmp_path / "state" / ".flow_walker_state"`.

**Verification:**

- Run this task's own test file from the repository root, as one foreground command: `bash scripts/python-service.sh --package devscene-flow-host test tests/test_store.py`. Every case passes.
- `commands.typecheck` exits zero.
- `host/store.py` re-implements no part of `FileStateStore`: no `fcntl`, `os.replace` or `tempfile` in it.
