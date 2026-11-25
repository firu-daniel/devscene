# Code Review: chore_retire_flow_graph_v3

## Context

**Branch:** `chore_retire_flow_graph_v3`
**Date:** 2026-11-25
**Reviewed:** the whole branch diff against `origin/dev`: 56 files, +626 / −4136. 21 run-artifact files were excluded from the reviewed diff. The diff was reviewed in these segments:
- `cli`: the format-4 graph renamed onto `flows/task_plan_writing.graph.json` and the format-3 template deleted, `OUTER_LOOP_SCRIPTS`, the `flow-walker.sh` header, `cli/test/helpers/walker.mjs` → `WALKER_GRAPH_PATH`, two suites and two READMEs.
- `plugin`: two planning commands and `AUTONOMOUS_FLOW.md`.
- `graphscene`: the `static_check.py` docstring and its suite's header.
- `devscene-flow-host`: `GRAPH_SUFFIX`, the `predicates.py` docstring, nine suites' `_GRAPH` paths, the README, and the new test checker `tests/core_agreement.py` with its suite `tests/test_core_agreement.py`.
- `general`: the deletion of the format-3 schema, both fixture families, the generator, `scripts/check-flow-graph.sh`, the `validate:flow-graph*` scripts and gate legs `3c`–`3f` and `3i` in `scripts/run-gates.sh`; and the doc updates in `docs/development.md`, `docs/flow-graph-walker.md`, `docs/watcher.md`, `schemas/README.md`, `schemas/negative/README.md` and `ROADMAP.md`.

**Headline conclusions:**
- **Pass 0 sweep.** `review-sweep.sh` exited `0`, so there were no hits and none became a finding. The new-exported-symbol caller check found every new public name of `devscene-flow-host/tests/core_agreement.py` called from `tests/test_core_agreement.py`. The branch adds no new TypeScript export.
- **Checks 4–7 port.** `core_agreement_violations` was read against the retired `scripts/check-flow-graph.sh` (`run_checks`, `load_owner_docs`, `between`, the `ANCHORS` here-doc) at `origin/dev`. All of these carry over check for check:
  - the owner-document reads;
  - every refuse-to-pass clause;
  - the `{state_dir}` / `{branch}` / `{round}` write-back;
  - the three cap anchors;
  - the flow-to-core table.
  
  The suite has one planted case per clause, one clean planted case and one case against the real tree, as `.claude/context/devscene-flow-host.md` → `## Tests — what "done" means here` requires. Gate 13's leg `13j` runs it (`scripts/run-gates.sh`). It sits under `tests/`, which `cli/src/flowHost/layout.ts` does not stage, so no shipped file names a `plugin/` path.
- **The rename.** On the branch tip, the renamed graph's node ids, kinds, agents, outcome keys in order, and round `gates` all equal the retired format-3 file's (compared with `jq` against `origin/dev`). So the planning driver's libraries and `cli/test/agent-return-schemas.test.mjs` read it unchanged, as the story claimed.
- **Leftover references.** Outside `harness-runs/`, a grep for `v4.graph.json`, `check-flow-graph`, `generate-flow-graph-v3`, `flow-graph-check`, `validate:flow-graph` and `flow-graph-schema-` leaves only these:
  - dated decision records in `docs/flow-graph-walker.md`, each followed by its new **Changed 2026-11-25 (#459)** paragraph;
  - the self-adopted copies under `scripts/`, which the story leaves to the post-merge re-render;
  - three passages of conventions documents (see `questions`).
- **Not executed.** This review ran no test. Every statement above about suites passing was established by reading, not by running. Run gates establishes it.
- **Parity.** `phases.parity` is `false`, so no parity cross-check applies.
- **Pass 2.** `harness-runs/task_plan_point_reviews/chore_retire_flow_graph_v3_task_plan/` does not exist, so there was nothing to carry over.

One finding remains.

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 1** — Say "the graph" rather than "the two graphs" in `docs/watcher.md`'s reachability paragraph _(layer: general)_

---

## Must Fix

_None._

---

## Should Fix

### 1. `docs/watcher.md` still says "the two graphs" after the shipped table went down to one graph row
→ [finding_1.md](chore_retire_flow_graph_v3_code_review/finding_1.md)

---

## Nice to Have

_None._

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from, and this section is empty.
