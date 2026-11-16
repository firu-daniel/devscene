## The plan needed 3 review rounds to converge
- **category:** optimization
- **evidence:** the plan unit's round files under `harness-runs/task_plan_reviews/feat_structured_planning_agent_outputs/` and `harness-runs/architecture_reviews/feat_structured_planning_agent_outputs/` carry rounds 0, 1 and 2 (business-parity gate skipped, `phases.parity` false). Round 0: `task-plan-reviewer` FAIL with 2 Must Fix, `architecture-reviewer` PASS. Round 1: both FAIL, 3 Must Fix, all 3 net-new by title against round 0 (0 re-raised); the round-1 task-plan review also carries Should Fix items under "Carried from round 0 and still open". Round 2: both PASS.
- **cost this run:** 2 extra writer revisions and 4 extra gate dispatches (9 planning dispatches in total).

## Plan writer reported corpus staleness against the plugin conventions document
- **category:** tooling-gap
- **evidence:** the `task-plan-writer` return (initial write and revision 2) carried a `## Corpus staleness` section with one `stale-rule` entry: `.claude/context/plugin.md` → `## Wires: dispatch in, return out`, the bullet "A return is a fenced block of `key: value` lines, and the discriminator is the literal rather than the prose…", which this branch makes untrue for the six planning agents that now end in a fenced `json` return object checked against a `## Return schema` section.
- **cost this run:** the conventions document owes a follow-up restatement — a supervised `/devscene:analyze plugin` re-run or a hand edit.

## Implementers could not delete their own scratch probe files
- **category:** tooling-gap
- **evidence:** three `layer-implementer` returns reported a refused `rm` of a probe file they had written: Task 2 (`harness-runs/scratch/tpw_schema_check.py`), Task 10 (`harness-runs/scratch/pnl_real_plugin_probe.mjs`) and Task 14 (`harness-runs/scratch/task14_jq_probe.mjs`). Each file is left in the run copy (git-ignored under `harness-runs/scratch/*`).
- **cost this run:** three stray scratch files left in the run copy; no commit affected.

## Branch reviewer's Pass 0 grep half did not run
- **category:** silent-failure
- **evidence:** the Phase B `branch-reviewer` return stated: "the grep half didn't run, because its regex list is still an empty stub. The new-export caller check found no dead symbols."
- **cost this run:** the Pass 0 grep sweep contributed nothing to the end-of-branch review.

## The run copy carries no local ref for the default branch
- **category:** tooling-gap
- **evidence:** `git log --format='%h %s%n%b' --name-only dev..HEAD` (the Phase-D dispositioned-units derivation) exited 128 with "fatal: ambiguous argument 'dev..HEAD': unknown revision or path not in the working tree."; the derivation was re-run against `origin/dev..HEAD`. The `branch-reviewer` and `statistics-plan-writer` returns each reported the same missing local `dev` and the same `origin/dev` substitution.
- **cost this run:** three consumers fell back to the remote-tracking ref; none failed.

## Implementers piped or skipped tree-guard runs the test-run rule requires in the foreground
- **category:** agent-contract
- **evidence:** `layer-implementer` returns for Task 1, Task 3, Task 10 and code-review Finding 4 each said they piped a test or tree-guard run through `grep` against the conventions' foreground rule (Task 1 and one Finding-1 run re-ran it plainly). Task 9's return said "no tree guard was selected" although its five modified files are all under `plugin/instructions/`, which the `plugin/**/*.md` guards in `devscene.config.json` → `treeGuards` cover. Skeptic Finding 1's return said "I did not run the point-7 tree guard check".
- **cost this run:** tree-guard evidence for those units is weaker than the rule requires; the round-1 Run gates passed, so no defect resulted.

# User-review fix round 1 — move planning return schemas to plugin/schemas and thin the return-contract module

## Finding 1's general layer was dispositioned: `.claude/` table rows could not be written
- **category:** tooling-gap
- **evidence:** commit `c281609a` carries the body line `record disposition of Finding 1 — tool-layer guard refused the Edit writes to .claude/context/plugin.md and .claude/CLAUDE.md for the two asset-table rows; the rest of the general layer landed` (the cause recorded on the commit). Detail file: `harness-runs/user_reviews/feat_structured_planning_agent_outputs_fix_plan/finding_1.md` → `## Disposition`. The implementer's return quoted the refusal as "Permission to use Edit has been denied because Claude Code is running in don't ask mode".
- **cost this run:** the two `.claude/` asset-table rows were closed without a fix and must be added by hand.

## Run gates round 1 log carried 12 timeout failures the planner classed as not fixable on the branch
- **category:** flow-efficiency
- **evidence:** the `test-fix-plan-writer` return for `harness-runs/test_run_logs/feat_structured_planning_agent_outputs/review_1_round_1.log` reported 16 failed and 1 cancelled tests; 5 were fixable (`cli/test/watcher-planning-driver.test.mjs` fixture missing `schemas/`), 12 were timeouts (planning-driver-control, planning-driver-walk, watcher-keep-awake, watcher-placeholder-host) listed under `## Not fixable on this branch` in `harness-runs/test_fix_plans/feat_structured_planning_agent_outputs_review_1_round_1.md`, with a suite wall time of 4194 s against 2454 s on the branch's earlier green run. Round 2 passed with no change to those 12 tests.
- **cost this run:** one gate round (about 70 min of suite time) whose log mixed 12 environmental failures with 5 real ones.
- **hypothesis:** host load during round 1, not the branch.

## Cross-layer findings left the edited suite red between layer dispatches
- **category:** flow-efficiency
- **evidence:** both fix-plan findings were tagged `_(layer: cli, plugin, general)_`. On Finding 1 the `cli` implementer reported `cli/test/agent-return-schemas.test.mjs` at 20/26 (6 failing on files the `plugin` layer had not yet written); on Finding 2 the `cli` and `plugin` implementers each reported that suite failing at module load ("docs/structured-agent-returns.md has no ### The return block") until the `general` layer landed. Each recorded the failures as an evidence downgrade.
- **cost this run:** four layer dispatches across the two findings were reviewed against a suite that could not yet pass.

## The run copy still carries no local ref for the default branch
- **category:** tooling-gap
- **evidence:** this round's Phase-D derivation `git log --format='%h %s%n%b' --name-only dev..HEAD` again exited 128 ("fatal: ambiguous argument 'dev..HEAD': unknown revision or path not in the working tree."); it was re-run against `origin/dev..HEAD`.
- **cost this run:** one fallback; no failure.

## Test-fix-plan writer could not read HOME for its machine-path check
- **category:** tooling-gap
- **evidence:** the `test-fix-plan-writer` return for round 1 stated "I couldn't run `printenv HOME` (it was denied)" and that it checked for machine paths using a shared path prefix instead.
- **cost this run:** that agent's machine-path check ran on a substitute needle.
