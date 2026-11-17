### 1. Rename the `layer-implementer` outcome `already passing` to the one-token `already_passing`

**File:** `plugin/schemas/layer-implementer.return.json` (the row-G.4 `oneOf` variant) — "\"const\": \"already passing\""

**Problem.** Every other `outcome` value under `plugin/schemas/` is one token: `PASS`, `FAIL`, `returned`, `questions`, `blocker`, `no_ui`, `implemented`, `prohibited`, `SAFE`, `UNSAFE`. So is every outcome key in `cli/templates/scripts/flows/task_plan_writing.graph.json`, along with `error`, which a caller records. `layer-implementer`'s row-G.4 variant is the one exception: `"const": "already passing"`. Outcome values are meant to become a graph node's outcome keys later without renaming (`docs/structured-agent-returns.md` → `### One discriminator, `outcome`, held to the graph`). A value with a space works today only because `flow-walker.sh` flattens the graph into tab-separated lines. It is the one value that has to be quoted wherever it is passed as an argument (`--outcome`), split from a list or turned into an identifier. The space came from carrying over the old literal `already passing — ` (`docs/structured-agent-returns.md` → "The literal a caller matched before becomes the outcome value it routes on."). That rule keeps the literal's words. It does not require keeping the space.

**Fix.** Rename the **outcome value** to `already_passing` everywhere it is used as an outcome, in one change, so the schema and every caller stay in agreement. Grep-verified sites in the current tree:

- [ ] `plugin/schemas/layer-implementer.return.json`: the row-G.4 variant's `"outcome": { "const": "already passing", … }` becomes `"const": "already_passing"`. Leave its `description` strings alone.
- [ ] `plugin/agents/layer-implementer.md`:
  - the row-G.4 check's **Passes:** bullet, "return an `outcome` of `already passing`" → `already_passing`;
  - `### Return fields`, the `outcome` bullet, "`already passing` only on a row-`G.4` dispatch" → `already_passing`;
  - the `flags` bullet, "`implemented`, `prohibited` and `already passing`, omitted when empty" → `already_passing`;
  - the `cause` bullet, "`prohibited` and `already passing` only" and "An `already passing` cause defaults to" → `already_passing`.
  - Keep the default cause text `already passing after an earlier fix`, the `## Already passing` record heading, `**The already-passing record.**` and the prose "a layer both refused and already passing returns `prohibited`". None of them is an outcome value.
- [ ] `plugin/instructions/unit_loop_core.md`. Rename only where the text says "an `outcome` of `already passing`", or names the value `` `already passing` `` as an outcome:
  - the `<escalate>` row of `## Mode contract — bindings this file uses` (both occurrences);
  - the paragraph "**The third unit outcome adds none either.**" ("Its second outcome, `already passing`");
  - `## The unit loop` step 3: the "The fields that check reads are" sentence and the two routing bullets, "An `outcome` of `already passing`, on row `G.4` only" and "an `outcome` of `already passing` on any other row … for an `outcome` of `already passing`";
  - `### The dispositioned outcome`, its opening paragraph ("on row `G.4` an `outcome` of `already passing`" and "the `already passing` route is row-scoped to `G.4`");
  - `#### The already-passing close`, its opening line ("returns an `outcome` of `already passing`");
  - the review-fix bullet "**A finding an earlier unit's fix already cleared.**" ("close on an `outcome` of `already passing`").
  - **Keep unchanged:** the heading `#### The already-passing close`, which other files cite as an anchor; the `## Already passing` record section name; the commit body line `mark <unit token> already passing — <cause>`; and step 6's progress clause `already passing: `. The user named the last two as not outcome values.
- [ ] `plugin/instructions/plan_orchestration_instructions_core.md` → `## Stop conditions (halt and do NOT continue)`, the implementer bullet: "or on row `G.4` of `already passing`" → `already_passing`.
- [ ] `plugin/instructions/user_review_fixes_instructions_core.md`: the `<escalate>` binding row ("an `outcome` of `already passing` on a row other than `G.4`" and "or of `already passing` on row `G.4`") and the `## Stop conditions (halt and do NOT continue)` implementer bullet ("or on row `G.4` of `already passing`").
- [ ] `plugin/instructions/user_review_fixes_instructions_autonomous.md`: the closed-list paragraph that opens "Both bindings resolve to the **same** file-based channel", at "an `outcome` of `already passing` on a row other than `G.4`".

**Out of this finding's scope.** Leave these untouched. They are commit-body or record wording, not outcome values:

- `cli/templates/scripts/lib/unit-commit-lib.sh` and its mirror `scripts/lib/unit-commit-lib.sh` (`ucl_body_record`, "mark $token already passing — $ap");
- `cli/templates/scripts/commit-on-branch.sh` and `scripts/commit-on-branch.sh` (the header comment's `mark <token> already passing — <cause>`);
- `cli/test/unit-commit-lib.test.mjs`;
- `cli/templates/claude/context/conventions.md`;
- `docs/work-report-research/**`.

**Check before closing.** A repo-wide grep for "outcome` of `already passing" and "\"already passing\"" under `plugin/` returns nothing. The surviving hits for "already passing" are exactly the commit-body line, the progress clause, the `## Already passing` record heading, the default cause text and the plain-prose uses listed above.
