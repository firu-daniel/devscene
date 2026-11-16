### Task 12 — Bind `<commit_call>` in the autonomous user-review-fix fork and move its fixed-subject commits onto `--artifact`

**Goal:** Make `plugin/instructions/user_review_fixes_instructions_autonomous.md` bind `<commit_call>` and drop the `<committer_push>` procedure. Its own fixed-subject commits become single `--artifact … --push` calls: Override D's statistics update, Override G's ledger flips and Override L's UI-test-plan augment. Update the autonomous user-review-fix command's summary of those bindings.

**Depends on:**

- **Task 3.** Its front end's `--artifact <kind> [--entry <id>] --push` commits the table's paths under the table's fixed subject and then pushes, after exit 0 or exit 3. Task 1's table includes:
  - `statistics-update` → `chore: Update branch statistics for <branch>`, path `<state_dir>/branch_statistics/<branch>/statistics.md`;
  - `ledger-flip` with `--entry <id>` → `chore: Flow progress <entry-id> for <branch>`;
  - `ui-test-plan` → `chore: Add UI-test plan for <branch>`, paths `<state_dir>/ui_test_plans/<branch>_ui_test_plan.md` and `<state_dir>/ui_test_plans/<branch>/`.
  
  Those two UI-test paths are the `<ui_test_index>` and `<ui_test_files_dir>` that `user_review_fixes_instructions_core.md` → `## Setup` defines.
- **Task 8**, which declares `<commit_call>`.

**The binding value for this fork:** `bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root> --push`, the same string Task 11 binds in the task fork.

### Targets

- `plugin/instructions/user_review_fixes_instructions_autonomous.md`
- `plugin/commands/branch-start-user-review-fix-autonomous.md`

**Work:**

- [ ] **Bindings.**
  - **The opening and notes.** The opening's "the committer half of Override E (`<committer_push>`)" → "the commit call (`<commit_call>`)". The **Values only.** note names `<commit_call>`.
  - **The binding rows.** The `<per_unit_review>` row → "… and the commit step". Replace the `<committer_push>` row with `| \`<commit_call>\` | \`bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root> --push\` — …`.
  - **The escalation list.** "a `committer` returning `error:`" → "a commit call printing `error:`".
  - **The subsection.** Replace ``### `<committer_push>` — `push: true` on every committer dispatch`` with ``### `<commit_call>` — the main checkout's wrapper, with `--push` ``, worded as Task 11 words the task fork's.
- [ ] **Override D and Override E.**
  - **The statistics update.** It becomes `bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root> --artifact statistics-update --push`, one call. Delete the "existing `committer` modes do not fit" rationale and the separate push paragraph.
  - **Override E's push delta.** Every commit this fork lands is pushed by `--push` inside the wrapper; only the docs phase keeps its own two-call form. The parenthesis about the task flow's Override D using `chore: Add branch statistics for <branch>` names the kind `statistics` instead.
- [ ] **Override G and the pause notes.**
  - **The flips.** The `## Fixing` flips become `--artifact ledger-flip --entry <entry-id> --push` calls in §1.6's form, citing `autonomous_pause_and_ledger.md` §1.6 by its unchanged heading.
  - **The pause notes.** "a `qa-tester` PASS whose mark-pass committer never landed" → "… whose mark-pass commit never landed". The **Commits** summary bullet names the wrapper's `--push`.
- [ ] **Override L and the command.**
  - **Override L's commit.** It becomes `bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root> --artifact ui-test-plan --push`, one call. Drop "Substitute the writer's returned `ui_test_index:` and `ui_test_files_dir:` values" and the separate push.
  - **One sentence.** Add it: the artifact table's two paths are this flow's `<ui_test_index>` and `<ui_test_files_dir>`, and a writer returning other paths is a `<escalate>`.
  - **What goes and what stays.** Delete **Why not a committer dispatch.** Keep **Shared rationale.** and its entry number.
  - **`plugin/commands/branch-start-user-review-fix-autonomous.md`.** In its three mentions, `<committer_push>` = `push: true` → `<commit_call>` = the main checkout's wrapper with `--push`. Keep both of its `<MAIN_REPO>` clause occurrences byte-for-byte: the corpus guard counts two there.

**Verification:**

- `git grep -n -e 'committer' -- plugin/instructions/user_review_fixes_instructions_autonomous.md plugin/commands/branch-start-user-review-fix-autonomous.md` prints nothing.
- `git grep -n -F -e '--artifact statistics-update --push' -e '--artifact ui-test-plan --push' -e '--artifact ledger-flip --entry' -- plugin/instructions/user_review_fixes_instructions_autonomous.md` shows Overrides D, L and G.
- `git grep -n -F 'chore: Update branch statistics for' -- plugin/instructions/user_review_fixes_instructions_autonomous.md` prints nothing.
