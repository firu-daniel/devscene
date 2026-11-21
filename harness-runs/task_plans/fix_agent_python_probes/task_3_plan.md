### Task 3 — Pin `probe` and `check` in `cli/test/python-service.test.mjs`

**Goal:** Pin Task 1's two new verbs: what each calls, from which directory, what each refuses, and how each grades. Use the suite's existing throwaway fixture and recording `uv` stub, so a later edit to the wrapper cannot silently widen the probe fence or let `BLOCKED` read as a pass.

**Depends on:** Task 1. The contract pinned here:

- **`probe <file> [args...]`**, optional leading `--package <dir>`. The path resolves against the repository root, or is absolute, and is judged by `hr_scratch_path_var` from `scripts/lib/harness-run-lib.sh` **before** the `cd`. Accepted, it runs `uv run --frozen --no-sync --no-cache python <physical target path> <args…>` from the package directory, with the four environment values every leg sets. The file's own status is passed through. Refusals exit `2` with a `python-service: probe:` stderr line and call no `uv`: missing argument, a leading `-`, an `HR_SCRATCH_WHY` refusal (outside, `..`, charset, itself, symlink, no-parent), a non-`.py` basename, a target that is not a readable regular file. The library unreadable exits `1`. Not provisioned exits `3`.
- **`check`**. No argument and no `--package` (either is exit `2`, no `uv` call). For each row in table order it runs `lint` (two `uv` calls) and then `typecheck` (one), printing `python-service: check: <row> <leg> PASS|FAIL|BLOCKED`. It exits `1` when any leg failed, `3` when none failed and at least one is `BLOCKED`, and `0` otherwise.
- **Root placement**: by `hr_script_root` when `lib/harness-run-lib.sh` sits beside the script, else unchanged.

### Targets

- `cli/test/python-service.test.mjs` — the existing suite for `scripts/python-service.sh`.

**Work:**

- [ ] **Header.** Extend the bold rule paragraph with the two verbs: `probe` runs only a `.py` file inside the state directory's `scratch/` and passes its status through, and `check` grades unprovisioned as exit `3`, never as a failure. Add to *Deliberately not covered*: the real `uv` running a real probe (that evidence is Task 1's own probe call and a reviewer's use), and the `F15` placeholder itself, which needs a bubblewrap host.
- [ ] **A probe-capable fixture.** Add an option to `buildFixture`, or a sibling helper, that also copies `scripts/lib/harness-run-lib.sh` from `WORKSPACE_ROOT` into the fixture's `scripts/lib/`. It writes a `devscene.config.json` the library resolves, carrying at least `version`, `defaultBranch` and a `stateDir`, creates that state directory's `scratch/`, and plants a probe file there. Add to `BASE_TOOLS` any tool the library's path test reaches that `/usr/bin` and `/bin` may not hold (`jq` at least). The existing cases keep the script-only fixture, which also pins the unchanged fallback root placement.
- [ ] **`probe` cases.** (a) Provisioned, default row and under `--package graphscene`: one recorded call, with argv `[...LEG_PREFIX, 'python', <target>, 'a', 'b']`, `cwd` the row's directory and the four values, and nothing under `HOME` (`assertNothingUnderHome`). (b) `FAKE_UV_STATUS=7` makes the probe exit `7`. (c) Each refusal above exits `2`, prints its `python-service: probe:` line and records no call: a path outside the scratch directory, a `..` path, `-c`, a `.mjs` file, an absent file, no argument. (d) No `pyvenv.cfg` exits `3`. (e) In the script-only fixture, `probe` exits `1`, naming the unreadable library.
- [ ] **`check` cases.** (a) Both rows provisioned: six recorded calls, in order (`docs-retrieval-service` `ruff check`, `ruff format --check`, `mypy`, then `graphscene`'s three), each with its row's site; four `PASS` lines; exit `0`. (b) Only `docs-retrieval-service` provisioned: its two `PASS` lines, `graphscene`'s two `BLOCKED` lines, exit `3`. (c) The same with `FAKE_UV_STATUS=1`: `FAIL` lines for the provisioned row, `BLOCKED` for the other, exit `1`, and every leg still run. (d) No `uv` on `PATH`: four `BLOCKED` lines, exit `3`. (e) `check x` and `--package graphscene check` exit `2` with no call.
- [ ] Keep every existing case green. Assert the usage line by its existing `USAGE_PREFIX` only, so its new verbs do not break the unknown-package and bare-`--package` cases.

**Verification:**

- `npm test --workspace cli -- test/python-service.test.mjs` passes, run once from the repository root as one foreground command, and its counts show the new cases ran.
- Each refusal case asserts both the exit code and that no `uv` call was recorded, so a refusal that still ran `uv` fails here. Confirm this by reading the cases.
