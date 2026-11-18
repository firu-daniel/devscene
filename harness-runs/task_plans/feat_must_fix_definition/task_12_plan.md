### Task 12 — Route refused round files through both planning cores

**Goal:** Both plan-review loops handle a refused round file without letting it reach the writer: the walker-routed task-plan loop acts on `refused:` output, and the prose-routed user-review fix-plan loop runs the same check itself.

**Depends on:** Task 2, whose contract is: `bash <scripts_dir>/flow-walker.sh check-round-file --findings <path>` exits 0 silently for a valid file, exits 3 with one `flow-walker: <path>: <reason>` stderr line for an invalid or absent one, exits 1 on a usage refusal, and exits 2 on a fault; and `next` prints `refused: <gate> attempt <n> of 3: <reason>`, re-dispatches refused gates as a set after their siblings finish, and holds the third refusal as `error`. Task 4, which states the entry rule in `plan_review_rounds.md` → `## The Must Fix entry`.

### Targets

- `plugin/instructions/task_plan_writing_instructions_core.md`
- `plugin/instructions/user_review_fix_plan_writing_instructions_core.md`
- `plugin/instructions/user_review_fix_plan_writing_instructions_autonomous.md`
- `plugin/instructions/user_review_fix_plan_writing_instructions.md`

**Work:**

- [ ] In the task-plan core → `## The walker` → **Acting on what it prints**, add: a `refused:` line names a gate whose round file failed the check and records nothing; on `action: wait` keep recording the other gates, and on `action: dispatch` send the printed set as usual, the reviewer replacing its file. Do not change the three command forms, any `###` dispatch heading, or any dispatch fence.
- [ ] In the task-plan core → `## Setup` step 4, keep `MAX_TOTAL_DISPATCHES = 40` byte-identical and extend the sizing sentence: the remaining 10 absorb writer clarification re-dispatches and refused-round-file re-dispatches.
- [ ] In the user-review core, add a `<scripts_dir>` row to `## Resolved values`. In step 7's **The round's set** paragraph, state once for both gates: on `PASS` or `FAIL`, run `bash <scripts_dir>/flow-walker.sh check-round-file --findings <findings_file>` from the checkout root as one literal command before recording. Exit 0 records the outcome. Exit 3 is a return that fails the check under `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## A return that fails the check`: record nothing and dispatch that gate again, and on the third consecutive failure take the held binding, naming the printed line. Every other non-zero exit, or a missing script, is a held binding at once, naming the printed line, with no reviewer re-dispatch: exit 1 is a usage refusal or a walker too old to have the subcommand, and no reviewer can fix either. Steps 7 and 8 each cite this paragraph from their parse sentence.
- [ ] In the user-review core's `<app_root>` paragraph, and in the supervised fork's `<app_root>` row, replace "invokes no wrapper script" wording with wording that says no step resolves a path against `<app_root>`, because this flow now runs `flow-walker.sh`.
- [ ] In the autonomous fork → `## Safety scaffolding`, keep `MAX_TOTAL_DISPATCHES = 24` and say the remainder absorbs clarification and refused-round-file re-dispatches. Change no binding.

**Verification:**

- `grep -n 'check-round-file' plugin/instructions/user_review_fix_plan_writing_instructions_core.md` shows the one defining paragraph and no restated copy of its exit rules.
- `grep -n 'MAX_TOTAL_DISPATCHES = ' plugin/instructions/task_plan_writing_instructions_core.md plugin/instructions/user_review_fix_plan_writing_instructions_autonomous.md` still shows `40` and `24`.
- Walking the user-review steps by hand shows an invalid `FAIL` file is not recorded, so it cannot enter `<findings_files>` at the round close.
- Walking the same steps with `unknown subcommand 'check-round-file'` at exit 1 shows a valid round reaches the held binding on the first return, with no second dispatch of that gate.
