### Task 8 — Replace `<committer_push>` with `<commit_call>` in the mode contract and the user-review-fix core

**Goal:** Declare the new mode-contract binding `<commit_call>` in the vocabulary, retire `<committer_push>`, and move the family-3 core — `user_review_fixes_instructions_core.md` — off every committer dispatch it describes.

**The binding, defined here and consumed by Tasks 9–12 and 20.** `<commit_call>` is the whole wrapper prefix a commit step issues ahead of its `--unit` / `--artifact` arguments: the main checkout's `commit-on-branch.sh`, `--repo <repo_root>`, and `--push` where the flow pushes.

- The autonomous forks bind it to `bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root> --push` (Tasks 11 and 12).
- The semi-autonomous forks bind it to `bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root>` (Task 20).

Every fork binds it. A commit step is a Bash call, not an Agent dispatch, so it takes no safety-contract step and moves no dispatch counter.

**Where this task stops.** The unit loop's own binding table and step 5 are Task 9's. The task-flow core is Task 10's. The forks are Tasks 11, 12 and 20's. Between this task and Task 20, the forks still bind `<committer_push>`; `## Context` names that interim state.

### Targets

- `plugin/instructions/mode_contract.md`
- `plugin/instructions/user_review_fixes_instructions_core.md`

**Work:**

- [ ] **`mode_contract.md`.**
  - **The vocabulary row.** Replace the `<committer_push>` row with a `<commit_call>` row: its meaning as defined above, bound by every fork. The "Exists because" cell cites `plan_orchestration_instructions_autonomous.md` → `## Mode contract — bindings`, an existing heading, and never a fork subsection.
  - **The `<per_unit_review>` row.** "between implementer and committer" becomes "between implementer and the commit step".
  - **`## Which files use this`.** The `unit_loop_core.md` entry declares `<escalate>`, `<per_unit_review>` and `<commit_call>`.
  - **Anchors.** Before changing a heading, grep `### Sanctioned cross-fork anchors` for any anchor naming `<committer_push>`; this task changes no heading.
- [ ] **`user_review_fixes_instructions_core.md` — header and binding table.**
  - **The header's reading line.** "Committer returns 5 lines (incl. `pushed:`), plus one for each of `staged: index-only` and `index_sync: failed` it adds. Read that, do not re-verify." becomes the same sentence about "The commit call prints".
  - **The `<per_unit_review>` row.** "runs between implementer and committer" → "… and the commit step".
  - **The binding row.** Replace the `<committer_push>` row with a `<commit_call>` row that lists every commit step this flow reaches through cited sections: the unit loop's commit step (rows `UR-A`, `E.3`, `G.4`), Phase E's per-test `--unit ui_test_pass` mark-pass and `--unit review_plan_file` QA-review commit, and Phase G's G.3 `--unit review_plan_file` test-fix-plan commit.
- [ ] **`user_review_fixes_instructions_core.md` — safety contract and budget prose.**
  - **The safety contract.** In `## Safety contract`, "(implementer, reviewer, committer — every single one)" becomes "(implementer, reviewer — every single one)". Delete the heartbeat example `[A · Item 3 · commit] → committer  (#14)`, and add one sentence: the commit step is a Bash call and takes no step of this contract.
  - **The dispatch-budget prose.** In the `MAX_TOTAL_DISPATCHES` paragraph, drop the per-test "`ui_test_pass` `committer` dispatch" and the "one `committer`" per failing gate round from what counts against the ceiling. Leave the numeric value unchanged.
- [ ] **`user_review_fixes_instructions_core.md` — the Phase QA restatements and the stop condition.**
  - **The restatements.** Each of these becomes the commit step's form:
    - "the qa-tester and committer behave identically" → "the qa-tester and the commit step behave identically";
    - "the committer's `mode: review_plan_file` fixed subject" → "`--unit review_plan_file`'s fixed subject";
    - "the `mode: review_item` index-agnostic checkbox flip" → "`--unit review_item`'s index-agnostic flip";
    - the per-test mark-pass sentence → `<commit_call> --unit ui_test_pass --plan <ui_test_index> --id <N>`;
    - the merged-index commit → `<commit_call> --unit review_plan_file --plan <qa_review_path>`;
    - the E.3 fix loop → the unit loop's `--unit review_item` with `--plan <qa_review_path>`;
    - the heartbeat example `[QA · qa · test 3 · mark-pass] → committer  (#N)` → deleted, the commit taking no heartbeat.
  - **The stop condition.** "`committer` returns `error:`" becomes "a commit call prints `error:`".

**Verification:**

- `git grep -n -e 'committer' -- plugin/instructions/mode_contract.md plugin/instructions/user_review_fixes_instructions_core.md` prints nothing.
- `git grep -n -F '<commit_call>' -- plugin/instructions/mode_contract.md` shows the vocabulary row and the `## Which files use this` mention.
- Every heading in both files is byte-identical to `git show HEAD:<file>`: `git diff -- <file>` shows no changed line beginning `#`.
