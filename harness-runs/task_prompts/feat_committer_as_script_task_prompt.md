`feat_committer_as_script` replaces the `committer` agent with a deterministic commit step in `commit-on-branch.sh`, and moves the orchestrator's own fixed-subject commit points onto the same step. It closes `ROADMAP.md` → `## Flow and orchestration` → **Committer as a script** (row 3).

## Why

Every committed unit costs one `committer` dispatch: a subagent that reads a 178-line contract (`plugin/agents/committer.md`) and the commit policy, only to do three mechanical things. It ticks one readiness checkbox, stages what `git status` shows, and calls `commit-on-branch.sh`. The one place it uses judgment is the subject. It chooses the wording, chooses whether the unit token survives, and decides how a title that is too long or carries marks gets cut. That is exactly what a commit subject should not depend on.

Most of the commit prose is already deterministic in practice. The orchestrator's fixed-subject commit points (task plan, ledger, statistics, lessons, …) call `commit-on-branch.sh` directly with a fixed string. The script-driven planning driver already commits from a script (`cli/templates/scripts/lib/planning-record-lib.sh` → `prl_commit`).

> ⚠️ **Find every anchor in this prompt by its quoted text, heading or function name, never by line number.**

## What to read first

- `plugin/agents/committer.md`: the whole contract this replaces. Its modes (`task`, `review_item`, `review_plan_file`, `ui_test_pass`), the stage-path rules, **Subject reconciliation**, the exit mapping and the `## Output contract`.
- `cli/templates/scripts/commit-on-branch.sh`: its header, above all **THE TARGET IS NOT TRUSTED**, **GIT NEVER RE-READS THE TARGET'S RECORDS** and **MESSAGE ARGUMENTS**.
- `cli/templates/scripts/lib/planning-record-lib.sh` → `prl_commit`: how a script caller interprets the wrapper's exits today.
- `plugin/instructions/unit_loop_core.md` → `## The unit loop` step 5 and `## Substitution table` (the `committer mode`, `committer extra args` and `commit_prefix rule` columns, rows `A`, `A1.5.3`, `A2.3`, `C`, `C2.4`, `E.3`, `UR-A`, `G.4`).
- `plugin/instructions/plan_orchestration_instructions_core.md` phases A1.5.2, A2.2, B.3, C2.3, E.1, E.2 and G.3 (the `review_plan_file` / `ui_test_pass` dispatches).
- Every orchestrator commit point that calls `commit-on-branch.sh` directly: `grep -rn "commit-on-branch.sh" plugin/`.
- `.claude/context/conventions.md` → `## Commit-message policy`.
- The readers of commit history: `plugin/agents/statistics-plan-writer.md` and `plugin/instructions/improvement_observations_instructions.md` (`record disposition of `, and the `mark … done — ` index-only frame).
- `cli/templates/claude/settings.autonomous.json`: the `excludedCommands` entry and the `allow` spellings for `commit-on-branch.sh`.

## The goal

1. **No `committer` agent.** `plugin/agents/committer.md` is deleted, and nothing in `plugin/` dispatches it. Every flow that dispatched it (supervised, semi-autonomous and autonomous alike) makes one `commit-on-branch.sh` call instead.
2. **The orchestrator's fixed-subject commit points use the same step.** Each one names an artifact kind rather than spelling a subject and a path set in prose.
3. **Every subject is built mechanically from the index, never judged.**
4. The `ROADMAP.md` row is closed.

## The design, already settled

- **The logic lives in a sourced library**, `cli/templates/scripts/lib/unit-commit-lib.sh` (name for planning to confirm). It ticks the readiness box, computes the stage-path set, builds the subject, and holds the table of artifact kinds. `commit-on-branch.sh` gains a thin front end over it:
  ```
  commit-on-branch.sh --repo <root> --unit <mode> --plan <index> --id <K> [--push]
  commit-on-branch.sh --repo <root> --artifact <kind> [--push]
  ```
  (flag spelling for planning to settle). The existing `--repo <root> <paths> -- "<subject>"` form stays as it is, so `prl_commit` and the watcher do not change.
- **Why the wrapper and not a new script.** An orchestrator session's Bash runs sandboxed. `commit-on-branch.sh` under the main checkout is already one of the four `excludedCommands` and already has a literal `allow` spelling. A new script would be a fifth excluded command, with its own profile entries and its own sandbox measurements. Extending the wrapper adds neither.
- **Why a library.** The script-driven autonomous flow (`ROADMAP.md` → **Script-driven autonomous flow**) will move the autonomous unit commit into the driver, which runs outside the sandbox. It will source this library and call the plain wrapper the way `prl_commit` does. The `--unit` / `--artifact` front end stays for the supervised and semi-autonomous flows, which keep the unit loop in a session. That driver wiring is **not** this branch's.
- **The subject.** `<prefix>: <unit label> — <short title>`, at most 72 characters:
  - `<prefix>` follows today's per-class rule in `## Commit-message policy`, computed by the script: the branch-name token for a story task, `fix` for the review-fix rows, the severity mapping for `UR-A`.
  - `<unit label>` names the unit and, for findings, which review it came from, because finding numbers repeat across reviews. For example: `Task 3`, `Code review finding 2`, `User review finding 4`, `Test fix 1`. The script derives it from the row / `plan_path`.
  - `<short title>` is the readiness entry's title with its `_(layer: …)_` / `_(points: …)_` markers removed. It is normalised (`` ` ``, `$`, `|`, `<` and `>` removed, words kept) and cut at a word boundary to fit. The unit label is always present, so the committer's "identifier survives" fallback disappears.
  - Examples: `feat: Task 1 — Add the clone trust check to the run library`, `fix: Code review finding 2 — Refuse a symlinked plan path`.
- **Fixed-form subjects are unchanged**, byte for byte, `for <branch>` included. The artifact table carries the current strings from `## Commit-message policy` → **Fixed-form subjects**.
- **Disposition and index-only records move to body lines.** The subject is always the title subject. A dispositioned unit carries `record disposition of <unit token> — <cause>` on a body line. The script reads the cause from the unit's detail file (`## Disposition`), never from the command line. An already-passing close and an index-only commit carry their records on a body line the same way. The readers in `statistics-plan-writer.md` and `improvement_observations_instructions.md` already scan every line for `record disposition of `. The index-only reader (the `mark … done — ` frame) moves from the subject to any line. The parsed substrings stay byte for byte.
- **The return.** The wrapper prints the lines the callers read today (`commit_sha:`, `subject:`, `files_committed:`, `plan_flipped:`, `pushed:`, and `staged: index-only` / `index_sync:` when they apply), so the readers in the cores change as little as possible.

## Constraints

- **The new code runs with full access, so it treats the target as untrusted, as the header already does.** `--plan` must resolve inside the target, be a regular file and not a symlink. The tick goes through a temporary file beside the index and `mv`. A subject built from index text is normalised before use. The stage set is read with the same `GIT_DIR` / `GIT_INDEX_FILE` / `GIT_WORK_TREE` the commit uses, never with a plain `git -C <target> status`. Each new refusal gets a header paragraph and a test.
- **The staging discipline does not change:** an explicit path set, never `git add -A`, a deletion passed as its parent directory, and the unit's findings folder staged and excluded from the work files, as `committer.md` step 3 states today.
- **The orchestrator's call stays spellable as a literal:** no `$`, no free text, nothing the script-allowlist guard or the profile's literal `allow` entry would refuse.
- **One subject, one source.** Until the graph work switches `prl_commit` to the library, the planning driver's callers keep their hardcoded fixed subjects (`chore: Add task plan for <branch>`, `chore: Add UI-test plan for <branch>`, `chore: Flow progress <entry-id> for <branch>`, `chore: Log improvement observations for <branch>`). A test asserts that each one matches the library's artifact table byte for byte, so the two cannot drift silently.
- **The orchestrator reads nothing new.** It passes the readiness index path and the unit token `K` it already holds from step 1 of the unit loop. The wrapper, not the orchestrator, reads the index entry and the unit's detail file. The orchestrator's rule against reading detail files (`unit_loop_core.md` → `## The unit loop` steps 1–2) is kept as it stands.
- No new `excludedCommands` entry and no new permission in any profile.
- Bash 3.2 and jq 1.5 floors. No new runtime dependency.
- `.claude/context/conventions.md` → `## Commit-message policy` and `cli/templates/claude/context/conventions.md` describe the new free-form subject and the body-line records. Every file that quotes a changed literal changes with it (`grep -rn` the literal across `plugin/` and `cli/templates/`).
- `bash scripts/typecheck.sh` and `scripts/run-gates.sh` pass.

## Interaction with #380

#380 lists `committer` among the agents that get a structured return. Whichever lands second adjusts. If this lands first, `committer` leaves #380's list, and the wrapper's printed return is a script output, not an agent return.

## Proposals, for planning to settle rather than constraints

- **Order.** Library and `--unit` front end with tests first. Then the unit-loop rows and the `review_plan_file` / `ui_test_pass` phases. Then `--artifact` and the orchestrator's fixed-subject commit points. Then the deletion of `committer.md` and the conventions/policy edits. No task leaves a caller dispatching an agent that no longer exists.
- **`--push` inside the wrapper** so a commit point is one call. Otherwise keep the separate `push-branch.sh` call; planning decides.
