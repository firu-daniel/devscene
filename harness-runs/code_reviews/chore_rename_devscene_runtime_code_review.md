# Code Review: chore_rename_devscene_runtime

## Context

**Branch:** `chore_rename_devscene_runtime`
**Date:** 2026-11-23
**Reviewed:** the whole branch diff against `origin/dev`, 15 files. Task 1 moved the package `devscene-runtime/` to `devscene-flow-host/`: `README.md`, `pyproject.toml`, `src/devscene_flow_host/__init__.py`, `py.typed`, `tests/requirement_names.py`, `tests/test_boundary.py`, `tests/test_graphscene_dependency.py` and `uv.lock`. It also updated `scripts/python-service.sh` (`PACKAGES`, `package_row` and the header). Task 2 updated `cli/test/python-service.test.mjs` (`RUNTIME` and the expected `provisioned` line). Task 3 updated the two `devscene.config.json` → `treeGuards` `covers` values. Task 4 updated `scripts/run-gates.sh` (legs 13h–13j and the header), `docs/development.md` (**Gate 13** and `## 8. The nightly supply-chain audit`) and `ROADMAP.md` (the GraphScene row). The maintainer's commit `ee90652b` re-locked the package (only the root `[[package]]` entry of `uv.lock` changed) and made the two-line edit to `.github/workflows/supply-chain.yml`. Task 5 changed only run artifacts. 19 run-artifact files were left out of the reviewed diff.

**Headline conclusions.**

- **Leftover-name sweep.** I re-ran the story plan's derivation entry A over the branch tip: `git grep -n -i -E "devscene[-_ ]runtime|DevScene.s own Python runtime|DevScene.s meanings" -- . ':!harness-runs'`. The only hits outside `harness-runs/` are in `.claude/CLAUDE.md`, `.claude/context/conventions.md`, `.claude/context/devscene-runtime.md`, `.claude/review-sweep.md`, and `devscene.config.json` → `layers` / `detection.review.rationale`. These are exactly the scope register's `no-change` rows 1–4 and 15–19. A run cannot write `.claude/**`, and the layer profile changes only through `devscene config set`, so these sites belong to the maintainer's after-merge steps 4–5 and are not findings.
- **No wording that announces a rename.** No added line says the name changed or gives an earlier name (I grepped the added lines for `renam|formerly|previously|was called|old name|used to be`). The narrowed scope reads as standing fact in `devscene-flow-host/README.md` → `## What it is` and in the module docstring.
- **Python static checks.** No line in `devscene-flow-host/src` or `devscene-flow-host/tests` is longer than 100 columns (checked with `awk`). The GraphScene-surface regex from `.claude/review-sweep.md` finds nothing on the added lines under `devscene-flow-host/src`. I ran it by hand because the row's `Covers` still names `devscene-runtime`. `graphscene/tests/test_boundary.py` → `_FORBIDDEN_PREFIX = "devscene"` still covers `devscene_flow_host` without any edit. `.gitignore`'s generic `.venv/`, `.mypy_cache/`, `.pytest_cache/` and `.ruff_cache/` rules match under the new directory (`git check-ignore -v devscene-flow-host/.venv/x` → `.gitignore:8:.venv/`). The ignored `devscene-runtime/` remnant in the run copy is untracked.
- **Tests.** The `cli` suite's expectations moved together with the script table they check. Whether they pass is for the Run gates phase to establish; this review ran no suite. Gate 13h–13j can only grade `BLOCKED` in this run copy. The story plan's manual step 3 provisions and runs them on a maintainer checkout before merge.
- **Pass 0 sweep.** `bash /Users/daniel/Work/devscene/scripts/review-sweep.sh --repo /Users/daniel/Work/devscene-chore_rename_devscene_runtime` exited `0` with no hits, so no hit became a finding. Half (b), the new-exported-symbol caller check, had nothing to check. The diff adds no new exported symbol: the added assignments (`_PACKAGE_DIR`, `_STDLIB_AND_SELF`, `_RELOCK`, `PACKAGES`) are re-spellings of existing private constants.
- **Incidental lead.** `task_plan_reviews/chore_rename_devscene_runtime/review_2.md` raised one lead: the maintainer's workflow commit does not trip the protected-surface check, and Task 5's push check cannot see whether the main checkout was fetched. I checked it against the diff. Task 5 changed only run artifacts, and the workflow change sits in the maintainer's commit `ee90652b` alone, so nothing here becomes a finding.
- **Parity.** `phases.parity` is `false`, so no parity check was made.
- **Pass 2.** `harness-runs/task_plan_point_reviews/chore_rename_devscene_runtime_task_plan/` does not exist, so there were no per-unit findings to reconcile.

---

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the per-item fix loop.** The orchestrator walks the `[ ]` entries below from top to bottom, and only the committing role flips a marker. This review found no fixable finding, so the list has no entries.

---

## Must Fix

None.

---

## Should Fix

None.

---

## Nice to Have

None.

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so this section has no reference-implementation call-outs.
