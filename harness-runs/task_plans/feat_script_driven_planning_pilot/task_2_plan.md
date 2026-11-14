### Task 2 — Add `lib/planning-record-lib.sh`: the planning commits, ledger flips, park and pause files and improvement observations

**Goal:** Ship the library through which the planning driver makes every durable write the autonomous planning fork makes today, by the same wrapper calls, under the same fixed subjects. It also writes the planning phase's improvement-observation entries.

**Where this library stops.** It writes what it is told to write. It does not decide when:
- which `round:` or `ledger:` line fires a commit, when a park, pause or hand-off happens, and what goes into a park's body are Task 3's (`lib/planning-driver-lib.sh`);
- the node results it records observations about come from Task 1's `pnl_reap`.

This task adds no `OUTER_LOOP_SCRIPTS` row; Task 4 does.

**The contracts it implements, cited rather than restated:**
- `plugin/instructions/task_plan_writing_instructions_autonomous.md` → `## Override 3 — commit the UI-test plan after it converges`, `## Override 4 — commit the task plan after it converges` (its seven-path list), `## Override 5 — pause/resume + flow-progress ledger (planning half)` (the `P1`–`P3` flips and the partial subject) and `## Override 6 — commit each plan-review round` (its six-path list);
- the same file's `## Clarification channel — file format (canonical, single source of truth)` (the index rule);
- `plugin/instructions/autonomous_pause_and_ledger.md` → `### 1.6 How to flip / create — direct `commit-on-branch.sh`, NEVER a committer dispatch` and `### 2.2 Honoring a PAUSE (driving fork, folded into the safety contract)`;
- `plugin/instructions/improvement_observations_instructions.md` → `## The entry format` and `## Commit mechanics` → **Machine-path check — before every wrapper call.**

### Targets

- `cli/templates/scripts/lib/planning-record-lib.sh` (new): the sourced library, functions prefixed `prl_`.
- `cli/test/planning-record-lib.test.mjs` (new): its suite.

**Work:**

- [ ] **Header, floors and `prl_init <branch> <worktree> <main_repo> <log_path>`.**
  - The header and `REPRO` block follow the same rules as Task 1's: no shell options, bash 3.2, `jq` 1.5, explicit `mktemp` templates, and no main-checkout anchor variable outside a comment.
  - `prl_init` resolves `stateDir` and `scriptsDir` through `lib/harness-run-lib.sh`.
  - **`prl_commit <subject> <path>…`** runs `bash <main_repo>/<scriptsDir>/commit-on-branch.sh --repo <worktree> <path>… -- "<subject>"` as one process, then `bash <main_repo>/<scriptsDir>/push-branch.sh <worktree>` as a separate one, unconditionally.
  - Exit 0, exit 3, and an exit 1 whose stderr opens `commit-on-branch.sh: committed ` are success. Any other exit returns 2, with the wrapper's stderr line as the cause.
  - Every narration line goes to `<log_path>` prefixed `[plan-drive]`.
- [ ] **The commits and the ledger.**
  - **`prl_round_commit <n>`**: Override 6's six paths, in its order, subject `chore: Plan round <n> for <branch>`.
  - **`prl_partial_commit <n>`**: the same paths, subject `chore: Plan round <n> partial for <branch>`.
  - **`prl_convergence_commits <ui_plan_written yes|no>`**:
    - with `yes`, Override 3's two paths and `chore: Add UI-test plan for <branch>`;
    - then, always, Override 4's seven paths and `chore: Add task plan for <branch>`.
  - **`prl_ledger_flip <id>`**, for `P1`, `P2` or `P3`:
    - rewrite the one `- [ ] <id>.` line of `<stateDir>/flow_progress/<branch>_progress.md` to `- [x] <id>.`, through a temp file and `mv`;
    - leave a `[x]` or `[-]` line untouched, so the flip is idempotent, and never flip a `[-]`;
    - commit the ledger with `chore: Flow progress <id> for <branch>`, then push;
    - a ledger with no such line is exit 2.
- [ ] **Park and pause.**
  - **`prl_park <raised_by> <q_title> <body_file>`** writes `<stateDir>/clarifications/<branch>/question_<n>.md`:
    - `<n>` is one above the highest index at the top level **and** under `answered/`;
    - the file opens on a title line, then `Raised by: <raised_by> (script-driven planning)`, then the body. When the body already carries `## Q<k>` headings it is kept verbatim; otherwise it goes under one `## Q1 — <q_title>`;
    - an existing question file is never overwritten;
    - then it logs `PARKED: <branch> — 1 question(s) at <stateDir>/clarifications/<branch>/`.
  - **`prl_pause <phase> <next_step>`**:
    - appends a timestamped entry, the phase and the exact next step to `<stateDir>/PAUSE_PROGRESS.md`, never overwriting it;
    - writes `<stateDir>/PAUSE_ACK`, without `touch`;
    - logs `PAUSED: <branch> — <phase>`.
- [ ] **Observations.**
  - **`prl_observe <category> <problem> <evidence> <cost>`** accumulates one block of `## The entry format`'s shape in a temp file. It refuses a category outside the seven, and folds newlines in `evidence` to spaces.
  - **`prl_observe_flush`**:
    - does nothing when nothing accumulated;
    - otherwise appends one label line `# Script-driven planning — <UTC ISO-8601 time>` plus the blocks to `<stateDir>/improvement_observations/<branch>.md`, creating the file when absent;
    - rewrites every occurrence of the home directory, `<main_repo>` and `<worktree>` to the repo-relative form plus `(main checkout)` where `## The entry format` requires that label;
    - re-checks with a fixed-string `grep` and commits only on a clean check, with `chore: Log improvement observations for <branch>`.

    It is best-effort: a failure is one log line and returns 0, never changing the caller's exit.
- [ ] **`cli/test/planning-record-lib.test.mjs`.**
  - Open it with the rule it enforces.
  - Each case builds a fixture repository with a bare `origin` under the system temp directory, using the isolated git config the fixture helper exports. It copies `lib/harness-run-lib.sh`, `commit-on-branch.sh`, `push-branch.sh` and this library from `cli/templates/scripts/`, and seeds a task-engine ledger.
  - Assert on the bytes on disk and on `git log`:
    - the round, partial and convergence commits carry exactly their path sets and subjects;
    - a second identical call commits nothing (exit 3 path);
    - a flip of `[x]` and of `[-]` changes nothing;
    - `prl_park` picks the index above one parked under `answered/`;
    - `prl_pause` appends to an existing `PAUSE_PROGRESS.md`;
    - a flushed block carries no fixture absolute path;
    - an empty flush writes no file.

**Verification:**

- `cli/test/planning-record-lib.test.mjs` passes, and its commits carry no attribution trailer, because the wrapper builds the message from the subject alone.
- Every subject in the new library matches, byte for byte, the subject the cited override spells. `chore: Add task plan for <branch>`, `chore: Add UI-test plan for <branch>`, `chore: Plan round <n> for <branch>`, `chore: Plan round <n> partial for <branch>`, `chore: Flow progress <id> for <branch>` and `chore: Log improvement observations for <branch>` each appear once.
