### 4. `pnl_load_schemas` skips a dispatch node with no string `agent`, so its own "names no agent" fault can never fire

**File:** `cli/templates/scripts/lib/planning-node-lib.sh` (`pnl_load_schemas`) — `.key + " " + (.value.agent | strings)`

**The problem.** The jq filter that lists the dispatch nodes builds each line as `.key + " " + (.value.agent | strings)`. When a node's `agent` is missing or is not a string, `strings` yields nothing, so the `+` yields nothing and the node produces no line at all. That makes the loop's guard `[ -n "$agent" ] || { pnl_fail "the planning graph '$PNL_GRAPH' names no agent for dispatch node '$node'"; return 2; }` unreachable. A graph with such a node loads with no fault at `pnl_init`, although the function's header promises *"so no session is launched against an agent with no schema"*. The fault surfaces only later, at `pnl_reap`, as *"no return schema is loaded for node …"*, after a session has already been launched and paid for. The shipped graph names every agent, so the defect is latent.

**Fix.** Make the filter emit the node with an empty agent, so the existing guard fires. In `pnl_load_schemas`, replace

```bash
pairs=$(jq -r '.nodes | to_entries[] | select(.value.kind == "dispatch") | .key + " " + (.value.agent | strings)' "$PNL_GRAPH" 2>/dev/null) \
```

with

```bash
pairs=$(jq -r '.nodes | to_entries[] | select(.value.kind == "dispatch") | .key + " " + (.value.agent | if type == "string" then . else "" end)' "$PNL_GRAPH" 2>/dev/null) \
```

The new filter uses no regex, and its `if` has an `else`, so it stays within the jq 1.5 floor. For the line `<node> `, `read -r node agent` leaves `agent` empty, and the guard reports the node by name.

**Test.** Add one case to `cli/test/planning-node-lib.test.mjs`, next to `pnl_init refuses an agent file with no usable ## Return schema, naming it`:

```js
test('pnl_init refuses a dispatch node that names no agent, naming the node', { skip: SKIP }, async (t) => {
  const f = await fixture(t);
  const graphPath = join(f.wt, 's', 'flows', 'task_plan_writing.graph.json');
  const graph = JSON.parse(await readFile(graphPath, 'utf8'));
  delete graph.nodes.plan_writer.agent;
  await writeFile(graphPath, JSON.stringify(graph));
  const r = await f.bash('pnl_init "$P" "$W"; rc=$?; printf "%s" "${PNL_TMP-}"; exit $rc');
  assert.equal(r.status, 2, r.stderr);
  assert.equal(r.stdout, '', 'no temporary directory is left set');
  assert.match(r.stderr, /^planning-driver: .*names no agent for dispatch node 'plan_writer'/);
});
```

The test edits only the fixture's own copy of the graph and leaves the shipped graph untouched. `readFile`, `writeFile` and `join` are already imported by that suite.

**Verification:** run the one test file this fix edits, from the repository root:

```
npm test --workspace cli -- test/planning-node-lib.test.mjs
```
