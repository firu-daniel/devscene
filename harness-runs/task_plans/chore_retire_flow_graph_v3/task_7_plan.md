### Task 7 — Delete the format-3 schema, its fixtures, the generator, the bash checker and gate legs 3c–3f and 3i

**Goal:** Remove the format-3 bridge's code from the repository root:
- the format-3 schema and both of its fixture families;
- the generator and its drift check;
- the bash checker;
- the `validate:flow-graph*` npm scripts;
- the five gate legs that ran them.

Gate 3 then holds legs `3a`, `3b`, `3g` and `3h`, and `3g` validates the format-4 graph under its shipped name.

**Depends on:** Task 1 and Task 6.
- **Task 1** moves the format-4 graph to `cli/templates/scripts/flows/task_plan_writing.graph.json` and removes `…/task_plan_writing.v4.graph.json`. This task re-points `validate:graphscene-schema` at the new path.
- **Task 6** ports the checks the bash checker ran that nothing else runs: 4–7, as `devscene-flow-host/tests/core_agreement.py` → `core_agreement_violations`, run by `devscene-flow-host/tests/test_core_agreement.py` and so by gate leg `13j`. Checks 1–3, 8 and 9 already run as `graphscene.static_violations` inside every `load_graph`. So deleting `scripts/check-flow-graph.sh` here drops no check.
- The generator's own names check needs no replacement: `graphscene.vocabulary_violations` runs inside every `load_graph`.

**Where this task stops.** This task removes code and its wiring. It changes no document's prose except the one paragraph of `schemas/negative/README.md` that describes fixtures it deletes. `docs/development.md` and `schemas/README.md` are **Task 8's**. `docs/flow-graph-walker.md`, `docs/watcher.md` and `ROADMAP.md` are **Task 9's**. The surviving legs keep their ids, so `3g` and `3h` are not renumbered. This repository's self-adopted `scripts/flows/` copies are not touched here: they are re-rendered after merge (story index → **Manual setup required**).

### Targets

- `scripts/generate-flow-graph-v3.mjs` — deleted.
- `scripts/check-flow-graph.sh` — deleted.
- `schemas/flow-graph.schema.json` — deleted.
- `schemas/flow-graph-check/` — deleted whole: its `README.md` and every `flow-graph-check-*.json`.
- `schemas/negative/flow-graph-schema-*.json` — deleted, every file matching.
- `schemas/negative/README.md` — the paragraph opening *"The second schema, `../flow-graph.schema.json`"*.
- `package.json` — `scripts`.
- `scripts/run-gates.sh` — the leg dispatch and the round's leg list.
- `scripts/check-rendered-workflows.mjs` — its header comment's second line.

**Work:**

- [ ] **Delete the scripts.** Delete `scripts/generate-flow-graph-v3.mjs` and `scripts/check-flow-graph.sh`. They are hand-written for this repository and are not `init` outputs, so no template or table names them.
- [ ] **Delete the schema and its fixtures.** Delete `schemas/flow-graph.schema.json`, the directory `schemas/flow-graph-check/` with its `README.md`, and every `schemas/negative/flow-graph-schema-*.json`. In `schemas/negative/README.md`, remove the paragraph that describes those six negatives and their `validate:flow-graph:negative` wiring. Keep every sentence about `devscene.config.schema.json`'s own negatives.
- [ ] **`package.json`.** Remove the `validate:flow-graph` and `validate:flow-graph:negative` scripts. In `validate:graphscene-schema`, change `-d cli/templates/scripts/flows/task_plan_writing.v4.graph.json` to `-d cli/templates/scripts/flows/task_plan_writing.graph.json`. Every other `-d` entry and every other script stays.
- [ ] **`scripts/run-gates.sh`.** Remove the `3c)`, `3d)`, `3e)`, `3f)` and `3i)` arms of the leg dispatch. Remove `3c 3d 3e 3f` and `3i` from the `gr_run_round run_unit 1 …` leg list, and from any other list or comment in the file that names those ids. Keep the `3g` / `3h` arms as they are, along with the gate-3 header text they print.
- [ ] **`scripts/check-rendered-workflows.mjs`.** Its header's *"Hand-written for this repository, like check-flow-graph.sh; not an `init` output."* names `check-llms-txt.sh` in place of `check-flow-graph.sh`. `check-llms-txt.sh` is the other hand-written check the deleted script itself cited. Change no code.

**Verification:**

- `git grep -n -E 'check-flow-graph|generate-flow-graph-v3|validate:flow-graph|flow-graph-check|flow-graph-schema-|(^|[^/])schemas/flow-graph\.schema\.json' -- package.json scripts schemas cli devscene-flow-host plugin ':!schemas/README.md' ':!scripts/flows'` prints nothing. The command is scoped to reach only the retired format-3 artifacts:
  - The `(^|[^/])` anchor keeps the schema alternative off the format-4 schema path `graphscene/src/graphscene/schemas/flow-graph.schema.json`, which stays. That path appears in `validate:graphscene-schema` / `validate:graphscene-schema:negative` (legs `3g` / `3h`) and in `cli/test/python-packages-staged.test.mjs`.
  - `graphscene` is left out of the pathspec. Its remaining hits are format-4 docstrings that cite their own package's schema as `` `schemas/flow-graph.schema.json` ``, which stays, and its bash-checker citations are Task 4's, checked by Task 4's own grep.
  - `schemas/README.md` is excluded because it is **Task 8's**.
  - `scripts/flows` is excluded because it holds this repository's self-adopted graph copies. No task edits them; they are re-rendered after merge (story index → **Manual setup required**).
  - Any hit in `cli/` (Tasks 1 and 2), `plugin/` (Task 3) or `devscene-flow-host/` (Tasks 5 and 6) is in a file an earlier task already finished, so this task does not own it.
  - Any hit under `docs/`, `ROADMAP.md` or `.claude/context/` falls outside this pathspec. It is a site of the story index's `## Scope register`, owned by Task 8 or Task 9 or recorded as stale, and is not this task's.
- `git ls-files schemas` lists `schemas/README.md`, `schemas/devscene.config.schema.json`, `schemas/validate.mjs`, and `schemas/negative/` with only the configuration negatives and their README.
- `grep -n -E '^ +3[a-z]\)' scripts/run-gates.sh` lists the arms `3a`, `3b`, `3g` and `3h` and no other gate-3 arm. The `gr_run_round run_unit 1` line names no removed id.
- `bash -n scripts/run-gates.sh` exits 0. This is a syntax check, not a run.
- `node -e "JSON.parse(require('fs').readFileSync('package.json','utf8'))"` exits 0. The `validate:graphscene-schema` value names `cli/templates/scripts/flows/task_plan_writing.graph.json`, and that file exists.
