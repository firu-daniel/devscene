# Review plan meta-review — iteration 1

## Must Fix
1. **Finding 1's renamed library test asserts the wrong work count (`5`, where the specified behaviour yields `4`)** — refers to review finding #1. Offending file: `harness-runs/code_reviews/feat_committer_as_script_code_review/finding_1.md`, Fix step 4, the `cli/test/unit-commit-lib.test.mjs` bullet *"In `test('ucl_stage_set stages a deletion as its parent directory and excludes …', …)`, rename it … Change the expected `staged` to `[PLAN, FINDINGS, 'src/a/old.ts', 'src/a/older.ts', 'src/b.ts', 'src/c.ts']` and `work` to `5`."*
   The finding's own `staged` list is correct for the changed `ucl_stage_set`. The `work` value is not. `ucl_stage_set` (`cli/templates/scripts/lib/unit-commit-lib.sh`, the counting loop `if [ "$p" = "$plan" ] || [ "$p" = "$detail" ] … || { [ -n "$findings" ] && ucl_under "$p" "$findings"; }`) counts every staged path as work **except** the plan and any path under the findings folder. Of the six staged paths, `PLAN` is the plan and `FINDINGS` (`devscene/task_plan_point_reviews/b_task_plan/task_3/`) is the findings folder, so they count as index. That leaves four work paths: `src/a/old.ts`, `src/a/older.ts`, `src/b.ts` and `src/c.ts`. The current test agrees with this rule: the same listing staged as `[PLAN, FINDINGS, 'src/a/', 'src/b.ts', 'src/c.ts']` asserts `work` `3`, which is three work paths. Splitting `src/a/` into its two deleted files adds one, not two. The finding also says *"a deletion is still one work change"*, which gives two deletions plus two edits = 4.
   A fix loop that follows this finding as written writes an assertion its own library change fails. The single-file run then goes red, and the implementer has to choose between the finding's text and the code.
   **Fix:** in `finding_1.md`, Fix step 4, first `cli/test/unit-commit-lib.test.mjs` sub-bullet, change `work` to `5` to read `work` to `4`. Change nothing else. Leave the index pointer, the readiness entry and the severity as they are.

## Should Fix
_None._

## Nice to Have
_None._
