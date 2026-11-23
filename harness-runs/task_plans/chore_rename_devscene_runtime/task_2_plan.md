### Task 2 — Point the Python-service test's third package row at `devscene-flow-host`

**Goal:** Make `cli/test/python-service.test.mjs` assert the wrapper's package table as Task 1 left it, with `devscene-flow-host` as its third row, and nothing else.

**Depends on:** Task 1. That task sets `scripts/python-service.sh` → `PACKAGES` to `docs-retrieval-service graphscene devscene-flow-host` and renames the `package_row` case to `devscene-flow-host)`, keeping that row's console script, compose prefix and models extra empty. The wrapper therefore prints `python-service: provisioned devscene-flow-host` as the third `provision` line, and lists the packages as `docs-retrieval-service, graphscene, devscene-flow-host` in its unknown-package refusal. This task changes no script. If the suite disagrees with the wrapper on anything other than the package's name, stop and report it rather than editing `scripts/`.

### Targets

- `cli/test/python-service.test.mjs`

**Work:**

- [ ] Set the `RUNTIME` constant to `'devscene-flow-host'`. Every use goes through the constant, so `ROWS`, `UNKNOWN_PACKAGE_LINE`, the fixture's directory, its planted `pyproject.toml` name and the test titles built with `${RUNTIME}` follow without further edits.
- [ ] In the `provision` case, change the third expected line from `'python-service: provisioned devscene-runtime\n'` to `'python-service: provisioned devscene-flow-host\n'`. It is the one literal not built from the constant. Keep it a literal rather than interpolating `RUNTIME`, so the assertion still states the contract verbatim (`.claude/context/conventions.md` → `## The testing bar`, *"Assert against the contract stated literally"*).
- [ ] Keep the constant's own name, `RUNTIME`. It names the table's third row beside `PACKAGE` and `LIBRARY`, not the package, and renaming it would touch every use for no change in what the suite asserts.

**Verification:**

- Run the edited test file:

  ```
  npm test --workspace cli -- test/python-service.test.mjs
  ```

  It passes: read the `# pass` / `# fail` counts and the exit status.
- `git grep -n -i "devscene-runtime" -- cli/test/python-service.test.mjs` prints nothing.

**Deviations from plan:**

- Evidence downgrade, the unit's `commands.typecheck` run: `bash scripts/typecheck.sh` ended `PASS: typecheck`, but its own output reported two steps as not run — `python-service: check: devscene-flow-host lint BLOCKED` and `python-service: check: devscene-flow-host typecheck BLOCKED`, each preceded by `python-service: not provisioned: no synced environment at <repo_root>/devscene-flow-host/.venv`. This unit changes no Python file; its change (`cli/test/python-service.test.mjs`) is covered by the TypeScript build and the single-file run, which passed (`# pass 25`, `# fail 0`). The `devscene-flow-host` lint and typecheck steps are verified by the Run gates phase's whole-tree `commands.typecheck` run in a provisioned run copy.
