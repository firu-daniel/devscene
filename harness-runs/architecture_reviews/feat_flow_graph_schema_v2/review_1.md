# Architecture review — round 1

verdict: PASS
review_mode: full

## Should Fix

1. **`task_1_plan.md` (and the story index `## Context`, *What is decided*): the format-4 source is placed in `cli/templates/`, but that tree's stated content is the files `init` writes into an adopting repository.** This was raised in round 0 and is unchanged in this revision.
   - **The rules.** `.claude/context/cli.md` → `## What this layer owns, and what it is not` says the layer owns *"`cli/templates/` (the files `init` writes into an adopting repository)"*. `.claude/context/conventions.md` → `### Where a new responsibility goes` sends *"a file a future adopter receives"* to `cli/templates/`. `cli/templates/README.md` maps each subdirectory to an *"Adopter-side home `init` writes to"*, and maps `scripts/` to the configured `scriptsDir`.
   - **Why the file does not fit.** `cli/templates/scripts/flows/task_plan_writing.v4.graph.json` has no adopter-side home. The plan states that `init` never writes it and that `OUTER_LOOP_SCRIPTS` has no row for it. Its only readers are the root `general`-layer tools of Tasks 4 and 5.
   - **Why the cited lead does not settle it.** The plan cites the task prompt's lead, which places the harness vocabulary *"with the harness's graphs"*. But the prompt calls its leads *"starting points … not requirements"*.
   - **The concrete cost.** The file ships in the npm tarball, which the plan accepts. `cli/templates/README.md`'s description of the tree also becomes false, and Task 1 amends only `cli/templates/scripts/README.md`.
   - **Why this is Should Fix, not Must Fix.** No failure sentence can be completed. No step in the plan fails, and no test lists the template tree against `OUTER_LOOP_SCRIPTS`. I checked this again: `cli/test/agent-return-schemas.test.mjs` walks `cli/templates/scripts/**`, but only for backticked `` `<agent>.<field>` `` citations, which JSON carries none of. The other `cli/templates/scripts/**` tree guards are limited to `*.sh` / `*.jq` or do not read `flows/`. Also, the planned cutover makes this the file adopters will receive.

   **Fix (suggested):** do one of these:
   - Move the v4 source out of `cli/templates/` to a root `general`-layer location beside its only readers (`scripts/generate-flow-graph-v3.mjs` and the `validate:graphscene-schema` npm script).
   - Keep it where it is, and have Task 1 also add a sentence to `cli/templates/README.md` naming the one file in the tree that `init` does not write, and why it sits there until the cutover.

## Nice to Have

1. **`task_4_plan.md`: the generator's "used name the vocabulary does not declare" refusal repeats clauses 1, 3 and 7 of Task 3's `graphscene.vocabulary.vocabulary_violations` in JavaScript.** This duplication is acceptable: the generator cannot map a name it has no entry for, and the plan forbids it from running Python. Task 4's header bullets still do not say which check owns the rule. Add one header line to `scripts/generate-flow-graph-v3.mjs` saying that its refusal exists only to make the mapping total, and that the authoritative used-against-declared check is `graphscene.vocabulary`. Without it, a later reader may treat the two as rival owners (`.claude/context/conventions.md` → *"Before adding a copy of anything, grep for it."*).
