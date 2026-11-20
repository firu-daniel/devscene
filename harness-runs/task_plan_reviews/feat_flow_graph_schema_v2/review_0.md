# Task plan review — round 0

verdict: FAIL
review_mode: full

## Must Fix
1. **`task_2_plan.md` — the first Verification command is a usage error under `schemas/validate.mjs`**
   `schemas/validate.mjs` → `parseArgs` takes one data file per `-d` flag (`(arg === '-s' ? schemas : data).push(value); i += 1;`). Any other bare argument goes to `positionals`, and `positionals.length !== 1` returns `null`, which prints the usage line and exits 2. The bullet gives `cli/templates/scripts/flows/task_plan_writing.v4.graph.json` as a second bare argument after a single `-d`, so `positionals` is `['validate', '…v4.graph.json']` and the command exits 2 before it compiles the schema. The header's own form is `-d <file> [-d <file> ...]`, which is the form `package.json` → `validate:flow-graph` uses.
   **Raised against:** "`node schemas/validate.mjs validate -s graphscene/src/graphscene/schemas/flow-graph.schema.json -d graphscene/tests/fixtures/flow_graph/valid_generic.json cli/templates/scripts/flows/task_plan_writing.v4.graph.json` exits 0"
   **Must hold:** Every `schemas/validate.mjs` command the task file gives puts its own `-d` flag before each data file, so the command runs as written.
   **Class:** Wrong action from operative text
   **Failure:** If the implementer runs Task 2's first Verification command as written, then `schemas/validate.mjs` prints `usage: …` and exits 2, so neither the strict-mode compile nor either graph is checked and the bullet's "exits 0" cannot be met.
   **Fix:** In `task_2_plan.md` → **Verification:**, rewrite the command as `node schemas/validate.mjs validate -s graphscene/src/graphscene/schemas/flow-graph.schema.json -d graphscene/tests/fixtures/flow_graph/valid_generic.json -d cli/templates/scripts/flows/task_plan_writing.v4.graph.json`.

2. **`task_2_plan.md` — the no-harness-name grep matches the verdict enum the same task requires**
   The bullet runs `git grep` with `-i`, and `-i` applies to every `-e` pattern. So `'"PASS"'` also matches the lowercase `"pass"`. Task 2's own **Work:** requires the schema to carry `verdict` (`enum: ["pass", "fail"]`), so the schema file always contains the string `"pass"` and the grep can never print nothing. The bullet contradicts the Work it is meant to verify.
   **Raised against:** "`git grep -n -i -e devscene -e \"<ask>\" -e '\"PASS\"' -- graphscene/src` prints nothing."
   **Must hold:** Every Verification bullet in the task file can pass on a tree that carries exactly what the task's Work requires. The check for harness names must not match the generic `pass`/`fail` verdict values.
   **Class:** Wrong build
   **Failure:** If the implementer builds the schema as the Work bullet requires and runs this Verification bullet, then `git grep` prints the `"enum": ["pass", "fail"]` line of `graphscene/src/graphscene/schemas/flow-graph.schema.json`, and the unit cannot meet its own acceptance without breaking its Work.
   **Fix:** In `task_2_plan.md` → **Verification:**, make the harness-name match case-sensitive. For example, keep `-i` only on the `devscene` pattern by running two greps: `git grep -n -i -e devscene -- graphscene/src` and `git grep -n -F -e '<ask>' -e '"PASS"' -e '"FAIL"' -- graphscene/src`. Each prints nothing.

3. **`task_3_plan.md` — the no-harness-name grep matches the text the same task requires**
   This is the same defect as entry 2, made worse because the pattern is `"PASS"` with no quotes, under `-i`. That matches every `pass`: the schema's `["pass", "fail"]` enum (Task 2), the violation strings Task 3's own clause 2 requires (`a round routes on one outcome declaring verdict pass and one declaring verdict fail`), and any `passed` in a description.
   **Raised against:** "`git grep -n -i -e devscene -e \"<ask>\" -e \"PASS\" -- graphscene/src` prints nothing."
   **Must hold:** Every Verification bullet in the task file can pass on a tree that carries the exact violation strings its Work requires.
   **Class:** Wrong build
   **Failure:** If the implementer writes `vocabulary.py` with clause 2's required message and runs this Verification bullet, then `git grep` prints that line and the schema's `"pass"` enum, and the unit cannot meet its acceptance without changing a required violation string.
   **Fix:** In `task_3_plan.md` → **Verification:**, replace the bullet with a case-sensitive, fixed-string harness-name check, as in entry 2, for example `git grep -n -F -e '<ask>' -e '"PASS"' -e '"FAIL"' -- graphscene/src` plus a separate `git grep -n -i -e devscene -- graphscene/src`. Both print nothing.

## Should Fix
- **`task_3_plan.md` → Verification and `task_5_plan.md` → Work, the `-d` form.** `-d <every vocabulary_negative_*.json>` (Task 3) and `-d <file>…` (Task 5, `validate:graphscene-schema`) can be read as one `-d` followed by several files, which `schemas/validate.mjs` → `parseArgs` refuses with exit 2 (see Must Fix 1). Spell out `-d` before every file. Task 5's script is a committed gate leg, so the run would catch it, but the plan should not leave it to be discovered.
- **`task_4_plan.md` → The printer.** The stated starting rule, "an object printed inline … when every value is a scalar and the line fits", is contradicted by the committed file. `nodes.convergence` (`{ "kind": "terminal", "binding": "<terminal_handoff>" }`, about 70 characters at indent 4) holds only scalars and is printed across several lines, while longer all-scalar edges such as `"PASS": { "to": "ui_writer", "reset": "iteration", "ledger": "P1" }` are inline. The bullet does say to derive the rule and adjust it until `--check` passes, but it would help to say that node objects (depth 2 under `nodes`) are always expanded.
- **`task_2_plan.md` → Work, "A dispatch node keeps v3's keys".** In v3, `heartbeat` carries `pattern: "\\{iteration\\}"` and `findingsFolder` carries `pattern: "^\\{state_dir\\}/.+/$"`. Both are harness tokens, and keeping v3's shape carries them into the generic schema. So `valid_generic.json` must use a `{iteration}` heartbeat and a `{state_dir}/…/` findings folder to be schema-valid, and the task file does not say so. Name the choice: either keep the patterns as carried-over review-loop keys, as the prompt's *Decided* list allows for `findingsFolder`, and say what the generic fixture must carry, or relax them.
- **`task_3_plan.md` → `test_vocabulary.py`.** The bullet quotes `.claude/context/graphscene.md` → `## Tests` (*"…plus one clean case and one run against the real tree"*) but plans no run against the real tree. The harness's v4 graph is outside `graphscene/` and must stay unread from there, so put the omission and its reason in the file's *"Deliberately not covered:"* list rather than leaving it out silently.

## Nice to Have
- **Story index → `## Scope register`.** Derivation entries 1 and 2 were re-run verbatim from the checkout root, and every file they print is a row (rows 1–29). Entry 3 was re-walked over `harness-runs/lessons.md`, and rows 30–32 are the rules it reaches. No gap was found. The register is noted here only as verified.
