### 1. The v3 generator accepts an `<escalate>` edge reason that the format-4 vocabulary does not declare

**File:** `scripts/generate-flow-graph-v3.mjs` (`checkVocabulary`, `usedBindings`, `generate`): "entry.reasons.every((r) => V3_ESCALATE_REASONS.includes(r))"
**Class:** Wrong behaviour
**Failure:** If a maintainer removes `"blocker"` from `vocabulary.bindings."<escalate>".reasons` in `cli/templates/scripts/flows/task_plan_writing.v4.graph.json` and leaves the six `{ "binding": "<escalate>", "reason": "blocker" }` edges in place, then `node scripts/generate-flow-graph-v3.mjs` (gate 3i) exits 0. Gates 3c and 3g also pass. The harness's format-4 source ships using a reason its own vocabulary does not declare.

The story index (`## Context` → **Used names checked against declared ones.**) says the generator "maps every name it uses through the vocabulary, so it refuses a name it cannot map". The generator checks the outcome, binding and predicate names a node uses against the declared sets. It does not check the stop reasons:

- `checkVocabulary` checks only that the declared `<escalate>.reasons` are a subset of `V3_ESCALATE_REASONS`, and records nothing about them.
- `generate` never compares an edge's or an `onCap`'s `reason` with the reasons its binding declares.

Nothing else catches the mismatch:

- The format-3 output carries no `reasons` list, so it is byte-identical either way (gate 3i).
- The v3 schema's `reason` enum still admits `blocker` (gate 3c).
- JSON Schema cannot check a used name against a declared one (gate 3g).
- `graphscene.vocabulary.vocabulary_violations`, which does make this check, runs only on the generic fixtures under `graphscene/tests/fixtures/flow_graph/` and never on the harness's own source.

**Fix:** record each stop binding's declared reasons in `checkVocabulary`. Return the object carrying each binding from `usedBindings`. Refuse a `reason` the binding does not declare.

1. In `checkVocabulary`, add a `reasons` map to the returned sets and fill it for every stop binding:

```js
const declared = { outcomes: new Set(), bindings: new Set(), predicates: new Set(), reasons: new Map() };
```

and in the bindings loop, directly after `declared.bindings.add(name);`:

```js
if (isObject(entry) && entry.primitive === 'stop' && Array.isArray(entry.reasons)) {
  declared.reasons.set(name, entry.reasons);
}
```

2. Make `usedBindings` return the carrier alongside each path and name:

```js
function usedBindings(node, nodePath) {
  const used = [];
  if (own(node, 'binding')) used.push([`${nodePath}.binding`, node.binding, node]);
  for (const [outcome, edge] of Object.entries(isObject(node.outcomes) ? node.outcomes : {})) {
    if (!isObject(edge)) continue;
    const edgePath = `${nodePath}.outcomes.${outcome}`;
    if (own(edge, 'binding')) used.push([`${edgePath}.binding`, edge.binding, edge]);
    if (isObject(edge.onCap) && own(edge.onCap, 'binding')) {
      used.push([`${edgePath}.onCap.binding`, edge.onCap.binding, edge.onCap]);
    }
  }
  return used;
}
```

3. In `generate`, replace the `usedBindings` loop with:

```js
for (const [path, binding, carrier] of usedBindings(node, nodePath)) {
  if (!declared.bindings.has(binding)) {
    fail(path, `uses binding ${JSON.stringify(binding)}, which the vocabulary does not declare`);
    continue;
  }
  const reasons = declared.reasons.get(binding);
  if (reasons !== undefined && own(carrier, 'reason') && !reasons.includes(carrier.reason)) {
    fail(
      path.replace(/\.binding$/, '.reason'),
      `uses reason ${JSON.stringify(carrier.reason)}, which binding ${JSON.stringify(binding)} does not declare`,
    );
  }
}
```

This leaves the committed source's output unchanged, because every reason its edges use is declared. Gate 3i confirms that in the Run gates round. This fix edits no test file, so it runs none.
