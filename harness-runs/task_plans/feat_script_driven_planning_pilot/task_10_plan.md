### Task 10 — Move the clarification channel's two index scans into `lib/harness-run-lib.sh` as `hr_max_question_index` and `hr_top_level_answered_pairs`

**Goal:** Give the clarification channel's two index answers one shell definition each, in the library every outer-loop script already sources, so the watcher, the planning record library (Task 2) and the planning driver (Task 3) all take them from the same code. Today both live only in `cli/templates/scripts/autonomous-watcher.sh`, which the planning libraries' suites never source. A second, library-private scan of the same directories would drift on numeric-only names, zero padding or base-10 handling with no failing test, and the clarification digest keys on these indices (`plugin/instructions/task_plan_writing_instructions_autonomous.md` → `## Clarification channel — file format (canonical, single source of truth)`).

This task ships first. It changes no behaviour: the watcher calls the same logic under the library's names.

**Why the names gain the `hr_` prefix.** Every function `lib/harness-run-lib.sh` defines carries `hr_`, and a sourced library's prefix is what keeps its names from colliding with a sourcing script's own. So the two functions move as `hr_max_question_index` and `hr_top_level_answered_pairs`, and every watcher call site is renamed with them. No unprefixed alias is left in the watcher: an alias is a second name for one answer.

**The interface later tasks call**, defined here and restated by its consumers:
- **`hr_max_question_index <clar_dir>`** prints the highest numbered `question_<n>.md` index under `<clar_dir>`, the top level and `answered/` together, or `0` when there is none, and nothing else. Numeric-only names; base 10 forced, so a zero-padded index is not read as octal. Consumed by Task 2's `prl_park`, which takes one above it.
- **`hr_top_level_answered_pairs <clar_dir>`** prints every top-level index that has both `question_<n>.md` and `answer_<n>.md`, space-separated, sorted numerically, each spelled as its file name spells it; it prints nothing when there is none and returns 0. Consumed by Task 3's `pd_entry`, which filters its output, and by the watcher's `spawn_engine`, which records it as the launch's answered set.

**What this task does not do.** It adds no caller beyond renaming the existing ones. Task 2 and Task 3 add the planning libraries' calls, and Task 6 edits `autonomous-watcher.sh` again for the pilot on top of this task's renamed call sites.

### Targets

- `cli/templates/scripts/lib/harness-run-lib.sh`: the two functions and the header's opening list.
- `cli/templates/scripts/autonomous-watcher.sh`: the two definitions removed, every call site renamed.
- `cli/test/clarification-index-lib.test.mjs` (new): the suite for the two library functions.

**Work:**

- [ ] **`lib/harness-run-lib.sh`.**
  - Add `hr_max_question_index` and `hr_top_level_answered_pairs`, each body moved byte-for-byte from the watcher's `max_question_index` and `top_level_answered_pairs` with only the name changed, each with its existing comment block carried over and its caller list updated: the watcher's park-loop guard, park resume and exit classification for the first, plus the planning record library; `spawn_engine` and the planning driver for the second.
  - Extend the header's opening list of what the library answers with *"the clarification channel's highest question index and its top-level answered pairs (`hr_max_question_index`, `hr_top_level_answered_pairs`)"*.
- [ ] **`autonomous-watcher.sh`.**
  - Delete the two definitions and their comment blocks.
  - Rename every call site: `spawn_engine`'s `launch_answered_set` record, `begin_park_resume`, the park-loop guard's `now_max`, and the exit classification's `-gt 0` check, plus any other site `grep -nE '(^|[^_[:alnum:]])(max_question_index|top_level_answered_pairs)' cli/templates/scripts/autonomous-watcher.sh` reaches. A registry field such as `resume_max_question_index` is a different name and is left alone; the pattern's leading class excludes it.
  - Where `archive_answered_pair`'s comment refers to `top_level_answered_pairs` by name, update the name.
- [ ] **`cli/test/clarification-index-lib.test.mjs`.** Open it with the rule it enforces: *one definition of each clarification-index answer, in the run library*. In the shape of `cli/test/credential-scan-lib.test.mjs`, copy the library template into a throwaway directory under the system temp directory, source it in one `bash` process under `set -u`, and assert:
  - an empty or absent channel → `hr_max_question_index` prints `0`, and `hr_top_level_answered_pairs` prints nothing and returns 0;
  - the maximum counts `answered/` as well as the top level;
  - a non-numeric name (`question_x.md`) is ignored by both;
  - a zero-padded `question_08.md` reads as 8, not as an octal error, and is printed by `hr_top_level_answered_pairs` as `08`;
  - a top-level question without its answer is left out of the pairs, and the pairs are numerically sorted.
- [ ] **Source guard — two fixed files, no tree read.** One case reads exactly two named files as text and asserts: `cli/templates/scripts/autonomous-watcher.sh` defines neither function under either name (`max_question_index()`, `top_level_answered_pairs()`, `hr_max_question_index()`, `hr_top_level_answered_pairs()`), and `cli/templates/scripts/lib/harness-run-lib.sh` defines both `hr_` names. It lists no directory and globs nothing, so it is not a tree-reading test under `plugin/instructions/unit_loop_core.md` → `## The test-run rule` point 8 and owes no `treeGuards` entry. The suite's opening comment states this: *"reads two fixed files only — the watcher template and the run library — never a directory"*. The planning libraries do not exist yet when this task ships; that they define no copy is checked by their own tasks' Verification greps (Task 2's `prl_park`, Task 3's `pd_entry`).

**Verification:**

- `cli/test/clarification-index-lib.test.mjs` passes.
- `grep -nE '(^|[^_[:alnum:]])(max_question_index|top_level_answered_pairs)' cli/templates/scripts/autonomous-watcher.sh` has no hit: every remaining mention is `hr_`-prefixed or a registry field name.
- `git diff` of the two functions' bodies shows only the name line changed between the watcher's removed copy and the library's added copy.
- This task edits no existing watcher suite. Their passing unchanged in the Run gates round is the evidence that the watcher's behaviour did not move.
