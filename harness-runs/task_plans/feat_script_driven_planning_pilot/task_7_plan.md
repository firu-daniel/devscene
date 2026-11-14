### Task 7 — Plugin side: the setup-only clause in the task engine command, the core's one-place note, and the observation intake's second writer

**Goal:** Make four plugin documents agree with the pilot:
- the task engine command runs only its setup steps when the watcher hands planning to the script;
- the planning core says, once, that the script-driven path does not read it and takes its dispatch blocks as prompts;
- the flow's own map and the improvement-observations contract name the planning driver as a second writer and router.

**Depends on:** Task 2, which produces the intake layout this task documents (the bullet on `improvement_observations_instructions.md` restates it), and Task 6, which produces the clause. When the pilot is ready, `autonomous-watcher.sh` → `spawn_engine` adds this sentence, verbatim, to the task engine's launch prompt, whatever resume or pause clause the prompt also carries:

> *"PLANNING IS SCRIPT-DRIVEN ON THIS LAUNCH: run only the task engine command's steps 1–4 and its script-driven setup step, then end the session; a script runs the planning loop."*

The wire literal both sides match is `PLANNING IS SCRIPT-DRIVEN ON THIS LAUNCH`. After the setup session ends with exit 0 and the ledger on disk, the watcher runs the driver (`<scripts_dir>/lib/planning-driver-lib.sh`, Task 3), and then this same command again without the clause. That second session finds `P0`–`P3` resolved and, by the planning fork's `## Override 5` → **Resume-from-ledger (planning).**, falls straight through to implementation. This task changes neither the fork nor any implementation document.

### Targets

- `plugin/commands/branch-start-plan-autonomous.md`: `## Steps`.
- `plugin/instructions/task_plan_writing_instructions_core.md`: its opening paragraphs.
- `plugin/instructions/improvement_observations_instructions.md`: `## Where it is written`, and `## Where it runs & the non-blocking rule`'s skip bullet.
- `plugin/docs/AUTONOMOUS_FLOW.md`: the *"Routing of the planning loop"* table row, and the *"Per-branch intake, human triage."* paragraph.

**Work:**

- [ ] **`branch-start-plan-autonomous.md`.** Insert a step between step 4 and step 5, as step 4a so the numbering every other file cites does not move. It is direct instructions only, no rationale. Its content:
  - **When it applies.** The launch prompt carries `PLANNING IS SCRIPT-DRIVEN ON THIS LAUNCH`. The step applies whatever resume or pause clause the prompt also carries.
  - **What it does.**
    1. Read `${CLAUDE_PLUGIN_ROOT}/instructions/task_plan_writing_instructions_autonomous.md` → `## Override 5 — pause/resume + flow-progress ledger (planning half)`.
    2. Apply only its **Create the ledger at Setup.**, **Record the run mode in that same write.** and **Who reads first.** paragraphs and its `P0` bullet, with the screen's `SAFE` pairs step 4 holds.
    3. Emit `PLANNING HANDED TO SCRIPT: <branch>` to the run log and end the session.
  - **What it does not do.** It runs neither step 5 nor step 6, reads neither the planning core nor the walker, and dispatches no agent beyond the screen's.
  - **The manual entry point** never carries the clause.

  Add *"except on a launch step 4a ends"* where `## Context` says planning chains into implementation *"in one uninterrupted session"*.
- [ ] **`task_plan_writing_instructions_core.md`.** Add one paragraph after its opening context-discipline paragraph. It states:
  - on the opt-in script-driven path, no session reads this file;
  - the watcher's planning driver (`<scripts_dir>/lib/planning-driver-lib.sh`) walks the graph itself;
  - it takes the dispatch blocks of `## Loop` and `## UI-test-plan write loop` as its prompts, filled with the walker's values and with nothing appended but a resumed writer's answers;
  - it takes `## Setup` step 4's `MAX_TOTAL_DISPATCHES` as its cap;
  - so those headings, the fence count under each and that line are wire text that `<scripts_dir>/lib/planning-node-lib.sh` keys on.

  Write it with the core's own `<scripts_dir>` token, which `## Resolved values` already declares. Add no slash-command name, binding or machine path, because the core is literal-free (`plugin/instructions/mode_contract.md` rule (4)).
- [ ] **`improvement_observations_instructions.md`.** Describe the file as Task 2's `prl_observe_flush` actually lays it out. Task 2 produces this layout: each driver flush appends an opening label `# Script-driven planning — <UTC ISO-8601 time>`, its `##` entries in `## The entry format`'s shape, and a closing label `# Task run (Phase D)`, and commits under `chore: Log improvement observations for <branch>`; a flush that finds the file already ending on a bare `# Task run (Phase D)` drops that one line first, so the file ends on exactly one closing label.
  - **In `## Where it is written`**, replace the sentence *"The task flow has no round concept and its single write carries **no** label, so the file's first, unlabelled block is always the task run's."* with: the task flow has no round concept and its single write carries **no** label of its own, so the task run's entries are the file's leading unlabelled block, or, on the opt-in script-driven planning path, the entries under the `# Task run (Phase D)` label the watcher's planning driver closes its own `# Script-driven planning — <time>` blocks with. A `#` label runs until the next one, so Phase D, appending at the end of the file, always lands under that closing label and never under a driver block. The Phase D duty itself is unchanged.
  - **In `## Where it runs & the non-blocking rule`**, in the skip bullet's sentence *"When the branch's intake file **is** already tracked (a resumed session, or a later round)"*, add a third case to the parenthesis, *"or a script-driven planning run, whose driver committed the file before Phase D"*, and one sentence after it: such a fresh run's Phase D treats the file exactly as that bullet states for a tracked file. It enters the step, appends only what this session observed beneath the closing label, writes no label of its own, and, having observed nothing, calls the wrapper on the unchanged file, which exits 3. The driver's blocks are an earlier block that Phase D leaves untouched, except for the machine-path rewrite.
- [ ] **`plugin/docs/AUTONOMOUS_FLOW.md`.**
  - In the *"Routing of the planning loop"* row, after *"run by the orchestrating session"*, add *"or, on the opt-in script-driven path, by the watcher's planning driver, which runs each node as its own headless session (`docs/flow-graph-walker.md`)"*.
  - In *"Per-branch intake, human triage."*, add that the script-driven planning path's driver writes labelled planning blocks before Phase D's write.

**Verification:**

- `grep -rn "PLANNING IS SCRIPT-DRIVEN ON THIS LAUNCH" plugin cli/templates/scripts/autonomous-watcher.sh` finds the literal in the engine command and in the watcher, spelled identically.
- `grep -rn "first, unlabelled block" plugin` finds nothing, and `grep -rn "Task run (Phase D)" plugin cli/templates/scripts/lib/planning-record-lib.sh` finds the closing label spelled identically in `improvement_observations_instructions.md` and in Task 2's library.
- The core gains exactly one paragraph and no change to any heading, fence or binding table: `git diff --stat` on the core shows only added lines in its opening.
- Every citation added is `${CLAUDE_PLUGIN_ROOT}`-rooted inside the plugin, or a repo-relative path for `docs/flow-graph-walker.md` (`.claude/context/plugin.md` → `## Citation`).
