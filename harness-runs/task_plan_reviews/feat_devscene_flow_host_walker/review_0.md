# Task plan review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **`task_2_plan.md` (and the story index's `## Context`, Decisions bullet 5) — the config reader says it mirrors the bash readers, but some of its rules differ from them.**
   Task 2 says *"Each key is read as the bash walker's readers read it: `hr_config_dir` / `hr_state_dir` and `hr_phase_enabled`"*, and the index says the host *"mirrors the bash walker's readers, construct for construct"*. Read against `cli/templates/scripts/lib/harness-run-lib.sh` → `hr_config_load`'s `jq` filter (`s("phases.parity"; try (.phases.parity | if type == "boolean" or . == null then . else "invalid" end) catch null)`, and `s()` drops `null`), the bash readers give:
   - `"phases": {"parity": null}` → off (`hr_cfg_scalar_var` finds no key, so `hr_phase_enabled` returns 1). Task 2 maps a value that is not a boolean to `None`.
   - `"phases": []` or `"phases": "x"` → off (the index error is caught as `null`). Task 2 maps that to all three `None`.
   - `"stateDir": null` → the default (`hr_config_dir`), and `"stateDir": 5` → `"5"` (`tostring`). Task 2 raises `RecordError("…: stateDir is not a string")` for both.
   Refusing these schema-invalid shapes is defensible: it is what the shim lesson in `harness-runs/lessons.md` asks for (*"lists the constructs it supports and refuses every other one"*). But the plan presents it as a mirror, and Task 7 then has the README say *"Each reader mirrors the bash walker's reader of the same record"*.
   **Fix:** Pick one. Either keep the refusals and list each divergence as deliberate, in Task 2's *"Deliberately not checked:"* list and in the index Decisions bullet, dropping "construct for construct". Or change the rules to match the bash results above, and update Task 2's test expectations to match.

2. **`task_5_plan.md` and `task_6_plan.md` — two test assertions, written exactly as the plans word them, would fail or mislead.**
   - Task 5, *"what is written"*: *"every path under `tmp_path`, walked with `rglob`, is inside `tmp_path / "state" / ".flow_walker_state"`"*. `rglob("*")` also yields the directory `tmp_path / "state"`, which is not inside `.flow_walker_state`, so the assertion fails as written. The property it means is "every **file** under `tmp_path`".
   - Task 6, two-branch case: *"the only state file is `state/.flow_walker_state/feat%2Fa.json`"*. After `start()` the directory also holds `feat%2Fa.json.lock`, so a "set of files equals" assertion would fail. Say "the only `*.json` file", or list the lock file too.
   **Fix:** Reword both bullets to the property meant: files, not every path; JSON state files, not every file.

3. **`task_7_plan.md` — it is unclear whether the README's deferrals cite a roadmap item.**
   The `## The layers` bullet says *"Describe a layer's future contents by kind only … never by an issue number: a deferral in this tree cites a numbered roadmap row, not an issue"*, and `## What it is` gains *"It has no command line yet"*. `.claude/context/conventions.md` → `## Documents of record` (*"A deferral cites a numbered roadmap item"*) and `docs/development.md` → `## 6. The roadmap this tree defers to` (*"Directory READMEs … defer their content to a numbered roadmap item"*) suggest those future-content cells should cite an item. That item is plausibly 14, GraphScene, whose `Left:` list carries the walker's port. The bullet's wording lets an implementer either cite one or cite none.
   **Fix:** State which: cite roadmap item 14 for the `commands` layer's and the `host` layer's future contents, or state that a by-kind description is not a deferral under that rule. Either way, give the reason.

## Nice to Have

1. **`task_3_plan.md` / `task_4_plan.md`.** The no-record reason, *"no run-mode record: no flow-progress ledger for '<branch>' and no skipped ids given"*, differs from `flow-walker.sh` → `eval_skip`'s *"… and no --skipped"*. Task 4 calls `refusal_reason` *"what such a renderer will read"*. One sentence saying the rewording is deliberate, because this package has no `--skipped` flag yet, would stop the compatibility command from having to guess which text is the wire.
2. **`task_8_plan.md`.** The last Verification bullet relies on the derivation commands in the index's `## Scope register`, which is outside the `## Context` an implementer is guaranteed to read. Restate the two `git grep` commands inline so the file stays self-contained.
3. **Story index `## Context`.** It carries a table and bullet lists, where the sample keeps Context to prose. Nothing reads it structurally, so this is presentation only.
