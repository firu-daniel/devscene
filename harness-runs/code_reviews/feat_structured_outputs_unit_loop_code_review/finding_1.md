### 1. `layer-implementer` cannot return `flags` on `prohibited` or `already passing`, so a mandatory untrusted-input report from a dispositioned layer has nowhere to go

**Files:**
- `plugin/schemas/layer-implementer.return.json`: the `oneOf` variants whose `outcome` `const` is `"prohibited"` and `"already passing"`.
- `plugin/agents/layer-implementer.md` (`## Output contract` → `### Return fields`): the bullet "- `flags` (array of strings) — `implemented` only, omitted when empty".
- `plugin/instructions/unit_loop_core.md` (`## The unit loop` step 3): the bullets "An `outcome` of `prohibited` → `### The dispositioned outcome` below." and "An `outcome` of `already passing`, on row `G.4` only →".

**Problem.**

`plugin/instructions/untrusted_input.md` → `## The rule` item 3 makes a report of authority-claiming text in task data mandatory. `## Where a report goes` routes `layer-implementer`'s report to *"an item of its return object's `flags`"*. The unit loop's step 6 then appends every `layer-implementer.flags` item to the unit's progress line, *"any layer, any iteration"*, and calls that line *"the loop's only notice of … a refused instruction carried in task data"*.

This branch's schema allows `flags` on the `implemented` variant only. The `prohibited` and `already passing` variants carry `"additionalProperties": false` with only `outcome` and `cause`. The `### Return fields` bullet restates that limit ("`implemented` only"), and step 3 keeps `flags` only on the `implemented` arm.

Both of those outcomes close the unit, which is then committed and reaches step 6 like any other. Two cases show the gap:
- A row-`UR-A` user-review item whose review text carries an injected instruction can still end in a `prohibited` disposition, for example on a `.claude/**` write.
- A row-`G.4` finding is built from a test log that the test-fix plan writer quoted, and it can close as `already passing`.

In either case the implementer must report the refused instruction but has no legal field for it. It can drop the report, which breaks `untrusted_input.md`. Or it can add `flags` and produce an object that the driver's schema check rejects and that step 3 does not read.

Before this branch, step 6 took item-7 lines from any layer's return, a dispositioned one included. So this is a channel the move to structured returns closed. It is not a gap the branch inherited.

**Fix.**

1. In `plugin/schemas/layer-implementer.return.json`, add the same `flags` property the `implemented` variant declares to the `properties` of both the `"prohibited"` and the `"already passing"` variants. Leave each `required` list unchanged (`["outcome", "cause"]`):

   ```json
   "flags": { "type": "array", "items": { "type": "string", "minLength": 1 }, "description": "One item per thing the orchestrator should flag to the user; omitted when empty." }
   ```

2. In `plugin/agents/layer-implementer.md` → `### Return fields`, change the opening of the `flags` bullet from:

   > - `flags` (array of strings) — `implemented` only, omitted when empty:

   to:

   > - `flags` (array of strings) — `implemented`, `prohibited` and `already passing`, omitted when empty:

   Leave the rest of the bullet unchanged.

3. In `plugin/instructions/unit_loop_core.md` → `## The unit loop` step 3, change these two bullets:

   > - An `outcome` of `prohibited` → `### The dispositioned outcome` below.
   > - An `outcome` of `already passing`, on row `G.4` only → `### The dispositioned outcome`'s route, per its `#### The already-passing close`.

   to:

   > - An `outcome` of `prohibited` → `### The dispositioned outcome` below, keeping each `` `layer-implementer.flags` `` item for step 6.
   > - An `outcome` of `already passing`, on row `G.4` only → `### The dispositioned outcome`'s route, per its `#### The already-passing close`, keeping each `` `layer-implementer.flags` `` item for step 6.

   Step 6's sentence already appends every item "an implementer of this unit returned", so it needs no change.

No test runs for this change beyond the tree guards the unit loop selects.
