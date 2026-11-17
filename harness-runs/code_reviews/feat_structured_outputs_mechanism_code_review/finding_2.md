### 2. The script-citation check passes when it finds no citation, so the screen's header can drop out of it silently

**File:** `cli/test/agent-return-schemas.test.mjs` — the test titled "every \`<agent>.<field>\` citation across ${SCRIPTS_DIR}/** names a declared field", body "assert.deepEqual(checkCitations(scriptFiles, SCHEMAS).problems, []);"

The decision record says this check is what holds the screen script to the agent's schema. `docs/structured-agent-returns.md` → `### Validation on each path, and why no validator script`, the third-path **Cost**, says: *"the static citation check, which reads the `` `prompt-injection-reviewer.<field>` `` citations in the script's header … hold the two together."* The story index says the same in `## Context`.

The new test asserts only that `problems` is empty. It never asserts that a citation was found. The `pluginMarkdown` test beside it does assert this: `assert.ok(seen > 0, 'no citation of a schema-carrying agent was found')`. So suppose a later edit stops the header's five citations from matching the citation pattern, for example:

- rewrapping a backticked citation across two `#` comment lines;
- dropping the `prompt-injection-reviewer.` prefix;
- deleting the block.

In each case the script reads nothing the check can see, and the test still passes. The schema and `PIS_JQ_VERDICT` could then drift with no failure.

**Fix:** in that test, keep the result and assert that the citations were seen. Replace:

```js
  assert.deepEqual(checkCitations(scriptFiles, SCHEMAS).problems, []);
```

with:

```js
  const { seen, problems } = checkCitations(scriptFiles, SCHEMAS);
  assert.ok(seen > 0, `no citation of a schema-carrying agent was found under ${SCRIPTS_DIR}`);
  assert.deepEqual(problems, []);
```

The screen script's header carries five such citations today, so the assertion holds on the current tree. Run that one file, `npm test --workspace cli -- test/agent-return-schemas.test.mjs`, from the repository root.
