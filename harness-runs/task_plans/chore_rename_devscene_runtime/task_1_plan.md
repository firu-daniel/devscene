### Task 1 — Move the package to `devscene-flow-host/`, rename it `devscene_flow_host` and narrow its stated scope

**Goal:** Move every tracked file of the package from `devscene-runtime/` to `devscene-flow-host/`. Rename the import package `devscene_runtime` to `devscene_flow_host` and the distribution `devscene-runtime` to `devscene-flow-host`. Restate what the package is as **the harness's GraphScene host**. Switch the toolchain wrapper's package table to the new directory in the same commit. No behaviour changes: the package stays a skeleton with an empty `__all__`.

**Layer.** This is a catch-all (`general`) task although half of what it touches sits under the `devscene-runtime` layer's path. A move cannot be split by layer, and the catch-all dispatch is the one with every layer path in scope. Read `.claude/context/devscene-runtime.md` for the package's own rules (still binding on the moved files under their new names) and `.claude/context/conventions.md` for the Python stack and the wrapper. Do **not** edit either document, or anything else under `.claude/`. Those are the maintainer's after-merge steps, listed in the story index's `## Context`.

**Where this task stops.** It changes no gate leg, no document outside the package, and neither `cli/test/python-service.test.mjs` nor `devscene.config.json`:

- Task 2 updates the test that asserts the wrapper's table. Between this commit and Task 2's, that test is expected to disagree with the wrapper.
- Task 3 moves the `treeGuards` entries.
- Task 4 updates `scripts/run-gates.sh`, `docs/development.md` and `ROADMAP.md`.
- No task edits `.github/workflows/supply-chain.yml`. The maintainer commits that edit at Task 5's park (story index `## Context` → **The workflow edit, and why the run never commits it.**).

It does not re-make `uv.lock` (see the uv.lock bullet below).

### Targets

- `devscene-runtime/README.md` → `devscene-flow-host/README.md` (moved and rewritten)
- `devscene-runtime/pyproject.toml` → `devscene-flow-host/pyproject.toml` (moved and edited)
- `devscene-runtime/uv.lock` → `devscene-flow-host/uv.lock` (moved only, content untouched)
- `devscene-runtime/src/devscene_runtime/__init__.py` → `devscene-flow-host/src/devscene_flow_host/__init__.py` (moved and edited)
- `devscene-runtime/src/devscene_runtime/py.typed` → `devscene-flow-host/src/devscene_flow_host/py.typed` (moved only)
- `devscene-runtime/tests/requirement_names.py` → `devscene-flow-host/tests/requirement_names.py` (moved only)
- `devscene-runtime/tests/test_boundary.py` → `devscene-flow-host/tests/test_boundary.py` (moved and edited)
- `devscene-runtime/tests/test_graphscene_dependency.py` → `devscene-flow-host/tests/test_graphscene_dependency.py` (moved and edited)
- `scripts/python-service.sh` (edited)

**Work:**

- [ ] **Move the eight tracked files one at a time; never the directory.**
  - Create `devscene-flow-host/src/devscene_flow_host/` and `devscene-flow-host/tests/`. Then `git mv` each file `git ls-files devscene-runtime` lists to its target path above.
  - Do **not** `git mv devscene-runtime devscene-flow-host`: a directory rename would also carry the ignored `.venv`, `.ruff_cache` and `.mypy_cache` into the new directory. A virtual environment is not relocatable, because its scripts' shebangs name the old absolute path, so every gate leg would *fail* rather than grade `BLOCKED`.
  - Leave the ignored remnant under `devscene-runtime/` untouched: no move, no delete.
  - **`uv.lock` is moved byte for byte and never edited.** Its root entry `name = "devscene-runtime"` stays stale until the maintainer runs `bash scripts/python-service.sh --package devscene-flow-host lock` outside the sandbox (the story index's manual step 1). That sub-command reaches the network, which this run's sandbox refuses (`scripts/python-service.sh` header → `WHO RUNS lock, sync AND provision`), and a hand edit is forbidden (`.claude/context/devscene-runtime.md` → `## What it may depend on`).
- [ ] **`pyproject.toml` and `__init__.py`.**
  - In `pyproject.toml`, set `[project] name` to `"devscene-flow-host"`, `description` to `"The harness's GraphScene host."` and `[tool.hatch.build.targets.wheel] packages` to `["src/devscene_flow_host"]`. Nothing else changes: `[tool.uv.sources]` stays `{ path = "../graphscene", editable = true }`, which still resolves from the new directory.
  - In `__init__.py`, the docstring's first line becomes `The harness's GraphScene host.`. Its second paragraph becomes this scope statement: the package holds only the code that feeds GraphScene the harness's configuration, records, predicates, executor configuration and hooks, and the commands over it; anything useful without DevScene belongs in GraphScene; and another DevScene Python integration gets its own `devscene`-prefixed package.
  - Keep the `The rule: …` paragraph and `__all__: list[str] = []` exactly as they are.
- [ ] **The two tests, names only.**
  - In `test_boundary.py`, the two docstring mentions of `src/devscene_runtime/` become `src/devscene_flow_host/`. `_PACKAGE_DIR` becomes `_ROOT / "src" / "devscene_flow_host"`. The self name in `_STDLIB_AND_SELF` becomes `"devscene_flow_host"`.
  - In `test_graphscene_dependency.py`, `_RELOCK` becomes `"bash scripts/python-service.sh --package devscene-flow-host lock"`.
  - Every edited line stays within `ruff`'s 100 columns. The longest, `test_boundary.py`'s first docstring line, grows from 96 to exactly 100, so re-wrap it if it would exceed that. No other test text changes.
- [ ] **`README.md`.** Rewrite it for the new name and the narrowed scope:
  - The heading becomes `# devscene-flow-host`.
  - `## What it is` states the following: `devscene-flow-host` is the harness's GraphScene host, imported as `devscene_flow_host`. It holds only the code that feeds GraphScene the harness's configuration, records, predicates, executor configuration and hooks, and the commands over it, and no behaviour yet. Any other DevScene Python integration gets its own `devscene`-prefixed package rather than a place here. Anything useful without DevScene goes in GraphScene (`graphscene/`). It stays in this repository, outside the npm package (`cli/package.json` → `files`), and adopters never import it.
  - Every command block and the `relative to …/` sentence name `devscene-flow-host`.
  - `## What it may depend on`, `## The lock follows GraphScene` and `## Gating` keep their content under the new name.
  - **No sentence names the old name or says the package was renamed** (`harness-runs/lessons.md`, the rename lesson under `## Adopter-facing documentation`). Each command sits in its own fenced block, one per line (the first lesson under the same heading).
- [ ] **`scripts/python-service.sh`.** Set `PACKAGES` to `"docs-retrieval-service graphscene devscene-flow-host"`, and rename the `package_row` case `devscene-runtime)` to `devscene-flow-host)`, keeping its three empty fields. In the header, the table paragraph's row description and the `WHERE IT WRITES` paragraph's `` `devscene-runtime` `` both become `` `devscene-flow-host` ``. No other line changes. In particular, leave the `# PROVIDES: provision` line exactly as it is (`commands.depInstall` greps it with `-qx`).

**Verification:**

- `git ls-files devscene-runtime` prints nothing. `git ls-files devscene-flow-host` prints exactly the eight target paths above. `git diff --cached -M --stat HEAD` (or the commit's own stat) shows each as a rename.
- `git grep -n -i -E "devscene[-_ ]runtime|DevScene.s own Python runtime" -- devscene-flow-host scripts/python-service.sh` has one hit only: the stale root entry in `devscene-flow-host/uv.lock`. `git grep -n -E "DevScene.s meanings" -- devscene-flow-host` has none.
- `awk 'length($0) > 100 {print FILENAME": "FNR}' devscene-flow-host/src/devscene_flow_host/__init__.py devscene-flow-host/tests/test_boundary.py devscene-flow-host/tests/test_graphscene_dependency.py` prints nothing.
- The wrapper's table refuses the old row and lists the new one. `bash scripts/python-service.sh --package devscene-runtime lint` exits `2` with `python-service: unknown package 'devscene-runtime'; the packages are: docs-retrieval-service, graphscene, devscene-flow-host`, which is a usage check that runs no tool.
- Run this task's own edited test files, the two it edits:

  ```
  bash scripts/python-service.sh --package devscene-flow-host test tests/test_boundary.py tests/test_graphscene_dependency.py
  ```

  In this run the wrapper is expected to exit `3`, *not provisioned*, because the new directory has no environment. Record that as **not run**, never as a pass, and raise no blocker: manual step 3 of the story index runs them on a provisioned checkout.
