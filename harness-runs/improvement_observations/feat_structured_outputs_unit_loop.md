# Script-driven planning — 2026-11-17T12:55:24Z

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #1 plan_writer (task-plan-writer), round 0: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #3 plan_review (task-plan-reviewer), round 0: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #6 plan_review (task-plan-reviewer), round 1: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## Script-driven planning node sessions (pd_drive returned 0)
- **category:** flow-efficiency
- **evidence:** seq node agent attempt result duration cost: #1 plan_writer task-plan-writer 1/3 returned 717s 6.4490132000000004; #2 architecture_review architecture-reviewer 1/3 PASS 94s 1.4557514000000003; #3 plan_review task-plan-reviewer 1/3 FAIL 290s 3.970212000000001; #4 plan_writer task-plan-writer 1/3 returned 49s 0.5335597999999999; #5 architecture_review architecture-reviewer 1/3 PASS 81s 1.2640196; #6 plan_review task-plan-reviewer 1/3 PASS 263s 3.5408370000000002
- **cost this run:** 6 node session(s)

# Task run (Phase D)

## The diff base `dev` handed to three branch-level reviewers does not exist as a local ref in the run copy
- **category:** agent-contract
- **evidence:** the A2 `architecture-reviewer`, B.1 `branch-reviewer` and C2.1 `skeptic-reviewer` returns each state the run copy has no local `dev` branch and that they diffed against `origin/dev` instead; the A2 dispatch block carried `diff_base: dev` (from `defaultBranch`). The Phase D `git log … dev..HEAD` derivation was likewise run against `origin/dev`.
- **cost this run:** 3 reviewer dispatches each resolved the base on their own; no review was lost
- **hypothesis:** the run copy is cut from `origin/dev` and never creates the local ref

## Two implementer dispatches piped a tree-guard run, against the foreground/unpiped rule
- **category:** agent-contract
- **evidence:** Phase A Task 3 `layer-implementer` return: its first `main-repo-resolution-corpus` guard run was piped and re-run unpiped; Phase C Finding 3 `layer-implementer` return: all five guard runs piped through `grep` to read counts (`unit_loop_core.md` → `## The test-run rule` point 6)
- **cost this run:** 1 re-run guard; 5 guard results recorded from a non-conforming form (all passed)

## Corpus staleness — `.claude/context/plugin.md` describes returns as `key: value` blocks
- **category:** tooling-gap
- **evidence:** `harness-runs/story_plans/feat_structured_outputs_unit_loop_story_plan.md` → `## Scope register` (row 15) records a `stale-rule` against `.claude/context/plugin.md` → `## Wires: dispatch in, return out`, which this branch falsifies for `layer-reviewer.md` / `layer-implementer.md`; the A2 `architecture-reviewer` and B.1 `branch-reviewer` returns both note it is not yet recorded. This session did not see the `task-plan-writer.corpus_staleness` return (planning ran script-driven in an earlier session).
- **cost this run:** a follow-up restatement of that rule is owed

## Optimization — reviewer overlap on the branch unit
- **category:** optimization
- **evidence:** the A2 `architecture-reviewer` return (Should Fix, no file written on PASS) and B.1 `branch-reviewer` Finding 1 (`harness-runs/code_reviews/feat_structured_outputs_unit_loop_code_review.md`) raised the same finding: `layer-implementer` cannot return `flags` on `prohibited` / `already passing`
- **cost this run:** the finding was carried by the second reviewer only because the first one's PASS writes no file

# User-review fix round 1 — optional-field rule stated once; `already passing` outcome renamed `already_passing`

## A Phase A implementer reported "No tree guard was selected" for a change its tree guards cover
- **category:** agent-contract
- **evidence:** Phase A Item 1 (`Finding 1`) `layer-implementer` return, item 5: "No tree guard was selected." Its commit `ec41bf57` changed files under `plugin/instructions/`, `plugin/agents/` and `plugin/schemas/`, which match the `devscene.config.json` `treeGuards` globs `plugin/**/*.md`, `**/*.md` and `plugin/schemas/**`. The Item 2 implementer, whose change matched the same `.md` globs, selected and ran five guards. The Item 1 `layer-reviewer` returned PASS without mentioning the skipped guards.
- **cost this run:** Item 1's guards first ran at the Phase G whole-suite round (`review_1_round_1`, `pass`), not inside the unit

## A Phase A implementer piped its tree-guard run, against the foreground/unpiped rule
- **category:** agent-contract
- **evidence:** Phase A Item 2 (`Finding 2`) `layer-implementer` return, item 5: it ran the five selected guards in one `npm test --workspace cli -- …` call and "piped that run's output through `grep` to read the counts", which it reported as a departure from the plugin conventions (`unit_loop_core.md` → `## The test-run rule` point 6)
- **cost this run:** 5 guard results (76 tests, all passed) were recorded from a run in a form the rule does not allow

## The Phase-D disposition derivation's `git log <default_branch>..HEAD` fails in the run copy
- **category:** agent-contract
- **evidence:** `git log --format='%h %s%n%b' --name-only dev..HEAD`, the command `improvement_observations_instructions.md` → `## Dispositioned units` (b) gives, exited 128 with `fatal: ambiguous argument 'dev..HEAD': unknown revision or path not in the working tree.` It was re-issued against `origin/dev`. That section gives no remote-tracking fallback. The core's D.2 delivery bullet does give one.
- **cost this run:** 1 failed command; the derivation was re-run against a base the section does not name
