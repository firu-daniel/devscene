# Code Review: fix_python_gate_run_copies

## Context

**Branch:** `fix_python_gate_run_copies`
**Date:** 2026-11-19
**Reviewed:** the whole branch diff against `origin/dev` (this run copy has no local `dev`). It covers 10 files, +544/−63:
- `scripts/python-service.sh`: the package table, `--package`, the in-package `.venv` and tool caches, `--no-cache` on the legs, and `provision` with its `# PROVIDES: provision` marker (Task 1).
- `scripts/check-machine-paths.sh` and the root `.gitignore`: gate 6a's four new exclusions and `.venv/` ignored everywhere (Task 2).
- `devscene.config.json` → `commands.depInstall` with its guarded `provision` step, and `scripts/run-gates.sh`'s gate-13 remedy text (Task 3).
- The new `cli/test/python-service.test.mjs` (Task 4) and the extended excluded-places case in `cli/test/check-machine-paths.test.mjs` (Task 5).
- `docs/development.md`, `docs-retrieval-service/README.md` and `docs/retrieval-eval.md` (Task 6).

15 run-artifact files were excluded from the reviewed diff.

**Headline conclusions.**
- **Tests.** Every accompanying test the conventions require is present. The wrapper's package selection, write locations, `provision` exit contract and marker line are pinned against a recording `uv` stub in a throwaway fixture under `os.tmpdir()`. The new suite reads one fixed file (`scripts/python-service.sh`), so it is not a tree-reading test and owes no `treeGuards` entry.
- **Sweep and caller check.** The Pass 0 sweep (`scripts/review-sweep.sh`) exited 0 with 0 hits, so 0 findings came from it. The new-exported-symbol caller check found no new exported symbol under a layer path.
- **Run-copy route.** The bootstrap route was traced end to end:
  - `scripts/setup-worktree.sh` → `run_configured` `eval`s `depInstall` from the copy's root, unsandboxed.
  - The `grep -qx` guard reads the copy's own wrapper.
  - `scripts/launch-sandboxed-gates.sh` binds the target writable and sets `TMPDIR=/tmp` on a private tmpfs, so the in-package `.venv` and `uv`'s `--no-cache` temporary directory are both writable there.
  - `docs-retrieval-service/.dockerignore` already excludes `**/.venv/`, so the now in-tree environment cannot leak into the service image.
- **Planning leads.** The planning rounds left no `## Incidental findings (not gating)` entries.
- **Parity.** `phases.parity` is `false`, so no parity check ran.

The three findings below are prose and message accuracy only. None of them is a Must Fix.

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 3** — Re-wrap gate 13's leg comment in `scripts/run-gates.sh` _(layer: general)_
2. [ ] **Finding 2** — Make the per-package `cd` failure in `scripts/python-service.sh` name the missing directory instead of asking about git _(layer: general)_
3. [ ] **Finding 1** — Reword the five sites that say pytest writes an in-tree `.pytest_cache` so the exclusion reads as a backstop _(layer: general)_

---

## Must Fix

_None._

---

## Should Fix

### 1. Five durable sites say pytest writes an in-tree `.pytest_cache`, but `docs-retrieval-service` turns pytest's cache off
→ [finding_1.md](fix_python_gate_run_copies_code_review/finding_1.md)

---

## Nice to Have

### 2. A missing package directory is reported as "is git on PATH?", after git has already answered
→ [finding_2.md](fix_python_gate_run_copies_code_review/finding_2.md)

### 3. Gate 13's leg comment in `run-gates.sh` is left with a broken wrap after the inserted run-copy sentence
→ [finding_3.md](fix_python_gate_run_copies_code_review/finding_3.md)

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false` in `devscene.config.json`, so there is no reference implementation to diverge from and this section is empty.
