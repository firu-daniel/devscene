### 1. The withheld-tools log line says "not refused" on sessions the driver did refuse

> **Self-contained per-finding file** for the `fix_planning_node_tool_check` code-review index (`harness-runs/code_reviews/fix_planning_node_tool_check_code_review.md`). Everything needed to apply the fix is here. The committer flips this finding's checkbox in the index's `## Phase 2 Readiness — Ordered Fix List`, never here.

**File:** `cli/templates/scripts/lib/planning-driver-lib.sh` (`pd_reap_one`): "the init event lacks declared tools [$withheld]; not refused"

`pd_reap_one` writes the withheld-tools line whenever `withheld=` is non-empty, for every `kind`. The Task 2 plan intends this: "The line is written whatever the session's `kind`, and a stalled session … still logs what its stream withheld". But `pnl_reap` sets `withheld=` on every branch after the `init` check, so it also does so when the session **is** refused:

- **A refused session.** The session lacks one declared tool and also carries an undeclared one. This is the `mixed` case in `cli/test/planning-node-lib.test.mjs` → `rule 2: …`, which gives `kind=error`, `class=agent` and `withheld=Grep`.
- **A stalled session.** The driver forces it to `kind=error` / `class=infra`.
- **Any other error.** For example, an undeclared outcome or a missing `findings_file`, on a session whose `init` withheld `Glob, Grep`. Under Claude Code 2.1.325 that is every writer and gate session.

For these sessions the run log shows two lines, one straight after the other:

```
[plan-drive] #1 plan_review: error (the init event grants tools the agent does not declare: [Edit])
[plan-drive] #1 plan_review (task-plan-reviewer): the init event lacks declared tools [Grep]; not refused
```

The second line says the session was not refused, and the first says it was. Someone reading `<branch>.log` after a park reads `; not refused` as a statement about the session, not about the lack. The suffix is wrong whenever `kind` is `error`. The fact the line exists to carry is that a lacking tool is never a reason to refuse, and that fact is true for every kind.

**Fix:** change the line's suffix so that it describes the lack, not the session. Make this exact text change at all three sites that carry the literal. Leave the test names and suite headers that say a session "is not refused" as they are: they describe a session that genuinely was not refused.

1. `cli/templates/scripts/lib/planning-driver-lib.sh` → `pd_reap_one`:

   ```bash
   [ -z "$withheld" ] || pd_log "#$seq $node ($agent): the init event lacks declared tools [$withheld] (a lacking tool is never refused)"
   ```

2. `cli/test/planning-driver-walk.test.mjs`, in the case `sessions whose init withholds Glob and Grep beside Bash are not refused, and each is logged`. Change the exact-line assertion to:

   ```js
   lines.includes('[plan-drive] #1 plan_writer (task-plan-writer): the init event lacks declared tools [Glob, Grep] (a lacking tool is never refused)'),
   ```

   The `architecture_review` assertion matches by `includes` on the text before the suffix, so it needs no change.

3. `docs/flow-graph-walker.md` → `### The schema-from-graph rule, and the \`init\` check` → **Decision.**. Change the quoted line in "the driver logs one `[plan-drive] #<seq> <node> (<agent>): the init event lacks declared tools [<tools>]; not refused` line for the session" to:

   ```
   `[plan-drive] #<seq> <node> (<agent>): the init event lacks declared tools [<tools>] (a lacking tool is never refused)`
   ```

The only test this fix runs is the test file it edits, `npm test --workspace cli -- test/planning-driver-walk.test.mjs`, from the repository root. The full suite runs in the Run gates phase.
