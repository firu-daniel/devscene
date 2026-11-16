# Agent return contract

## Resolved values

| Token | Class | How to resolve it |
|---|---|---|
| `<scripts_dir>` | config value | `scriptsDir` — the directory the generated wrapper and outer-loop scripts live in. |

Every other `<…>` name here is defined by this file's own text at its use site.

## The return block

An agent that adopts this contract ends its reply with its **return object**: one fenced code block whose info string is `json`, holding one JSON object, with nothing but whitespace after its closing fence. Prose may sit above it; nothing may sit below it.

Every adopting agent carries this sentence verbatim in its `## Output contract`:

```
End your reply with your return object: one fenced code block whose info string is `json`, holding one JSON object with exactly the fields `### Return fields` below lists for your outcome, with nothing after its closing fence.
```

## The return schema

The agent's return schema is the file `${CLAUDE_PLUGIN_ROOT}/schemas/<agent>.return.json`, `<agent>` being the definition's basename. The agent never reads it, and its definition carries no copy of it. The file holds one JSON object: a draft-07 JSON Schema written in this **closed dialect**.

- **Top level:** `$schema` (`http://json-schema.org/draft-07/schema#`), `title`, `description`, `type: "object"`, and `oneOf`, a non-empty array of variants.
- **Each variant:** `type: "object"`, `description`, `properties`, `required` — which always includes `outcome` — and `additionalProperties: false`.
- **`properties.outcome`:** `{ "const": "<value>" }` plus `description`. The `const` values are distinct across the variants.
- **Every other property:** `type`, one of `string`, `integer`, `boolean` or `array`, with `description`, and optionally `const`, `enum`, `minLength` (`string` only), `minimum` (`integer` only), `minItems` and `items` (`array` only). `items` is `{ "type": "string" }`, optionally with `minLength`.

No other keyword appears anywhere in the schema.

`outcome` is the one discriminator. For an agent a planning graph dispatches, its values are exactly that node's outcome keys minus `error`. `error` is never an agent's outcome: a caller records it for a return that keeps failing `## Reading a return`.

## Return fields

The agent's `## Output contract` carries a `### Return fields` subsection, the only return description the agent carries. It has one bullet per schema property, each opening with the property name in backticks (`` - `findings_file` — … ``), `outcome` included with its values. A property whose `type` is not `string` carries its type in parentheses right after the name, separated by one space: `(integer)`, `(boolean)` or `(array of strings)` (`` - `must_fix_count` (integer) — … ``). The prose says which outcome carries which field and states each lower bound. It never restates the schema in another form, so a fenced `key: value` or `json` block has no place in it.

## Citing a field

A document other than the agent's own definition names a return field it reads as `` `<agent>.<field>` `` — `` `task-plan-reviewer.findings_file` `` — and an outcome as "an `outcome` of `PASS`". A static check holds each such citation to the named agent's schema file, so this is the only spelling a caller uses.

## Reading a return

An orchestrating caller applies this **routing check** to a return before acting on it:

1. The reply's last fenced block opened with `json` exists, has only whitespace after its closing fence, and parses as one JSON object.
2. Its `outcome` is one the dispatching section routes on for this dispatch.
3. Every field that section reads for that outcome is present and not empty.

The driver applies the agent's full schema file instead (`<scripts_dir>/lib/planning-node-lib.sh` → `pnl_reap`). The routing check is deliberately lighter because an orchestrating session runs no validator.

## A return that fails the check

A return that fails `## Reading a return` is **not a return**. Record nothing for it, and send the same dispatch again through the dispatching flow's safety contract — a heartbeat and a counted dispatch like any other.

After the **third** consecutive failing return for the same dispatch, take the dispatching section's `error` route: `--outcome error` where that section passes outcomes to `flow-walker.sh`; otherwise the flow's blocker route — `<escalate>` where the flow binds it, else stop and report. Name the agent and the check that failed.

The driver's bound is the same three attempts, taken as its infrastructure class.

## Adopting it for another agent

An agent author adds, in this order:

1. The file `${CLAUDE_PLUGIN_ROOT}/schemas/<agent>.return.json`, per `## The return schema`.
2. The `### Return fields` subsection, per `## Return fields`.
3. The sentence `## The return block` carries, verbatim, in the `## Output contract`.

Then rewrite every caller's citation of that agent's fields into `## Citing a field`'s form, and point each caller that routes on the return at `## Reading a return`.

An agent with no schema file is outside every check until it gains one, so agents adopt the contract one at a time.

## Who may cite this

These documents point at a section of this file:

- `${CLAUDE_PLUGIN_ROOT}/docs/AUTONOMOUS_FLOW.md`
- `${CLAUDE_PLUGIN_ROOT}/instructions/task_plan_writing_instructions_core.md`
- `${CLAUDE_PLUGIN_ROOT}/instructions/plan_orchestration_instructions_core.md`
- `${CLAUDE_PLUGIN_ROOT}/instructions/user_review_fix_plan_writing_instructions_core.md`
- `${CLAUDE_PLUGIN_ROOT}/instructions/user_review_fixes_instructions_core.md`
- `${CLAUDE_PLUGIN_ROOT}/instructions/qa_test_instructions.md`

A citer **points and never restates**, and no plugin asset beyond this list points at this file. A new citer joins this list. An edit that rewords or moves a heading updates every roster member in the same change. The agents carry the sentence `## The return block` fixes and do not point here. A document outside the plugin cites this file by its repo-relative path and is not a roster member.
