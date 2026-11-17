### Task 22 — Close the roadmap row and document the front end and its library in the watcher and CLI references

**Goal:** Close `ROADMAP.md` → `## Flow and orchestration` → **Committer as a script**, and take the committer out of #380's list. Then document what the shipped wrapper now does in the two reference documents that inventory it: `docs/watcher.md`'s shipped-scripts table and `docs/cli.md`'s `## 6` sandbox paragraphs.

**Depends on:**

- **Task 3.** `commit-on-branch.sh` gains the front-end forms `--unit task|review_item|review_plan_file|ui_test_pass` and `--artifact <kind>`, with `--push`.
  - **New refusals.** It refuses a `--plan` / `--findings` / `--extra` / `--path` that leaves the target or `<state_dir>`, crosses a symbolic link, or, for `--plan`, is not a regular file.
  - **Where it reads.** It reads the stage set through the commit's own `GIT_DIR` / `GIT_INDEX_FILE` / `GIT_WORK_TREE` triple.
- **Task 2**, which ships `lib/unit-commit-lib.sh`, mode `644`, sourced and never run.
- **Task 20**, which deletes the `committer` agent.

**Catch-all task.** Its implementer reads every configured layer's conventions document, `.claude/context/cli.md` and `.claude/context/plugin.md` beside `.claude/context/conventions.md`. These documents describe a `cli` artifact consumed by `plugin` flows.

### Targets

- `ROADMAP.md`
- `docs/watcher.md`
- `docs/cli.md`

**Work:**

- [ ] **`ROADMAP.md`.**
  - **The closed row.** The **Committer as a script** row's status becomes `Done`. Its description states what shipped: `commit-on-branch.sh`'s `--unit` / `--artifact` front end over `lib/unit-commit-lib.sh`, replacing the `committer` agent. It names the follow-up the task prompt assigns elsewhere: the script-driven autonomous flow will source the library from its driver.
  - **#380's row.** In the **Structured agent outputs** row, drop "the committer's sha and subject" from the list. The wrapper's printed return is a script output, not an agent return.
- [ ] **`docs/watcher.md`.**
  - **The `commit-on-branch.sh` row.** Its "dispatched agents only" caller cell becomes "the orchestrating session's unit loop and fixed-subject commit points, through `--unit` / `--artifact`; the planning driver and the docs flows, through the plain form". Its description names the front end.
  - **A new row.** Add a row for `lib/unit-commit-lib.sh` in the libraries' shape: what it decides (entry tick, subject, body record, stage set, artifact table), "sourced by `commit-on-branch.sh`; never executed, and it ships without an executable bit", agent-invocable **no**.
- [ ] **`docs/cli.md` `## 6`.**
  - **The target-check paragraph.** In **The excluded rule's `:*` accepts any argument, so all four excluded scripts check their target first**, add one sentence: `commit-on-branch.sh`'s front end also refuses an index or folder argument outside the target's `<state_dir>`, or one reached through a symbolic link, before it reads or ticks anything.
  - **The pushed-failed sentence.** "every committer returns `pushed: failed`" → "every commit call prints `pushed: failed`". "the committers' returns" → "the commit calls' returns".
  - **Leave alone** every measured row and verdict citation.

**Verification:**

- `git grep -n -w committer -- ROADMAP.md docs/watcher.md docs/cli.md` prints only the closed roadmap row's own description of what it replaced.
- `git grep -n 'unit-commit-lib.sh' -- docs/watcher.md` shows the new row, and `git grep -n 'Committer as a script' -- ROADMAP.md` shows the row with `Done`.
