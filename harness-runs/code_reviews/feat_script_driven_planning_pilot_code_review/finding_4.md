### 4. The planning core's script-driven note names only part of the text `planning-node-lib.sh` keys on

**File:** `plugin/instructions/task_plan_writing_instructions_core.md` (the opening paragraph that begins "On the opt-in script-driven planning path no session reads this file") — "Those headings, the fence count under each and that line are therefore wire text"

**The problem.** The branch adds a note to the planning core. It tells a maintainer which of the core's text a script now parses, so that they do not rename it. `.claude/context/plugin.md` → `## Writing agent prose` says *"Never paraphrase a wire literal or a cited anchor"*. A heading a script matches is carried byte-for-byte. The note gets the wire set wrong in two ways:

- **It names `## Setup`.** The heading `cli/templates/scripts/lib/planning-node-lib.sh` keys on is `PNL_CORE_SETUP_HEADING='## Setup (once per session)'`, which is the core's real heading. A maintainer who reads the note as calling `## Setup` the wire text could shorten the heading to that and believe the change safe.
- **It names only the two `##` headings.** "Those headings" points back to `## Loop` and `## UI-test-plan write loop`. But `PNL_CORE_BLOCKS` also keys on the six `###` headings under them: `### 1. Spawn \`task-plan-writer\``, `### 2. Business-parity review (plan-review mode)`, `### 3. Architecture review (plan-review mode)`, `### 4. Spawn \`task-plan-reviewer\``, `### 1. Spawn \`ui-tests-plan-writer\`` and `### 2. Spawn \`ui-tests-plan-reviewer\``. The fence count `pnl_init` checks is per `###` heading (`the heading '$heading' carries $fences fence lines … where $count fenced block(s) are expected`), not per `##` section.

A maintainer who renames one of those `###` headings, or `## Setup (once per session)`, gets no warning from the note. `pnl_init` then fails (`pnl_fail`, return 2) inside the driver. That happens after the setup session has ended, so planning stops on the next pilot launch. It does not fall back to the orchestrated path. `cli/test/watcher-planning-driver.test.mjs` copies the real core into its fixture, so the suite would catch the rename. That is why this is a Should Fix and not a Must Fix.

`.claude/context/plugin.md` → `## Cores, forks and the single-owner rule` rule 4 holds for the note as it stands, and for the fix below. It carries no reader-naming escalation phrase, no slash-command name, no absolute machine path and no step a mode deletes. It names the scripts only through the `<scripts_dir>` placeholder, which the core's `## Resolved values` table declares.

**Fix.** Replace the note's two sentences with:

```markdown
On the opt-in script-driven planning path no session reads this file: the watcher's planning driver (`<scripts_dir>/lib/planning-driver-lib.sh`) walks the graph itself, takes the dispatch blocks of `## Loop` and `## UI-test-plan write loop` as its prompts — filled with the walker's values, with nothing appended but a resumed writer's answers — and takes `## Setup (once per session)` step 4's `MAX_TOTAL_DISPATCHES` as its cap. `<scripts_dir>/lib/planning-node-lib.sh` keys on all of the following, so each is wire text: the `## Setup (once per session)` heading and its `MAX_TOTAL_DISPATCHES = ` line; the `## Loop` and `## UI-test-plan write loop` headings; each `###` heading under them that carries a dispatch block; and the fence count under each of those `###` headings.
```

The edit changes no heading, no fence and not the cap line, so `pnl_init`'s parse of the core is unchanged and the fix runs no test.
