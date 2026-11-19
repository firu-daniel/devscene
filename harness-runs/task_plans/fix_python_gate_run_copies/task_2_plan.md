### Task 2 — Gate 6a skips the Python environment and tool-cache directories, and the root `.gitignore` ignores `.venv/` in any package

**Goal:** Keep the in-tree Python environment out of commits and out of gate 6a's `$HOME` grep. After Task 1, each package's virtual environment and tool caches sit inside the checkout. A venv names the interpreter's location (its `pyvenv.cfg`, its console-script shebangs, its editable-install `.pth`), and a mypy cache records the absolute paths of the stubs it read. Without exclusions, gate 6a would print every one of those lines.

**Depends on:** Task 1. It writes, under each table package's directory, `.venv` (`UV_PROJECT_ENVIRONMENT`), `.ruff_cache` (`RUFF_CACHE_DIR`) and `.mypy_cache` (`MYPY_CACHE_DIR`), and pytest writes `.pytest_cache` there. Those four basenames are this task's whole input. This task changes no wrapper.

**Where this task stops.** Task 5 covers the new exclusions in `cli/test/check-machine-paths.test.mjs`. Task 6 states them in `docs/development.md`'s gate 6 paragraph.

### Targets

- `scripts/check-machine-paths.sh`
- `.gitignore` (repository root; the hand-written lines above the managed `devscene` block only)

**Work:**

- [ ] `.gitignore`: replace `docs-retrieval-service/.venv/` with an unanchored `.venv/`, so a later table package is covered without a new line. Rewrite the comment above the Python block, which now says *"Backstop for running uv directly: scripts/python-service.sh keeps these outside the checkout"*. It should state that these four directories are where `scripts/python-service.sh` keeps each package's environment and tool caches inside the checkout, and that none is ever committed. Leave `__pycache__/`, `.mypy_cache/`, `.pytest_cache/` and `.ruff_cache/` as they are. Touch nothing inside the managed block.
- [ ] `scripts/check-machine-paths.sh`: add `--exclude-dir=.venv --exclude-dir=.mypy_cache --exclude-dir=.ruff_cache --exclude-dir=.pytest_cache` to the `grep -rn` line, beside `--exclude-dir=__pycache__`.
- [ ] `scripts/check-machine-paths.sh` header, `THE EXCLUDED DIRECTORIES` paragraph: add one sentence on the four names, matching the existing `__pycache__` sentence. Say what each holds (the per-package environment and tool caches `scripts/python-service.sh` keeps inside the checkout, which record the interpreter's and the stubs' absolute paths). Say they are gitignored by the root `.gitignore` and never committed. Say grep matches `--exclude-dir` against the base name, so the exclusion holds for every table package.

**Verification:**

- `git check-ignore -v docs-retrieval-service/.venv/pyvenv.cfg some-future-package/.venv/pyvenv.cfg docs-retrieval-service/.mypy_cache/x docs-retrieval-service/.ruff_cache/x docs-retrieval-service/.pytest_cache/x` names a root `.gitignore` rule for every path.
- `grep -n 'exclude-dir' scripts/check-machine-paths.sh` shows the four new names on the same `grep -rn` line as `__pycache__`.
- Gate 6a's behaviour on the new names is pinned by Task 5's case. This task does not run the gate script.
