# Code Review: feat_flow_graph_schema_v2

## Context

**Branch:** `feat_flow_graph_schema_v2`
**Date:** 2026-11-20
**Reviewed:** the whole branch diff against `origin/dev` (`defaultBranch` `dev`, which this run copy has no local branch for). It contains:

- the format-4 planning graph source `cli/templates/scripts/flows/task_plan_writing.v4.graph.json` and the `cli/templates/scripts/README.md` sentence about it (Task 1);
- the generic format-4 schema shipped as `graphscene` package data, with its generic and schema-negative fixtures and `graphscene/tests/test_flow_graph_schema.py` (Task 2);
- `graphscene.vocabulary.vocabulary_violations`, with its `__all__` entry, vocabulary-negative fixtures and `graphscene/tests/test_vocabulary.py` (Task 3);
- `scripts/generate-flow-graph-v3.mjs` (Task 4);
- the `validate:graphscene-schema*` npm scripts and gate legs `3g`–`3i` in `scripts/run-gates.sh` (Task 5);
- the documentation in `docs/development.md`, `docs/flow-graph-walker.md`, `schemas/README.md`, `graphscene/README.md` and `ROADMAP.md` (Task 6).

18 run-artifact files excluded from the reviewed diff.

**Headline conclusions:**

- **Tests.** The new `graphscene` module lands with its opening docstring, its `__all__` entry and a test suite. That suite has a planted case per clause, a clean fixture and a check of each negative fixture. Every format-4 fixture is wired by name into `validate:graphscene-schema` or `validate:graphscene-schema:negative`, and both scripts are gate legs. This review ran no suite. Whether the suites pass, and whether gate 3i's generated output is still byte-identical to both committed format-3 copies, is for the Run gates phase to establish.
- **Pass 0 sweep.** `review-sweep.sh` exited `0` with no hits, so no candidate became a finding.
- **Caller check.** The one new exported symbol, `vocabulary_violations`, has callers outside its defining file: `graphscene/src/graphscene/__init__.py` and `graphscene/tests/test_vocabulary.py`. The generator exports nothing.
- **Boundary.** The schema and the module stay inside `.claude/context/graphscene.md` → `## What it may depend on`. The module imports only `collections.abc`, and no `devscene` literal appears.
- **cli layer.** `cli/templates/scripts/flows/task_plan_writing.v4.graph.json` has no row in `cli/src/generators/outerLoopScripts.ts` → `OUTER_LOOP_SCRIPTS` (its only `flows` row is `task_plan_writing.graph.json`), so `init` never writes it into an adopter's `scriptsDir` (`.claude/context/cli.md` → `## How a module in this layer is written` → **One string, one producer.**). Under `.claude/context/cli.md` → `## What this layer owns, and what it is not`, it reaches the published tarball only through `cli/package.json` → `files` (`"templates"`), which the story index accepts. The `cli/templates/scripts/README.md` sentence ("`flows/task_plan_writing.v4.graph.json` beside that graph is **not** written into `scriptsDir` … `cli/src/generators/outerLoopScripts.ts` carries no row for it") matches the table. No finding.
- **Negative fixtures.** The format-4 schema negatives live under `graphscene/tests/fixtures/flow_graph/`, not `schemas/negative/`. That is the placement the story index decided. It is already recorded as a `stale-rule` against `.claude/context/conventions.md` → `## What accompanies a new unit of each kind`, so it is not a finding here.
- **Incidental leads.** The planning rounds' lead about *"The last four lines cover the flow graph"* was resolved: it now reads "third to sixth". The lead about the wider derivation (`docs/cli.md`, `cli/README.md`, the planning core) found no stale site.
- **Parity.** `phases.parity` is `false`, so nothing was checked for parity.
- **Pass 2.** The per-unit findings root `harness-runs/task_plan_point_reviews/feat_flow_graph_schema_v2_task_plan/` does not exist, so Pass 2 had nothing to reconcile.

The findings below are what is left. The two Must Fix items: the generator does not refuse an edge reason that its stop binding does not declare, so the harness's format-4 source can use an undeclared name while every gate passes; and `docs/flow-graph-walker.md` still directs a cap change at the generated format-3 file, an edit gate 3i's own remedy reverts.

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 4** — Name the format-4 package-data schema, not the root format-3 path, in `vocabulary.py`'s docstring _(layer: graphscene)_
2. [x] **Finding 1** — Make the v3 generator refuse an `<escalate>` edge or `onCap` reason that the vocabulary does not declare _(layer: general)_
3. [x] **Finding 2** — Say which check covers the harness's format-4 graph in `docs/development.md` and `docs/flow-graph-walker.md` _(layer: general)_
4. [ ] **Finding 3** — Point the cap-change sentence in `docs/flow-graph-walker.md` at the format-4 source and the regenerate step _(layer: general)_

---

## Must Fix

### 1. The v3 generator accepts an `<escalate>` edge reason that the format-4 vocabulary does not declare
→ [finding_1.md](feat_flow_graph_schema_v2_code_review/finding_1.md)

### 3. `docs/flow-graph-walker.md` still calls a cap change an edit to "the graph", which is now a generated file
→ [finding_3.md](feat_flow_graph_schema_v2_code_review/finding_3.md)

---

## Should Fix

### 2. Two documents say `graphscene.vocabulary` checks the harness's format-4 graph, but it runs only on generic fixtures
→ [finding_2.md](feat_flow_graph_schema_v2_code_review/finding_2.md)

---

## Nice to Have

### 4. `vocabulary.py`'s docstring names the schema by a path that is also the repository's format-3 schema
→ [finding_4.md](feat_flow_graph_schema_v2_code_review/finding_4.md)

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from and this section is empty.
