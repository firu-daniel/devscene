### Task 5 — Re-point the state-directory README templates and two script comments from the committer to the commit step

**Goal:** Every README `init` writes into an adopter's state directory stops naming the `committer` agent and its `## Process` section. Each one names **the commit step** instead — `<scripts_dir>/commit-on-branch.sh` with `--unit` — and the header paragraph that states the behaviour it describes. Two shipped script comments that name the agent are reworded the same way.

**Depends on:** Task 3, which writes these paragraphs into `commit-on-branch.sh`'s header:

- **THE TICK** — the readiness-entry flip;
- **THE STAGE SET** — the findings folder staged with the unit and left out of the work-file test, so an index-only commit is still reported;
- **THE SUBJECT AND ITS RECORD**.

Cite them as `<scripts_dir>/commit-on-branch.sh` → **THE STAGE SET**, and so on.

**The replacement wording.** The noun is **the commit step**. "the committer flips" → "the commit step flips". "`${CLAUDE_PLUGIN_ROOT}/agents/committer.md` → `## Process`" → "`<scripts_dir>/commit-on-branch.sh` → **THE STAGE SET**". "from implementer to committer" → "from implementer to the commit step". Change no other sentence.

### Targets

- `cli/templates/state-dir/{task_plan_point_reviews,review_plan_point_reviews,architecture_branch_review_point_reviews,business_parity_branch_review_point_reviews,skeptic_review_point_reviews,qa_review_point_reviews,test_fix_point_reviews,user_review_fix_plan_point_reviews}/README.md`
- `cli/templates/state-dir/{code_reviews,architecture_branch_reviews,business_parity_branch_reviews,skeptic_reviews,test_fix_plans,user_reviews}/README.md`
- `cli/templates/state-dir/{story_plans,task_plans,ui_test_plans,branch_statistics}/README.md`
- `cli/templates/scripts/push-branch.sh` — header comment only.
- `cli/templates/scripts/remote-run.sh` — the one comment that says "the committer flips the entry".

**Work:**

- [ ] **The eight per-unit review-folder READMEs** (`*_point_reviews`). Each carries the same two sentences, "which the committer flips as the fix lands" and "The committer leaves these files out of its test … (`${CLAUDE_PLUGIN_ROOT}/agents/committer.md` → `## Process`)". Reword them per the replacement wording, citing **THE STAGE SET**. Keep the eight copies of the shared sentence byte-identical to one another, as they are today.
- [ ] **The six review-index READMEs.** Reword "the committer flips the item's `[ ]` to `[x]`", "worked through by … the committer", "the only place the committer flips anything" and "with the committer flipping each readiness entry" to the commit step.
- [ ] **The four plan and report READMEs.** `story_plans`, `task_plans`, `ui_test_plans` and `branch_statistics` carry the commit-step wording. In `task_plans` the per-task file is staged "when the implementer changed it", because the commit step stages every changed path — not "only when the implementer appended deviation notes". In `branch_statistics`, "no commit step flips a checkbox for it".
- [ ] **The two script comments.**
  - **`push-branch.sh`.** Its header's "`committer` agent's opt-in push" becomes "the commit step's `--push`", naming `commit-on-branch.sh`'s front end.
  - **`remote-run.sh`.** "the committer flips the entry in the" becomes "the commit step flips the entry in the". Leave the two `committer time` comments alone: they name git's committer timestamp.
  - Change no executable line in either script.

**Verification:**

- `git grep -n -w committer -- cli/templates/state-dir` prints nothing. `git grep -n -w committer -- cli/templates/scripts/push-branch.sh cli/templates/scripts/remote-run.sh` prints only the two `committer time` comment lines of `remote-run.sh`.
- `git grep -n 'agents/committer.md' -- cli/templates` prints nothing.
- `git diff -U0 -- cli/templates/scripts` shows only lines beginning `#`.
