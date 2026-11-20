`feat_flow_graph_schema_v2` lets each flow graph declare its own vocabulary instead of being checked against the harness's fixed lists. Part of #376.

## Why

`schemas/flow-graph.schema.json` has closed lists built in: outcomes (`returned/PASS/FAIL/questions/no_ui/error/blocker`), phases (`parity/qa/docs`), bindings (`<ask>/<escalate>/<terminal_handoff>`) and node kinds (`dispatch/round/terminal`). A generic engine can't ship those.

The walker also gives some of those names fixed behaviour: `<ask>` parks and resumes with `answered`, `<escalate>` stops with a reason, `<terminal_handoff>` ends the walk, `error`/`blocker` are held in a round until their siblings finish, and a round routes on `PASS`/`FAIL`. Declaring the names alone would move that coupling, not remove it.

## Decided (2026-11-20)

- **The generic schema moves into `graphscene/`**, and the harness reads it from there. It travels with the library when it is extracted.
- **The bash walker stays on formatVersion 3.** The harness's planning graph is authored in the new format, and the v3 file the bash walker and `scripts/check-flow-graph.sh` read is generated from it until the cutover (#419). The v3 schema in `schemas/` stays as it is for that file.
- **The review-loop keys are carried over unchanged:** `findingsFolder`, a round's `writer`, `convergingFrom`, `revisionNote`, `plan`, `prompts` and an edge's `prompt`. Turning them into a pattern is #417's.

## Leads

_The leads below are starting points from #376 and the discussion that split it, not requirements. The planning session decides what holds when this branch is planned._

- **Format version.** The branch name's "v2" means the second generation of the schema; the current formatVersion is 3, so the new one is 4.
- **A graph declares behaviour, not only names (proposal).** Each declared name maps to an engine primitive, and the engine routes on the primitive, never on the name. A sketch, not a shape to copy:
  ```json
  "vocabulary": {
    "outcomes": {
      "returned": {}, "questions": {}, "no_ui": {},
      "PASS": { "verdict": "pass" },
      "FAIL": { "verdict": "fail" },
      "error": { "held": true },
      "blocker": { "held": true }
    },
    "bindings": {
      "<ask>": { "primitive": "interrupt", "resumeOutcome": "answered" },
      "<escalate>": { "primitive": "stop", "reasons": ["cap", "error", "blocker"] },
      "<terminal_handoff>": { "primitive": "end" }
    }
  }
  ```
  A round's join reads `verdict` and `held`. An interrupt needs a `resume` node, a stop carries a reason, and an end finishes the walk. Which primitives exist is the engine's, matching #376's "park as an interrupt".
- **Node kinds probably stay engine vocabulary (proposal).** `dispatch`, `round` and `terminal` are what the engine executes, so a graph declaring a new kind could not give it behaviour. #376 lists node kinds among what a graph declares; if a reason to declare them turns up while planning, that wins.
- **Skips become host-answered predicates that keep today's two statuses (proposal).** Both skip types route the same way: no dispatch, and a round's join counts the node as passed. They differ in:
  - *Source:* `skipped` is answered by `phases.<x>` in `devscene.config.json` (the project's setting); `passedByExclusion` by the run mode's skipped ids (this run's choice).
  - *What is recorded:* `skip: <node> skipped` is reported as not converged (`task_plan_writing_instructions_core.md` → hand-off report); `passed-by-exclusion` is disclosed with the run mode as a pass.
  - *Cap escalation:* only a `skipped` node is left out of `roundCounts` (`flow-walker.sh` → `add_skipped_node`).
  - *Precedence:* entry order, run mode first (`cli/test/flow-walker.test.mjs` case 6).

  One shape: a skip entry names a predicate (`{ "when": "<predicate>", "to": …, "report": … }`), and the graph declares each predicate with the status it records and whether the node counts in round counts. The host answers true, false or "cannot answer"; "cannot answer" refuses, as both types do today. The graph never reads config.
- **Used names checked against declared ones.** JSON Schema draft-07 cannot take an enum from the document's own data, so this check cannot live in the schema. It could land in the schema's own tests here, in #414's loader or in #415's checker. The v3 negatives `flow-graph-schema-unknown-outcome.json` and `-unknown-binding.json` show what it must reject.
- **The v3 generator is harness code.** Mapping predicates back to `phase`/`runModeId` and primitives back to the fixed names is harness knowledge, so it stays outside `graphscene/`. A gate check that the committed v3 file equals the generated one keeps the two from drifting, as `scripts/check-rendered-workflows.mjs` does for workflows. Both v3 copies are in scope: `cli/templates/scripts/flows/` and the self-adoption copy in `scripts/flows/`.
- **The v4 source isn't shipped to adopters until the cutover.** `cli/src/generators/outerLoopScripts.ts` ships only the v3 file.
- The harness's own vocabulary lives with the harness's graphs (`cli/templates/scripts/flows/task_plan_writing.graph.json`), not in `graphscene/`.
- Readers of the graph that stay on v3: `cli/test/agent-return-schemas.test.mjs` (agent `outcome` values equal a node's outcome keys), `scripts/check-flow-graph.sh`, the `validate:flow-graph*` npm scripts.

## Depends on

#412 (ordering only)

