# Code Review: feat_script_driven_planning_pilot

## Context

**Branch:** `feat_script_driven_planning_pilot`
**Date:** 2026-11-15
**Reviewed:** the whole branch diff against the default branch `dev`. No local `dev` ref exists in this checkout, so the base was `origin/dev...HEAD`. The diff covers 26 files:
- Task 10: the two clarification-index answers moved into `lib/harness-run-lib.sh`.
- Tasks 1–3: the three planning libraries `lib/planning-node-lib.sh`, `lib/planning-record-lib.sh` and `lib/planning-driver-lib.sh`.
- Task 4: their `OUTER_LOOP_SCRIPTS` rows and README and template mentions.
- Task 5: the stub-driven suites.
- Task 6: the watcher wiring (`PLANNING_DRIVER_PLUGIN_DIR`, `session_exec`, `engine_pipeline`, `planning_driver_ready`, `planning_driver_run`).
- Task 7: the plugin side (step 4a, the core's note, the observation intake's second writer).
- Tasks 8–9: the docs and the `ARCHITECTURE.md` §5 row.

21 run-artifact files excluded from the reviewed diff.

The diff was checked against the task prompt and against `docs/flow-graph-walker.md`'s **What a second driver must do.** These hold:
- The safety contract runs per set (STOP per block, PAUSE once, the cap against the whole set, nothing launched in part).
- Recording happens in finish order through `flow-walker.sh next --node`.
- Siblings are not cancelled on `error`, `blocker` or a stall kill.
- The commit subjects and path sets match the autonomous fork's Overrides 3–6 byte for byte.
- `P2` → Overrides 3/4 → `P3` keeps the fork's order.
- The pilot is off by default and job mode is excluded.

`.claude/context/conventions.md` → `## What accompanies a new unit of each kind`, row *An outer-loop script*, was checked for each of the three new libraries (`planning-node-lib.sh`, `planning-record-lib.sh`, `planning-driver-lib.sh`). All three members hold for all three libraries:
- **(a) The row.** Each library has its own row in `cli/src/generators/outerLoopScripts.ts` → `OUTER_LOOP_SCRIPTS` (`subdir: 'lib'`, `mode: 0o644`) with `agentInvocable: false`. The flag is set on purpose: the comment above the rows says the watcher's planning driver sources them from its own `lib/` and nothing runs them.
- **(b) The permission profile.** `cli/src/generators/permissionProfile.ts` → `selectOuterLoopScripts` and `fromWrittenOuterLoop` both filter on `script.agentInvocable`. So an `agentInvocable: false` row gets no profile entry, which is correct for a file no agent is dispatched to run. No entry is owed.
- **(c) The deny list.** `OuterLoopScript.agentInvocable`'s doc comment says the script-allowlist guard auto-allows any `.sh` under `scriptsDir` whose basename it does not deny. So a library run directly through the guard must be harmless. Each library's top level is only variable assignments and function definitions (checked line by line), so running one does nothing. The rows' claim that no `DENY_SCRIPT_BASENAMES` entry is owed holds, and `plugin/hooks/autonomous-script-allowlist-guard.sh` correctly lists none of them.

The one `cli/src` change (`cli/src/generators/outerLoopScripts.ts`) and its test were checked against `.claude/context/cli.md`:
- **A generator change lands with a case that drives the compiled CLI against a throwaway fixture repository (`## What "done" means here`).** `cli/test/outer-loop-scripts.test.mjs` adds `test("the planning driver's three libraries land verbatim under scriptsDir/lib, and a re-run keeps them", …)`. It builds each fixture with `fixtureFor` and runs `initOk` twice; both go through `cli/test/helpers/fixture.mjs`, whose helpers run the compiled `dist/cli.js`. It covers both the generated and a relocated `scriptsDir`, and asserts the template's bytes, the single landing site under `lib/`, mode `0o644`, and that a second `init` leaves each file as it was. This holds.
- **The shipped tables are single declarations of their sets (`## How a module in this layer is written` → "One string, one producer.").** `git grep` finds `planning-node-lib`, `planning-record-lib` and `planning-driver-lib` in `cli/src` only in the three new `OUTER_LOOP_SCRIPTS` rows. The watcher's `PLANNING_DRIVER_LIBS="planning-node-lib planning-record-lib planning-driver-lib"` in `cli/templates/scripts/autonomous-watcher.sh` falls outside the rule. The rule binds this layer's TypeScript sources, which resolve, join or read a table's names as paths. The watcher is a shipped template, copied verbatim into the adopter's `scriptsDir`, and the sibling files it sources from its own `lib/` there are the rows' output, not a second declaration of the table. This holds.
- **A reviewer holds a change to its module's own header (`## What "done" means here`).** The header's list of shipped files now names "the planning driver's three libraries". The header's ordering rule (a row arrives in the same change as its template, never before it) is met: the branch adds `cli/templates/scripts/lib/planning-node-lib.sh`, `planning-record-lib.sh` and `planning-driver-lib.sh` together with their rows. The rows' comment matches what the rows do. Each library only defines functions, `agentInvocable: false` is a calling convention, and the watcher that runs the driver is withheld because `autonomous-watcher.sh` is in `plugin/hooks/autonomous-script-allowlist-guard.sh` → `DENY_SCRIPT_BASENAMES`. This holds.

The four plugin-layer files (`plugin/commands/branch-start-plan-autonomous.md`, `plugin/instructions/task_plan_writing_instructions_core.md`, `plugin/instructions/improvement_observations_instructions.md`, `plugin/docs/AUTONOMOUS_FLOW.md`) were checked against `.claude/context/plugin.md`:
- **The reader set of each new wire literal (`## Verifying a change in this layer`: a wire is verified by the grep that re-derives its readers).**
  - `PLANNING IS SCRIPT-DRIVEN ON THIS LAUNCH`: `git grep -nF` finds step 4a, the watcher's `planning_clause` in `spawn_engine`, the watcher's header comments, `docs/watcher.md` and `cli/test/watcher-planning-driver.test.mjs`'s `CLAUSE`. All spell it byte for byte, and the clause step 4a matches on is the prefix the watcher writes. This holds.
  - `PLANNING HANDED TO SCRIPT: <branch>`: its only occurrence is step 4a. No script, doc or test reads it, and the watcher decides the hand-off from the setup session's exit, `PAUSE_ACK`, the open questions and the ledger (`planning_driver_run`). This is a narration line no rule prescribes and nothing reads, so it does not hold: Finding 5.
  - `# Task run (Phase D)`, `# Script-driven planning — ` and `chore: Log improvement observations for <branch>` in `improvement_observations_instructions.md` match `planning-record-lib.sh`'s `PRL_CLOSING_LABEL`, its flush `printf` and its `prl_commit` subject byte for byte. This holds.
- **Rule 4 of `## Cores, forks and the single-owner rule` (cores are literal-free).** The core's new note carries no reader-naming escalation phrase, no slash-command name, no absolute machine path and no step a mode deletes. It names the scripts only through `<scripts_dir>`, which the core's `## Resolved values` table declares. This holds.
- **The headings the note makes wire text, against what `planning-node-lib.sh` extracts (`## Writing agent prose`: never paraphrase a wire literal or a cited anchor).** Every heading `PNL_CORE_SETUP_HEADING` and `PNL_CORE_BLOCKS` name exists verbatim in the core, and so does the `MAX_TOTAL_DISPATCHES = 40` line under `## Setup (once per session)` step 4. So the lib's parse resolves. The note itself, though, calls the setup heading `## Setup` and leaves out the six `###` headings and the per-`###` fence count the lib also keys on. That does not hold: Finding 4.
- **Step 4a's cited anchors.** `## Override 5 — pause/resume + flow-progress ledger (planning half)`, its **Create the ledger at Setup.**, **Record the run mode in that same write.** and **Who reads first.** paragraphs and its `P0` bullet all resolve in `task_plan_writing_instructions_autonomous.md`. This holds.

`harness-runs/lessons.md` → `## Unattended control loops` (*"Every automatic retry in an unattended path is bounded by a count or a deadline …"*) was checked against the diff's one new automatic retry, `pd_undelivered`:
- **The bound holds.** It is three consecutive undelivered sets. The first is re-dispatched at once and the second after a backoff of `PD_BACKOFF_SECS`, capped at 60s. On the third, `prl_pause` pauses the run and the driver returns 3. A delivered set (`pd_main`'s `out` arm) or any other set result resets `PD_STRIKES` to 0.
- **Exactly one notification fires.** It is `classify_run_exit`'s local `notify paused`, reached through `planning_driver_run`'s 3 → 0 mapping and `PAUSE_ACK`. That notification names the manual way on but not the error, so the lesson is not met: Finding 3.

Every task-prompt test case has a suite: the walk, sets, held binding, undeclared outcome, `<ask>` park and resume, STOP and PAUSE mid-set, the cap, undelivered sessions and observations. Whether those suites pass is the Run gates phase's to establish, because this review runs no suite. The Pass 0 sweep of added lines found no recursive removal, no `git add -A`, no `set -e` in a library, no machine path and no line coordinate. Every new shell function has a caller outside its definition. `phases.parity` is `false`, so no parity cross-check applies. Pass 2 had nothing to reconcile: the per-unit findings root holds no review folders. Two findings need a fix before merge (Findings 1 and 3). Two are Should Fix (Findings 4 and 5). One is wording (Finding 2).

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 2** — Reword the step-4a clause in the engine command's `## Context` sentence so it parses _(layer: plugin)_
2. [x] **Finding 5** — Drop the unread `PLANNING HANDED TO SCRIPT` narration line from step 4a _(layer: plugin)_
3. [ ] **Finding 4** — Name every heading, the cap line and the per-heading fence count `planning-node-lib.sh` keys on in the planning core's script-driven note _(layer: plugin)_
4. [ ] **Finding 1** — Record the planning plugin directory's `.mcp.json` in the placeholder manifest when the pilot is on _(layer: cli)_
5. [ ] **Finding 3** — Name the undelivered-dispatch overload in the planning driver's self-pause notification _(layer: cli)_

---

## Must Fix

### 1. The placeholder manifest leaves out the plugin directory that every planning node session adds with `--add-dir`
→ [finding_1.md](feat_script_driven_planning_pilot_code_review/finding_1.md)

### 3. The planning driver's undelivered-dispatch self-pause sends a notification that does not name the error
→ [finding_3.md](feat_script_driven_planning_pilot_code_review/finding_3.md)

---

## Should Fix

### 4. The planning core's script-driven note names only part of the text `planning-node-lib.sh` keys on
→ [finding_4.md](feat_script_driven_planning_pilot_code_review/finding_4.md)

### 5. Step 4a adds its own narration line, `PLANNING HANDED TO SCRIPT: <branch>`, which nothing reads
→ [finding_5.md](feat_script_driven_planning_pilot_code_review/finding_5.md)

---

## Nice to Have

### 2. The engine command's `## Context` sentence on step 4a does not parse
→ [finding_2.md](feat_script_driven_planning_pilot_code_review/finding_2.md)

---

## Intentional divergences — confirm

_None: `phases.parity` is `false`, so there is no reference implementation to diverge from._
