### 3. `remote-run.sh`'s REPRO still plants a flat `flow_walker_state` and expects `restore` to put `.flow_walker_state` back

**File:** `cli/templates/scripts/remote-run.sh` (the header's REPRO block for `restore` and `save`) — "(the bundle also carrying clarifications/feat_x/question_1.md and"

**The problem.** This branch changed the bundle's walker state from one flat file to a directory (`lib/harness-run-lib.sh` → the bundle format's `<bundle>/flow_walker_state/<path>` row, `hr_remote_bundle_write`, `hr_remote_bundle_restore` → `THE WALKER STATE.`). A `flow_walker_state` that is a regular file is now treated as a pre-cutover bundle and placed nowhere. `cli/test/outer-loop-scripts.test.mjs` → *"a pre-cutover bundle whose flow_walker_state is a regular file restores no walker state"* pins that.

The REPRO in `remote-run.sh`'s header was not updated:
- It still says the stub bundle is "also carrying clarifications/feat_x/question_1.md and flow_walker_state".
- Its `restore` line still expects "the checkout carries clarifications/feat_x/question_1.md, .flow_walker_state and autonomous_logs/remote_status.json".

Someone reproducing `restore` by hand from these lines plants a flat file. They then find no `.flow_walker_state` placed, which is the opposite of what the line says. It is a code comment, so it is a Should Fix: no flow reads it as input.

**Fix.** In `cli/templates/scripts/remote-run.sh`'s REPRO block, make three edits:

1. The stub-bundle sentence becomes:
   ```
   #   (the bundle also carrying clarifications/feat_x/question_1.md and
   #   flow_walker_state/feat_x.json, the branch's walk) and GITHUB_RUN_ID set to another id:
   ```
2. The `restore` expectation becomes:
   ```
   #   restore    bash scripts/remote-run.sh restore feat_x --resume none   -> 0; the
   #              checkout carries clarifications/feat_x/question_1.md,
   #              .flow_walker_state/feat_x.json and autonomous_logs/remote_status.json, and
   ```
3. In the `save` line, `flow_walker_state (and` becomes `flow_walker_state/ with the branch's walk files (and`.

Keep each line's existing indentation and wrapping. No test changes with this, and the fix runs no test.
