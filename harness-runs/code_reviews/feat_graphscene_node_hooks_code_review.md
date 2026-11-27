# Code Review: feat_graphscene_node_hooks

## Context

**Branch:** `feat_graphscene_node_hooks`
**Date:** 2026-11-26
**Reviewed:** the whole branch diff against `origin/dev`, 80 files, segment by segment.

- **`cli`:** the format-5 planning graph's `promptSource`, `vocabulary.hooks`, `plan_round.after` and `convergence.before` declarations, with the `PNL_CORE_BLOCKS` alignment case in `cli/test/planning-node-lib.test.mjs` (Task 1).
- **`graphscene`:** format 5 across the schema, model and builder; the undeclared-hook vocabulary clause; `model/hooks.py` with `HookHost` and the five `HookCall` variants; `execute_set`'s per-attempt `before_dispatch`; `run_loop`'s node, round and terminal hooks; and the public surface and README (Tasks 2–7).
- **`devscene-flow-host`:** `records/prompt_blocks.py`, `records/clarifications.py`, `read_planning_marks`, `CorePromptBuilder`, `host/commit_points.py`, `PlanningHooks`, `decide_planning_entry`, core-agreement check 10 and the README (Tasks 8–16).
- **`general`:** the decision record, Gate 3, the schemas README, the roadmap and `package.json` (Task 17).

29 run-artifact files were excluded from the reviewed diff.

**Headline.** The hook seam and the host ports are sound.

- **Hook firing points.** I checked `run_loop._drive` / `_take` / `_refuse_unprovided` and `set_execution._run` against their own docstrings and against `graphscene/README.md` → `## What it is`. A `Refused` is never taken. The provider check runs before any walker call. Before-dispatch hooks sit inside the attempt's task and outside the `run_timeout_seconds` deadline. Round after-hooks re-fire on `current`.
- **`PlanningHooks` against bash.** I read it beside `pd_act` / `pd_handoff` in `cli/templates/scripts/lib/planning-driver-lib.sh` and the wrapper call spelling in `plugin/instructions/task_plan_writing_instructions_autonomous.md`. It commits the round before the ledger flips. It uses the same artifact kinds: `plan-round`, `ledger-flip`, `ui-test-plan` and `task-plan`, all present in `unit-commit-lib.sh` → `ucl_artifact`. The round number is taken from `RoundPassage.number`, as `render.py` prints `round:`. Exit `3` is treated as nothing to commit. `commit-on-branch.sh` writes its front-end `error:` line on stdout, which is the stream `_last_error` reads.
- **`decide_planning_entry` against bash.** It follows `pd_entry` / `pd_walk_usable` / `pd_block_usable` in their order. Only `<ask>` is an `interrupt` binding in the graph, so the generic `Interrupt` arm matches bash's `<ask>`-only continuation.
- **`CorePromptBuilder` against bash.** It follows `pnl_prompt`'s token order and `", "` join.

**Accompanying items.**

- Every new module carries its docstring rule and its own suite. Every new test file opens with *"The rule this file exists to enforce"*.
- `valid_hooks.json` is listed in `_FIXTURE_NAMES` and in `validate:graphscene-schema`.
- Each new public name sits in both `__all__` lists, in order, with its `_EXPECTED` and `_DEFINED_IN` entries.
- No new test reads a tree of files, so no `treeGuards` entry is owed.
- This review ran no suite. Whether the tests pass is for the Run gates phase to establish.

**Pass 0.** The grep sweep (`review-sweep.sh`) exited `0` with no hits, so 0 hits became findings. The caller check found a caller outside its defining file for every new exported symbol across all layer paths. The host-side entry points (`CorePromptBuilder`, `PlanningHooks`, `decide_planning_entry`) are called only by their suites, which the task prompt and the story index state as this branch's intended callers until the run-mode cutover (#424).

**Pass 2.** The per-unit findings root `harness-runs/task_plan_point_reviews/feat_graphscene_node_hooks_task_plan/` does not exist. Per-unit review was off, so there was nothing to reconcile.

**Parity.** `phases.parity` is `false`, so no parity check runs.

**Outside this review.** The conventions documents `.claude/context/conventions.md` and `.claude/context/graphscene.md` still say "format 4". The scope register records these as `stale-rule` items for a supervised `/devscene:analyze` re-run, and they are not plannable targets.

The three findings below are what is left. All three are stale or garbled prose.

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 3** — Restore the space after "format 5:" in the flow-graph schema's top-level description _(layer: graphscene)_
2. [x] **Finding 2** — Say format 5 in the shipped `flow-walker.sh` header and the `WALKER_GRAPH_PATH` doc comment _(layer: cli)_
3. [x] **Finding 1** — Print "format-5" in gate legs `3g` and `3h` of `scripts/run-gates.sh` _(layer: general)_

---

## Must Fix

_None._

---

## Should Fix

### 1. Gate legs `3g` and `3h` still print "format-4", while `docs/development.md` now says the legs as printed cover format 5
→ [finding_1.md](feat_graphscene_node_hooks_code_review/finding_1.md)

### 2. The shipped `flow-walker.sh` header and the walker test helper still describe the planning graph as format 4
→ [finding_2.md](feat_graphscene_node_hooks_code_review/finding_2.md)

---

## Nice to Have

### 3. The schema's top-level `description` lost the space after "format 5:"
→ [finding_3.md](feat_graphscene_node_hooks_code_review/finding_3.md)

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from and this section is empty.
