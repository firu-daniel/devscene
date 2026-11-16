### Task 18 — Re-point the supervised flows, the QA instructions and the instructions README at the commit step

**Goal:** Remove every remaining reference to the `committer` agent from the supervised item loops, the supervised QA instructions and the instructions directory's README.

- **The prefix source.** The supervised item loop's `## Commit conventions` currently sends the orchestrator to `committer.md`'s contract for its subject prefix. It now names the rule the wrapper applies: the branch-name token for new work, `fix` for a fix to existing work.
- **What stays the same.** The supervised flows keep committing items themselves, with the orchestrator as the committing role.

**Depends on:**

- **Task 1**, whose library computes the unit-commit prefix: `feat_` → `feat`, `fix_` → `fix`, `refactor_` → `refactor`, else `chore` for a story task; `fix` for every review-fix row; the severity mapping for a user-review item.
- **Task 9**, which renames the unit loop's columns to `commit unit`, `commit extra args` and `commit prefix`.

### Targets

- `plugin/instructions/plan_orchestration_instructions.md`
- `plugin/instructions/code_review_fixes_instructions.md`
- `plugin/instructions/user_review_fixes_instructions.md`
- `plugin/instructions/qa_test_instructions.md`
- `plugin/instructions/README.md`

**Work:**

- [ ] **`plan_orchestration_instructions.md` → `## Commit conventions`.**
  - **The prefix source.** Replace "Read `committer.md`'s own contract for the `commit_prefix` argument — the same source the dispatching flows' `commit_prefix rule` cells read —" with a pointer to `unit_loop_core.md` → `## Substitution table`'s `commit prefix` column, the rule the commit step applies.
  - **The prefix itself.** Use the designated prefix for the class: the branch-name token for new work, `fix` for a fix to existing work.
  - **What goes.** Delete the "no prefix designated" and "policy silent" paragraphs, which existed only to mirror the committer's `none` / fallback arguments.
  - **What stays.** Keep the fenced `<the designated prefix>: <short description …>` form and the **Never batch commits** note.
- [ ] **`code_review_fixes_instructions.md` and `user_review_fixes_instructions.md`.** Each carries "this flow dispatches no committer, so the orchestrator itself flips each entry … the `[ ]` → `[x]` transition always belongs to the committing role, which is the `committer` agent only in the flows that dispatch one". It becomes "this flow runs no commit step, so the orchestrator itself flips each entry … which is `commit-on-branch.sh --unit` only in the flows that run the unit loop".
- [ ] **`qa_test_instructions.md`.** "(via a `committer` `mode: ui_test_pass` dispatch)" → "(via a `commit-on-branch.sh --unit ui_test_pass` call)". "does **not** dispatch the committer" → "does **not** make that call". "the normal implementer / reviewer / committer agents" → "the normal implementer and reviewer agents and the commit step".
- [ ] **`plugin/instructions/README.md`.** Drop `committer` from the parenthesised agent list, "(`task-plan-writer`, `layer-implementer`, `layer-reviewer`, `branch-reviewer`, `qa-tester`, `committer` and the rest)".

**Verification:**

- `git grep -n -e 'committer' -e 'commit_prefix' -- plugin/instructions/plan_orchestration_instructions.md plugin/instructions/code_review_fixes_instructions.md plugin/instructions/user_review_fixes_instructions.md plugin/instructions/qa_test_instructions.md plugin/instructions/README.md` prints nothing.
- `git diff -- plugin/instructions/plan_orchestration_instructions.md plugin/instructions/qa_test_instructions.md` changes no heading line.
