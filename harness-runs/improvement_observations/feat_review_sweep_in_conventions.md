# Script-driven planning — 2026-11-17T21:38:37Z

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #2 architecture_review (architecture-reviewer), round 0: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #3 plan_review (task-plan-reviewer), round 0: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #4 plan_writer (task-plan-writer), round 1: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #5 architecture_review (architecture-reviewer), round 1: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #6 plan_review (task-plan-reviewer), round 1: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #9 plan_review (task-plan-reviewer), round 2: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## Script-driven planning node sessions (pd_drive returned 0)
- **category:** flow-efficiency
- **evidence:** seq node agent attempt result duration cost: #1 plan_writer task-plan-writer 1/3 returned 749s 5.791538800000001; #2 architecture_review architecture-reviewer 1/3 FAIL 123s 1.6118280000000003; #3 plan_review task-plan-reviewer 1/3 FAIL 348s 4.2408564; #4 plan_writer task-plan-writer 1/3 returned 171s 1.2452678; #5 architecture_review architecture-reviewer 1/3 PASS 119s 1.5287655999999998; #6 plan_review task-plan-reviewer 1/3 FAIL 410s 4.293970999999999; #7 plan_writer task-plan-writer 1/3 returned 173s 1.1838351999999999; #8 architecture_review architecture-reviewer 1/3 PASS 46s 0.8312376; #9 plan_review task-plan-reviewer 1/3 PASS 68s 0.7959850000000002
- **cost this run:** 9 node session(s)

# Task run (Phase D)

## A layer-implementer could not set a self-adopted script's executable bit
- **category:** tooling-gap
- **evidence:** Task 9's `layer-implementer` returned `outcome: blocker` because the session's permission mode (don't ask) refused `cp` and then `chmod 0755 scripts/review-sweep.sh`. It wrote the file with the file tool, byte-identical to `cli/templates/scripts/review-sweep.sh`. The orchestrator took a documented low-stakes assumption and committed it in 1c4dcc80 as `100644`, while the other agent-invocable copies under `scripts/` (e.g. `scripts/task-offer-check.sh`) are `100755`. The A2 `architecture-reviewer` return then raised the same mode mismatch as a Should Fix.
- **cost this run:** one unit closed with a known mode deviation; `scripts/review-sweep.sh` is tracked `100644`.

## Sub-agent shell probes refused in the unattended permission mode
- **category:** tooling-gap
- **evidence:** Each of these agents reported a refused Bash call in its return:
  - Task 2's `layer-implementer`: `bash -n` on the new script and its header's `REPRO` lines ("direct `bash` calls were refused in this session's permission mode"); it substituted the typecheck's shell-parse step and test cases.
  - The C2 `skeptic-reviewer`: "the session refused the shell probes I tried"; it dropped one `$'\001'` bash 3.2 concern as unverifiable.
  - The B.2 re-dispatched `branch-reviewer`: "My first attempt to apply the edits with a script was denied."
- **cost this run:** two planned verifications replaced by proxies, one skeptic concern dropped unverified.

## `diff_base: <default_branch>` names a ref the run copy does not carry
- **category:** agent-contract
- **evidence:** The core's A2/B/C2 dispatches and D.1 pass `dev` (`defaultBranch`) as a diff base or log range, and this run copy has no local `dev` (`git log … dev..HEAD` → `fatal: ambiguous argument 'dev..HEAD': unknown revision`). Six returns each state they fell back to `origin/dev` on their own:
  - the A2 `architecture-reviewer`;
  - the B.1 `branch-reviewer`;
  - the C2 `skeptic-reviewer`;
  - the D.1 `statistics-plan-writer`;
  - the Task 6 and Task 8 `layer-implementer`s.
  
  The improvement-observations module's own `## Dispositioned units` command failed here the same way, and was re-issued against `origin/dev`. The branch's own code-review Finding 1 was this same defect in the new `review-sweep.sh`.
- **cost this run:** every diff-based review relied on each agent independently choosing the same fallback.
- **hypothesis:** the run-copy cut point is `origin/<default_branch>` while the dispatch blocks name the local ref.

## Tree guards reported "none selected" for changes a guard's `covers` glob matches
- **category:** agent-contract
- **evidence:** `devscene.config.json` → `treeGuards` maps `test/main-repo-resolution-corpus.test.mjs` to `plugin/**/*.md`. Three `layer-implementer` returns nonetheless reported running no tree guard for `plugin/**/*.md` edits:
  - Task 5 (`plugin/agents/conventions-writer.md`): "no tree guard was selected";
  - Task 6 (`plugin/agents/conventions-reviewer.md`): "none selected";
  - Task 8 (`plugin/agents/branch-reviewer.md`, `plugin/instructions/main_repo_resolution.md`): "no tree guard was selected".
  
  The Task 7 and Code-review Finding 2 implementers, editing files under `plugin/` too, ran that guard and four others.
- **cost this run:** three units committed without their selected guard runs; the Phase G round-1 gates passed.

## Plan convergence took three review rounds
- **category:** optimization
- **evidence:** These are the plan unit's rounds 0–2 across the `harness-runs/task_plan_reviews/feat_review_sweep_in_conventions/` and `harness-runs/architecture_reviews/feat_review_sweep_in_conventions/` roots, counted from their finding titles.
  - **`task_plan_reviews`:**
    - round 0: FAIL, 8 findings (2 Must Fix);
    - round 1: FAIL, 11 findings (4 Must Fix), of which 5 were re-raised from round 0 (two marked "carried over from round 0", the skeleton-inlined-command finding promoted to Must Fix, and two Nice to Have) and 6 were net-new;
    - round 2: PASS, Nice to Have only.
  - **`architecture_reviews`:** round 0 FAIL (1 Must Fix), round 1 PASS, round 2 PASS.
- **cost this run:** two writer revisions and six gate dispatches beyond round 0.
