# Task plan review — round 1

verdict: FAIL
review_mode: full

## Must Fix
1. **Index structure — the story index's `## Scope register` (`feat_structured_outputs_setup_story_plan.md`) has no row for `plugin/schemas/conventions-writer.return.json`, a site its own derivation entry P1 reaches**
   I re-walked P1 as written. Its traversal says the pattern `plugin/schemas/<agent>.return.json` *"is expanded once for each of the two agents the opening paragraph names"*. The pattern appears in the task prompt's `## Why` (*"The schema is `plugin/schemas/<agent>.return.json`"*), and P1's decision rule reaches *"a schema file"*. So P1 reaches two sites, `plugin/schemas/conventions-reviewer.return.json` and `plugin/schemas/conventions-writer.return.json`. The register has a row for the first only (row 1, Task 1). There is no row for the writer's schema, which `task_2_plan.md` → `### Targets` creates. No other site P1 reaches is missing. I also re-ran C1, C2 and C3 verbatim and re-walked P2: every site they reach is a row. This finding is disposition (i): an entry reaches a site that is not a row. The site list is complete: `plugin/schemas/conventions-writer.return.json`.
   **Raised against:** "| 1 | `plugin/schemas/conventions-reviewer.return.json` (new) | — | P1, `## The goal` item 1 | `change` | Task 1 |"
   **Must hold:** Every site any derivation entry in the register reaches appears as a row. That includes both expansions of P1's `plugin/schemas/<agent>.return.json` pattern, each with its disposition and owning task.
   **Fix:** In the story index's `## Scope register`, add a row for `plugin/schemas/conventions-writer.return.json` (new), with Copy `—`, Evidence `P1, `## Why` / `## The goal` item 1`, Disposition `change`, and owning task Task 2. Renumber the rows that follow, or append the new row.

## Should Fix
1. **`task_3_plan.md` — the decision-record paragraph still names the old `action_taken:` field and says it was folded into `outcome`.** Round 0 raised this. It is restated here only as a record for a human reader, not as a gating item. `docs/structured-agent-returns.md` is maintainer-facing, and it already records renames this way (`statistics-plan-writer`'s `error:` → `not_written`).

## Nice to Have
1. **`task_1_plan.md` — the clause added to `## What you do not do`** (*"`outcome` names the axis reviewed, never a judgement"*) adds words to the reviewer's definition without new behaviour. The reviewer already acts on *"No severity band and no verdict field"*. `.claude/context/plugin.md` → `## Writing agent prose` (*"An agent's growth is paid for by behaviour"*) leans against adding it. The decision record (Task 3) is where that rationale belongs.

## Incidental findings (not gating)
- Round 0's Must Fix is resolved. `task_3_plan.md` now rewrites `docs/analyze.md` → `## 8.` item 2's *"whose omission the caller's stop condition is what catches"* clause, with a `grep -n 'stop condition' docs/analyze.md` verification. I confirmed that `stop condition` occurs only in item 2 of that file. Register row 7's reason now names the clause.
- Checked against the tree: every pre-change hit of each task's `**Verification:**` grep in `plugin/agents/conventions-reviewer.md`, `plugin/agents/conventions-writer.md` and `plugin/commands/analyze.md` falls in a sentence that the owning task's `**Work:**` names. `cli/test/agent-return-schemas.test.mjs` → `itemProperties` unions item properties across variants, so the reviewer's axis-dependent `findings` items (with `document_path` / `check_id` only on `corpus_reviewed`) pass the static check as planned.
