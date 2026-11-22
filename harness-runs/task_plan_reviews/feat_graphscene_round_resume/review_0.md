# Task plan review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **`task_2_plan.md` — the skipped-gate cases cannot be built over `_two_gates` as it stands.** The `test_rounds.py` bullet says to add every case "over the module's existing two-gate planted graph (`_two_gates`)". That includes "**A record for a gate whose skip holds** (answered `True` by an `AnswerTable`)" and the variant "where every gate is skipped and the round would close at once". But `_two_gates`'s `_gate(crash_reason)` (`graphscene/tests/engine/test_rounds.py`) declares no `skip` entry. So `open_round` never asks the host, an `AnswerTable` answering `True` is never consulted, the gate stays due, and `enter_round` records the outcome instead of refusing it. The case cannot reach the skipped text unless the graph changes. Fix: say the skipped-gate cases use a skip-carrying variant of the planted graph — for example a `skip` parameter on `_gate` / `_two_gates` adding `{"when": "stage_disabled", "to": "review_round"}`, as `graphscene/tests/engine/test_walker.py` → `_gate(skip)` / `_graph(skip=True)` already does — with the skip on one gate for the first case and on both for the close-at-once variant.

## Nice to Have

1. **`task_4_plan.md` — the expected writer dispatch's `passed` is not named.** The end-to-end case asserts the final writer `draft` dispatch "from `_editor`'s sibling shape", and `_editor` hard-codes `passed=()`. The fail close appends a `RoundPassage("review_round", 2, "fail")` before following the `rejected` edge (`graphscene/src/graphscene/engine/transitions.py` → `close_round`), so the hand-written value should carry it. Naming it in the bullet saves the implementer a failing first run.
2. **`task_4_plan.md` → Verification** cites "the README's lines 14 and 15". Naming the two rows by anchor (the `src/graphscene/model/` and `src/graphscene/engine/` rows) would survive a line shift.

## Checks run (record)

- Index structure, per-task-file structure and the 1:1 correspondence all hold: 5 readiness entries, 5 task files, and headings match.
- Every task is single-layer. The order is graphscene ×4 then `general` last, which matches the configured `layers[]` order. Points are 8/15/20/15/5, and Work-bullet counts are 3/5/5/4/2 — all within budget.
- No conventions document is a target. Register rows 1–3 are `no-change`, and row 3 is recorded as `stale-rule`.
- `## Scope register` is owed, because `graphscene/README.md` and `ROADMAP.md` are corpus targets. It is present and correctly positioned. Re-running its command entry verbatim reaches exactly the 7 sites listed as rows 1–7. Re-walking the procedure entry over `harness-runs/lessons.md` reaches no rule. No gap.
- The cross-task interfaces (`RoundResume`, `enter_round`, `Walker.start(..., *, resume=...)`) are restated on both sides.
- Every planned behaviour was traced against the code: `record_gate`, `open_round`, `close_round`, `_dispatch`, the fixtures `_graph`, `_two_gates`, `_four_gate_graph` and `valid_generic.json`, and the `_EXPECTED[7:28]` slice. Every expected value checked holds (round 2 → fail → round 3 with `attempt` 1, held join, `Wait` → trimmed `DispatchSet`).
- No forbidden test run. "the one test file this task edits" describes the file and does not limit the guard run. No `lessons.md` lesson is repeated. The parity group was skipped (`phases.parity` is `false`).
