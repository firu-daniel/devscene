### Task 9 — Add a pinned `setup-uv` step to the shipped `devscene-run.yml`

**Goal:** Put `uv` on the remote job's runner before the job bootstraps its checkout, so that `Bootstrap the checkout` → `setup-worktree.sh` step 6 (Task 4) provisions the walker there, as it does locally.

**Depends on:** Task 4, whose step 6 skips with a `SKIPPED` line when `uv` is absent. With this step, a GitHub-hosted runner gets an environment instead.

**Why this is not a hand-pushed workflow change.** The file is the template `cli/templates/github/workflows/devscene-run.yml`. `push-branch.sh` refuses only a commit changing a path under the root `.github/workflows/` (`cli/templates/scripts/lib/harness-run-lib.sh` → `HR_REMOTE_WORKFLOWS_DIR`), and this repository's own `.github/workflows/` is not touched.

### Targets

- `cli/templates/github/workflows/devscene-run.yml`.
- `cli/test/workflow-setup-uv.test.mjs` (new).

**Work:**

- [ ] Add a step `Set up uv` to the `run` job, immediately before `Preflight with doctor`, which already precedes `Bootstrap the checkout`. It goes after the job-surfaces refusal, so nothing new runs before that trust check.
  - It carries `if: env.HARNESS_STOPPED != '1'`.
  - `uses: astral-sh/setup-uv@1c37ad07a6a961277cf70c0d37d6f313000f5884`, the pin this repository's `.github/workflows/supply-chain.yml` already carries, with its version comment on the line above in this file's style (`# astral-sh/setup-uv v10.3.0`).
  - `with: enable-cache: false`, with a one-line comment: a cache restored from another branch's run would feed an unsandboxed install.
  - Every GitHub expression keeps its space after the opening braces (the header's *TWO RULES EVERY EDIT KEEPS*).
- [ ] `ACTION PINS` block: add the `astral-sh/setup-uv v10.3.0` line. The block's sentence claiming each release's `action.yml` declares `runs.using: node24` was a lookup of the five existing pins only. Reword it to name those five, and add one sentence: setup-uv's `runs.using` and runner floor are owed a maintainer's lookup. That is the story index's manual step. No figure is asserted here.
- [ ] `workflow-setup-uv.test.mjs`, its header stating the rule. It reads the template as one fixed file and asserts:
  - Exactly one `astral-sh/setup-uv@<40 hex>` step exists in the `run` job, with its version comment on the line above.
  - The step carries `enable-cache: false` and the `HARNESS_STOPPED` condition.
  - It sits after `Refuse a branch that changed the job's own files` and before `Preflight with doctor` and `Bootstrap the checkout`.
  - `ACTION PINS` names it.

**Verification:**

- `npm test --workspace cli -- test/workflow-setup-uv.test.mjs` passes.
- `git diff --name-only` for this task lists nothing under the root `.github/workflows/`.
