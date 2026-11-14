### Task 6 — Bring this repository's live run-artifact README copies byte-identical to Task 1's templates

**Goal:** This repository has adopted its own harness, so `harness-runs/` holds `init`'s output in this checkout (`.claude/context/conventions.md` → `## Documents of record`). `init` writes these READMEs `create-if-absent`, so Task 1's template edits never reach the live copies by themselves (`cli/src/generators/stateDir.ts`). This task copies the final template text over the two live copies that exist, as #365 did for the same pair of trees.

**Depends on:** Task 1, which leaves the final text in `cli/templates/state-dir/test_fix_plan_reviews/README.md` and `cli/templates/state-dir/plan_revisions/README.md`. This task changes no wording of its own. Each live file must end up byte-identical to its template, so any wording question is Task 1's.

**What this task does not do.** There is no `harness-runs/ui_test_plan_reviews/` directory, because `phases.qa` is `false` in `devscene.config.json`, so this task creates no live copy of Task 1's third template. Running `devscene init` or `init --force` to re-render is also out: it would touch generated files beyond these two, and the copy is the whole change.

This is the catch-all task. It reads every configured layer's conventions document, because the files sit at the repository root rather than under a layer path.

### Targets

- `harness-runs/test_fix_plan_reviews/README.md`
- `harness-runs/plan_revisions/README.md`

**Work:**

- [ ] `harness-runs/test_fix_plan_reviews/README.md`: replace its content with the exact bytes of `cli/templates/state-dir/test_fix_plan_reviews/README.md`, trailing newline included.
- [ ] `harness-runs/plan_revisions/README.md`: replace its content with the exact bytes of `cli/templates/state-dir/plan_revisions/README.md`, trailing newline included.

**Verification:**

- `git diff --no-index --exit-code cli/templates/state-dir/test_fix_plan_reviews/README.md harness-runs/test_fix_plan_reviews/README.md` exits 0.
- `git diff --no-index --exit-code cli/templates/state-dir/plan_revisions/README.md harness-runs/plan_revisions/README.md` exits 0.
- `git grep -nE "per failed plan review|one per failed review|per finding of the round" -- 'harness-runs/*/README.md'` prints no line.
