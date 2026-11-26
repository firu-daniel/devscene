# Task plan review — round 2

verdict: PASS
review_mode: converging

## Should Fix
- **`task_9_plan.md` — the module docstring does not name the bash code that `read_pair_text` reads as.** `.claude/context/devscene-flow-host.md` → `## What accompanies a new unit of each kind` requires a record reader to have "a docstring naming the bash reader it reads as". Task 9's *"The rule:"* bullet names only `hr_top_level_answered_pairs` and `pd_raised_by`. The bash code that reads a pair file's text is `cli/templates/scripts/lib/planning-driver-lib.sh` → `pd_pairs_text` (its `grep -qF` / `cat "$abs"`). Name `pd_pairs_text` as the code `read_pair_text` reads as. This is a docstring only, so it is not a Must Fix (`finding_grades.md` → `## Never a Must Fix on its own`).
- **`task_9_plan.md` / `task_11_plan.md` — the new `RecordError` cases differ from the bash behaviour they port, and nothing records the difference.** `pd_pairs_text` does not stop on a missing or non-UTF-8 pair file: `cat` passes the bytes through, or prints nothing plus an error, and the prompt is still built. `read_pair_text` raises in both cases, and Task 11 lets that error propagate out of the first writer build. Refusing is consistent with this layer's `RecordError` rule (`.claude/context/devscene-flow-host.md` → *"`RecordError` is the one anticipated failure of reading a repository record"*), so it is a sound choice. Record it as a difference, though: either in Task 16's README `## Differences from flow-walker.sh`, or in Task 11's docstring. Then the first run-mode cutover (#424) will not find it by surprise.

## Incidental findings (not gating)
- Round 1's Should Fix and Nice to Have items for `task_2`, `task_4`, `task_7`, `task_13`, `task_14` and `task_16`, and for the story index's `Manual setup required:`, were not re-checked. They are outside this round's changed text.
