### 1. Two plugin instructions cite the wrapper header `STAGING POLICY, AND THE ONE TRAP IN IT`, which the code-review fix renamed

> **Self-contained per-finding file** for the `feat_committer_as_script` skeptic-review index (`harness-runs/skeptic_reviews/feat_committer_as_script_skeptic_review.md`). The implementer reads only this file to apply the fix. The commit step flips this finding's checkbox in the index's `## Phase 2 Readiness — Ordered Fix List`, never here.

**Files:**
- `plugin/instructions/plan_orchestration_instructions_core.md` → `### B.3` paragraph opening "(`--extra` is what gets B.2's meta-review findings committed" — the citation "`<scripts_dir>/commit-on-branch.sh` → **STAGING POLICY, AND THE ONE TRAP IN IT**".
- `plugin/instructions/improvement_observations_instructions.md` → the **Wrapper exit status (surface the error).** paragraph — the sentence beginning "On a **first** write, delete nothing:", which cites "`<scripts_dir>/commit-on-branch.sh`'s **STAGING POLICY, AND THE ONE TRAP IN IT** header".

**Problem.** Code-review Finding 1's fix (commit `138e34bf`) renamed the header paragraph in `cli/templates/scripts/commit-on-branch.sh` (and the self-adopted `scripts/commit-on-branch.sh`) from `STAGING POLICY, AND THE ONE TRAP IN IT.` to `STAGING POLICY.` and deleted its `THE TRAP:` sentences. That fix's steps listed only the wrapper, the library, their tests and the self-adopted copies. They never named the two plugin files that cite the old title, so both now point at a heading that does not exist.

Proof:
- `grep -n 'STAGING POLICY' cli/templates/scripts/commit-on-branch.sh` returns only `# STAGING POLICY. Only the explicit paths passed before`, `deleted path (STAGING POLICY)` and `# STAGING POLICY (header).`. No line carries `AND THE ONE TRAP IN IT`.
- `git grep -n 'STAGING POLICY, AND THE ONE TRAP'` outside `harness-runs/` returns exactly the two plugin sites above.

`.claude/context/plugin.md` → `## Citation` states that a cited heading is a wire, and that a rename strands every citer. A reader who follows either pointer finds no such paragraph.

The improvement-observations sentence also restates the old general rule: "a deleted path is skipped rather than staged as a removal". After the fix, the wrapper commits an absent path as a removal when the branch's tip holds it, and skips it only when neither the tip nor the working tree holds it. The sentence's conclusion still holds for the case it covers. On a first write the intake file is not in the tip, so deleting it still leaves the staged addition uncleared. But the stated reason is now false as a general claim about the wrapper.

**Fix.**

1. In `plugin/instructions/plan_orchestration_instructions_core.md`, in the paragraph opening "(`--extra` is what gets B.2's meta-review findings committed", make this replacement:
   - Replace: `the wrapper skips an absent path with a warning (`<scripts_dir>/commit-on-branch.sh` → **STAGING POLICY, AND THE ONE TRAP IN IT**)`
   - With: `the wrapper skips a path neither the branch's tip nor the working tree holds, with a warning (`<scripts_dir>/commit-on-branch.sh` → **STAGING POLICY**)`
2. In `plugin/instructions/improvement_observations_instructions.md`, in the **Wrapper exit status (surface the error).** paragraph, make this replacement:
   - Replace: `the kind stages exactly the intake file's path, and a deleted path is skipped rather than staged as a removal (`<scripts_dir>/commit-on-branch.sh`'s **STAGING POLICY, AND THE ONE TRAP IN IT** header), so no call can clear the staged addition`
   - With: `the kind stages exactly the intake file's path, and a path neither the branch's tip nor the working tree holds is skipped rather than staged as a removal (`<scripts_dir>/commit-on-branch.sh`'s **STAGING POLICY** header) — a first write's file is not in the tip — so no call can clear the staged addition`
3. Change no other text in either paragraph. Then run `git grep -n 'ONE TRAP' -- plugin cli docs scripts`. It must print nothing.

Neither file has a `cli/test` suite of its own, so no test file is run for this fix. The `test/commit-step-calls.test.mjs` and `test/main-repo-resolution-corpus.test.mjs` tree guards cover `plugin/**/*.md` and run in the Run gates phase.
