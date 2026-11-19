# Script-driven planning — 2026-11-19T08:38:04Z

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #1 plan_writer (task-plan-writer), round 0: 2 denial(s)
- **cost this run:** 2 refused tool call(s)

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
- **evidence:** #4 plan_writer (task-plan-writer), round 1: 2 denial(s)
- **cost this run:** 2 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #5 architecture_review (architecture-reviewer), round 1: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #6 plan_review (task-plan-reviewer), round 1: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## Script-driven planning node sessions (pd_drive returned 0)
- **category:** flow-efficiency
- **evidence:** seq node agent attempt result duration cost: #1 plan_writer task-plan-writer 1/3 returned 742s 5.354951; #2 architecture_review architecture-reviewer 1/3 PASS 70s 1.2712484000000002; #3 plan_review task-plan-reviewer 1/3 FAIL 336s 3.7115274; #4 plan_writer task-plan-writer 1/3 returned 185s 1.0410548; #5 architecture_review architecture-reviewer 1/3 PASS 87s 1.4666962000000001; #6 plan_review task-plan-reviewer 1/3 PASS 277s 2.8333224000000006
- **cost this run:** 6 node session(s)

# Task run (Phase D)

## A standalone `bash -n` parse of a changed shell script was refused for the layer implementer
- **category:** tooling-gap
- **evidence:** Task 1's `layer-implementer` return: "a separate `bash -n` on the wrapper was refused", parse rested on `bash scripts/typecheck.sh`'s shell-parse step instead; code-review Finding 2's `layer-implementer` return: a grep plus `bash -n` on `scripts/python-service.sh` "The permission mode refused that command"
- **cost this run:** two units fell back to the typecheck wrapper's whole-tree shell parse; one unit relied on the finding's statement instead of its own grep

## `rm` of a unit's own scratch directory under `harness-runs/scratch/` was refused, leaving it behind
- **category:** tooling-gap
- **evidence:** Task 3's `layer-implementer` flag: "harness-runs/scratch/depinstall-check/ was not removed: the permission profile refused rm"; Task 4's return: "My `rm -r` of its leftover work directory `harness-runs/scratch/task4-mutations/` was refused"
- **cost this run:** two gitignored scratch directories left in the run copy for manual removal

## Running a unit-written scratch script directly with `bash harness-runs/scratch/…` was refused
- **category:** tooling-gap
- **evidence:** Task 3's `layer-implementer` return: "the profile refused `bash harness-runs/scratch/depinstall-check/check.sh …`"; it re-ran the same script through `bash scripts/scratch-run.sh`
- **cost this run:** one refused call and a workaround route for Task 3's verification

## The `dev` diff base did not resolve in the run copy; four agents fell back to `origin/dev`
- **category:** agent-contract
- **evidence:** dispatch blocks passed `diff_base: dev` (Phase A2) and the statistics range is `dev..HEAD`; `architecture-reviewer` (A2): "`git diff dev...HEAD` failed with `fatal: bad revision`", diffed `origin/dev`; `branch-reviewer` (B.1), `skeptic-reviewer` (C2.1) and `statistics-plan-writer` (D.1) each reported the same fallback
- **cost this run:** none measured; every agent recovered on its own, with the base choice left to each agent
- **hypothesis:** a run copy cloned for the run carries only `origin/<default_branch>`, not a local branch of that name
