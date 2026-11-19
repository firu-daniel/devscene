### Task 2 — Add `graphscene` to `scripts/python-service.sh`'s package table, refuse `run` and `container-test` on a row without them, and lock the package

**Goal:** Make `graphscene` the second row of the wrapper's closed package table. `provision` and every leg then reach it through `--package graphscene`, and a run copy's bootstrap syncs it. Produce the `graphscene/uv.lock` that the row's `uv sync --frozen` needs. The row and its lock land together.

**Depends on:** Task 1, which creates `graphscene/pyproject.toml`. Its package is named `graphscene`, and it declares no `[project.scripts]` console script and no `compose.yaml`. This task reads that manifest through `uv lock` and changes nothing in it.

**Where this task stops.** This task adds the table row and produces the lock. The other work is owned elsewhere:
- **Task 3** owns gate 13's legs in `scripts/run-gates.sh` that call `bash scripts/python-service.sh --package graphscene lint|typecheck|test`. This task adds no gate.
- **Task 4** owns `cli/test/python-service.test.mjs`. That suite pins today's one-row table, so it fails from this task's commit until Task 4 lands. That is expected: the suite is not this task's to run (`## The test-run rule` point 1), and the Run gates round comes after Task 4.

### Targets

- `scripts/python-service.sh` — the table row, the two refusals, the header.
- `graphscene/uv.lock` (new) — produced by the wrapper's `lock`, never written by hand.

**Work:**

- [ ] **The row.**
  - `PACKAGES="docs-retrieval-service graphscene"`, in that order. `provision` syncs rows in table order and prints `python-service: provisioned graphscene` after the existing row's line. `DEFAULT_PACKAGE` stays `docs-retrieval-service`, so every existing bare call keeps its meaning.
  - Add a `package_row` arm `graphscene)` that sets `row_console_script=""` and `row_compose_prefix=""`. An empty value means the row does not serve that sub-command.
  - The unknown-package line is built by `package_list`. It now reads `python-service: unknown package '<dir>'; the packages are: docs-retrieval-service, graphscene`. Change nothing in that function.
- [ ] **The two refusals.** Both exit `2` (usage), are printed before `require_env` and before the `docker` probe, and never call `uv` or `docker`.
  - In the `run` arm, when `row_console_script` is empty, print `python-service: package 'graphscene' has no console script` (the package name taken from `$package`), then the usage line.
  - In the `container-test` arm, when `row_compose_prefix` is empty, print `python-service: package 'graphscene' has no container tests`, then the usage line.
  - So on that row, a host with no `docker` gets `2` rather than `4`.
- [ ] **The header.**
  - Replace *"Its one row is `docs-retrieval-service` (…)"* with both rows: `docs-retrieval-service` (`devscene-docs-retrieval`, `devscene-docs-retrieval-test`) and `graphscene` (no console script, no compose project).
  - Add to the exit contract's `2` line: *"or `run` / `container-test` on a row that has no console script / no compose project"*.
  - Under `WHERE IT WRITES`, note that `graphscene` also carries `-p no:cacheprovider`.
  - Leave the `# PROVIDES: provision` line byte-identical. `commands.depInstall` matches it with `grep -qx`.
- [ ] **The lock.** Run `bash scripts/python-service.sh --package graphscene lock` as one plain foreground command from the checkout root. This is provisioning, not a test run or a gate leg: `lock` is in no gate.
  - It reaches PyPI and writes the shared `uv` cache. A sandboxed run is expected to refuse one or both.
  - **If the call is refused, exits non-zero or leaves no `graphscene/uv.lock`, return a blocker and commit nothing.** The blocker names these two commands, to be run from an unsandboxed terminal at this checkout's root, after which the task resumes: `bash scripts/python-service.sh --package graphscene lock`, then `bash scripts/python-service.sh provision`. They are the story index's first manual-setup step.
  - Never write or edit `uv.lock` by hand, and never land the row without the lock. A row with no lock makes `provision`'s `uv sync --frozen` fail for that row, and so the bootstrap of every later run copy.

**Verification:**

- `graphscene/uv.lock` exists and is in this task's change beside `scripts/python-service.sh`. Its root package entry is `name = "graphscene"`, and it pins `ruff`, `mypy` and `pytest`.
- The new arms use no bash-4 construct (no `${var,,}`, no associative array), so the script still parses under `/bin/bash`, the 3.2 floor. Gate 16 grades that in the Run gates round. An unattended run refuses a free-standing `bash -n`.
- `git diff scripts/python-service.sh` shows no change to the `# PROVIDES: provision` line.
- Read the `run` and `container-test` arms: each empty-field check is the arm's first statement after its argument check, ahead of `require_env` and of the `command -v docker` probe.
