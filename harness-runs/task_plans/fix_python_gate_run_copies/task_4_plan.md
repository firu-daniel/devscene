### Task 4 — Pin `python-service.sh`'s package selection, write locations and exit contract in `cli/test/python-service.test.mjs`

**Goal:** Write a suite that drives `scripts/python-service.sh` from a throwaway fixture, with a fake `uv` on `PATH`. It pins what makes gate 13 runnable in a run copy:

- Every write the wrapper causes lands in the package directory, or in `uv`'s own temporary cache, and never under `HOME` or `XDG_CACHE_HOME`.
- The read-only legs carry `--no-cache`, and provisioning does not.
- The package is a closed table row, selected with `--package`.
- `provision` lets a host with no `uv` bootstrap, while the legs still exit `3` (`BLOCKED`).

**Depends on:** Task 1, which fixes this contract in `scripts/python-service.sh`. This task asserts the contract and changes no script.

- **Invocation.** `bash scripts/python-service.sh [--package <dir>] <lock|sync [--with-models]|provision|lint|typecheck|test [path...]|run [args...]|container-test>`. The repository root comes from `git -C <the script's directory> rev-parse --show-toplevel`.
- **The table.** Exactly one row, `docs-retrieval-service` (console script `devscene-docs-retrieval`), and it is the default.
  - A missing `--package` value, or a directory that is not a row, prints `python-service: unknown package '<dir>'; the packages are: docs-retrieval-service` plus the usage line to stderr, then exits `2`.
- **Environment every `uv` call sees.** Working directory `<root>/<package>`, plus:
  - `UV_PROJECT_ENVIRONMENT=<root>/<package>/.venv`
  - `RUFF_CACHE_DIR=<root>/<package>/.ruff_cache`
  - `MYPY_CACHE_DIR=<root>/<package>/.mypy_cache`
  - `PYTHONDONTWRITEBYTECODE=1`
- **Leg argv.**
  - `lint`: `run --frozen --no-sync --no-cache ruff check`, then `run --frozen --no-sync --no-cache ruff format --check`. Both run, and the wrapper exits `1` if either failed.
  - `typecheck`: `run --frozen --no-sync --no-cache mypy`.
  - `test`: `run --frozen --no-sync --no-cache pytest <paths…>`.
  - `run`: `run --frozen --no-sync --no-cache devscene-docs-retrieval <args…>`.
- **Provisioning argv.**
  - `sync`: `sync --frozen --group dev`, with `--extra models` appended under `--with-models`, and no `--no-cache`.
  - `provision`: `sync --frozen --group dev` once per row. It prints `python-service: provisioned <package>` on stdout. On a failure it prints `python-service: provision: <package> failed (exit <n>)` on stderr and exits `1`.
- **Exits.**
  - Any non-zero tool status maps to `1`.
  - Legs exit `3` when `uv` is not on `PATH` or `<root>/<package>/.venv/pyvenv.cfg` is absent. The message names `provision`.
  - `provision` with no `uv` prints one stderr line containing `SKIPPED` and `uv is not on PATH`, then exits `0`.
  - `provision` given an argument or `--package` exits `2`.
  - `container-test` with no `docker` on `PATH` exits `4`.

### Targets

- `cli/test/python-service.test.mjs` (new)

**Work:**

- [ ] **Header.** Open with the rule this suite enforces, in the words above: one wrapper, writes only inside the package directory or `uv`'s temporary cache, a closed package table, and `provision`'s no-`uv` skip beside the legs' `BLOCKED`. Then name what it deliberately does not cover, and why:
  - **The real `uv` under the two sandboxes.** That evidence is gate 13 itself, run in a run copy bootstrapped with `provision`.
  - **`container-test` against a real Docker daemon.** No case here starts a service (`.claude/context/cli.md` → `## What "done" means here`).

  Reach the script as `join(WORKSPACE_ROOT, 'scripts', 'python-service.sh')`, as `cli/test/check-machine-paths.test.mjs` reaches its script (`cli/test/helpers/fixture.mjs` → `WORKSPACE_ROOT`).
- [ ] **Fixture and fake `uv`.** Build each case's fixture under `os.tmpdir()` and remove it in process:
  - `git init -q` a directory and copy the script into its `scripts/`.
  - Create `docs-retrieval-service/pyproject.toml`. Also create `other-package/pyproject.toml` and `other-package/uv.lock`: a Python package that is **not** a table row.
  - Add a `bin/uv` stub. It appends one record per call to a file: its working directory, its argv, and the four environment values above. It exits with `FAKE_UV_STATUS` (default `0`). On a `sync` call it creates `$UV_PROJECT_ENVIRONMENT/pyvenv.cfg`, as a real sync would.

  Run the script with `runBash`, with these settings:
  - `HOME` and `XDG_CACHE_HOME` each set to a fresh empty directory.
  - An inherited `UV_PROJECT_ENVIRONMENT` set to a decoy path, so the case proves the wrapper's own value wins.
  - `PATH` set to the stub directory in front of a base `PATH` holding `git`, `cksum` and `awk`.

  Expected paths come from the fixture's `realpath`, because `git` answers with the physical path (`/private/var/…` on macOS). Where the base `PATH` itself resolves a real `uv` (or `docker`, for the `container-test` case), skip only the case that needs its absence, with a reason naming the path found.
- [ ] **The legs, provisioned.** Plant `docs-retrieval-service/.venv/pyvenv.cfg`. Then:
  - Assert each leg's recorded argv, working directory and four environment values exactly, for both the default and an explicit `--package docs-retrieval-service`.
  - `test tests/a.py tests/b.py` forwards both paths verbatim.
  - With `FAKE_UV_STATUS=5`, `test` exits `1`, and `lint` records both of its calls and exits `1`.
  - Across every recorded call, no value starts with the case's `HOME` or `XDG_CACHE_HOME`, and both directories are still empty after the run.
- [ ] **Refusals and `BLOCKED`.**
  - `--package other-package lint` and a bare `--package` each exit `2`, with the unknown-package line, and record no `uv` call.
  - With the stub present but no `pyvenv.cfg`, each leg exits `3`, names `provision` on stderr, and records no call.
  - With no `uv` on `PATH`, each leg exits `3`.
  - `container-test` with no `docker` on `PATH` exits `4`.
- [ ] **Provisioning.**
  - `provision` records exactly one `sync --frozen --group dev` call, in `<root>/docs-retrieval-service` with that package's `.venv`, prints the `provisioned` line, and exits `0`.
  - With `FAKE_UV_STATUS=1` it exits `1` and prints the `failed (exit 1)` line.
  - With no `uv` on `PATH` it exits `0`, prints the `SKIPPED` line, and leaves `git status --porcelain --ignored` in the fixture unchanged.
  - `provision extra` and `--package docs-retrieval-service provision` each exit `2`.
  - `sync` records no `--no-cache`, and `sync --with-models` appends `--extra models`.
  - The script carries exactly one line that is, in full, `# PROVIDES: provision`. Task 3's `commands.depInstall` line tests for that exact line before it runs `provision`, so a respelling would silently stop every run copy from provisioning. The assertion names that consumer.

**Verification:**

- `npm test --workspace cli -- test/python-service.test.mjs` passes, run from the repository root as one plain foreground command.
- Each of these breaks a case. Check each against a deliberately broken copy of the script under `harness-runs/scratch/`, never by editing `scripts/python-service.sh`, and record the result in the return:
  - removing `--no-cache` from the `test` leg;
  - pointing `UV_PROJECT_ENVIRONMENT` back under `$HOME`;
  - making `provision` exit `3` when `uv` is absent;
  - accepting `other-package`.
- The suite builds nothing inside this checkout: `git status --short` after the run lists only the new test file.

**Deviations from plan:**

- The no-`uv` `provision` case compares `git status --porcelain --ignored --untracked-files=all`, not the bare form: in the fixture every package directory is untracked, so the bare listing collapses to `?? docs-retrieval-service/` and a `.venv` created inside it would not change it.
- The base `PATH` is `/usr/bin` and `/bin`, plus the runner's directory for any of `bash`, `git`, `cksum`, `awk`, `dirname`, `mkdir` neither holds: `runBash` resolves `bash` on it, the wrapper calls `dirname`, and the stub calls `mkdir`.
