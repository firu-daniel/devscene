### Task 10 — Move the task-flow core's review-file and mark-pass commits onto `<commit_call> --unit`

**Goal:** Rewrite `plugin/instructions/plan_orchestration_instructions_core.md` so every commit it spells is one `<commit_call>` Bash call rather than a `committer` dispatch: phases A1.5.2, A2.2, B.3, C2.3, E.1, E.2 and G.3.

**Depends on:**

- **Task 3.** Its front end takes:
  - `<commit_call> --unit review_plan_file --plan <index> [--extra <dir>]`, which stages the index, its per-finding folder and `--extra` unconditionally, under the fixed subject `chore: add code review for <branch>`;
  - `<commit_call> --unit ui_test_pass --plan <index> --id <N>`, which flips the `**Test N**` entry and commits only the index, under `chore: Mark UI test N passing for <branch>`.
  
  An already-`[x]` test prints `noop: UI test N already marked` and exits 0. The per-finding folder is derived by the wrapper: `${plan%.md}/` for a sibling-`.md` index, the index's own folder for the QA merged `qa_review_<iteration>.md`. Returns and exits are as in the story index's `## Context`.
- **Task 8**, which declares `<commit_call>`.
- **Task 9**, which rewrites the unit loop and renames its `commit unit` / `commit extra args` / `commit prefix` columns.

### Targets

- `plugin/instructions/plan_orchestration_instructions_core.md`

**Work:**

- [ ] **Header, bindings and safety contract.**
  - **The header's reading line.** "Committer returns 5 lines …" becomes "The commit call prints 5 lines … Read that, do not re-verify."
  - **The binding rows.** The `<per_unit_review>` row's "between implementer and committer" → "… and the commit step". The `<committer_push>` row becomes `<commit_call>`, used by the unit loop's step 5 and the phase commits listed below.
  - **The safety contract.** In `## Safety contract`, "(implementer, reviewer, committer — every single one)" → "(implementer, reviewer — every single one)". Delete the heartbeat example `[A · Task 3 · commit] → committer  (#14)`. Add one sentence: a commit call is a Bash call and takes no step of this contract.
- [ ] **The four review-file phases A1.5.2, A2.2, B.3 and C2.3.** Each "Spawn `committer` …" with its fenced `mode: review_plan_file` block becomes a fenced one-line call, spelled literally:
  - A1.5.2: `<commit_call> --unit review_plan_file --plan <parity_review_path>`.
  - A2.2: `<commit_call> --unit review_plan_file --plan <arch_review_path>`.
  - B.3: `<commit_call> --unit review_plan_file --plan <code_review_path> --extra <review_plan_review_folder>`.
  - C2.3: `<commit_call> --unit review_plan_file --plan <skeptic_review_path> --extra <skeptic_review_meta_folder>`.
  
  **The existence guard.** Delete the "The existence guard is yours" paragraphs: `--extra` is passed unconditionally, and the wrapper skips an absent path with a warning (`<scripts_dir>/commit-on-branch.sh` → **STAGING POLICY, AND THE ONE TRAP IN IT**). Rewrite the "index-agnostic, derives the folder by stripping `.md`" parentheses as the commit step's behaviour.
- [ ] **Phase E.**
  - **E.1's mark-pass.** It becomes `<commit_call> --unit ui_test_pass --plan <ui_test_index> --id <N>`. Delete the heartbeat `[E · qa · test 3 · mark-pass] → committer  (#N)` and the safety-contract step before it. Its idempotence sentence quotes the `noop: UI test N already marked` line.
  - **E.2's commit.** It becomes `<commit_call> --unit review_plan_file --plan <qa_review_path>`. Its **Subject is fixed.** paragraph cites `<scripts_dir>/commit-on-branch.sh` → **THE SUBJECT AND ITS RECORD** instead of `committer.md` → the subject-line step.
  - **The re-test paragraph and the opening.** The re-test paragraph's "via the `mode: ui_test_pass` committer dispatch" and "The committer's idempotent `noop:`" become the commit step's. In the phase opening, "the normal implementer / reviewer / committer agents" becomes "the normal implementer and reviewer agents and the commit step".
- [ ] **Phase G and the stop conditions.**
  - **G.3.** "Apply the safety contract (heartbeat `[G · test-fix-plan · commit] → committer …`), then spawn `committer`" with its block becomes `<commit_call> --unit review_plan_file --plan <test_fix_plan_path> --extra <test_fix_review_folder>`. Delete its existence-guard paragraph, as above.
  - **The stop condition.** In `## Stop conditions`, "`committer` returns `error:`" → "a commit call prints `error:`".
  - **The phase bindings blockquotes.** Where the E and G "Two flow-dependent vocabularies" blockquotes list `<committer_push>`, list `<commit_call>`.

**Verification:**

- `git grep -n -e 'committer' -e 'mode: review_plan_file' -e 'mode: ui_test_pass' -e 'meta_findings_folder' -- plugin/instructions/plan_orchestration_instructions_core.md` prints nothing.
- `git grep -n -F -e '--unit review_plan_file --plan' -- plugin/instructions/plan_orchestration_instructions_core.md` lists one call per review-file phase. `git grep -n -F -e '--unit ui_test_pass --plan <ui_test_index> --id <N>' -- plugin/instructions/plan_orchestration_instructions_core.md` shows E.1.
- `git diff -- plugin/instructions/plan_orchestration_instructions_core.md` changes no heading line, so every `→ ### A1.5.2 …` / `### G.1 Run the gates` citation elsewhere still resolves.

- **Deviations from plan:**
  - The first verification grep (`committer` prints nothing) also matched four sites the Work list did not name. They were rewritten so the grep holds:
    - `## Setup` step 5's `MAX_TOTAL_DISPATCHES` bullet: dropped the per-passing-test `committer` dispatch and the G.3 `committer` from the dispatch accounting, and stated that both commits are Bash calls and count nothing. The `≈2–3×` multiplier was removed because it counted the mark-pass dispatch; no new figure replaces it.
    - E.2 step 1: "`committer.md` resolves the readiness entry by that token alone" became "the commit step resolves …".
  - "mark-pass dispatch" / "duplicate dispatch" became "mark-pass call" / "duplicate call" in E.1, E.2 and E.4, because no dispatch remains.
  - The `<commit_call>` binding row's Phase D note now says Phase D issues no `<commit_call>` and calls the statistics commit "a fork-added operation". It no longer says "direct-`git`", which the autonomous fork's Override D no longer does.
