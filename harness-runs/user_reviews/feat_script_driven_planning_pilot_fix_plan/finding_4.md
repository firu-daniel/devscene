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
