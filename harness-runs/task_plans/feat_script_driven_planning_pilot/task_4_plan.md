### Task 4 — Ship the three planning libraries through `OUTER_LOOP_SCRIPTS`, name them in the two CLI READMEs, and name the driver as an intake writer in the two state-directory templates

**Goal:** Make `init` write the three new libraries into the adopter's `scriptsDir`, under `lib/`, verbatim and without an executable bit, so that the watcher (Task 6) can source them and the end-to-end suite (Task 5) can drive the copies `init` ships. Name them wherever the CLI's own READMEs list the outer-loop file set. Make the two state-directory templates `init` writes, which say who writes the improvement-observations intake and when, true on the script-driven planning path as well.

**Depends on:** Tasks 1, 2 and 3, which create:
- `cli/templates/scripts/lib/planning-node-lib.sh`;
- `cli/templates/scripts/lib/planning-record-lib.sh`;
- `cli/templates/scripts/lib/planning-driver-lib.sh`.

`OUTER_LOOP_SCRIPTS`'s rule is that a row arrives after its template, never before it, so this task follows them.

**Why each row is `agentInvocable: false` with no deny entry.** Each library is sourced by `autonomous-watcher.sh` and never run. Run directly, it only defines functions, exactly as `lib/harness-run-lib.sh` does, so the script-allowlist guard auto-allowing a `bash <scriptsDir>/lib/<file>` call runs nothing. The watcher, which is the one thing that runs the driver, already carries a `DENY_SCRIPT_BASENAMES` entry. So `false` here is a calling convention, and no `plugin/hooks/autonomous-script-allowlist-guard.sh` entry is owed. The row comment states this, the way the existing `lib` rows' comments do.

### Targets

- `cli/src/generators/outerLoopScripts.ts`: three rows, and the module header's file list.
- `cli/test/outer-loop-scripts.test.mjs`: the verbatim, mode and idempotence assertions for the three files.
- `cli/templates/scripts/README.md`: *"The other family in this directory is not generated."*
- `cli/README.md`: the outer-loop shell-asset sentence.
- `cli/templates/state-dir/improvement_observations/README.md`: *"The first, unlabelled block is always the delivery run's."* and the paragraph opening *"Each block is written by the run's own orchestrator"*, with the one after it opening *"The file is committed and pushed by the run itself"*.
- `cli/templates/state-dir/improvement_suggestions.md`: **How entries arrive.**

**The intake layout these two templates describe**, produced by Task 2's `prl_observe_flush` (`cli/templates/scripts/lib/planning-record-lib.sh`): on the opt-in script-driven planning path, the watcher's planning driver appends, during planning, an opening label `# Script-driven planning — <UTC ISO-8601 time>`, its `##` entries, and a closing label `# Task run (Phase D)`, and commits the file under `chore: Log improvement observations for <branch>`. The task run's own Phase D write is unchanged: it carries no label, so on that path it lands under the closing label. Task 7 states the same layout in the plugin contract (`plugin/instructions/improvement_observations_instructions.md` → `## Where it is written`); this task writes only the adopter-facing templates.

**Work:**

- [ ] **`outerLoopScripts.ts`.**
  - Add `Object.freeze({ file: '<name>', subdir: 'lib', mode: 0o644, agentInvocable: false })` for `planning-node-lib.sh`, `planning-record-lib.sh` and `planning-driver-lib.sh`.
  - Place them after the `lib/harness-run-lib.sh` row and before the `WATCHER_SCRIPT_NAME` row, because the table's order rule writes a sourced file before the script that sources it.
  - Give the rows one comment: *sourced by the watcher's planning driver from its own `lib/`, never run; run directly each only defines functions, so `false` is a calling convention and no `DENY_SCRIPT_BASENAMES` entry is owed — the watcher that runs the driver is withheld.*
  - Extend the module header's opening list (*"the flow walker with its gate library and flow graph, …"*) with *"the planning driver's three libraries"*.
- [ ] **`outer-loop-scripts.test.mjs`.** Add a case in the shape of the existing *"the flow walker, its gate library and its graph land verbatim under scriptsDir, and a re-run keeps them"* case. It covers a generated `scriptsDir` and a relocated one, and asserts for each of the three paths:
  - the bytes are the template's;
  - the file is written only under `<scriptsDir>/lib/`;
  - the mode is `0o644`;
  - a second `init` leaves them byte-identical.
- [ ] **`cli/templates/scripts/README.md`.** In the outer-loop family sentence, add *"the planning driver's three libraries `lib/planning-node-lib.sh`, `lib/planning-record-lib.sh` and `lib/planning-driver-lib.sh`, which the watcher sources and runs only for the opt-in script-driven planning pilot (`docs/watcher.md`)"* beside the flow walker's entry. Add one sentence after the *"Three of them are run by the orchestrating session"* passage: on the opt-in script-driven planning path the watcher's driver, not the orchestrating session, runs `flow-walker.sh`.
- [ ] **`cli/README.md`.** In the outer-loop shell-asset sentence, add *"the planning driver's three libraries (`lib/planning-*-lib.sh`), which the run watcher sources for the opt-in script-driven planning pilot"* beside *"the flow walker (`flow-walker.sh`) and its gate library"*.
- [ ] **The two state-directory templates.** Make each statement true on both planning paths:
  - **`improvement_observations/README.md`**: replace *"The first, unlabelled block is always the delivery run's."* with: the delivery run's block is the first, unlabelled one, or, when the opt-in script-driven planning pilot ran, the one under the `# Task run (Phase D)` label the watcher's planning driver closes its own `# Script-driven planning — <time>` blocks with. In the paragraph opening *"Each block is written by the run's own orchestrator"*, add one sentence: on that path the watcher's planning driver also writes labelled blocks, during planning, from what the node sessions it launched reported. In the paragraph opening *"The file is committed and pushed by the run itself"*, add that the driver commits and pushes its blocks as it writes them, so on that path the file can be tracked before the run's closing phase.
  - **`improvement_suggestions.md`** → **How entries arrive.**: replace *"Each run writes exactly one intake file at `improvement_observations/<branch>.md`, once, at the end of the run"* with: each run writes to exactly one intake file, `improvement_observations/<branch>.md`, at the end of the run, and on the opt-in script-driven planning path its planning driver also writes to it during planning.

**Verification:**

- `cli/test/outer-loop-scripts.test.mjs` passes, including the new case for both `scriptsDir` layouts.
- `git grep -n "first, unlabelled block is always\|once, at the end of the run" -- cli/templates/state-dir` has no hit, and `git grep -n "Task run (Phase D)" -- cli/templates/state-dir` finds the closing label spelled as Task 2's library spells it.
- `grep -n "planning-" cli/src/generators/outerLoopScripts.ts` shows the three file names only in the three rows and the header list: no other `.sh` literal for them is added anywhere in `cli/src` (`.claude/context/cli.md` → **One string, one producer.**).
