# Task plan review — round 2

verdict: PASS
review_mode: converging

## Incidental findings (not gating)
- Round 1's Must Fix is resolved. The story index's `## Scope register` now has row 36: `plugin/schemas/conventions-writer.return.json` (new), `change`, Task 2. The row has the same six columns as the table header, and `task_2_plan.md` → `### Targets` lists the file as `(new)`. The diff since `chore: Plan round 1 for feat_structured_outputs_setup` touches only that row, and no per-task file changed.
- The revision note shows a change to the register, so I re-ran the derivation duty in full:
  - I re-ran C1, C2 and C3 verbatim. Every file they reach is a row.
  - I re-walked P1 over the task prompt's sections in file order. `plugin/schemas/<agent>.return.json` expands to rows 1 and 36. The prompt's other backticked corpus paths map to rows 2–6 and 26. The script and test paths (`cli/test/agent-return-schemas.test.mjs`, `scripts/typecheck.sh`, `scripts/run-gates.sh`) are correctly not reached.
  - I re-walked P2 over the output of `grep -nE '^## |^- ' harness-runs/lessons.md`. The reached rules are the five under `## Agent prose`, the two rename rules and the two outcome rules, and they map to rows 27–35.
  - No site is missing, and the closure test holds. The register is still placed after `## Phase 2 Readiness`, with no `## Rejected findings` section.
