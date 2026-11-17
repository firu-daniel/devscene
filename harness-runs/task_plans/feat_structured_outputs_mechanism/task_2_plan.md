### Task 2 — Hold object items, nested return fields and nested citations in the return-schema check

**Goal:** Extend `cli/test/agent-return-schemas.test.mjs` to the dialect's object item (Gap 2) generically, with no agent-specific case.
- The dialect check accepts the object-item shape.
- `### Return fields` names an object item's properties as indented bullets, under an `(array of objects)` annotation.
- A caller's citation of an item property, `` `<agent>.<field>.<property>` ``, is held to the schema.
- The citation scan also reads `cli/templates/scripts/**`, so a script that reads an agent's return names the fields it reads and is held to them.

**Depends on:** Task 1. It makes the driver's `PNL_REAP_JQ` → `vfail` accept the same object-item shape. Both must accept exactly the shape below, so neither admits a schema the other refuses.

**Where this task stops.** This task changes the static check only.
- No real schema uses the object item until Task 5 adds `plugin/schemas/prompt-injection-reviewer.return.json`. Until then the new paths run only on the suite's inline bad samples.
- The decision record that states these rules for authors is Task 6's (`docs/structured-agent-returns.md` → `### The return schema`, `### Return fields`, `### Citing a field`). This suite reads only the canonical sentence from it, which no task changes.

**The shapes this task holds (restated from the story index `## Context`):**

- **The schema.** `items` is either `{ "type": "string" }`, optionally with `minLength`, or `{ "type": "object", "description": …, "properties": { … }, "required": [ … ], "additionalProperties": false }`.
  - Each item property: `type` (`string`, `integer` or `boolean`), `description`, and optionally `const`, `enum`, `minLength` (`string` only) and `minimum` (`integer` only).
  - `required` lists only item properties.
- **`### Return fields`.** A top-level field bullet is at column 0, as today: `` - `findings` (array of objects) — … ``. Its item properties follow directly as bullets indented two spaces: `` - `check_id` — … ``. A non-string item property carries `(integer)` or `(boolean)`.
  - `(array of strings)` means `type: array` with string items.
  - `(array of objects)` means `type: array` with object items.
- **Citation.** `` `<agent>.<field>.<property>` ``: `<field>` must be a property of `<agent>`'s schema whose items are objects, and `<property>` one of those items' properties.

### Targets

- `cli/test/agent-return-schemas.test.mjs` — the dialect check, the `### Return fields` check, the citation check and its scanned file set, the bad samples, and the header.

**Work:**

- [ ] `checkDialect`: accept `items` of `type: "object"` with exactly the keys above.
  - Reject the following, each with a problem naming the path (`oneOf[i].properties.<name>.items…`):
    - a missing `description`, `properties`, `required` or `additionalProperties: false`;
    - an unknown keyword on the item or on an item property;
    - an item property `type` outside `string` / `integer` / `boolean`;
    - `minLength` on a non-string or `minimum` on a non-integer item property;
    - a `required` entry that is not an item property.
  - The existing `{ "type": "string" }` branch stays as it is.
- [ ] `checkOutputContract`: match nested bullets under `(array of objects)` fields.
  - Read top-level bullets (column 0, `^- \``) as today.
  - Read nested bullets (`^  - \``) and attach each run of them to the top-level bullet directly above.
  - Add `(array of objects)` to the annotation map. An `(array of strings)` or `(array of objects)` annotation must agree with the schema's `items.type`, not only with `type: array`.
  - For each field whose schema items are objects (the union across variants), its nested bullets name exactly the item properties, each non-string one annotated, and a mismatch is a problem naming field and property.
  - A nested backticked bullet under a field whose items are not objects is a problem.
  - Nested bullets that do not open with a backticked name (for example `` - **`stale-rule`** — `` in `task-plan-writer`) are not field bullets and are ignored, so the six existing agents pass unchanged.
- [ ] `checkCitations`: hold the three-part item-property citations, and also scan the outer-loop scripts.
  - Match an optional third segment, `` `<agent>.<field>.<property>` ``, and hold it to the field's object items. A two-part citation is held as today, and `.md` stays excluded.
  - Run the scan over `cli/templates/scripts/**` text as well as `plugin/**/*.md`. That tree is already covered by this suite's `treeGuards` entry for `cli/templates/scripts/**`, so no `devscene.config.json` change is owed.
  - Keep the `seen > 0` assertion on the plugin scan.
- [ ] Bad samples, each run against an inline sample as the suite already does:
  - a good schema whose second variant carries an `array` of object items, with its sample agent using nested bullets, passes every per-agent check;
  - each `checkDialect` rejection above, the missing or extra nested bullet, the missing `(integer)` on a nested property, and `(array of strings)` on object items are rejected with their named problem;
  - a citation of an undeclared item property (`` `sample-reviewer.items_list.nope` ``) is rejected;
  - a citation inside a sample script text (`{ path: 'cli/templates/scripts/x.sh', text: … }`) is checked like a Markdown one.
- [ ] Header: amend the rule paragraph so it says the closed dialect includes object items, that `### Return fields` names an object item's properties as indented bullets, and that citations — including `` `<agent>.<field>.<property>` `` — are held across the plugin's Markdown and the outer-loop scripts.

**Verification:**

- `cli/test/agent-return-schemas.test.mjs` passes, every new bad sample included. Its per-agent tests for the six existing schema-carrying agents pass with no change to any file under `plugin/`.
- Mutating the good object-item sample by deleting its item's `additionalProperties` makes `checkDialect` report a problem. Check this by reading the new bad-sample case, not by editing a corpus file.
- **Not done here.** No file outside `cli/test/agent-return-schemas.test.mjs` changes in this task.

**Deviations from plan:** The plan excludes only `.md` from the citation scan. With an optional third segment, the scan would also read the schema file name `` `<agent>.return.json` `` as a citation of field `return`, which Task 5's prose about `prompt-injection-reviewer.return.json` would then fail. Implemented as: a three-part match equal to `<agent>` + `SCHEMA_SUFFIX` is not a citation either, and the bad sample `a citation of an undeclared item property is rejected; the schema file name is not a citation` asserts it. A three-part citation of a field whose items are not objects reports its own problem (`cites an item property, but the items of <field> are not objects`).
