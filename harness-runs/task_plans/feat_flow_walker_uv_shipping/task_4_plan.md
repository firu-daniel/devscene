### Task 4 — Provision the walker's environment as `setup-worktree.sh`'s bootstrap step 6

**Goal:** Give every bootstrapped checkout a provisioned walker environment: each local run copy, the remote job's checkout and a hand-bootstrapped worktree. Today an adopter's run copy has no route to one.

**Depends on:** Task 3, which defines `hr_flow_host_provision <source_scripts_dir> <env_scripts_dir>` in `lib/harness-run-lib.sh`. Both arguments are absolute `scriptsDir` paths. The function builds the project `<source_scripts_dir>/python/devscene-flow-host` into the environment `<env_scripts_dir>/python/.venv`. A `SKIPPED` case returns `0`, a sync failure returns `1`. This task only calls it.

**Where this task stops.** It runs the function; it does not change it. Protecting the main checkout's `<scriptsDir>/python/` is Task 5's. Ignoring the run copy's `.venv` is Task 6's.

### Targets

- `cli/templates/scripts/setup-worktree.sh`.
- `cli/test/setup-worktree-flow-host.test.mjs` (new).

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

**Verification:**

- `npm test --workspace cli -- test/setup-worktree-flow-host.test.mjs` passes.
- The header's `REPRO` block still reproduces every exit it lists.
