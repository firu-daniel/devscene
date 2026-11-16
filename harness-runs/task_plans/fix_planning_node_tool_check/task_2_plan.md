### Task 2 — Log each session's withheld tools as one `[plan-drive]` line, and drive a walk whose sessions withhold `Glob, Grep`

**Goal:** Make the driver read `pnl_reap`'s `withheld=` key and write one `[plan-drive]` line to the run log for each session whose `init` event lacked declared tools, so a change in what Claude Code withholds is visible. Then prove with a whole walk that sessions withholding `Glob` and `Grep`, as Claude Code 2.1.325 does beside `Bash`, no longer park planning.

**Depends on:** Task 1, which makes `cli/templates/scripts/lib/planning-node-lib.sh` → `pnl_reap` print **`withheld=<names>`** on its own line, after `denials=` and before `reason=`. `<names>` is the agent's declared non-`mcp__` tools the `init` event lacks, in `tools:`-line order, joined with `", "` (e.g. `withheld=Glob, Grep`). It is empty when nothing is withheld or there is no `init` event, and it is printed for every `kind`. Task 1 also stops refusing a session for a lacking tool. Only an `init` tool the agent does not declare is still `kind=error`, `class=agent`. This task reads that key and changes nothing in `planning-node-lib.sh`.

**What this task deliberately does not do.** It adds **no observation** (`pd_observe`) for a withheld tool. Under 2.1.325, every writer and gate session of every run withholds `Glob, Grep`, so an observation per session would flood the improvement-observations intake with an already-recorded fact (story index `## Context`). The log line is the whole of the visibility.

### Targets

- `cli/templates/scripts/lib/planning-driver-lib.sh` — `pd_reap_one`.
- `cli/test/helpers/planning-driver.mjs` — the stub agent CLI's `mode` vocabulary and the module header that lists it.
- `cli/test/planning-driver-walk.test.mjs` — one new case.

**Work:**

- [ ] `pd_reap_one`: declare `withheld=""` among its locals, and add a `withheld=*) withheld="${line#withheld=}" ;;` arm to the `case` that parses `pnl_reap`'s output. After the existing `pd_log "#$seq $node: $kind…"` line, when `$withheld` is non-empty, write exactly one line:
  `pd_log "#$seq $node ($agent): the init event lacks declared tools [$withheld]; not refused"`
  which lands in the run log as, e.g., `[plan-drive] #1 plan_writer (task-plan-writer): the init event lacks declared tools [Glob, Grep]; not refused`. The line is written whatever the session's `kind`, and a stalled session, whose result the function overrides, still logs what its stream withheld. Keep Bash 3.2: no new array, no associative array.
- [ ] `cli/test/helpers/planning-driver.mjs`, `STUB_SOURCE`: add a `mode` value **`withhold`** that emits the `init` event's `tools` as the agent's declared list minus `Glob` and `Grep`, and only when that list includes `Bash`. That mirrors the measured 2.1.325 behaviour. The `result` event stays the normal `success` one, as for an entry with no `mode`. Add `withhold` to the header comment's `mode` list with one clause saying what it drops and when.
- [ ] `cli/test/planning-driver-walk.test.mjs`: add a case, for example *"sessions whose init withholds Glob and Grep beside Bash are not refused, and each is logged"*. It scripts `task-plan-writer`'s first call and `architecture-reviewer`'s first call with `{ mode: 'withhold' }` and drives once. Assert `r.status === 0`, and that the subjects include `chore: Flow progress P3 for ${BRANCH}` (planning handed off, with no park). Assert that `r.log` contains the exact line `[plan-drive] #1 plan_writer (task-plan-writer): the init event lacks declared tools [Glob, Grep]; not refused`, and a line beginning `[plan-drive] #` that names `architecture_review (architecture-reviewer): the init event lacks declared tools [Glob, Grep]`. Write every literal in the test, never read from the library. Assert too that no `lacks declared tools` line names `business-parity-reviewer` or `task-plan-reviewer`, which ran with no `mode`. The writer's `[Glob, Grep]` order follows `plugin/agents/task-plan-writer.md`'s `tools:` line (`… Bash, Glob, Grep, …`), which the fixture's plugin copy carries. If that line's order differs when you implement, write the literal in the order it actually has.

**Verification:**

- `cli/test/planning-driver-walk.test.mjs` passes. It is this task's own edited test file, and its new case shows a walk with withheld tools handing off and both `[plan-drive]` lines in the log.
- `bash scripts/typecheck.sh` exits 0.
- Read `pd_reap_one` once more and check that `withheld=` changes no routing: `kind`, `class`, `retry` and the recorded `--outcome` are computed exactly as before, and the only new effect is the one `pd_log` call.
