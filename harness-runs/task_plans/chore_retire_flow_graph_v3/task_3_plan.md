### Task 3 — Name the planning graph by its shipped name in the plugin's planning commands and flow document

**Goal:** Every plugin asset that names the planning loop's graph names `flows/task_plan_writing.graph.json`, the one graph `init` ships after Task 1.

**Depends on:** Task 1, which ships the format-4 graph as `<scriptsDir>/flows/task_plan_writing.graph.json` and stops shipping `flows/task_plan_writing.v4.graph.json`. This task changes only the plugin's text that names the file. What the walker reads is Task 5's.

**Wording rule.** These are adopter-facing contracts. Replace the name and add nothing: no sentence that names the `.v4` file or says the name changed (`harness-runs/lessons.md` → *"A rename declared breaking ships no compatibility path"*). Keep every surrounding placeholder (`<scripts_dir>`) and every cited anchor byte for byte (`.claude/context/plugin.md` → `## Writing agent prose`, *"Never paraphrase a wire literal or a cited anchor"*).

### Targets

- `plugin/commands/branch-start-plan-autonomous.md` — `## Resolved values`, the `<scripts_dir>` row.
- `plugin/commands/branch-start-plan-semi-autonomous.md` — `## Resolved values`, the `<scripts_dir>` row; and step 3 of `## Steps`.
- `plugin/docs/AUTONOMOUS_FLOW.md` — the table row *"Routing of the planning loop: next node, counter, cap, escalation payload"*.

**Work:**

- [ ] `branch-start-plan-autonomous.md`: in the `<scripts_dir>` row, *"`flow-walker.sh` with its graph `flows/task_plan_writing.v4.graph.json`"* becomes `flow-walker.sh` with its graph `flows/task_plan_writing.graph.json`.
- [ ] `branch-start-plan-semi-autonomous.md`: change `flows/task_plan_writing.v4.graph.json` in the `<scripts_dir>` row, and `<scripts_dir>/flows/task_plan_writing.v4.graph.json` in step 3, to the same name without `.v4`.
- [ ] `AUTONOMOUS_FLOW.md`: in the routing row, *"`flow-walker.sh` and `flows/task_plan_writing.v4.graph.json` in `<scripts_dir>`"* becomes `flow-walker.sh` and `flows/task_plan_writing.graph.json` in `<scripts_dir>`.

**Verification:**

- `git grep -n -e 'v4\.graph' -e 'format-3' -e 'format 3' -- plugin` prints nothing.
- `git grep -n 'flows/task_plan_writing.graph.json' -- plugin` lists every line the three Work bullets changed. Each still carries its `<scripts_dir>` placeholder where it had one, and its surrounding text is byte-identical to before.
- No frontmatter line of the two command files changed (`git diff -- plugin/commands` touches body lines only).
