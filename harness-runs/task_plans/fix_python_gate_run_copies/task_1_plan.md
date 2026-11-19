### Task 1 — `scripts/python-service.sh` serves a package table, keeps each package's environment and tool caches in its own directory, runs legs with `--no-cache`, and gains `provision`

**Goal:** Make every write the Python wrapper causes land somewhere both run-copy sandboxes can write: the package's own directory, or `uv`'s temporary cache under `$TMPDIR`. Add the `provision` sub-command that a bootstrap runs unsandboxed. Let the wrapper serve more than one package through a closed table, selected with `--package <dir>`, defaulting to `docs-retrieval-service`.

**Where this task stops.** This task changes `scripts/python-service.sh` only. Each of the following is owned by another task, and this task must not do it:

- `.gitignore`'s `.venv/` rule and gate 6a's exclusions: **Task 2**.
- Wiring `provision` into `commands.depInstall`, and `run-gates.sh`'s remedy text: **Task 3**.
- The suite that pins the contract below: **Task 4**.
- Every document: **Task 6**.

The file is hand-written (its own header says so) and is not in the set `init --force` rewrites, so there is no template copy to keep level.

**Why these locations** (story index `## Context`, decisions 2 and 3). A run copy's gates run sandboxed. In-session on macOS, and under `scripts/launch-sandboxed-gates.sh`'s `bwrap` vector on Linux (`--bind <target> <target>`, `--tmpfs /tmp`, `--setenv TMPDIR /tmp`, `--unshare-all`), the only writes allowed are the run copy itself and a temporary directory. Today's `${XDG_CACHE_HOME:-$HOME/.cache}/devscene-docs-retrieval/{venvs,ruff,mypy}/<key>` and `uv`'s `~/.cache/uv` are neither.

### Targets

- `scripts/python-service.sh`

**Work:**

- [ ] **The package table and `--package`.** Declare the table once, bash-3.2-compatible (no associative arrays): for example, a `PACKAGES` list plus a `case` function that sets each row's fields. Each row carries the package directory (repo-relative, at the root), the console script `run` invokes, and the compose project prefix `container-test` uses. Exactly one row today: `docs-retrieval-service`, with `devscene-docs-retrieval`, with `devscene-docs-retrieval-test`. Parse one optional leading `--package <dir>` before the sub-command, defaulting to `docs-retrieval-service`:
  - A missing value, or a directory that is not a table row (even one holding a `pyproject.toml`), prints `python-service: unknown package '<dir>'; the packages are: <rows, comma-separated>` and the usage line to stderr, then exits `2`.
  - Then `cd "$repo_root/<package>"`, keeping today's exit-`1` message when that fails.
  - The usage line becomes `usage: bash scripts/python-service.sh [--package <dir>] <lock|sync [--with-models]|provision|lint|typecheck|test [path...]|run [args...]|container-test>`.
- [ ] **Write locations.** Remove `cache_root` and every path under `${XDG_CACHE_HOME:-$HOME/.cache}`, so no code line names `HOME` or `XDG_CACHE_HOME`. Export these for every sub-command:
  - `UV_PROJECT_ENVIRONMENT="$repo_root/<package>/.venv"`
  - `RUFF_CACHE_DIR="$repo_root/<package>/.ruff_cache"`
  - `MYPY_CACHE_DIR="$repo_root/<package>/.mypy_cache"`
  - `PYTHONDONTWRITEBYTECODE=1`, kept.

  `pytest` keeps its own `.pytest_cache` under the package directory (its rootdir). Keep `checkout_key` (the `cksum` of `$repo_root`) for `container-test`'s project name and port only. `require_env` tests `"$UV_PROJECT_ENVIRONMENT/pyvenv.cfg"` as today. Its message names that path and the remedy `run bash scripts/python-service.sh provision outside the sandbox (a run copy's bootstrap runs it)`. The no-`uv` message names `provision` the same way.
- [ ] **The read-only legs take `--no-cache`.**
  - `lint` runs `uv run --frozen --no-sync --no-cache ruff check`, then `… ruff format --check`. Today's both-run, either-fails status is kept.
  - `typecheck` runs `uv run --frozen --no-sync --no-cache mypy`.
  - `test` runs `uv run --frozen --no-sync --no-cache pytest "$@"`.
  - `run` runs `uv run --frozen --no-sync --no-cache <row's console script> "$@"`.
  - `container-test`'s `pytest -m container -rs` takes `--no-cache` the same way.

  `lock` (`uv lock`) and `sync` (`uv sync --frozen --group dev`, plus `--extra models` under `--with-models`) are unchanged and keep the machine's shared `uv` cache: they are provisioning, run unsandboxed and allowed to reach the network. `container-test`'s project name becomes `<row's compose prefix>-$checkout_key`, which is today's name for the one row. Its port derivation is unchanged.
- [ ] **`provision`.** It takes no argument and no `--package`. Either one prints the usage line and exits `2`.
  - **No `uv`.** Where `uv` is not on `PATH`, print one stderr line, `python-service: provision: SKIPPED — uv is not on PATH; gate 13 grades BLOCKED until uv is installed and provision is re-run`, then exit `0`. It writes nothing.
  - **Each package.** Otherwise, for every table row in order, in a subshell so each `cd` and export stays per package: `cd` into the package, export that package's three locations, and run `uv sync --frozen --group dev`. On success, print `python-service: provisioned <package>` to stdout. On failure, print `python-service: provision: <package> failed (exit <n>)` to stderr, and carry on with the next row.
  - **Exit.** Exit `1` when any row failed, else `0`.
- [ ] **The header.** Rewrite it to match the code:
  - **Sub-commands.** The list gains `[--package <dir>]` (the table, its one row, the default) and `provision` (every row, the bootstrap's step, the `SKIPPED` exit `0`).
  - **Exit contract.** `3` is "never from `provision`", and `1` gains "a `provision` sync failed".
  - **`WHERE IT WRITES`.** A new paragraph replaces *"Nothing lands inside the checkout"*:
    - `.venv`, `.ruff_cache`, `.mypy_cache` and `.pytest_cache` sit under the package directory: per checkout by construction, ignored by the root `.gitignore`, and skipped by gate 6a.
    - The legs' `--no-cache` sends `uv`'s own writes to a temporary directory under `$TMPDIR`.
    - Only `lock`, `sync` and `provision` touch the shared `uv` cache.

    It closes with the reason: a run copy's two sandboxes allow writes to that copy and to a temporary directory only (`scripts/launch-sandboxed-gates.sh` → `THE BWRAP VECTOR`).
  - **`provision`'s trust.** A short paragraph: it runs unsandboxed from `commands.depInstall` during `setup-worktree.sh`'s bootstrap, inside the residual that script's header names (`THE RESIDUAL --target DOES NOT CLOSE`).

**Verification:**

- `grep -nE '^[^#]*(XDG_CACHE_HOME|\$HOME)' scripts/python-service.sh` prints nothing: no code line names the home directory any more.
- Every line `grep -nE '^[^#]*uv run' scripts/python-service.sh` prints contains `--no-sync --no-cache`. No line `grep -nE '^[^#]*uv (lock|sync)' scripts/python-service.sh` prints contains `--no-cache`.
- The usage string, the unknown-package line, the `SKIPPED` line, the `provisioned` line and the exit codes appear in the file exactly as spelled above. Task 4's suite asserts them byte for byte, so a respelling here is a break there.
- The behaviour itself is pinned by Task 4's suite, which drives this file against a throwaway fixture with a fake `uv`. This task runs none of the wrapper's sub-commands, because each one is a gate-13 leg.
