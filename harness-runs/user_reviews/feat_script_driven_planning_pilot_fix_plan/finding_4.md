### 4. Establish and test which gates a resume after an escalation park re-runs

**File:** `cli/templates/scripts/lib/planning-driver-lib.sh` (`pd_entry`) — "entry=plan_round"

**Problem.** After an escalation park is answered, `pd_entry` finds the saved walk finished. `flow-walker.sh current` re-prints `binding: <escalate>`, and `pd_entry` logs `saved walk finished (<escalate>): never continued`. It then starts a fresh walk with `flow-walker.sh start --entry <entry>`. No suite establishes whether that fresh round re-dispatches gates that already passed in the round that escalated. `cli/test/planning-driver-control.test.mjs` covers the `<ask>` resume, STOP, PAUSE and undelivered, but has no escalation-resume case. The user's rule: **gates that passed in that round must not run again unless the plan changed since their verdict (a writer revision ran). If the walker cannot tell, record that as the reason they re-run, in `docs/flow-graph-walker.md` → `## 5. The two drivers`.**

**What the code reads as today** (to confirm, not to assume):

- **With an answered pair** (the ordinary case: the escalation park's question/answer pair is top-level and is neither a Phase G nor a prompt-injection-screen origin), `pd_pairs` fills `PD_PAIRS`. The entry is then `plan_writer`, or `ui_writer` for a UI-loop origin, ahead of the `plan_round` branch. The writer runs with the answer appended, and the next round opens its whole set. That satisfies the rule only because a writer revision ran.
- **With no answered pair and the story index present**, the entry is `plan_round`. `flow-walker.sh start` then applies the complete-round rule (`flow-walker.sh` → STATE):
  - a round with files missing, whose evidence is consistent (no present gate `unreadable`, `plan:` `not-newer`), records the present gates' verdicts and opens the set with only the missing gates;
  - but **"a complete all-PASS round is reviewed again"**. If the escalated gate left a PASS findings file before it ended in `error`, for example a stall after writing, every gate re-runs with no plan change.
- After Finding 3, an escalation for an infra failure happens only once its attempts run out. Its park is the one this case resumes.

**Fix.**

1. **Establish the behaviour for each path**, by driving `pd_drive` against the fixture rather than by reading. For each path, record which gates the fresh round dispatches:
   - (a) the escalation park answered, entry `plan_writer` with the pair;
   - (b) entry `plan_round` with no answered pair, the escalated gate having written no findings file;
   - (c) entry `plan_round` with the escalated gate's findings file present.

   Also cover a UI-loop escalation entering at `ui_writer` if the fixture reaches it cheaply.
2. **Where a passed gate re-runs with no writer revision since its verdict, and the walker can tell**, fix the entry so that gate is not re-dispatched. The walker can tell when `fw_round_evidence` reports `plan:` `not-newer` and the gate's findings file for that round is present and readable. Prefer a driver-side fix in `pd_entry`, for example by choosing `--entry plan_round` and not `plan_writer` when the only pending pairs answer a gate escalation the writer has nothing to act on. A change to `flow-walker.sh`'s complete-round rule touches the orchestrated path too: take it only if the driver cannot express the fix, and state the reason in the walker's header. Path (a) re-runs the gates after a writer revision, which the user's rule permits, so it needs no fix.
3. **Where the walker cannot tell** (for example, path (c) cannot separate a PASS file written by a session that then failed from a clean PASS), the gates re-run. Record that reason, and which paths re-run passed gates and which do not, as a short decision/reason/cost block in `docs/flow-graph-walker.md` → `## 5. The two drivers`. A new `### A resume after an escalation park` subsection fits the section's existing shape. Record the paths that re-run nothing that passed there too, so the section states the established behaviour in full.
4. **Tests.** In `cli/test/planning-driver-control.test.mjs`, one case per path established in step 1, each built like the existing `'<ask>: questions park with the return text, and an answer resumes the saved walk'` case:
   - drive to an escalation park, using an agent-reported `blocker` on one gate so no retry intervenes, or an infra failure on all three attempts once Finding 3 lands;
   - write the answer file for the park's question;
   - drive again;
   - assert which gates' call indices advanced in the second drive. Passed gates are not re-dispatched on the `plan_round` path with no writer revision. On the `plan_writer` path the writer runs first and then the whole set.

   If the stub needs a mode to leave a findings file and then fail (path (c)), add it to `cli/test/helpers/planning-driver.mjs` and to its header.

**Established behaviour (cli layer, by driving `pd_drive` against the fixture with an agent-reported `blocker` on `architecture-reviewer` in round 0):**

- **Before the fix**, the escalation park committed nothing of round 0: a held join prints no `round:` line, so `prl_round_commit` never ran, and after the park `git status` showed the story index, `task_plans/`, `business_parity_reviews/` and `task_plan_reviews/` untracked. The resume's `start --entry plan_round` therefore read `plan: unknown`, so path (b) re-dispatched all three gates in round 0 (`business-parity-reviewer#1 architecture-reviewer#1 task-plan-reviewer#1`) with no writer revision. The walker could not tell, but only because the driver had not committed the evidence.
- **The fix** (`cli/templates/scripts/lib/planning-driver-lib.sh` → `pd_escalate_park`): when the escalation carries `held:` lines, the driver commits the round's planning artifacts with `pd_partial` (subject `chore: Plan round <n> partial for <branch>`, `<n>` the set's `arg.iteration:`) before `prl_park`. This is the same commit the PAUSE and undelivered self-pause paths already make. `flow-walker.sh` is unchanged.
- **Path (a), answered pair:** entry `plan_writer`. The writer runs first, then all three gates in round 1. This needed no fix; the rule permits it because a writer revision ran.
- **Path (b), no answered pair, the escalated gate wrote no file:** entry `plan_round`. With the fix, only `architecture-reviewer` is dispatched, at round 0. The passed gates are not re-dispatched.
- **Path (c), no answered pair, the escalated gate left a PASS file:** entry `plan_round`. The round is complete and all-PASS, so the walker's complete-round rule ("a complete all-PASS round is reviewed again") re-dispatches all three gates in round 0 with no writer revision. **The walker cannot tell**: from the files alone, a PASS written by a session that then failed looks the same as a clean PASS, and convergence is never inferred from files. This is the reason passed gates re-run on this path. The cli layer leaves it as it is.
- **Path (d), answered pair, the escalated gate left a PASS file:** behaves as (a): entry `plan_writer`, the writer runs, then round 1's whole set. Pinned by `escalation resume (d)` (review_2 Must Fix 1, option 1).
- **UI-loop escalation entering at `ui_writer`:** not covered. The fixture runs `phases.qa` `false` and hands off without entering the UI loop, so reaching that path is not cheap.

**Deviations from plan:**
- The fix is in `pd_escalate_park`, not `pd_entry`. The defect was that the evidence was uncommitted at the park, not the entry choice. Entering at `plan_round` for gate-escalation pairs, as the plan suggested, would still have re-run every gate under `plan: unknown`.
- Step 3, the `docs/flow-graph-walker.md` → `## 5. The two drivers` → `### A resume after an escalation park` block, is outside the `cli` path scope and is left for the `general` layer dispatch. The behaviour it records is the list above.
- The escalation-park commit is a divergence from the autonomous fork (`task_plan_writing_instructions_autonomous.md` defines a `Plan round <n> partial` commit only for Override 5's PAUSE and the API-overload self-pause, and Override 6 commits a round only on a `round:` line). The orchestrated path does not make it, so path (b) re-dispatches only the escalated gate on the script-driven path only; the orchestrated path still leaves the held round uncommitted (not driven in this unit; by the same `plan: unknown` reading as the pre-fix driver, it would re-run every gate). The `general`-layer docs block must record this. The divergence is stated in `planning-driver-lib.sh`'s module header (review_0 Must Fix 1).
- Step 3 (`general` layer): the `### A resume after an escalation park` block is placed directly after `### How each runs a parallel round`, whose closing sentences cover the park that this subsection resumes. The orchestrated path's re-run of every gate is recorded as inferred from `flow-walker.sh` → `STATE`, not driven, because no unit drove it.
- Path (b)'s case drives again with no answer file written, because an answer file would make an answered pair and enter at `plan_writer`, which is path (a).
