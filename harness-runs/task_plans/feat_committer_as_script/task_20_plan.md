### Task 20 — Delete the `committer` agent and re-home its `<MAIN_REPO>` resolution in the semi-autonomous forks

**Goal:** Delete `plugin/agents/committer.md` once nothing dispatches it, and in the same unit move the `<MAIN_REPO>` resolution clause it carried for supervised-checkout flows into the two semi-autonomous forks. Those forks now bind `<commit_call>` and spell `<MAIN_REPO>` in it. The resolution module's roster swaps the one file for the two in the same unit too.

**Depends on:**

- **Tasks 8–19**, which leave no file under `plugin/` dispatching `committer`, passing it a `mode:`, or citing `agents/committer.md` — except the roster and the README this task edits.
- **Task 6**, after which the expected `<MAIN_REPO>` clause carriers are the files listed in `plugin/instructions/main_repo_resolution.md` → `## Who may cite this`, with a count of 1 per carrier, and every roster entry must name an existing file. A carrier and its roster entry therefore move in the same unit.
- **Task 8**, which declares `<commit_call>` in `mode_contract.md`: the wrapper prefix ahead of `--unit` / `--artifact`, bound by every fork.

**The binding value for both semi-autonomous forks:** `bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root>` — no `--push`, because these flows leave commits unpushed for the human merge step.

### Targets

- `plugin/agents/committer.md` (deleted)
- `plugin/agents/README.txt`
- `plugin/instructions/main_repo_resolution.md`
- `plugin/instructions/plan_orchestration_instructions_semi_autonomous.md`
- `plugin/instructions/user_review_fixes_instructions_semi_autonomous.md`

**Work:**

- [ ] **Confirm, then delete.** `git grep -n -e 'agents/committer.md' -e 'dispatch `committer`' -e 'spawn `committer`' -e 'Spawn `committer`' -e 'mode: review_plan_file' -e 'mode: ui_test_pass' -- plugin` must list only `plugin/agents/committer.md`, `plugin/agents/README.txt` and `plugin/instructions/main_repo_resolution.md`.
  - **Any other hit** is an earlier task's unfinished site: report it as a blocker naming the file, and do not delete.
  - **Otherwise** delete `plugin/agents/committer.md` with a plain `rm` naming that one tracked path. The commit step stages the deletion through its parent directory.
- [ ] **The two semi-autonomous forks.** In each:
  - **`## Resolved values`.** Add the `<MAIN_REPO>` row, copied byte-for-byte from the row `git show HEAD:plugin/agents/committer.md` carries. It holds the clause and the literal-spelling sentence the corpus guard counts. Add a `<scripts_dir>` row (`scriptsDir`, the wrappers' directory, invoked under `<MAIN_REPO>`), and correct the preamble's token count.
  - **The binding rows.** Replace the `<committer_push>` row with `| \`<commit_call>\` | \`bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root>\` — …`. Its cell says there is no `--push`, because this flow deliberately leaves commits unpushed for the human merge step. The `<per_unit_review>` row's "between implementer and committer" → "… and the commit step".
- [ ] **`plugin/instructions/main_repo_resolution.md` → `## Who may cite this`.** Remove `${CLAUDE_PLUGIN_ROOT}/agents/committer.md`. Add `${CLAUDE_PLUGIN_ROOT}/instructions/plan_orchestration_instructions_semi_autonomous.md` and `${CLAUDE_PLUGIN_ROOT}/instructions/user_review_fixes_instructions_semi_autonomous.md` in the list's existing order.
- [ ] **`plugin/agents/README.txt`.** Drop the committer from the two roster sentences ("…, the committer, …"). Remove the paragraph about `committer`'s mode-step range: its `grep -n 'steps 1–' plugin/agents/committer.md` sweep names a file that no longer exists. Keep every other sample-pointer note byte-for-byte.

**Verification:**

- `git grep -n -w committer -- plugin` prints exactly one line, the heading `### 1.6 How to flip / create — direct `commit-on-branch.sh`, NEVER a committer dispatch` in `plugin/instructions/autonomous_pause_and_ledger.md`. Task 13 kept it byte-for-byte because `cli/test/flow-walker-resume.test.mjs` and Task 21's suite cite it, and it stays true.
- `test -e plugin/agents/committer.md` exits non-zero.
- `git grep -c -F 'resolves, and a stop with its sentence when it resolves none' -- plugin/instructions/plan_orchestration_instructions_semi_autonomous.md plugin/instructions/user_review_fixes_instructions_semi_autonomous.md` reports each file once.
- `git grep -n -F '<committer_push>' -- plugin` prints nothing, and `git grep -l -F '<commit_call>' -- plugin/instructions` lists both semi-autonomous forks.

**Deviations from plan:**

- `plugin/instructions/main_repo_resolution.md` → `## Who may cite this`: the sentence after the list stated *"no document beyond these 26"*. The roster went from 26 entries to 27 (one removed, two added), so it now says 27. The plan did not mention this edit. The count was taken by listing the `- ` lines under that heading after the edit.
- `test -e plugin/agents/committer.md`: the tool did not show this command's exit status. The deletion is shown instead by `git status --short`, which lists ` D plugin/agents/committer.md`.
