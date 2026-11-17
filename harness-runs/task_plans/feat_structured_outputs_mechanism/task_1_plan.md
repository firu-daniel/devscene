### Task 1 — Validate array-of-object items in the planning driver's return check

**Goal:** Teach the planning driver's whole-object return check, `cli/templates/scripts/lib/planning-node-lib.sh` → `PNL_REAP_JQ` → `vfail` (and through it `schemafail`), the one dialect extension this branch settles: an `array` whose `items` is an **object item**, one level deep. A node whose schema declares such a field then has each item held to the item's `properties`, `required` and `additionalProperties: false`, exactly as a variant's top-level keys already are.

**Where this task stops.** This task changes the validator and its own behavioural suite only.
- It writes no schema that uses the new shape. That is Task 5's, for `prompt-injection-reviewer`, an agent the planning graph does not dispatch.
- It does not change the static return-schema check's dialect test. That is Task 2's.
- It does not change the decision record `docs/structured-agent-returns.md`. That is Task 6's.

The validator and the static check accept exactly the same shape, stated below, so neither admits a schema the other refuses.

**The object-item shape (the contract this task implements; Tasks 2, 5 and 6 restate it):**
- `items` is `{ "type": "object", "description": …, "properties": { … }, "required": [ … ], "additionalProperties": false }`. `items: { "type": "string" }`, optionally with `minLength`, stays legal and unchanged.
- Each item property is `type` (`string`, `integer` or `boolean`) plus `description`, and optionally `const`, `enum`, `minLength` (`string` only) and `minimum` (`integer` only).
- No `array` or `object` property sits inside an item.

### Targets

- `cli/templates/scripts/lib/planning-node-lib.sh` — `PNL_REAP_JQ` → `vfail` and the header comment above `PNL_REAP_JQ` that describes it.
- `cli/test/planning-node-lib.test.mjs` — new rule-5 cases for object items, and the header sentence naming what rule 5 covers.

**Work:**

- [ ] `PNL_REAP_JQ` → `vfail`: add the `object` type, with a value of the wrong type, missing keys, unknown keys and per-key failures each reported in order.
  - A value whose property `type` is `"object"` and whose JSON type is not object yields `is not an object`.
  - For an object value, check in this order, the first failure winning:
    1. a key in the property's `required` that the value lacks yields `missing required key <k>`;
    2. a key the property's `properties` does not declare yields `unknown key <k>`;
    3. otherwise the first key whose value fails `vfail` against its item property yields `<k> <that failure>`.
  - The existing `items` branch already prefixes `item <i> `, so a top-level failure reads, for example, `findings item 0 missing required key reason`, and `schemafail`'s per-key wrapper adds the field name. Keep `schemafail` itself unchanged except where reuse is cleaner. A shared object check used by both is acceptable, provided `schemafail`'s existing failure texts are byte-identical.
- [ ] Keep the jq 1.5 floor the library header states (`BASH 3.2 AND JQ 1.5 ARE THE FLOORS`): no regex builtin, every `if` with an `else`, recursion only through the existing `def`. Amend the comment above `PNL_REAP_JQ`, which says `vfail` and `schemafail` *"hold a value to the closed dialect that file is written in"*, so it names the object item as part of that dialect. Do not restate the dialect there: `docs/structured-agent-returns.md` → `### The return schema` owns it.
- [ ] `cli/test/planning-node-lib.test.mjs`: add rule-5 cases, written the way the suite already writes its fixture schema files rather than copying a corpus schema.
  - The fixture schema gives one dispatch node's agent a variant with an `array` of object items (for instance `items_list`, with a required string `name` and an optional integer `count`).
  - These must each be an infrastructure `error` whose reason is `the return fails its schema: <field> item <i> …`, naming the first failure with the texts above:
    - an item that is not an object;
    - an item missing a required key;
    - an item carrying an unknown key;
    - an item whose integer property holds a string.
  - A return whose items all conform is `kind=returned`.
  - Update the suite header's rule-5 sentence so it says object items are held too.

**Verification:**

- `cli/test/planning-node-lib.test.mjs` passes, including the new cases.
- The existing rule-5 cases in that suite still produce the same `reason=` texts for string items and scalar properties, byte for byte.
- `grep -n 'test(\|match(\|sub(\|gsub(\|splits(' cli/templates/scripts/lib/planning-node-lib.sh` shows no regex builtin introduced into `PNL_REAP_JQ`.
- **Not done here.** No schema under `plugin/schemas/` uses the new shape after this task, and `docs/structured-agent-returns.md` is unchanged.
