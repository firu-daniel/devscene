## The run copy carries no local `dev` ref, so every `<default_branch>..HEAD` range fails
- **category:** tooling-gap
- **evidence:** At Phase D, the plain command `git log --format='%h %s%n%b' --name-only dev..HEAD` (the `## Dispositioned units` derivation, with `defaultBranch` = `dev` from `devscene.config.json`) exited 128 with `fatal: ambiguous argument 'dev..HEAD': unknown revision or path not in the working tree.` The same range succeeded against `origin/dev`. The Phase B `branch-reviewer` and Phase C2 `skeptic-reviewer` returns each reported the same fact ("this run copy only has `origin/dev`") and diffed against `origin/dev` instead.
- **cost this run:** the dispositioned-unit and index-only-commit derivations were run against `origin/dev` rather than the documented `dev`; two reviewers each spent effort discovering and working around the missing ref.

## The word-count command was refused to an implementer
- **category:** tooling-gap
- **evidence:** The Phase A `layer-implementer` return for Task 3 (`harness-runs/task_plans/fix_reviewers_should_fix_only_pass/task_3_plan.md`) states: "I counted the words by reading the two phrases, because the word-count command was refused in this session." The task's own verification asked whether each edited `## Revision mode` section got shorter.
- **cost this run:** a plan verification step (section word count) was performed by eye instead of by command.

## `cp` was refused to an implementer copying a template over its live copy
- **category:** tooling-gap
- **evidence:** The Phase A `layer-implementer` return for Task 6 (`harness-runs/task_plans/fix_reviewers_should_fix_only_pass/task_6_plan.md`) states: "The `cp` call was refused, so I wrote each file's text with the file-write tool". Byte-identity was then confirmed with `git diff --no-index --exit-code`.
- **cost this run:** two files that should have been byte copies were re-typed through the file-write tool, with a separate byte check needed to confirm them.

## Phase C implementers reported no tree guard selected for edits under `plugin/**/*.md`
- **category:** silent-failure
- **evidence:** The three Phase C `layer-implementer` returns (code-review Findings 3, 2 and 1, commits `347ad5bd`, `3996f165`, `c763e0be`) each reported "Tree guards: none selected" for edits to `plugin/instructions/plan_review_rounds.md`, `plugin/agents/task-plan-writer.md`, `plugin/agents/user-review-fix-plan-writer.md`, `plugin/agents/test-fix-plan-writer.md` and `plugin/agents/ui-tests-plan-writer.md`. `devscene.config.json` `treeGuards` maps `plugin/**/*.md` to `test/main-repo-resolution-corpus.test.mjs` and `test/untrusted-input-corpus.test.mjs`, and `**/*.md` to `test/no-container-home-paths.test.mjs`; the Phase A implementers editing the same kind of files (Tasks 2–5) did select and run all three.
- **cost this run:** three per-unit commits landed without the tree-guard run `unit_loop_core.md` → `## The test-run rule` point 7 requires; the Phase G round-1 gate run (`pass`) was the only check of those edits.
- **hypothesis:** (guess) the implementers may have read "prose only" as exempting the edit from guard selection.

## The `branch-reviewer`'s Pass 0 grep sweep list is an empty stub
- **category:** tooling-gap
- **evidence:** The Phase B `branch-reviewer` return states: "The grep half of Pass 0 did nothing: its sweep list is still an empty stub, a configuration gap to close."
- **cost this run:** the Pass 0 grep sweep contributed nothing to the end-of-branch review.
