### Task 6 — Document run-copy provisioning, the in-tree environment and gate 6a's new exclusions in `docs/development.md`, the service README and `docs/retrieval-eval.md`

**Goal:** Make the project's own documents say what Tasks 1–3 made true:

- Each Python package's environment and tool caches live in that package's directory.
- A run copy is provisioned at bootstrap by `commands.depInstall` → `bash scripts/python-service.sh provision`.
- The gate legs run `uv run --frozen --no-sync --no-cache`, so they write only inside the run copy and under `$TMPDIR`.
- A host with no `uv` still grades `BLOCKED`.
- Gate 6a skips the four Python directories.

This task edits exactly the sites the story index's `## Scope register` marks `change` (rows 1, 2, 3, 4 and 13).

**Depends on:** Tasks 1, 2 and 3, and it restates their contracts so this file stands alone:

- **Task 1** (`scripts/python-service.sh`): an optional leading `--package <dir>` selects a row of a closed table, whose one row, `docs-retrieval-service`, is the default. `UV_PROJECT_ENVIRONMENT`, `RUFF_CACHE_DIR` and `MYPY_CACHE_DIR` are `<package>/.venv`, `<package>/.ruff_cache` and `<package>/.mypy_cache`, and pytest's `.pytest_cache` sits there too. Every leg runs `uv run --frozen --no-sync --no-cache`, and only `lock`, `sync` and `provision` use the shared `uv` cache. `provision` takes no argument and syncs every row with `uv sync --frozen --group dev`. It exits `0` with a `SKIPPED` line when `uv` is not on `PATH`, and `1` when a sync failed. The header paragraph that states the write locations is `WHERE IT WRITES`.
- **Task 2:** the root `.gitignore` ignores `.venv/` in any package, and `scripts/check-machine-paths.sh` adds `--exclude-dir=.venv --exclude-dir=.mypy_cache --exclude-dir=.ruff_cache --exclude-dir=.pytest_cache`.
- **Task 3:** `commands.depInstall` is `npm ci && bash scripts/python-service.sh provision`, which `scripts/setup-worktree.sh` step 5 runs unsandboxed in the copy it bootstraps. `run-gates.sh`'s `BLOCKED` remedy names `provision`.

### Targets

- `docs/development.md`
- `docs-retrieval-service/README.md`
- `docs/retrieval-eval.md`

**Work:**

- [ ] `docs/development.md` → `**Gate 13 — the Python docs-retrieval service.**` paragraph:
  - Leg commands: the "every leg runs through `uv run --frozen --no-sync`" sentence gains `--no-cache`, and says `uv` therefore writes only to a temporary directory under `$TMPDIR`.
  - The `BLOCKED` sentence keeps its condition. Its remedy becomes provisioning. The block after "Provision it once per checkout" becomes `bash scripts/python-service.sh provision`, still one command per line in its own fenced block, and the paragraph says:
    - A run copy needs no hand step: its bootstrap runs `provision` through `commands.depInstall`, wherever `uv` resolves on the run daemon's `PATH`.
    - A host with no `uv` bootstraps anyway and grades the legs `BLOCKED`.
    - `sync` stays the per-package command, and `sync --with-models` stays the models route.
- [ ] `docs/development.md`, the paragraph after the `HARNESS_GATES_CONTAINERS=1` block: replace **"The Python environment lives outside the checkout"** with the in-tree layout from Task 1, and say why. A run copy's gates run sandboxed, and both sandboxes allow writes only to the copy and a temporary directory (`scripts/launch-sandboxed-gates.sh` → `THE BWRAP VECTOR` for Linux; the run profile's `.sandbox.filesystem` for macOS). Add one sentence that `provision` runs unsandboxed inside the residual `scripts/setup-worktree.sh`'s header already names (`THE RESIDUAL --target DOES NOT CLOSE`), so it adds no new trust class. Add one sentence that `--package` exists so a later Python package joins the same wrapper as a table row. State no measured figure: nothing on this branch measured gate 13 in a provisioned run copy.
- [ ] `docs/development.md` → `**Gate 6 — self-containment.**`: after the sentence ending "`--exclude-dir=__pycache__` skips Python bytecode, which records each source's absolute path and which the root `.gitignore` already keeps out of every commit", add the four new exclusions. Say what each directory holds, that each records `$HOME`-bearing paths (the interpreter in a venv's `pyvenv.cfg`, shebangs and `.pth`; stub paths in a mypy cache), and that the root `.gitignore` keeps each out of every commit. Grep matches each flag against a base name, so the exclusion covers every package.
- [ ] `docs-retrieval-service/README.md`:
  - **`## Standing it up`:** "Provision the environment, which lives outside the checkout" becomes the in-tree `docs-retrieval-service/.venv`. Keep `bash scripts/python-service.sh sync` as the per-package command, and add `bash scripts/python-service.sh provision` as what a run copy's bootstrap runs, each in a fenced block of its own, one command per line.
  - **`## Testing`:** after "where `uv` or the synced environment is missing", add that a run copy is provisioned at bootstrap.
- [ ] `docs/retrieval-eval.md`, step **5. The footprint**: the environment sentence now names `docs-retrieval-service/.venv` (`scripts/python-service.sh` → `WHERE IT WRITES`) instead of a directory keyed by the `cksum` of the checkout root. Its `du` line becomes `du -sh docs-retrieval-service/.venv >> harness-runs/scratch/backend-comparison/footprint.txt`. Change no other line of the protocol.

**Verification:**

- Re-run the story index's scope-register entries A and B verbatim from the repository root. Each one's output stays ⊆ the register's rows.
- `grep -n 'outside the checkout' docs/development.md docs-retrieval-service/README.md` no longer prints a sentence about the Python environment.
- `grep -n 'devscene-docs-retrieval/venvs\|checkout_key' docs/retrieval-eval.md docs/development.md docs-retrieval-service/README.md` prints nothing.
- Every command this task writes into a document sits in a fenced block, one command per line (`harness-runs/lessons.md` → `## Adopter-facing documentation`, first rule).
- Read the rewritten gate 13 paragraph against `scripts/python-service.sh`'s header and `scripts/run-gates.sh`'s `python_gate`. Every sub-command, flag, exit status and path the prose names exists there as spelled.
