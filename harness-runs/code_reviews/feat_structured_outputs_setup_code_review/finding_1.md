### 1. Drop the old `action_taken` name from the writer schema's outcome descriptions

**Severity:** Must Fix

**Site:** `plugin/schemas/conventions-writer.return.json` → the `outcome` property of the `written` variant (`"The document now stands written; carried over from the old action_taken value."`) and of the `merged` variant (`"The document now stands merged; carried over from the old action_taken value."`).

**Problem.** This branch removes the writer's `action_taken` field and folds its values into `outcome`, with no fallback. That is a breaking rename, and the story index's scope register, row 27, binds this branch to the lessons-ledger rule `harness-runs/lessons.md` → `## Adopter-facing documentation` → *"A rename declared breaking ships no compatibility path: no fallback to the old value, no repair of a file an earlier release wrote, and no sentence that names the old value or says a name changed; adopters migrate by hand."*

The schema file ships in the plugin, and both outcome descriptions name the old field and say the value was carried over from it. That is a shipped sentence that names the old value and says a name changed. The ledger entry carries no grade of its own, so it is a Must Fix trigger.

The history belongs in the decision record, which already has it: `docs/structured-agent-returns.md` → `### One discriminator, `outcome`, held to the graph` → *"The writer's old `action_taken:` values became its outcomes `written` and `merged`"*. That document does not ship.

**Fix.** In `plugin/schemas/conventions-writer.return.json`, make these two replacements:

- `"description": "The document now stands written; carried over from the old action_taken value."` becomes `"description": "The document now stands written."`
- `"description": "The document now stands merged; carried over from the old action_taken value."` becomes `"description": "The document now stands merged."`

Change nothing else. `git grep -n action_taken -- plugin` must then return no hit.
