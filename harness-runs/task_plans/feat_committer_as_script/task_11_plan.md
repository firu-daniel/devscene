### Task 11 — Bind `<commit_call>` in the autonomous task fork and move its fixed-subject commits onto `--artifact`

**Goal:** Make `plugin/instructions/plan_orchestration_instructions_autonomous.md` bind `<commit_call>` and drop the `<committer_push>` procedure. Its own fixed-subject commits become single `--artifact … --push` calls: Override D's branch statistics and Override G's ledger flips. Update the autonomous task-flow command that summarises those bindings.

**Depends on:**

- **Task 3.** Its front end's `--artifact <kind> [--entry <id>] --push` commits the artifact table's paths under the table's fixed subject, then runs `push-branch.sh` after exit 0 or exit 3, so one call replaces the commit-then-push pair. Task 1's table includes:
  - `statistics` → `chore: Add branch statistics for <branch>`, path `<state_dir>/branch_statistics/<branch>/statistics.md`;
  - `ledger` → `chore: Add flow-progress ledger for <branch>`;
  - `ledger-flip` with `--entry <id>` → `chore: Flow progress <entry-id> for <branch>`, path `<state_dir>/flow_progress/<branch>_progress.md`.
  
  It prints `error: <line>` on a refusal (exit 1 / 2) and `error: nothing to commit` on exit 3.
- **Task 8**, which declares `<commit_call>` — the wrapper prefix ahead of `--unit` / `--artifact`.
- **Task 10**, which moves the core's phase commits onto it.

**The binding value for this fork:** `bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root> --push`.

**Where this task stops.** `autonomous_pause_and_ledger.md` §1.6, which this fork's ledger flips cite, is Task 13's. This task rewrites the flip *points* here and cites §1.6 for the call's form.

### Targets

- `plugin/instructions/plan_orchestration_instructions_autonomous.md`
- `plugin/commands/branch-start-plan-autonomous.md`

**Work:**

- [ ] **Bindings.**
  - **The opening.** The fork's opening paragraph names "the commit call (`<commit_call>`)" where it names "the committer push (`<committer_push>`)". The **Values only.** note names `<escalate>` and `<commit_call>`.
  - **The binding rows.** The `<per_unit_review>` row's "between an implementer and committer" → "… and the commit step". Replace the `<committer_push>` row with `| \`<commit_call>\` | \`bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root> --push\` — …` and point to the subsection below.
  - **The subsection.** Replace the ``### `<committer_push>` — `push: true` on every committer dispatch`` subsection with ``### `<commit_call>` — the main checkout's wrapper, with `--push` ``. It states that:
    - the call names `<MAIN_REPO>`'s copy, because that copy runs outside the sandbox;
    - every placeholder is spelled literally, with no `$`;
    - the push is best-effort inside the wrapper (`pushed: failed` never undoes the commit);
    - `error: nothing to commit` and `noop:` still push or commit nothing beyond what the wrapper states.
  - **Citers of the old heading.** Grep `plugin/` for the old heading text first. Its only citer outside this file, `mode_contract.md`, is rewritten by Task 8 to cite `## Mode contract — bindings`.
- [ ] **Override D.**
  - **The commit.** Replace the statistics commit block with `bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root> --artifact statistics --push`, spelled literally, one call.
  - **The prose.** Rewrite **Commit mechanism (direct `git` in the fork, not a committer dispatch).** as the artifact kind's commit. Delete the "existing `committer` modes do not fit" rationale; nothing is left to argue against. Delete the separate push paragraph, because `--push` carries it.
  - **What stays.** Keep the wrapper-exit handling. Exit 3 is a re-entry whose statistics already landed, and the landed exit 1 is now re-synced inside the wrapper.
- [ ] **Override G and the clean-tree list.**
  - **The flip points.** Each ledger flip becomes `bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root> --artifact ledger-flip --entry <entry-id> --push`, and creation becomes `--artifact ledger --push`. Cite `autonomous_pause_and_ledger.md` §1.6 for the form; keep its heading text byte-for-byte.
  - **Wording.** "its `review_plan_file` committer landed" → "its `--unit review_plan_file` commit landed". "the cleaning committer would fail too" → "the cleaning commit call would fail too".
  - **The clean-tree list.** In `## Autonomous-fork commit points — the clean-tree invariant (single source of truth)`, entries 9, 10 and 16 lose "(never a committer)" and the separate `push-branch.sh` call; each names its `--artifact` kind and `--push`.
  - **The other mentions.** Rewrite **Post-commit push.** so every commit point pushes through `--push` inside the wrapper. The docs flows' two-call form is the one exception, and stays as it is. Make the same change in the `<per_unit_review>`-off paragraph ("between an implementer and its committer") and **Interaction with the clean-tree invariant** ("the implementer→committer commit per unit … pushes via `<committer_push>`").
- [ ] **`plugin/commands/branch-start-plan-autonomous.md`.** In its three mentions, `<committer_push>` = `push: true` becomes `<commit_call>` = the main checkout's wrapper with `--push`. In the third-vocabulary list, `<committer_push>` → `<commit_call>`. Keep its `<MAIN_REPO>` `## Resolved values` row byte-for-byte: the corpus guard pins it.

**Verification:**

- `git grep -n -e 'committer' -- plugin/instructions/plan_orchestration_instructions_autonomous.md plugin/commands/branch-start-plan-autonomous.md` prints nothing.
- `git grep -n -F 'bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root> --push' -- plugin/instructions/plan_orchestration_instructions_autonomous.md` shows the binding row.
- `git grep -n -F -e '--artifact statistics --push' -e '--artifact ledger-flip --entry' -- plugin/instructions/plan_orchestration_instructions_autonomous.md` shows Override D and the flip points.
- `git grep -n -F 'chore: Add branch statistics for' -- plugin/instructions/plan_orchestration_instructions_autonomous.md` prints nothing. The subject now lives only in the library's table.
