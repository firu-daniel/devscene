### 2. The commit-guard rows of record predate the library move and miss the decisions it changed

**Site:** `docs/guard-verification.md` → `#### The commit guard's amend and remit rows (fix_run_commit_trailer_amend)`: the **What this block records.** paragraph (*"is a non-git command other than a leading `cd`"*), the CG1–CG16 table, and **Which two trees these columns are.** (*"\"after\" is this checkout's `plugin/hooks` at `80119479`"*).

**The problem.** `.claude/context/plugin.md` → `## Guards, the shared library and the helper scripts` says: *"A change to any guard or to the library re-measures itself in `docs/guard-verification.md`."* The block records the guard at `80119479` (Task 4). Commit `25f7f047` then moved the ride-along answer into the library as `hc_commit_piece_may_ride_along`, and Finding 1 changes it again. Both change decisions. A leading `cd` now has to match an `hc_path_anchored_patterns` arm with its vetoes, so `cd <work>/<project>-x/.. && …` and a relative `cd sub && …` went from `allow` to silent. The arch-review fix measured those rows but did not record them: `harness-runs/architecture_branch_reviews/fix_run_commit_trailer_amend_arch_review/finding_1.md` → **Deviations from plan:** says *"Step 4's write to `docs/guard-verification.md` lies outside the dispatched `plugin` layer path and was not made"*. So the document of record shows the "after" column of a guard tree this branch no longer ships, and it names a `cd` rule (*"a non-git command other than a leading `cd`"*) that is no longer the rule. A reader who re-drives CG3's neighbours from this block would expect `allow` where the shipped guard is silent.

**Fix.** Do this after Finding 1 lands. Edit only this block.

1. Re-drive CG1–CG16, plus the new rows below, against `plugin/hooks` at the commit that lands Finding 1. Use the block's own fixture recipe, plus one more throwaway repository, `<other>`, on its protected `main`, built the same way. Drive through a probe under the run-artifact tree's `scratch/` directory with `bash scripts/scratch-run.sh`, from `/bin/bash`, on a fixture under the system temp directory. Take "before" from `52143799` with `git archive`, as the block already does. Record each payload's printed object, or "no output", and its exit status.
2. Append these rows to the table, numbered after CG16. Fill each "before" and "after" cell from the drive, not from this list:
   - `cd <work>/<project>-x/.. && git -C <dir> commit -m x` (ordinary): the veto case.
   - `cd <work>/<project>-x && git -C <dir> commit -m x` (ordinary): its control.
   - `cd sub && git -C <dir> commit -m x` (ordinary): a relative `cd`.
   - `git -C <dir> commit -m x && git -C <other> commit -m y` (ordinary `<dir>`, protected `<other>`): Finding 1.
   - `git -C <dir> commit -m x && git -C <other> add f` (same): Finding 1.
   - `git commit -m "$(cat <<'EOF'` / `fix: thing` / `EOF` / `)"` as one multi-line command (ordinary): Claude Code's default commit spelling.
   - `git commit -m "fix: handle <branch> names"` (ordinary): angle-bracket prose in a message.
3. Rewrite **What this block records.** so its list of SILENT conditions matches the guard's FAIL-CLOSED row word for word in substance:
   - a leading `cd` *"that an arm of `hc_path_anchored_patterns` grants through `hc_matches_any_pattern`, vetoes included"*;
   - a git piece *"that runs in a repository other than the one judged"*;
   - the answer is *"owned by the library's `hc_commit_piece_may_ride_along`"*.
4. In **Which two trees these columns are.**, replace `80119479` with the short id of the commit that lands Finding 1. Update the tool versions to the ones the re-drive printed.
5. In **What these rows establish.**, name the new rows by number: which are narrowings (`allow` → SILENT) and which are controls.
