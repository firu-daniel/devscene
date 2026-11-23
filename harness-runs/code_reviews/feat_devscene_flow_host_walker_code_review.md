# Code Review: feat_devscene_flow_host_walker

## Context

**Branch:** `feat_devscene_flow_host_walker`
**Date:** 2026-11-23
**Reviewed:** the whole branch diff against `origin/dev`, in three segments:

- **The package.** `devscene-flow-host/src/devscene_flow_host/` has three new layers: `records` (`config.py`, `ledger.py`, `errors.py`), `host` (`predicates.py`, `store.py`, `walking.py`) and `commands` (its docstring only). The two `import-linter` contracts are in `devscene-flow-host/pyproject.toml`.
- **The suite.** `devscene-flow-host/tests/` has six new suites: `test_layers.py`, `test_config.py`, `test_ledger.py`, `test_predicates.py`, `test_store.py` and `test_walking.py`.
- **Documents and configuration.** `devscene-flow-host/README.md`; the two `treeGuards` entries in `devscene.config.json`; gate 13j in `docs/development.md`; the `GraphScene` row in `ROADMAP.md`.

14 run-artifact files excluded from the reviewed diff.

**Tests.** Every new module has its own suite. Each suite opens with *"The rule this file exists to enforce"* and plants its records under `tmp_path`. `tests/test_layers.py` reads the package tree, and it is registered as a tree guard over `devscene-flow-host/src/devscene_flow_host/**` and `devscene-flow-host/pyproject.toml`. `tests/test_walking.py` reads one fixed file, the harness graph, so it owes no entry. This review ran no suite. Whether the suites pass is for the Run gates phase to establish.

**Pass 0 sweep.** The main checkout's `scripts/review-sweep.sh`, run with `--repo` naming this checkout, exited `0`: 0 hits, so 0 findings. The new-exported-symbol caller check ran over every `layers[].path` scope. Every new public function and class has a call site outside its defining file, either in another module of the package or in its suite. The `commands` layer is a docstring by the story plan's decision, so `open_walker` and `refusal_reason` have only test callers until the command line lands.

**Parity.** `phases.parity` is `false`, so there was no parity cross-check and the call-out section is empty. The host does state that it mirrors the bash walker's readers. That mirror was checked against `hr_phase_enabled`, `hr_state_dir` / `hr_config_load`, `fw_run_mode_skipped`, `fw_id_in_list` and `eval_skip`:

- **The ledger reader and the predicate-name patterns match.** The `## Run mode` heading match, the `- skipped: ` prefix, trailing-whitespace stripping, the ledger winning over the given ids, `none` read as the empty set, and the two `V3_PREDICATES` patterns.
- **The configuration reader does not.** It refuses the inputs the bash readers treat as unset (Finding 1). It also answers for a configuration with no `defaultBranch`, which they treat as unresolvable (Finding 2). Both were measured with probes run through `bash scripts/python-service.sh --package devscene-flow-host probe …`.

**Pass 2.** `per_task_findings_root` (`harness-runs/task_plan_point_reviews/feat_devscene_flow_host_walker_task_plan/`) does not exist, so there was nothing to carry over. The planning rounds' review files carry no `## Incidental findings (not gating)` section.

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 1** — Read a JSON `null` phase, a non-object `phases` and a `null` `stateDir` as unset in `read_config`, as `hr_config_load` does _(layer: devscene-flow-host)_
2. [ ] **Finding 2** — Refuse a configuration with no `defaultBranch` in `read_config` with a `RecordError`, as `hr_config_load` does _(layer: devscene-flow-host)_

---

## Must Fix

### 1. `read_config` refuses a phase that the bash walker reads as off: a JSON `null` value, a non-object `phases`, and a `null` `stateDir`
→ [finding_1.md](feat_devscene_flow_host_walker_code_review/finding_1.md)

### 2. `read_config` accepts a configuration with no `defaultBranch`, which every bash reader it ports treats as unresolvable
→ [finding_2.md](feat_devscene_flow_host_walker_code_review/finding_2.md)

---

## Should Fix

None.

---

## Nice to Have

None.

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so this section is empty.
