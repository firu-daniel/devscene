### 1. Default-mode `create-worktree.sh` case fails at bootstrap step 6: the fixture has no flow host

**File:** `cli/test/create-worktree.test.mjs` (`reproFixture`) — "for (const name of ['create-worktree.sh', 'setup-worktree.sh', 'lib/harness-run-lib.sh'])" and the `create:` member "create: (args) => runBash(d, [join(d, 'scripts', 'create-worktree.sh'), ...args])" (around line 88 and line 105, navigation hints only).

**Failing test:** `cli/test/create-worktree.test.mjs` — `the default mode bootstraps the clone, then pushes from the main checkout and mirrors the tip` (TAP `not ok 278`).

**Class:** Wrong behaviour
**Failure:** If the running program runs `cli/test/create-worktree.test.mjs` → `the default mode bootstraps the clone, then pushes from the main checkout and mirrors the tip`, then it fails with `create-worktree.sh exited 4` / `4 !== 0`, because `setup-worktree.sh` step 6 prints `flow-host: provision: failed — no flow host at …/demo/scripts/python/devscene-flow-host; run npx devscene init --upgrade`.

**Failure as logged** (gate 4, first round):

```
not ok 278 - the default mode bootstraps the clone, then pushes from the main checkout and mirrors the tip
  location: 'cli/test/create-worktree.test.mjs:283:1'
  error: |-
    create-worktree.sh exited 4
    setup-worktree.sh: dependency install: printf x > deps.marker
    setup-worktree.sh: commands.build is not set — skipping build
    setup-worktree.sh: no pre-push hook at /private/tmp/claude-501/create-worktree-PObC5A/demo-feat-x/githooks — skipping hook install
    flow-host: provision: failed — no flow host at /private/tmp/claude-501/create-worktree-PObC5A/demo/scripts/python/devscene-flow-host; run npx devscene init --upgrade
    setup-worktree.sh: step 6 (flow-host provision) failed
    setup-worktree.sh: bootstrap finished with failures for /private/tmp/claude-501/create-worktree-PObC5A/demo-feat-x (see above)
    create-worktree.sh: the bootstrap '…/demo/scripts/setup-worktree.sh --target …/demo-feat-x' failed (exit 1) — the working copy was created but NOT bootstrapped
    4 !== 0
  stack: TestContext.<anonymous> (file://…/cli/test/create-worktree.test.mjs:288:10)
```

**Diagnosis.** Class: first round (no earlier log). This branch's Task 3 (commit `29f6f57f`, "Declare the flow host's layout names once in the gate") changed `cli/templates/scripts/setup-worktree.sh` step 6 so that "No `uv` on PATH, no project there, or a failed sync prints one `flow-host: provision: failed …` line and fails the bootstrap" — before it, a missing project printed `SKIPPED` and passed. `hr_flow_host_provision` in `cli/templates/scripts/lib/harness-run-lib.sh` returns 1 when `"$project/pyproject.toml"` is absent, where `project` is `<main checkout>/<scriptsDir>/python/devscene-flow-host` (under `--target` the project is read from the main checkout, `$cfg_root`). `reproFixture` copies only `create-worktree.sh`, `setup-worktree.sh` and `lib/harness-run-lib.sh` into `demo/scripts/`, so there is no `demo/scripts/python/devscene-flow-host/pyproject.toml`; the bootstrap fails, `create-worktree.sh` rolls back and exits 4. The test file was not updated alongside Task 3. The production behaviour is the intended one; the fixture is stale.

The sibling suite `cli/test/setup-worktree-clone-target.test.mjs` (`fixture`) already carries the pattern that satisfies step 6: a flow-host `pyproject.toml` at `join(main, DEFAULTS.scriptsDir, FLOW_HOST_DIRNAME, FLOW_HOST_PROJECT)` and a stub `uv` (`'#!/usr/bin/env bash\nexit 0\n'`) first on `PATH`. A stub is required, not merely the project file: this host has a real `uv` on `PATH` (the log's failure is "no flow host", not "uv is not on PATH"), and a real `uv sync --frozen` against an empty `pyproject.toml` would fail or reach the network, which `cli` tests must not do.

**Fix** (test fixture only; no change to `setup-worktree.sh` or the library):

- [ ] In `reproFixture`, after the template scripts are copied and before `git add -A`, create `join(d, 'scripts', FLOW_HOST_DIRNAME, FLOW_HOST_PROJECT, 'pyproject.toml')` (empty content) with `mkdir(…, { recursive: true })`. Import `FLOW_HOST_DIRNAME` and `FLOW_HOST_PROJECT` from `'../dist/flowHost/layout.js'`, as `setup-worktree-clone-target.test.mjs` does, rather than spelling `python` / `devscene-flow-host`. `CONFIG.scriptsDir` is already `'scripts'`, so the path matches what step 6 resolves.
- [ ] In `reproFixture`, create a `bin` directory under `w` (outside `demo`, so it is not committed and no copy contains it), write an executable `uv` stub `#!/usr/bin/env bash\nexit 0\n` (mode `0o755`), and change the `create` member to pass `{ PATH: \`${bin}${delimiter}${process.env.PATH ?? ''}\` }` as `runBash`'s env argument; import `delimiter` from `node:path`.
- [ ] Update the file header's fixture paragraph ("Each case builds the script header's REPRO fixture …") to say the fixture also commits a flow-host `pyproject.toml` under `scripts/python/devscene-flow-host` and runs every `create-worktree.sh` call with a stub `uv` exiting 0 first on `PATH`, because `setup-worktree.sh` step 6 fails a bootstrap with no `uv` or no project.
- [ ] Leave the assertions unchanged: the stub writes nothing, so `(E5)`'s `git status --porcelain` cleanliness check and the rollback assertions are unaffected.
