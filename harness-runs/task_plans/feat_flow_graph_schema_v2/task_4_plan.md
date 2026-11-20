### Task 4 — Generate both format-3 graph copies from the format-4 source with `scripts/generate-flow-graph-v3.mjs`

**Goal:** Make the format-4 graph the one the harness authors, and the format-3 graph the bash walker reads a generated file. A hand-written root script maps format 4's declared predicates and primitives back to the fixed v3 names, writes both committed v3 copies on request, and by default checks that both equal what it would write.

**Depends on:** Task 1, which produces `cli/templates/scripts/flows/task_plan_writing.v4.graph.json`. That file has the format-3 graph's key order with a `vocabulary` key inserted after `description`, `"formatVersion": 4`, and skips written as `{ "when", "to", "report"? }`. Its vocabulary is:

- `outcomes` `returned`/`questions`/`no_ui` `{}`, `PASS` `{ "verdict": "pass" }`, `FAIL` `{ "verdict": "fail" }`, `error`/`blocker` `{ "held": true }`;
- `bindings` `<ask>` `{ "primitive": "interrupt", "resumeOutcome": "answered" }`, `<escalate>` `{ "primitive": "stop", "reasons": ["cap", "error", "blocker"] }`, `<terminal_handoff>` `{ "primitive": "end" }`;
- `predicates` `phase_parity_off`, `phase_qa_off` (`records: "skipped"`, `inRoundCounts: false`) and `run_mode_skips_parity`, `run_mode_skips_architecture`, `run_mode_skips_qa` (`records: "passed-by-exclusion"`, `inRoundCounts: true`).

This task does not validate the v4 file against the schema; that is Task 5's `npm run validate:graphscene-schema`.

**Where this layer stops.** This is harness code and it stays outside `graphscene/`: it imports nothing from there and runs no Python. It changes no committed v3 byte. Its acceptance is that `--check` passes against the two v3 copies **as they are committed today**. Wiring `--check` into gate 3 is **Task 5's**, and documenting it is **Task 6's**.

### Targets

- `scripts/generate-flow-graph-v3.mjs` (new) — the generator and drift check.

**Work:**

- [ ] **Header**, modelled on `scripts/check-rendered-workflows.mjs`:
  - `#!/usr/bin/env node`, then `// generate-flow-graph-v3.mjs — …`, *"Hand-written for this repository, like check-flow-graph.sh; not an `init` output."*
  - **THE RULE**: both committed format-3 graphs equal the one generated from the format-4 source, which is the file the harness authors until the bash walker reads format 4.
  - Why the mapping is harness knowledge kept here and not in `graphscene/`.
  - **Usage**: `node scripts/generate-flow-graph-v3.mjs [--check]` (the default) | `--write` | `--check --source <path>`.
  - **Exit**: 0 clean or written · 1 one or more findings, each on stderr as `generate-flow-graph-v3: <file> — <reason>`, all reported · 2 bad usage.

  Paths are fixed constants resolved against the repository root, which it takes from `git rev-parse --show-toplevel` run with `cwd` at the script's own directory, as `check-rendered-workflows.mjs` does: the source `cli/templates/scripts/flows/task_plan_writing.v4.graph.json` and the targets `cli/templates/scripts/flows/task_plan_writing.graph.json` and `scripts/flows/task_plan_writing.graph.json`. Use only `node:` builtins.
- [ ] **The mapping tables**, each a frozen constant with a comment naming the walker behaviour it encodes (`cli/templates/scripts/flow-walker.sh` → the `answered` refusal, `round.held.<gate>`, `add_skipped_node`):
  - `V3_OUTCOMES` — `returned`, `questions`, `no_ui` → `{}`; `PASS` → `{ verdict: 'pass' }`; `FAIL` → `{ verdict: 'fail' }`; `error`, `blocker` → `{ held: true }`.
  - `V3_BINDINGS` — `<ask>` → interrupt with `resumeOutcome: 'answered'`; `<escalate>` → stop whose `reasons` ⊆ `cap`, `error`, `blocker`; `<terminal_handoff>` → end.
  - Predicate names: `^phase_(parity|qa|docs)_off$` → `{ construct: 'skipped', phase: <x> }`, and it must declare `records: 'skipped'`, `inRoundCounts: false`. `^run_mode_skips_([a-z][a-z0-9_-]*)$` → `{ construct: 'passedByExclusion', runModeId: <id> }`, and it must declare `records: 'passed-by-exclusion'`, `inRoundCounts: true`.
  - `V3_DESCRIPTION` — the v3 graph's current `description` string, verbatim, because the v3 file's description is about the v3 file.
- [ ] **Generation** — `generate(v4) → { text } | { findings }`. It refuses, and produces no text, on each of these, one finding per occurrence, naming the JSON path:
  - a `formatVersion` other than 4;
  - a declared outcome or binding whose name is not in the tables above, or whose entry differs from the table's;
  - a predicate that matches neither pattern, or whose `records`/`inRoundCounts` disagree with its construct;
  - a used outcome, binding or `when` that the vocabulary does not declare (it cannot be mapped).

  Otherwise it builds the v3 object: `formatVersion: 3`; `vocabulary` dropped; `description` ← `V3_DESCRIPTION`; each skip `{ when, to, report }` → `{ construct, phase | runModeId, to, report? }` in that key order; every other key and value carried in its source order.
- [ ] **The printer** reproduces the committed v3 files byte for byte: two-space indent, arrays of scalars on one line, an object printed inline as `{ "k": v, … }` when every value is a scalar and the line fits, and a trailing newline. Derive the exact rule from the committed file (`counters.iteration`, an `error` edge and `ui_writer`'s `no_ui` `report` are inline; `paths` and every `onCap` are not). Adjust the rule, never the committed bytes, until `--check` passes. `docs/flow-graph-walker.md` → `## 1. The core's size, measured` records the file's `wc -c` as a measured fact, and `init --upgrade` replaces every adopter copy whose bytes differ.
- [ ] **Modes**:
  - `--check` (default) — generate, then compare the text with each target's bytes. A difference is the finding `<target> — differs from the graph generated from cli/templates/scripts/flows/task_plan_writing.v4.graph.json; run node scripts/generate-flow-graph-v3.mjs --write`.
  - `--write` — generate, and only when there are no findings write both targets.
  - `--source <path>` (accepted only with `--check`) — read another format-4 file, so a refusal can be reproduced by hand against a planted copy under `$TMPDIR`.
  - Anything else exits 2 with a usage line. An unreadable or unparseable file is a finding naming it.

**Verification:**

- `node scripts/generate-flow-graph-v3.mjs` exits 0 with the two v3 copies unedited. This is the first `Top risks:` entry in the story index.
- `node scripts/generate-flow-graph-v3.mjs --write` followed by `git diff --exit-code -- cli/templates/scripts/flows/task_plan_writing.graph.json scripts/flows/task_plan_writing.graph.json` shows no change.
- Copy the v4 source to `$TMPDIR` and plant each change in turn: `PASS` re-declared as `{ "held": true }`; a `when` renamed to `phase_lint_off`; an edge outcome `skipped_review` that the vocabulary does not declare. `--check --source <copy>` exits 1, printing a finding that names the planted path, and writes nothing.
- `node scripts/generate-flow-graph-v3.mjs --bogus` exits 2.
- `git grep -n -e "graphscene" -- scripts/generate-flow-graph-v3.mjs` finds no import: only prose may name the library.
