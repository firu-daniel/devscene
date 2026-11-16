### 1. A unit's deletion at the repository top is refused, and one whose parent directory is gone is never committed

**Site:**
- `cli/templates/scripts/lib/unit-commit-lib.sh` → `ucl_stage_set`, the `D*)` arm: `ucl_fail "the deletion '$p' sits at the repository top; its parent would stage the whole tree"`.
- `cli/templates/scripts/lib/unit-commit-lib.sh` → the header paragraph `THE STAGE-SET LISTING`, sentence `Residual: a deletion whose parent directory is gone too is skipped by the wrapper and not committed.`
- `cli/templates/scripts/commit-on-branch.sh` → the staging loop under the comment `# STAGING POLICY (header). The count guard is required`, the check `if [ ! -e "$top/$p" ]; then` and the `rel=""` normalization below it.
- `cli/templates/scripts/commit-on-branch.sh` → the header paragraphs `STAGING POLICY, AND THE ONE TRAP IN IT` and `THE STAGE SET` (*"a deletion staged as its parent directory (STAGING POLICY)"*), and the REPRO line `deleted path      rm "$d/f.txt"; passing `f.txt` -> a "skipping" line,`.
- `cli/test/unit-commit-lib.test.mjs` → `test('ucl_stage_set refuses a deletion at the repository top', …)` and `test('ucl_stage_set stages a deletion as its parent directory and excludes the findings folder from the work count', …)`.
- `cli/test/commit-on-branch-unit.test.mjs` → `test('a deletion is staged as its parent directory', …)`.
- The self-adopted copies `scripts/lib/unit-commit-lib.sh` and `scripts/commit-on-branch.sh`, which must stay byte-identical to the templates.

**Problem.** `ucl_stage_set` stages a deletion as its parent directory, because the wrapper's staging loop skips any path that does not exist in the working tree (`commit-on-branch.sh: path '…' does not exist under '…' — skipping`). Two cases come out wrong:

1. **A deletion at the repository top is refused.** `ucl_stage_set` returns 2, the wrapper prints `error: …`, exit 1, and the unit loop (`plugin/instructions/unit_loop_core.md` → `## The unit loop` step 5) `<escalate>`s. So any unit that deletes or renames a root-level file (`README.md`, `ROADMAP.md`, `ARCHITECTURE.md` here; any root file in an adopter's catch-all layer) cannot commit and halts the run. `plugin/agents/layer-implementer.md`, rewritten on this branch, tells the implementer the opposite: a rename is `Write <new>` then `rm <old>`, and *"the commit step stages both halves"*. For a root file that sentence is false.
2. **A deletion whose parent directory was removed too is silently dropped.** This happens when a unit deletes a whole directory. The library stages `<parent>/`, the wrapper finds no `<parent>/` under the target and prints only a `skipping` warning, and the commit lands without the deletion. The next unit's listing shows the same `D` lines and drops them the same way, so the run finishes with the tree still holding files the implementation deleted. No exit code and no return line reports it. The library header records this as a "Residual", but it is a silent loss of work in deterministic code that can avoid it.

**Staging an ancestor is not the fix.** Replacing the refusal with `.`, or climbing a missing parent to its nearest existing ancestor, would stage far more than the listing. The wrapper's directory arm (`if [ -d "$top/$p" ] && [ ! -L "$top/$p" ]; then`) expands a directory into every path the tip holds under it (`main_git ls-tree -r -z "$old_tip" -- "$rel"`) plus every index and untracked path there, and all of them go through the `NO FILTER DRIVER RUNS` check (`wt_git check-attr -z --stdin filter`). That check fails the whole commit if **any** of them carries a `filter` attribute, even one that did not change. So with `.`, an adopter repository holding one filter-attributed tracked file anywhere (git-lfs is the common case) would still refuse every top-level deletion, and a climbed ancestor could pull an unrelated filtered file into a commit that never touched it. Each such commit would also list and hash the whole tree.

The narrow fix is to commit the deleted path itself. `hr_commit_paths_var` already supports this: `hr_run_blob_var` returns `HR_RUN_BLOB_MODE=0` for a leaf or a parent that does not exist, and the loop writes that as a removal record (`printf '0 %s\t%s\0' "$null" "$rel"`). The only thing stopping it is the wrapper's skip-with-warning check, which treats "absent from the working tree" as "optional and not there" even when the tip holds the path.

**Fix.** Make the wrapper commit an absent path the tip holds as a removal, and have the library stage each deleted path as itself.

1. **`commit-on-branch.sh`, staging loop.** Move the `/*)` absolute-path refusal and the `rel` normalization (`rel=""` … the `while [ -n "$rest" ]` loop) above the existence check. Then replace the existence check with this, so an absent path that the tip holds is committed as the removal of every blob the tip holds at or under it, and an absent path the tip does not hold is still skipped with the same warning:

   ```bash
       if [ ! -e "$top/$p" ]; then
         : >"$work/listing"
         if [ -n "$rel" ] && ! main_git ls-tree -r -z "$old_tip" -- "$rel" >"$work/listing"; then
           fail 1 "commit-on-branch.sh: refusing to commit: git could not list '$p' at '$branch' (see output above)"
         fi
         if [ ! -s "$work/listing" ]; then
           echo "commit-on-branch.sh: path '$p' does not exist under '$top' — skipping" >&2
           continue
         fi
         while IFS= read -r -d '' entry; do
           case "$entry" in 160000\ *) continue ;; esac
           printf '%s\0' "${entry#*	}" >>"$work/paths"
         done <"$work/listing"
         continue
       fi
   ```

   The `ls-tree -r` form covers both a deleted file (it lists that one path) and a deleted directory passed by a caller (it lists every blob the tip held under it), and it skips a gitlink exactly as the directory arm does. The `${entry#*	}` pattern carries a literal tab, as in the directory arm. Only paths the tip holds at or under the deleted path reach `check-attr`, so an unrelated filter-attributed file is never pulled in. The existing tolerance is unchanged for the case it exists for: an optional path absent from both the tip and the working tree (an empty per-finding folder, say) is still skipped with the warning, and still never fails the commit.

2. **`unit-commit-lib.sh`, `ucl_stage_set`.** Delete the `D*)` arm's whole `case "$status" in … esac` block, so a deleted path is emitted unchanged, like any other changed path. Keep the de-duplication loop and the `UCL_WORK_COUNT` count as they are: a deletion is still one work change.

3. **Headers.**
   - In `unit-commit-lib.sh` → `THE STAGE-SET LISTING`, replace the two sentences from `A deletion is` through `and not committed.` with: *"A deleted path is staged as itself; the wrapper commits an absent path the tip holds as a removal (`commit-on-branch.sh` → STAGING POLICY)."*
   - In `commit-on-branch.sh` → `STAGING POLICY, AND THE ONE TRAP IN IT`, rename the paragraph `STAGING POLICY.` and replace the text from `A path that does not exist is` through `keeps an absent optional path from failing a commit.` so it says: a path absent from the working tree that the tip holds, as a file or a directory, is committed as the removal of every blob the tip holds at or under it; a path absent from both is skip-with-warning rather than a hard error. Keep the existing sentences explaining why callers pass their paths unconditionally and must not add an existence check, and why the check is made against `<repo_top>/<path>`. Keep the directory and gitlink sentences. Delete the `THE TRAP` sentences: passing the exact deleted path now commits the deletion, and passing its parent directory still does too.
   - In `commit-on-branch.sh` → `THE STAGE SET`, replace *"a deletion staged as its parent directory (STAGING POLICY)"* with *"a deletion staged as the deleted path (STAGING POLICY)"*.
   - In the REPRO line `deleted path`, replace `passing `f.txt` -> a "skipping" line, exit 3, the deletion NOT committed; passing `.` instead -> exit 0` with `passing `f.txt` -> exit 0`, keeping `and `git -C "$d" ls-files f.txt` prints nothing`. Add a second REPRO case: passing a path neither the tip nor the working tree holds -> a "skipping" line, exit 3.

4. **Tests.**
   - `cli/test/unit-commit-lib.test.mjs`:
     - Replace `test('ucl_stage_set refuses a deletion at the repository top', …)` with `test('ucl_stage_set stages a deletion at the repository top as itself', …)`. It runs the listing `['D', 'README.md']` and asserts status `'0'`, `staged` equal to `[PLAN, 'README.md']`, and `work` `1`.
     - In `test('ucl_stage_set stages a deletion as its parent directory and excludes …', …)`, rename it to `… stages a deletion as itself and excludes …`. Change the expected `staged` to `[PLAN, FINDINGS, 'src/a/old.ts', 'src/a/older.ts', 'src/b.ts', 'src/c.ts']` and `work` to `4`.
   - `cli/test/commit-on-branch-unit.test.mjs`:
     - Rename `test('a deletion is staged as its parent directory', …)` to `test('a deletion is staged as the deleted path', …)`. Its assertions do not change.
     - Add four `--unit task` cases against the fixture. Seed a `[ ] **Task 1**` readiness entry for each, as the existing deletion test does.
       - **Top-level deletion.** Delete a top-level tracked file. Assert exit 0 and that `git ls-files <file>` at the new tip prints nothing.
       - **Whole-directory deletion.** Delete a whole tracked directory. Assert exit 0 and that `git ls-tree -r <new tip> -- <dir>` prints nothing.
       - **The two deletions above with an unrelated filtered file.** First seed and commit a `.gitattributes` with `kept/lfs.bin filter=lfs` and a tracked `kept/lfs.bin`, through the fixture's own seed commit. Then repeat the top-level and the whole-directory deletions, each in its own case. Assert exit 0, that each deletion is committed, and that `git diff --name-only <old tip> <new tip>` names neither `kept/lfs.bin` nor `.gitattributes`.
   - `cli/test/commit-on-branch-plumbing.test.mjs`:
     - Add `test('(d2) A deletion is committed by passing the deleted path itself', …)`. It is the same as `(d)`, but calls `f.commit(['dir/gone.txt'])` and makes the same assertions.
     - Leave `(c)` as it is. `missing.txt` is held by neither the tip nor the working tree, so it is still skipped with the warning.
   - Run only those three files, each through the single-file test command.

5. **Self-adopted copies.** Copy both edited templates byte-for-byte over `scripts/lib/unit-commit-lib.sh` and `scripts/commit-on-branch.sh`.

- **Deviations from plan:**
  - Fix step 4, the two filtered-file cases in `cli/test/commit-on-branch-unit.test.mjs`: the plan specified `kept/lfs.bin filter=lfs`. Implemented as `filter=marker`. With `filter=lfs`, both cases exited 1 before the staging loop: `error: refusing to commit: git could not list the changes in '<wt>' against 'feat_w'`, preceded by `git-lfs filter-process: git-lfs: command not found`. The wrapper drops `GIT_CONFIG_GLOBAL` (`hr_git_env_drop`, the residual recorded in `cli/test/helpers/fixture.mjs`), so the host's `~/.gitconfig` `filter.lfs.process` runs during THE STAGE SET's `git diff` listing. The `check-attr` refusal these cases guard does not depend on the driver's name, so `marker` exercises the same path. Out of this finding's scope and flagged to the orchestrator: on a host where git-lfs is configured but not installed, that listing runs the filter and fails.
  - Fix step 5 (copy both templates over `scripts/lib/unit-commit-lib.sh` and `scripts/commit-on-branch.sh`): not done. Those paths are outside the dispatched `cli` layer path. They need a `general`-layer dispatch, or the committer, to copy them byte-for-byte; until then the self-adopted copies still hold the old behaviour.
  - Fix step 5, closed by the `general`-layer dispatch: the template diff was replayed onto `scripts/lib/unit-commit-lib.sh` and `scripts/commit-on-branch.sh` hunk by hunk with the edit tool (a `cp` call was refused by the permission mode). `cmp` against each template exits 0 with no output, and `git diff --summary -- scripts` reports no mode change.
