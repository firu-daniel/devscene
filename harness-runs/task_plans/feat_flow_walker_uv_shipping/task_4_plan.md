### Task 4 — Provision the walker's environment as `setup-worktree.sh`'s bootstrap step 6

**Goal:** Give every bootstrapped checkout a provisioned walker environment: each local run copy, the remote job's checkout and a hand-bootstrapped worktree. Today an adopter's run copy has no route to one.

**Depends on:** Task 3, which defines `hr_flow_host_provision <source_scripts_dir> <env_scripts_dir>` in `lib/harness-run-lib.sh`. Both arguments are absolute `scriptsDir` paths. The function builds the project `<source_scripts_dir>/python/devscene-flow-host` into the environment `<env_scripts_dir>/python/.venv`. A `SKIPPED` case returns `0`, a sync failure returns `1`. This task only calls it.

**Where this task stops.** It runs the function; it does not change it. Protecting the main checkout's `<scriptsDir>/python/` is Task 5's. Ignoring the run copy's `.venv` is Task 6's.

### Targets

- `cli/templates/scripts/setup-worktree.sh`.
- `cli/test/setup-worktree-flow-host.test.mjs` (new).
- `cli/test/helpers/watcher.mjs` → `createWatcherFixture` and its `watcherEnv`.

**Which existing suites step 6 reaches, and why only through this helper.** After Task 2, `init` writes `<scriptsDir>/python/devscene-flow-host/pyproject.toml` into every fixture it wires, so a bootstrap of such a fixture's run copy reaches step 6, and with `uv` on the inherited `PATH` a real `uv sync`. That fails inside the gate sandbox (exit `2`, so `status=1` and `create-worktree.sh` removes the copy), and outside one it reaches PyPI, which `.claude/context/cli.md` → `## What "done" means here` forbids. The routes into a bootstrap, as the plan's author found them by grep:

- **The watcher's three `"$CREATE_WORKTREE"` arms** (`cli/templates/scripts/autonomous-watcher.sh`: the task path, the docs path, and `--existing`) pass no `--no-bootstrap`. Every suite that drives them builds its fixture with `createWatcherFixture` (30 suites, among them `watcher-stall-reset-payloads.test.mjs` and `watcher-review-drop-payloads.test.mjs`, which assert the cut copy exists).
- **`remote-run.sh`** cuts with `--no-bootstrap` and `--existing --no-bootstrap` only, so `remote-start`, `remote-collect` and `remote-review-payloads` never reach step 6.
- **`create-worktree.test.mjs`, `setup-worktree-clone-target.test.mjs` and `setup-worktree-checkout-sparse.test.mjs`** copy only the scripts and `lib/` into a fixture `init` did not wire. They reach the `no flow host` `SKIPPED` arm and need nothing.
- **`sandbox-probe-gate-sandbox-legs.test.mjs`** cuts its clone with `--no-bootstrap`.

So the one helper is where the fix goes. The stub must survive a suite that hands `watcherEnv` its own `PATH`: `watcher-keep-awake.test.mjs`, `watcher-placeholder-host.test.mjs` and `watcher-stall-reset-payloads.test.mjs` each build one from `process.env.PATH`, and `watcherEnv` spreads the caller's `env` last. The two `restart-watcher-*` suites also set their own `PATH`, but they run `restart-watcher.sh` against a recorded `DEVSCENE_CLI` stub and cut no copy.

**Work:**

- [ ] Step 6, after step 5's dependency install and build, runs whatever step 5 answered, because the two are independent. It calls `hr_flow_host_provision`, and a non-zero return sets `status=1` and prints which step failed.
  - **With `--target <dir>`:** `<source_scripts_dir>` is this script's own `scriptsDir`, the main checkout's, and `<env_scripts_dir>` is the same repo-relative `scriptsDir` under `<dir>`. The copy's environment is built from the main checkout's packages, never from the tree the run wrote.
  - **With no argument:** both arguments are this checkout's own `scriptsDir`.
- [ ] Header:
  - Rename `THE FIVE STEPS, AND WHAT EACH DOES WHEN ITS INPUT IS ABSENT` to six steps and add step 6's paragraph: its two `SKIPPED` cases print a line and pass, and why `--target` builds from the main checkout.
  - In `THE RESIDUAL \`--target\` DOES NOT CLOSE`, add one sentence: step 6 is outside that residual for `--target`, because it builds from the main checkout's protected packages. With no argument it builds the checkout's own, and a remote job's surface check covers that case.
  - First grep `plugin/`, `docs/` and `cli/` for the old heading text, and carry every citer you find in this task's own targets. Report a citer outside them in your return rather than editing it.
- [ ] `setup-worktree-flow-host.test.mjs`, its header stating the rule. Model its fixture on `cli/test/setup-worktree-clone-target.test.mjs` for the registered-clone `--target` case, with a stub `uv` on `PATH` recording argv and `UV_PROJECT_ENVIRONMENT`. It asserts:
  - With no argument: `--project <checkout>/<scriptsDir>/python/devscene-flow-host` and the environment `<checkout>/<scriptsDir>/python/.venv`.
  - With `--target <clone>`: `--project <main>/<scriptsDir>/python/devscene-flow-host` and the environment `<clone>/<scriptsDir>/python/.venv`.
  - The bootstrap exits `0` when `uv` is absent, and when the project directory is absent, each printing its `SKIPPED` line.
  - It exits `1`, naming step 6, when the stub fails.
- [ ] `cli/test/helpers/watcher.mjs`: keep every watcher a `createWatcherFixture` fixture starts away from a real `uv`.
  - In `createWatcherFixture`, write an executable stub `uv` at `<recorderDir>/bin/uv`. It records nothing and exits `0`: `#!/usr/bin/env bash` then `exit 0`. `<recorderDir>` is the existing `RECORDER_DIR` directory inside the fixture.
  - `watcherEnv` sets `PATH` **after** spreading the caller's `env`, to `<recorderDir>/bin` + `delimiter` + (the caller's `env.PATH` if it passed one, else `process.env.PATH`, else `''`). A suite's own `PATH` then keeps its own entries, behind the stub. With the stub, `hr_flow_host_provision` takes its success arm, so the bootstrap exits `0` and the copy is kept.
  - Add a numbered choice to the module header, beside choices 1–8, stating the rule: after Task 2, `init` writes the flow host into every fixture, so the watcher's bootstrap reaches `setup-worktree.sh` step 6. The stub keeps that step off the network and out of the shared `uv` cache (`.claude/context/cli.md` → `## What "done" means here`), and inside the gate sandbox it keeps a real `uv sync` from exiting `2` and losing the copy. Its `PATH` is composed after the caller's `env`, and a suite that passes its own `PATH` keeps the stub ahead of it.
  - Before editing, re-run the grep this file's `### Targets` note summarises, from the checkout root: `git grep -nE 'CREATE_WORKTREE|create-worktree\.sh|setup-worktree\.sh' -- cli/templates/scripts cli/test`. For each call without `--no-bootstrap`, confirm that every suite reaching it gets its environment from `watcherEnv`. Name in your return any suite that reaches it through an environment `watcherEnv` did not build, and do not edit that suite.

**Verification:**

- `npm test --workspace cli -- test/setup-worktree-flow-host.test.mjs` passes.
- The header's `REPRO` block still reproduces every exit it lists.
- Read-only check of `cli/test/helpers/watcher.mjs`: `watcherEnv`'s returned object assigns `PATH` after `...env`, and its first entry is the directory holding the stub `uv`. For each call into `"$CREATE_WORKTREE"` or `setup-worktree.sh` without `--no-bootstrap` that the grep in **Work:** lists, the suites reaching it must be ⊆ the `createWatcherFixture` suites that get their environment from `watcherEnv`, plus the script-only fixtures named in `### Targets` that reach the `no flow host` skip.

**Deviations from plan:**

- The `REPRO` verification bullet rests on reading, not execution: the fixture there commits no `<scriptsDir>/python/devscene-flow-host`, so step 6 takes its `no flow host` `SKIPPED` arm (return 0) — or its `no uv` arm — and every listed exit is unchanged; the same arm is executed by `cli/test/setup-worktree-flow-host.test.mjs` case (d).
- The `watcher.mjs` read-only check rests on `git grep` and reading: the calls without `--no-bootstrap` are the watcher's three `"$CREATE_WORKTREE"` arms and the script-only fixtures of `create-worktree.test.mjs`, `setup-worktree-clone-target.test.mjs` and `setup-worktree-checkout-sparse.test.mjs`; every inbox-dropping watcher suite reaches a pass through `tick` or `w.watcherEnv(...)`. The 30 `createWatcherFixture` suites were not run here — deferred to the Run gates phase.
