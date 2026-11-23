# Task plan review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **`task_5_plan.md` / story index `## Scope register` — `docs/development.md` § 8's per-job command list misses the new audit step, and Task 5's verification forbids fixing it.**
   Task 3 adds a third `uv-audit` step (`working-directory: devscene-runtime`). `docs/development.md` → `## 8. The nightly supply-chain audit` describes the commands each job runs, and its line *"`uv-audit`, once from `docs-retrieval-service/` and once from `graphscene/`:"* (above the `uv audit --preview-features audit-command --frozen` block) still names only two directories. It is not a register row: row 13 is the job table's `uv-audit` row and row 14 the dated audit table. Task 5's `**Verification:**` bullet *"no paragraph outside rows 8, 9 and 13 changed"* then stops the implementer from correcting it. The command still runs, so this is a stale description and not a failing step. That makes it a Should Fix: a maintainer who reproduces the nightly job by hand from this section audits two locks and never `devscene-runtime/uv.lock`.
   Register-gap disposition (ii). Entries A–D are file-grain `git grep -l` commands. They reach `docs/development.md`, but no entry reaches this anchor: the line carries no `uv.lock`, `python-service.sh`, `gate 13` or `13[e-g]`. A corrected entry, wider than D, at line grain: `git grep -nE 'uv\.lock|uv-audit|graphscene/' -- 'docs/*.md' 'ROADMAP.md' '*.yml'`. This is the only newly reached site that is not already a row's anchor: `docs/development.md` → § 8, the `uv-audit` command sentence. Add it as a `change` row owned by Task 5, and widen Task 5's last verification bullet to include it.

## Nice to Have

1. **`task_1_plan.md` — README sentence that a decided direction will falsify.** Task 1's README **What it is** section says the package *"is not part of the npm package (`cli/package.json` → `files`)"*. That is true today, but the task prompt's Decided list says it *"ships inside the `devscene` npm package with `graphscene` (#419)"*. Saying "not yet part of the npm package" and leaving out the `cli/package.json` citation would keep the sentence true after #419 without promising the work.
2. **`task_3_plan.md` — the new tree-guard `test` value matches a file in another layer.** `{"test": "tests/test_boundary.py", …}` follows the `graphscene` entries' shape, as the plan says. However, `doctor`'s `tree-guards` check (`cli/src/doctor/checks.ts` → `treeGuardTestResolves`, resolved against every `layers[].path`) accepts it today because `graphscene/tests/test_boundary.py` exists. So that warning cannot catch a missing `devscene-runtime/tests/test_boundary.py`. This is worth a sentence in the story index's third manual-setup step, which adds the layer that makes the entry resolve where it is meant to.
