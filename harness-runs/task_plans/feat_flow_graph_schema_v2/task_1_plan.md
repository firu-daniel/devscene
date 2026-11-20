### Task 1 — Author the planning graph in format 4 at `cli/templates/scripts/flows/task_plan_writing.v4.graph.json`

**Goal:** Write the harness's planning graph in the generic format 4, declaring its own vocabulary, as the authoring source the two committed format-3 copies will be generated from. Routing does not change: every node, edge, counter, path, report slot and skip order equals today's `cli/templates/scripts/flows/task_plan_writing.graph.json`.

**Where this layer stops.** This task writes data and one README sentence. It adds **no** `OUTER_LOOP_SCRIPTS` row, so `init` never writes the file to an adopter. It also changes no format-3 file. Validating this file against the format-4 schema is Task 5's job (`npm run validate:graphscene-schema`), and the schema itself is Task 2's. Generating the v3 copies from this file is Task 4's job. The format this file follows is the story index `## Context` → **The vocabulary block**, restated below so this file is complete on its own.

### Targets

- `cli/templates/scripts/flows/task_plan_writing.v4.graph.json` (new) — the format-4 planning graph.
- `cli/templates/scripts/README.md` — one sentence on the new file.

**Work:**

- [ ] **Copy, then change only the format-4 differences.** Start from `cli/templates/scripts/flows/task_plan_writing.graph.json` and keep every key in its order: `formatVersion`, `flow`, `description`, then insert `vocabulary`, then `start`, `entries`, `counters`, `paths`, `reports`, `nodes`. Keep every node's own key order as well. Change only these:
  - `"formatVersion": 4`.
  - `description` becomes a statement of what *this* file is: the planning flow's routing in format 4, the source from which `scripts/generate-flow-graph-v3.mjs` generates the format-3 graph the walker reads, and a file `init` does not copy. Write the description without the v3 text's "Copied verbatim into the adopter's scripts directory" sentence, because that sentence is false of this file. Task 4 owns the v3 description.
  - Every `skip` entry is rewritten as in the next bullet.
  - Every other value (`agent`, `heartbeat`, `prompts`, `findingsFolder`, `outcomes`, edges, `onCap`, `ledger`, `report`, round keys) is carried over unchanged.
- [ ] **Declare the vocabulary** — exactly what the graph uses, no more:
  - `"outcomes"`: `"returned": {}`, `"questions": {}`, `"no_ui": {}`, `"PASS": { "verdict": "pass" }`, `"FAIL": { "verdict": "fail" }`, `"error": { "held": true }`, `"blocker": { "held": true }`.
  - `"bindings"`: `"<ask>": { "primitive": "interrupt", "resumeOutcome": "answered" }`, `"<escalate>": { "primitive": "stop", "reasons": ["cap", "error", "blocker"] }`, `"<terminal_handoff>": { "primitive": "end" }`.
  - `"predicates"`:
    - `"phase_parity_off": { "records": "skipped", "inRoundCounts": false }`
    - `"phase_qa_off": { "records": "skipped", "inRoundCounts": false }`
    - `"run_mode_skips_parity": { "records": "passed-by-exclusion", "inRoundCounts": true }`
    - `"run_mode_skips_architecture": { "records": "passed-by-exclusion", "inRoundCounts": true }`
    - `"run_mode_skips_qa": { "records": "passed-by-exclusion", "inRoundCounts": true }`

  These predicate names are the contract Task 4 maps back to v3: `phase_<x>_off` ↔ `{ "construct": "skipped", "phase": "<x>" }` and `run_mode_skips_<id>` ↔ `{ "construct": "passedByExclusion", "runModeId": "<id>" }`.
- [ ] **Rewrite the skips as `{ "when", "to", "report" }`, keeping entry order** (order is precedence):
  - `business_parity_review`: first `{ "when": "run_mode_skips_parity", "to": "plan_round", "report": { "business_parity_review": "passed-by-exclusion" } }`, then `{ "when": "phase_parity_off", "to": "plan_round", "report": { "business_parity_review": "skipped" } }`.
  - `architecture_review`: `{ "when": "run_mode_skips_architecture", "to": "plan_round", "report": { "architecture_review": "passed-by-exclusion" } }`.
  - `ui_writer`: first `{ "when": "phase_qa_off", "to": "convergence", "report": { "ui_test": "qa-phase-off" } }`, then `{ "when": "run_mode_skips_qa", "to": "convergence", "report": { "ui_test": "run-mode-skipped" } }`.
- [ ] **Format it like the v3 file**: two-space indent, short flat objects on one line (`{ "to": "plan_round" }`), arrays of scalars on one line, and a trailing newline. Carry no `$schema` key, as the v3 graph carries none.
- [ ] `cli/templates/scripts/README.md`: in the paragraph that lists `flows/task_plan_writing.graph.json`, add one sentence saying that `flows/task_plan_writing.v4.graph.json` beside it is **not** written into `scriptsDir`. It is the format-4 source that this repository generates that graph from, and `cli/src/generators/outerLoopScripts.ts` carries no row for it. Name no adopter value.

**Verification:**

- `jq empty cli/templates/scripts/flows/task_plan_writing.v4.graph.json` exits 0.
- Delete the `vocabulary` key and map each skip back through the predicate table above. The result equals the v3 graph's nodes, edges, counters, paths, reports and entries, read side by side: no route moved.
- Every outcome key under any node's `outcomes`, every `binding` on an edge, an `onCap` or the terminal, and every `when` names an entry declared under `vocabulary`. Every declared entry is used at least once.
- `git grep -n "v4" cli/src/generators/outerLoopScripts.ts` prints nothing: no shipped row names the file.
- `cli/templates/scripts/flows/task_plan_writing.graph.json` and `scripts/flows/task_plan_writing.graph.json` are unchanged (`git diff --exit-code` on both).
