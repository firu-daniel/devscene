# Architecture review — round 1

verdict: PASS
review_mode: full

## Should Fix

1. **`task_1_plan.md` — the fixed in-record literals are not all module-level `Final` constants.** `.claude/context/devscene-flow-host.md` → `## Shared code and constants` requires that *"A record's fixed file name, directory name and fixed in-record literals are module-level `Final` constants in the module that reads or writes them"*. The Task 1 **Constants and the verdict** bullet lists `REVIEW_FILE_PREFIX`, `REVIEW_FILE_SUFFIX`, `MUST_FIX_HEADING` and `NO_SINGLE_VERDICT_LINE` as the constants to add. The other fixed literals `round_files.py` reads are written inline in the plan: the verdict lines `verdict: PASS` / `verdict: FAIL`, the `**Class:**` / `**Failure:**` markers and the `## ` heading prefix. The plan does not forbid making them constants, and the implementer reads the conventions document as well, so no step is certain to fail. That is why this is not a Must Fix. Add them to the bullet's constant list, as `records/ledger.py` does with `_RUN_MODE_HEADING` and `_SKIPPED_PREFIX`.

2. **`task_9_plan.md` — the README names one departure where Task 7 writes two markers.** Task 9's **Resuming a round** paragraph and its second Verification bullet refer to *"the one departure the `TODO: @claude` marker in `host/round_gates.py` names"*. Task 7 writes two entry-point markers in that module: the held-gate re-dispatch, and the non-round findings file that is required but not kept. The story index's `## Context` (**Two departures, each deferred with a marker.**) states both. A README written to Task 9 as worded would describe only one of them. This is outside the architecture lens (it is plan coherence), so it is noted here and does not gate.

## Nice to Have

1. **`task_5_plan.md` — say why the refusal file's reader sits in `host`.** `.claude/context/devscene-flow-host.md` → `## The internal layers` says *"Reading a record into a value is `records`"*. `host/refusals.py` reads and writes its own JSON file in `host`. That placement is sound: the file is host-owned walk position beside `host/store.py`, and the story index's `## Context` (**Decided here — where the refusal count lives.**) calls it position, not record. One clause in the module docstring's *"The rule:"* saying it is host state, not a repository record, would stop a later reviewer from reading it as a misplaced `records` reader.
