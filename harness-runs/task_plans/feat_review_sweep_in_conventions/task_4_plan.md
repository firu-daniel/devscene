### Task 4 — Add the `review-sweep` doctor check for a missing or unfilled sweep document

**Goal:** Make `devscene doctor` predict what the end-of-branch review will find. It warns when `.claude/review-sweep.md` is missing or still an untouched skeleton, so a sweep that never runs is visible at setup rather than in every review.

**Depends on:** Task 1, which exports `REVIEW_SWEEP_PATH` (`'.claude/review-sweep.md'`) from `cli/src/generators/claudeContext.ts` and writes the skeleton carrying both halves of the two-part test. Import both the path and `isUntouchedSkeletonText` from that module. Never re-spell either.

### Targets

- `cli/src/doctor/checks.ts` — the new check and its place in `CHECKS`.
- `cli/test/doctor.test.mjs` — the accompanying cases.

**Work:**

- [ ] `checks.ts`: add `REVIEW_SWEEP_CHECK`, id `review-sweep`, title "the review-sweep document the end-of-branch reviewer reads exists and has been filled in". Its doc comment states that it grades substring facts only and that every state warns and none fails, both for `SETUP_ANALYSIS_CHECK`'s reasons, cited rather than restated. The answers:
  - `unevaluated` when the repository root did not resolve;
  - `warn` when the file is absent: the reviewer's grep sweep reports a configuration gap and does not run; `npx devscene init` creates the skeleton and rewrites nothing else;
  - `warn` when `isUntouchedSkeletonText` is true: fill it with `/devscene:analyze sweep` or by hand, and commit it on the default branch, which is where the sweep reads its rows;
  - `pass` otherwise.

  Every message names the path through `REVIEW_SWEEP_PATH`, and `/devscene:analyze` through `ANALYZE_COMMAND`.
- [ ] Register it in `CHECKS` immediately after `SETUP_ANALYSIS_CHECK`'s neighbourhood (beside `task-offer-rules`). Extend the ordering doc comment above `CHECKS`, which explains why `setup-analysis` and `task-offer-rules` sit where they do, with one clause for `review-sweep`.
- [ ] `doctor.test.mjs`: three fixture cases — file absent → `warn` naming `npx devscene init`; untouched skeleton → `warn` naming `/devscene:analyze sweep`; a filled document → `pass`. Extend any assertion that lists every check id.

**Verification:**

- `npm test --workspace cli -- test/doctor.test.mjs` passes. It is this task's own edited test file.
- `bash scripts/typecheck.sh` exits zero.
- `git grep -n -F 'review-sweep.md' -- cli/src/doctor` prints nothing: the path reaches this module only through `REVIEW_SWEEP_PATH`.
