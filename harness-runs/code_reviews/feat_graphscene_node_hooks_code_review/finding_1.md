### 1. Gate legs `3g` and `3h` still print "format-4", while `docs/development.md` now says the legs as printed cover format 5

**File:** `scripts/run-gates.sh` (the `3g)` and `3h)` arms of the gate dispatch `case`) — "3g format-4 graphs validate against the graphscene schema" and "3h format-4 schema negatives are refused"

This branch moves the flow-graph schema to format 5 (`graphscene/src/graphscene/schemas/flow-graph.schema.json` → `formatVersion.const` is `5`, and `cli/templates/scripts/flows/task_plan_writing.graph.json` is `"formatVersion": 5`). Task 17 updated `docs/development.md` → **Gate 3** to read *"The last two lines, legs `3g` and `3h` as `scripts/run-gates.sh` prints them, cover format 5"*. The script still prints the old labels, so the document of record and the gate output a maintainer reads now disagree: every `bash scripts/run-gates.sh` run prints `3g format-4 graphs validate …` and `3h format-4 schema negatives are refused` over a check that validates format-5 graphs.

`scripts/run-gates.sh` is hand-written and is not in the set `init --force` regenerates (`docs/development.md` → `## 5. Verifying a change`, opening), so the scope register's exclusion of self-adopted copies under `scripts/` does not cover it. It belongs to the `general` layer, and nothing else in the tree quotes either label. A `git grep` for both strings outside `harness-runs/` matches only these two lines.

Graded Should Fix: the label is output wording, and no step a reader follows from it fails.

**Fix:** in `scripts/run-gates.sh`, change the two gate labels. Leave the `gate_header` text and the commands as they are:

```bash
    3g) gate_header 3 "configuration and flow-graph schemas"; gate "3g format-5 graphs validate against the graphscene schema" npm run validate:graphscene-schema ;;
    3h) gate_header 3 "configuration and flow-graph schemas"; gate "3h format-5 schema negatives are refused" npm run validate:graphscene-schema:negative ;;
```

This fix edits no test file, so it runs no test. The gates themselves run in the Run gates phase.
