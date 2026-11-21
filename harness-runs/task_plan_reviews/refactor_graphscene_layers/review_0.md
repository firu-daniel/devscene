# Task plan review — round 0

verdict: FAIL
review_mode: full

## Must Fix
1. **`task_4_plan.md` — the closing Verification bullet fails on the edit Task 4 itself makes**
   Task 4's last Verification bullet re-runs the story index's `## Scope register` derivation entry A. It then requires that every line the command prints belongs to a `no-change` row and that no printed line belongs to a `change` row's site. Entry A's third alternative, `test_(errors|vocabulary|model|loader|public_surface)\.py`, is not anchored to a directory, so it also matches the new paths this branch writes. Task 4's own second Work bullet makes `docs/development.md`'s "two homes" paragraph name `graphscene/tests/engine/test_vocabulary.py`. Entry A matches that line, and it belongs to register row 5, a `change` row, so the bullet fails on correct work. Task 3's Work also adds `test_public_surface.py` to `graphscene/README.md`'s `tests/` row. Entry A prints that line too, and it belongs to no register row at all. Measured: at HEAD, entry A already prints `docs/development.md:308` on `test_vocabulary.py` alone. That alternative cannot tell an old path from its moved form.
   **Raised against:** "Re-run the story index's `## Scope register` derivation entry A verbatim. Every line it prints belongs to a register row whose disposition is `no-change`, and no line it prints belongs to a `change` row's site."
   **Must hold:** Every Verification bullet in Task 4 must pass when Tasks 1–4 are carried out as written. A check meant to show that no deleted path survives must match only the deleted path forms: never their moved forms (`tests/engine/test_vocabulary.py`), and never the unchanged package-wide test files that Task 3's README names.
   **Class:** Wrong action from operative text
   **Failure:** If the Task 4 implementer completes the Work bullet that names `graphscene/tests/engine/test_vocabulary.py` in `docs/development.md` and then runs the closing Verification bullet, entry A prints that line, which belongs to `change` row 5, and the bullet fails. The implementer either cannot finish or reverts the correct path to make the check pass.
   **Fix:** In `task_4_plan.md`, replace the bullet with a check that matches only the deleted forms. One way is to anchor the test-file alternative to the flat directory (`graphscene/tests/test_(errors|vocabulary|model|loader)\.py`), restrict the check to the documents Task 4 edits, and state the invariant as "prints nothing". Alternatively, keep entry A and state an invariant its output can meet after Tasks 1–4: every printed line is a `no-change` row's site or a line naming a moved path. Do not bake in a count.

## Should Fix
- **`\b` is inert under this checkout's `git grep -E`, in three commands.** Measured here: `git grep -cE 'graphscene\.errors\b' -- graphscene` prints nothing, while `git grep -cE 'graphscene\.errors' -- graphscene` reports 14 matches across 8 files. Three commands rely on a `\b` alternative:
  - **Story index:** `## Scope register` derivation entry A's first alternative, `graphscene\.(loader|model|errors|vocabulary)\b`, matches nothing. Rows 5 and 7 cite `graphscene.vocabulary` as entry-A evidence, but they were reached only through the path alternatives. Re-running that alternative portably, as `graphscene\.(loader|model|errors|vocabulary)([^A-Za-z0-9_]|$)` with `harness-runs/`, `graphscene/src` and `graphscene/tests` excluded, reaches only `docs/development.md` and `docs/flow-graph-walker.md`, which rows 5 and 7 already cover, so no site is missing.
  - **`task_1_plan.md`:** the "No old module path survives" bullet's `graphscene\.(loader|vocabulary|errors)\b` alternative prints nothing whatever survives. A leftover module path in a docstring would pass unseen; a leftover import would still fail the typecheck.
  - **`task_4_plan.md`:** the first Verification bullet's `graphscene\.vocabulary\b` alternative would not catch a leftover `graphscene.vocabulary.vocabulary_violations` in `docs/development.md` or `docs/flow-graph-walker.md`.

  In each command, replace `\b` with `([^A-Za-z0-9_]|$)`.
- **Story index → `## Scope register`: entry C reaches sites that have no row (disposition (i)).** Re-running entry C also prints these lines, none of them a row:
  - `.claude/context/conventions.md:253`, the closing `_Written by …_` provenance paragraph, which cites `graphscene/tests/test_boundary.py`. Row 12 lists only `## The layers`, `## The testing bar` and `## Not determined`.
  - `.claude/context/graphscene.md:52`, the `## Not determined` mocking bullet.
  - `.claude/context/graphscene.md:55`, the closing `_Written by …_` paragraph. Row 10 lists only `## What it may depend on`, `## Naming and layout` and `## Tests`.

  All three are conventions-document sites, so each takes `no-change`. Add them to rows 10 and 12, or as rows of their own, so the closure invariant holds.
- **`task_1_plan.md` granularity.** Task 1 sits at the 20-point cap. Its five top-level Work bullets carry 15 nested bullets covering about 25 file creations, deletions and edits. The story index argues why the move cannot be split without two tasks editing the same files, and this review accepts that argument. Even so, this is the task most likely to overrun one unit. Consider whether the work can be split along a line that keeps each file with one owner.

## Nice to Have
- **Story index → `## Context`** carries a Markdown table (Layer | Path | Holds | May import), where the sample keeps Context to prose. Task 3 restates the same table in the README, so the Context copy could become one prose sentence that points at Task 3.

## Incidental findings (not gating)
- `devscene.config.json` → `treeGuards` already holds `{ "test": "test/no-container-home-paths.test.mjs", "covers": "**/*.md" }`, a `cli`-relative test path. Task 3, a `graphscene`-layer unit, edits `graphscene/README.md`, so that guard is selected for it. Point 7 runs the guard through the dispatched layer's single-file command, `bash scripts/python-service.sh --package graphscene test …`, which cannot run a `.mjs` file. This is a pre-existing configuration issue, not one this plan introduces. It is a lead for the end-of-branch reviewers.
