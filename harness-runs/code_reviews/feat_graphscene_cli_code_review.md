# Code Review: feat_graphscene_cli

## Context

**Branch:** `feat_graphscene_cli`
**Date:** 2026-11-23
**Reviewed:** the whole branch diff against `origin/dev`, 10 files. In the `graphscene` layer:

- the step document and the round-resume document added to `adapters/walk_json.py` (Task 1);
- the check document's encoder, `adapters/check_json.py` (Task 2);
- the command line, `facade/cli.py`, with its `[project.scripts]` declaration in `graphscene/pyproject.toml` (Task 3);
- `graphscene/README.md` → `## The command line` and its rows (Task 4).

In the `general` layer, the `ROADMAP.md` GraphScene row and the gate 13 paragraph of `docs/development.md` (Task 5). The three suites that ship with the code were reviewed too: `tests/adapters/test_check_json.py`, `tests/adapters/test_walk_json.py` and `tests/facade/test_cli.py`. 17 run-artifact files excluded from the reviewed diff.

**Conclusions:**

- **Layering and boundary:** `facade/cli.py` imports only `adapters`, `engine`, `model` and the standard library, and is the only module that writes output. Neither new adapter imports `engine`. Nothing names a `devscene` module or `devscene.config.json`. No public name was added: `__all__` is untouched, and `walk_json.py`, `check_json.py` and `cli.py` are each marked *"not public"* in the README.
- **Wire forms:** the step encoder reuses `_action_out` rather than re-encoding an action, so the story's first top risk holds.
- **Required items:** every new module has its opening docstring with *"The rule:"*, its README row and its own suite under `tests/<layer>/`.
- **Tests:** the three branch suites ran green (96 passed). The command was `bash scripts/python-service.sh --package graphscene test tests/facade/test_cli.py tests/adapters/test_check_json.py tests/adapters/test_walk_json.py`. The full gate set is the Run gates phase's.
- **Pass 0 sweep:** `review-sweep.sh` exited `0` with no hits. The caller check found every new export called outside its defining file: `check_document`, `step_document` and `resume_from_json` from `facade/cli.py`, and `main` from the `graphscene/pyproject.toml` entry point.
- **Planning leads:** the planning rounds carry no `## Incidental findings (not gating)` section.
- **Per-unit carry-over:** `harness-runs/task_plan_point_reviews/feat_graphscene_cli_task_plan/` does not exist, so Pass 2 had nothing to reconcile.
- **Parity:** `phases.parity` is `false`, so there was no parity check.

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 3** — State `--help`'s exit `0` and non-JSON stdout in the command line's exit contract _(layer: graphscene)_
2. [ ] **Finding 1** — Fence the `provision` step in `## The command line` instead of giving it inline _(layer: graphscene)_
3. [ ] **Finding 2** — Cover `next`'s `--node` and `--detail` flags in the command line's suite _(layer: graphscene)_

---

## Must Fix

### 1. `## The command line` gives the `provision` step as an inline command instead of a fenced block
→ [finding_1.md](feat_graphscene_cli_code_review/finding_1.md)

---

## Should Fix

### 2. `next`'s `--node` and `--detail` flags are never exercised by the command line's suite
→ [finding_2.md](feat_graphscene_cli_code_review/finding_2.md)

### 3. The exit contract leaves out `--help`, which exits `0` with non-JSON text on stdout
→ [finding_3.md](feat_graphscene_cli_code_review/finding_3.md)

---

## Nice to Have

None.

---

## Out of scope / verified-OK (intentional divergences / call-outs)

None: `phases.parity` is `false`, so there is no reference implementation to diverge from.
