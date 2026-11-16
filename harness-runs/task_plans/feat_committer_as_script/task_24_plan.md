### Task 24 — Re-render this repository's self-adopted script and state-directory README copies, and register the commit-step suite as a tree guard

**Goal:** This repository has adopted its own harness, so `scripts/` and the `harness-runs/*/README.md` files are `init`'s byte-for-byte copies of `cli/templates/`. After merge, the plugin's unit and artifact calls hit this checkout's own `scripts/commit-on-branch.sh`, which must therefore be the new one. Copy every template this branch changed over its self-adopted copy, as `d953d476` (`chore: Re-render the planning scripts after #381`) did for #381. Then register Task 21's tree-reading suite as a tree guard.

**Depends on:**

- **Tasks 1, 2, 3 and 5**, which change `cli/templates/scripts/commit-on-branch.sh`, `lib/unit-commit-lib.sh` (new), `lib/planning-record-lib.sh` (header only), `push-branch.sh` and `remote-run.sh` (comments only), and the `cli/templates/state-dir/*/README.md` templates.
- **Task 21**, which creates `cli/test/commit-step-calls.test.mjs`. It reads the `plugin/` tree in its case (e), and its file names this task as the registering task.

**Catch-all task.** Its implementer reads every configured layer's conventions document. The files it writes are the `general` layer's copies of `cli` templates, governed by `.claude/context/conventions.md` → `## Documents of record` (*"`devscene.config.json`, `.claude/`, `harness-runs/`, `scripts/` and `githooks/` at this root are `init`'s output in this checkout"*).

### Targets

- `scripts/commit-on-branch.sh`, `scripts/lib/unit-commit-lib.sh` (new), `scripts/lib/planning-record-lib.sh`, `scripts/push-branch.sh`, `scripts/remote-run.sh`
- `harness-runs/{architecture_branch_review_point_reviews,architecture_branch_reviews,branch_statistics,code_reviews,review_plan_point_reviews,skeptic_review_point_reviews,skeptic_reviews,story_plans,task_plan_point_reviews,task_plans,test_fix_plans,test_fix_point_reviews,user_review_fix_plan_point_reviews,user_reviews}/README.md`
- `devscene.config.json` — one `treeGuards` entry.

**Work:**

- [ ] **The scripts.** Copy each of the five `cli/templates/scripts/` files over its `scripts/` counterpart byte-for-byte, with the `Write` tool or a plain `cp` of one named path per call. Set `scripts/lib/unit-commit-lib.sh` to mode `644` and keep `scripts/commit-on-branch.sh`'s `755`, matching the `OUTER_LOOP_SCRIPTS` rows.
  - **Before copying,** compare `git diff --no-index <template> <copy>` with `git diff dev -- <template>`. The first must show exactly the hunks the second shows, reversed: the copy differs from the template only by this branch's template edits. A copy carrying any other difference holds a local change. Stop and report it rather than overwrite it.
- [ ] **The fourteen self-adopted READMEs.** Copy each `cli/templates/state-dir/<dir>/README.md` this branch changed over `harness-runs/<dir>/README.md`, byte-for-byte, for the fourteen directories that exist here. The parity- and QA-gated directories (`business_parity_*`, `qa_review_point_reviews`, `ui_test_plans`) are not materialised in this repository, whose `phases.parity` and `phases.qa` are `false`, and get no copy. Apply the same before-copy check.
- [ ] **The guard entry.** Add `{ "test": "test/commit-step-calls.test.mjs", "covers": "plugin/**/*.md" }` to `devscene.config.json` → `treeGuards`, after the existing entries, preserving the file's two-space formatting. Change no other key.

**Verification:**

- For each script and README pair, `git diff --no-index --exit-code cli/templates/<path> <copy>` exits zero.
- `git grep -n -w committer -- 'harness-runs/*/README.md'` prints nothing.
- `ls -l scripts/lib/unit-commit-lib.sh scripts/commit-on-branch.sh` shows modes `-rw-r--r--` and `-rwxr-xr-x`.
- `jq -e '.treeGuards[] | select(.test == "test/commit-step-calls.test.mjs")' devscene.config.json` exits zero.

**Deviations from plan:**

- **`dev` is `origin/dev`.** This checkout has no local `dev` branch (`git diff --stat dev -- …` → `fatal: bad revision 'dev'`). Every before-copy comparison used `origin/dev`.
- **Before-copy check, run as a blob-identity test.** I did not compare the two hunk sets. Instead I compared each copy's indexed blob (`git ls-files -s`, tree clean) with the template's blob at `origin/dev` (`git rev-parse origin/dev:<template>`). The 4 existing scripts and the 14 READMEs all matched hash for hash. That is the stronger form of the check: the copy equals the dev template, so it carries no local change. The 4 parity- and QA-gated directories have no copy here (`git ls-files -s` printed nothing for them).
- **Copies made with the file tools, not `cp`.** The permission profile refused `cp <template> <copy>` ("Permission to use Bash has been denied"). Each copy was written instead with `Write` (`commit-on-branch.sh`, `lib/unit-commit-lib.sh`) or with `Edit` hunks taken from `git diff origin/dev -- <template>` (the other three scripts and the 14 READMEs). The byte-identity verification below covers this route.
- **The verification's `--exit-code` exits 1 on three scripts, because of mode only.** `git diff --no-index --exit-code` exits 1 for `commit-on-branch.sh`, `push-branch.sh` and `remote-run.sh` and prints only `old mode 100644 / new mode 100755`. The templates are `100644`; the copies keep the `100755` this plan's mode bullet requires (both were `100755` at `origin/dev` too). `git diff --no-index --numstat` prints `0	0` for each of the three, so the content is identical. The two libraries and the 14 READMEs exit 0.
- **`cli/templates/scripts/README.md` changed on this branch but was not copied.** It has no self-adopted copy (`scripts/README.md` does not exist), and it is not in this task's targets.
