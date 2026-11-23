### Task 3 — Point the two `devscene.config.json` tree guards at the renamed package paths

**Goal:** Keep the package's boundary test selected as a tree guard. Its two `treeGuards` entries' `covers` move from the old package paths to the new ones. A `covers` glob naming a path that no longer exists fails nothing: it simply never matches a changed path, so the guard would silently stop running for every later unit that touches the package (`plugin/instructions/unit_loop_core.md` → `## The test-run rule` point 7, *"The match"*). A Run gates round does not read `treeGuards`, so this is the only place the stale entry would bite.

**Depends on:** Task 1, which moves the package source to `devscene-flow-host/src/devscene_flow_host/` and its manifest to `devscene-flow-host/pyproject.toml`. The guard's test file keeps its package-relative name, `tests/test_boundary.py`.

**Where this task stops.** It edits only the two `covers` values. The `layers` row (`name`/`path`/`conventions` `devscene-runtime`) and `detection.review` stay exactly as they are. The layer profile changes only through `devscene config set layers`, which is the maintainer's after-merge step 4 in the story index's `## Context`, and that step writes a new `detection.review` record too. Editing the row here would also re-route this run's own readiness entries mid-run.

### Targets

- `devscene.config.json` → `treeGuards`

**Work:**

- [ ] In the entry `{ "test": "tests/test_boundary.py", "covers": "devscene-runtime/src/devscene_runtime/**" }`, set `covers` to `"devscene-flow-host/src/devscene_flow_host/**"`.
- [ ] In the entry `{ "test": "tests/test_boundary.py", "covers": "devscene-runtime/pyproject.toml" }`, set `covers` to `"devscene-flow-host/pyproject.toml"`. Leave both `test` values, every other entry, the entries' order and the file's two-space formatting unchanged.

**Verification:**

- `jq -r '.treeGuards[] | select(.test == "tests/test_boundary.py") | .covers' devscene.config.json` prints exactly `devscene-flow-host/src/devscene_flow_host/**` and `devscene-flow-host/pyproject.toml`.
- `jq -r '.layers[] | select(.path == "devscene-runtime") | .name' devscene.config.json` still prints `devscene-runtime`. The layer row is untouched.
- `jq empty devscene.config.json` exits `0`: the file still parses.
- `git diff HEAD -- devscene.config.json` shows two changed lines and no others.

**Deviations from plan:**

- Evidence downgrade: `bash scripts/typecheck.sh` (`commands.typecheck`, run as written from the repository root) closed with `PASS: typecheck`, but two of its steps reported not run: `python-service: check: devscene-flow-host lint BLOCKED` and `python-service: check: devscene-flow-host typecheck BLOCKED`, both after `python-service: not provisioned: no synced environment at <repo_root>/devscene-flow-host/.venv`. This unit edits only two `covers` strings in `devscene.config.json`, which neither leg reads; the Run gates phase's whole-tree run, in a provisioned environment, verifies those legs. All four `**Verification:**` bullets were executed and met.
