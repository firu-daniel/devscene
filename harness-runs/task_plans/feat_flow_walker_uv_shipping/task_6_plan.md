### Task 6 — Ignore the walker's environment `<scriptsDir>/python/.venv/` in the managed `.gitignore` block

**Goal:** Keep the walker's environment out of `git status` in every checkout that provisions it. That is the main checkout, each run copy that Task 4 bootstraps, and a remote job's checkout. Without the rule, a fresh run copy opens with an untracked `.venv/`.

**Depends on:** Task 1, whose `cli/src/flowHost/layout.ts` → `flowHostEnvDir(config)` returns the repo-relative `<scriptsDir>/python/.venv`. The rule is built from it, never retyped.

**Where this task stops.** It renders the rule for adopters. This repository's own `.gitignore` and `examples/notes-app/.gitignore` get the line from Task 12.

### Targets

- `cli/templates/repo/gitignore`.
- `cli/src/generators/repoRoot.ts`.
- `cli/src/doctor/checks.ts` → `IGNORE_RULES_CHECK`, only if it holds an expected-rule list of its own. Task 8 edits this file later and depends on this task.
- `cli/test/flow-host-ignore.test.mjs` (new).

**Work:**

- [ ] `gitignore` template: add a token line `{{flowHostEnvPath}}`. Put above it a comment in the block's own voice: the flow walker's environment is per checkout, built by `flow-host-provision.sh` and by each bootstrap, records machine paths, and is never committed.
- [ ] `repoRoot.ts`: render `flowHostEnvPath` as `${flowHostEnvDir(config)}/`, beside `runControlArtifacts`. If `doctor`'s `ignore-rules` check (`cli/src/doctor/checks.ts` → `IGNORE_RULES_CHECK`) grades against a list of expected rules rather than reading the rendered block, extend that list from the same producer in this task.
- [ ] `flow-host-ignore.test.mjs`, its header stating the rule. It asserts:
  - `init` writes `devscene-scripts/python/.venv/` under the default `scriptsDir`, and `tools/harness/python/.venv/` under `--scripts-dir tools/harness`.
  - A second `init` adds no line.
  - `git status --porcelain` in the fixture shows nothing after `<scriptsDir>/python/.venv/pyvenv.cfg` is created by hand.

**Verification:**

- `npm test --workspace cli -- test/flow-host-ignore.test.mjs` passes.
- `grep -n "python/.venv" cli/src` finds no literal outside `cli/src/flowHost/layout.ts`.
- **Deviations from plan:**
  - The plan says `flowHostEnvDir(config)` returns `<scriptsDir>/python/.venv`; as Task 1 shipped it, it returned `<scriptsDir>/python/devscene-flow-host/.venv` (joined onto `flowHostProjectDir`). The story plan, `harness-run-lib.sh` → `hr_flow_host_provision` (`environment="$env_root/$flow_dir/$flow_env"`) and `cli/test/flow-host-provision.test.mjs` / `setup-worktree-flow-host.test.mjs` all place the environment at `<scriptsDir>/python/.venv`, and nothing called `flowHostEnvDir` yet. Fixed `cli/src/flowHost/layout.ts` → `flowHostEnvDir` to join onto `flowHostDir`, and corrected the `FLOW_HOST_ENV_DIRNAME` doc comment, so the rendered rule matches where the environment is actually built.
  - `doctor`'s `IGNORE_RULES_CHECK` grades against `clarificationsIgnoreRules` and `contentsIgnoredDirectories` plus `git check-ignore`, not a general expected-rule list, so it was left unchanged.
  - The third test assertion compares `git status --porcelain --untracked-files=all` before and after creating `pyvenv.cfg` instead of asserting empty output: the fixture's `git commit` after `init` exited 1 with empty stderr, and the files `init` writes are untracked until a commit exists.
  - Verification bullet 2: `grep -rn "python/.venv" cli/src` also matches a pre-existing prose comment in `cli/src/generators/outerLoopScripts.ts` (the `flow-host-provision.sh` row of the outer-loop table, written by Task 4). It is a comment, not a path literal, so it was left as is.
