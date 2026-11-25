### 2. `(E5)` `--existing` case fails at bootstrap step 6: the fixture has no flow host

**File:** `cli/test/create-worktree.test.mjs` (`reproFixture`, used by the test `(E5) an honest --existing branch is cloned at its tip and bootstrapped from the main configuration`) — "const result = await f.create(['--existing', 'feat/e5']);" (around line 448, navigation hint only).

**Failing test:** `cli/test/create-worktree.test.mjs` — `(E5) an honest --existing branch is cloned at its tip and bootstrapped from the main configuration` (TAP `not ok 290`).

**Class:** Wrong behaviour
**Failure:** If the running program runs `cli/test/create-worktree.test.mjs` → `(E5) an honest --existing branch is cloned at its tip and bootstrapped from the main configuration`, then it fails with `expected exit 0, got 4`, because `setup-worktree.sh` step 6 prints `flow-host: provision: failed — no flow host at …/demo/scripts/python/devscene-flow-host; run npx devscene init --upgrade`.

**Failure as logged** (gate 4, first round):

```
not ok 290 - (E5) an honest --existing branch is cloned at its tip and bootstrapped from the main configuration
  location: 'cli/test/create-worktree.test.mjs:434:1'
  error: |-
    expected exit 0, got 4
    setup-worktree.sh: dependency install: printf x > deps.marker
    setup-worktree.sh: commands.build is not set — skipping build
    setup-worktree.sh: no pre-push hook at /private/tmp/claude-501/create-worktree-tnlGpr/demo-feat-e5/githooks — skipping hook install
    flow-host: provision: failed — no flow host at /private/tmp/claude-501/create-worktree-tnlGpr/demo/scripts/python/devscene-flow-host; run npx devscene init --upgrade
    setup-worktree.sh: step 6 (flow-host provision) failed
    setup-worktree.sh: bootstrap finished with failures for /private/tmp/claude-501/create-worktree-tnlGpr/demo-feat-e5 (see above)
    create-worktree.sh: the bootstrap '…/demo/scripts/setup-worktree.sh --target …/demo-feat-e5' failed (exit 1) — the working copy was created but NOT bootstrapped
    4 !== 0
  stack: TestContext.<anonymous> (file://…/cli/test/create-worktree.test.mjs:450:10)
```

**Diagnosis.** Class: first round (no earlier log). Same mechanism as Finding 1: this branch's Task 3 (commit `29f6f57f`) made `setup-worktree.sh` step 6 (`hr_flow_host_provision` in `cli/templates/scripts/lib/harness-run-lib.sh`) fail the bootstrap when `<main checkout>/scripts/python/devscene-flow-host/pyproject.toml` is absent, and `reproFixture` creates no such file and puts no stub `uv` on `PATH`. The `--existing` bootstrap reads the project from the main checkout (`--target`), so the branch's own commit (`devscene.config.json`, `src/e5.txt`) is irrelevant to the failure.

**Suspected shared cause:** likely the same cause as Finding 1 — both cases share `reproFixture`, which lacks the flow-host project and the `uv` stub that step 6 now requires.

**Fix:**

- [ ] If Finding 1's fixture change has already landed (`reproFixture` commits `scripts/<FLOW_HOST_DIRNAME>/<FLOW_HOST_PROJECT>/pyproject.toml` and `create` runs with a stub `uv` first on `PATH`), no further code change is needed for this case.
- [ ] Otherwise apply exactly the fixture change Finding 1 describes, in `reproFixture` — the empty flow-host `pyproject.toml` committed under `join(d, 'scripts', FLOW_HOST_DIRNAME, FLOW_HOST_PROJECT)`, a `uv` stub `#!/usr/bin/env bash\nexit 0\n` in a `bin` directory under `w`, and the `create` member passing `{ PATH: \`${bin}${delimiter}${process.env.PATH ?? ''}\` }` to `runBash` — with the matching file-header update.
- [ ] Keep every `(E5)` assertion as it is; in particular `git status --porcelain` must stay empty, which holds because the stub writes nothing and the `pyproject.toml` is committed on `trunk`, from which `feat/e5` is cut.
