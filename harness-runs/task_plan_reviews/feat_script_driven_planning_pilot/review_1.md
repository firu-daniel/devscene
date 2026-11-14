# Task plan review — round 1

verdict: FAIL
review_mode: full

## Must Fix

1. **`task_10_plan.md` — the new suite reads a tree of repository files as text, and no task registers it as a tree guard**
   Task 10's **Source guard** case scans every file under `cli/templates/scripts/` and asserts that only `lib/harness-run-lib.sh` defines `hr_max_question_index()` or `hr_top_level_answered_pairs()`. That makes `cli/test/clarification-index-lib.test.mjs` a test that reads a tree of repository files as text, not one module or one fixed file. `plugin/instructions/unit_loop_core.md` → `## The test-run rule` point 8 requires such a test to get a `treeGuards` entry in `devscene.config.json`, either in the same change or from a later catch-all-layer task that the adding task names. It grades a plan whose adding task names no registering task as a Must Fix for every reviewer. Task 10 names no such task. Neither catch-all task, Task 8 nor Task 9, lists `devscene.config.json` among its `### Targets`. This tree already has the precedent: `test/watcher-main-anchor.test.mjs` is registered with `covers: "cli/templates/scripts/**"`. Without an entry, a later unit that adds a second definition under `cli/templates/scripts/` never runs this guard.
   **Raised against:** "no file under `cli/templates/scripts/` other than `lib/harness-run-lib.sh` defines `hr_max_question_index()` or `hr_top_level_answered_pairs()`."
   **Must hold:** Every tree-reading test the plan adds is either registered as a `treeGuards` entry by a task that `task_10_plan.md` names, or narrowed so that it reads only fixed files and owes no entry.
   **Fix:** Pick one of these.
   - **Register it.** In `task_10_plan.md`, name the registering task. Add that registration to a `general`-layer task, Task 8 or Task 9, as a Work bullet plus a `devscene.config.json` line under `### Targets`. The entry is `{ "test": "test/clarification-index-lib.test.mjs", "covers": "cli/templates/scripts/**/*.sh" }`, or a `covers` glob the writer argues for.
   - **Narrow it.** Rewrite the Source guard case so it reads only named, fixed files: `autonomous-watcher.sh`, `lib/harness-run-lib.sh`, and the planning libraries by path. Then state in the suite's header that it reads fixed files only.

## Should Fix

- **`task_1_plan.md` ↔ `task_5_plan.md` — a consumer that does not consume.** Task 1 says its declared heading list is one *"which Task 5's suite reads"*. Task 5 never reads it, and says every expected literal is *"written in the suite, never read from the graph, the walker or the library under test"*. Drop the claim from Task 1, or have Task 5 restate what it reads from that list.
- **`task_2_plan.md` → `prl_observe_flush`: a failed commit leaves the intake file behind.** The observations commit is best-effort and returns 0 on any failure. `plugin/instructions/improvement_observations_instructions.md` → `## Commit mechanics` requires the opposite for a non-landed exit 1 or an exit 2: the edit is reverted, and on a branch-moved exit 1 the wrapper is called again to re-stage the path. Otherwise the tree is dirty-tracked when the engine session's clean-tree checkpoint runs after hand-off. State whether the driver applies that revert rule. If it does not, say why the hand-off is still clean.
- **`task_3_plan.md` → `pd_entry` (a), carried over from round 0.** This round rewrote the bullet, but case (a) still fires on answered pairs with no story index. `## Override 2 — resumability` (a) requires that *"Story index exists AND clarification answers are pending"*. With no story index and no usable `<ask>` walk, the fork takes (c), a fresh start, while the driver takes **extend**. Either encode the condition, or state the deliberate divergence and its reason.
- **Story index `## Context` — the cross-half boundary, carried over from round 0.** `.claude/context/conventions.md` → `## The layers` says the halves are coupled *"in one direction"*. On this branch, `cli/templates` scripts read plugin headings, the agent files' `tools:` lines and `plugin.json` as wire text at run time. Say how this squares with that rule, and raise it as a `stale-rule` entry in `## Corpus staleness`.

## Nice to Have

- `task_4_plan.md` → `outerLoopScripts.ts`: the `OuterLoopScript.agentInvocable` doc comment lists by name the `false` rows for which *"`false` is a calling convention rather than a gate"*. Adding the three planning libraries to that list would keep the interface comment and the new rows' comment in agreement.
