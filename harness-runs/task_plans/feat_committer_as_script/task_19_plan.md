### Task 19 — Re-point the semi-autonomous implement commands and the flow documents at the commit step

**Goal:** The two semi-autonomous implement commands summarise the flow they start. The two flow documents describe the unit loop to a reader. All four stop telling the reader that a `committer` agent is dispatched once per unit. They say instead that the loop makes one `commit-on-branch.sh --unit` call per unit, which flips the readiness entry and commits it with the code.

**Depends on:**

- **Task 3**, the front end: `commit-on-branch.sh --unit task|review_item|review_plan_file|ui_test_pass`, which ticks, stages and commits in one call.
- **Task 9**, which makes the unit loop's step 5 that call.

### Targets

- `plugin/commands/branch-implement-plan-semi-autonomous.md`
- `plugin/commands/branch-implement-user-review-semi-autonomous.md`
- `plugin/docs/AUTONOMOUS_FLOW.md`
- `plugin/docs/AUTONOMOUS_FLOW_WHITEBOARD.md`

**Work:**

- [ ] **`branch-implement-plan-semi-autonomous.md`.** "then dispatch the `committer` agent to commit. One commit per task." becomes "then commit it with one `commit-on-branch.sh --unit task` call. One commit per task." In the A1.5, A2 and E bullets, "the normal implementer/reviewer/committer agents" becomes "the normal implementer and reviewer agents and the commit step".
- [ ] **`branch-implement-user-review-semi-autonomous.md`.** Make the same two edits for "dispatch the `committer` agent to commit. One commit per item." and "the normal implementer / reviewer / committer agents".
- [ ] **`plugin/docs/AUTONOMOUS_FLOW.md`.**
  - **The table row.** The row `| The one agent that commits | \`${CLAUDE_PLUGIN_ROOT}/agents/committer.md\` |` becomes `| The one call that commits a unit | \`<scripts_dir>/commit-on-branch.sh --unit\` (its **THE UNIT AND ARTIFACT FORMS** header paragraph) |`.
  - **The unit-loop paragraph.** "then dispatches the committer **once per unit**. The committer flips that readiness entry to `[x]` and stages the code with the index" becomes the commit call making the same flip and stage.
  - **What stays.** Keep its `<MAIN_REPO>` `## Resolved values` row byte-for-byte: the corpus guard pins it.
- [ ] **`plugin/docs/AUTONOMOUS_FLOW_WHITEBOARD.md`.** "then dispatch the committer once — which flips that entry to `[x]`" → "then make the one commit call — which flips that entry to `[x]`". "Same unit loop, same committer, same readiness heading" → "Same unit loop, same commit call, same readiness heading".

**Verification:**

- `git grep -n -w committer -- plugin/commands/branch-implement-plan-semi-autonomous.md plugin/commands/branch-implement-user-review-semi-autonomous.md plugin/docs/AUTONOMOUS_FLOW.md plugin/docs/AUTONOMOUS_FLOW_WHITEBOARD.md` prints nothing.
- `git grep -n 'agents/committer.md' -- plugin/docs` prints nothing.
- Each command's frontmatter (`description:`, `argument-hint:`) is byte-identical to `git show HEAD:<file>` unless it names the committer.
