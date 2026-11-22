# Task plan review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **Scope register misses a lessons-ledger row its own procedure entry reaches** — story index (`feat_graphscene_static_checker_story_plan.md`), `## Scope register`.
   I followed the standing-artifact procedure entry step by step. Its decision rule is *"a rule is reached when it names GraphScene, a flow graph, a check over a graph, a test-fixture family or a library's public surface"*. That rule reaches `harness-runs/lessons.md` → `## Agent prose`, *"A value a script or graph may route on (an outcome, a key, an id) is one token with no space; when it is carried over from an old literal, keep the literal's words and drop its spacing."* The "graph" in it is the harness's flow graph, so the rule is reached. It is not a row of the register. This is disposition (i): an entry reaches a site that is not a row. The only such site is that rule. It is graded Should Fix because it is a `no-change` site: the plan already complies, since `## Context` states *"Each id is one token with no space"*, and every check id it names (`node-known`, `reachable-from-start`, …) is one hyphenated token. So no work is missing; only the closure invariant is broken. Fix: add a row for that rule, disposition `no-change`, with the reason that every static check id is one token and the bash ids are carried over verbatim.

## Nice to Have

1. **The register's first `harness-runs/lessons.md` row cites the derivation as "command, `static check`; procedure not reached"** — story index, rows 22–23. Those two rules name a "static check" over agent prose, not over a graph. Saying in the reason cell why the procedure's decision rule does not reach them (the check is over prose, not over a graph) would let a later reviewer re-walk them without having to judge it again.

## Incidental findings (not gating)

- These derivations and plan claims were checked, and no gap was found:
  - The register's command entry was re-run verbatim. Every hit it prints appears as a row (`docs/development.md` 302/308, `docs/structured-agent-returns.md` ×3, `docs/flow-graph-walker.md` ×2, `graphscene/README.md` ×5, `ROADMAP.md`, both `harness-runs/lessons.md` hits, `schemas/flow-graph-check/README.md`, the conventions-document sites).
  - Each of the six `static_negative_*.json` fixtures was traced by hand against `valid_generic.json`, the model in `graphscene/src/graphscene/model/flow_graph.py` and the schema's `ordinaryEdge` `dependencies`. Each stays schema-valid and vocabulary-valid and fires exactly its one stated violation.
  - The `_EXPECTED[6:]` → `[7:]` shift in `graphscene/tests/test_public_surface.py` is correct.
  - The builder tolerates undeclared names, which the schema → build → vocabulary → static order needs. `test_a_vocabulary_failure_never_reaches_the_static_stage` relies on the same thing.
