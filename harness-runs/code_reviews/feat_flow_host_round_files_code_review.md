# Code Review: feat_flow_host_round_files

## Context

**Branch:** `feat_flow_host_round_files`
**Date:** 2026-11-23
**Reviewed:** the whole branch diff against `origin/dev` (local `dev` absent in this checkout, so `.claude/review-sweep.md` was read from `origin/dev`). That is 21 files, +2644/−6. It covers:

- **Readers (`records`), Tasks 1–3.** `records/round_files.py`, `records/round_evidence.py`, `records/index_evidence.py`.
- **Host modules (`host`), Tasks 4–8.** `host/paths.py`, `host/reviewers.py`, `host/refusals.py`, `host/resume.py`, `host/round_gates.py`, `host/re_entry.py`.
- **Tests.** Their eight new suites and the support module `tests/round_fixtures.py`.
- **Docs, Tasks 9–10.** The package README (Task 9), and the `ROADMAP.md` and `docs/development.md` → **Gate 13** edits (Task 10).

22 run-artifact files were excluded from the reviewed diff (`git diff --shortstat` over the excluded pathspecs: 22 files changed, 853 insertions).

**Pass 0 sweep.** `review-sweep.sh` exited 0: no hits, 0 findings. The caller check covered all 38 new public module-level symbols. Each is referenced outside its defining file, in `host` modules, in the new suites and in `devscene-flow-host/README.md`. The top-level entry points `record_outcome`, `start_walk` and `current_step`, and the readers `read_index_evidence` and `fail_count`, are reached only by tests today. That is by design: the story index keeps `commands/` empty, and the task prompt assigns the compatibility command that consumes them to #465.

**Parity.** Not run: `phases.parity` is `false`.

**Port fidelity (confirmed by reading).** Each reader was read against the bash function its docstring names in `cli/templates/scripts/lib/flow-walker-gates.sh`, and each host rule against `cli/templates/scripts/flow-walker.sh`:

- `fw_review_verdict`, `fw_round_file_check`, `fw_next_review_index`, `fw_fail_count`, `fw_round_evidence`, `fw_index_evidence`.
- `render_path` / `subst`, `round_of_gate`, `round_of_writer`, `render_block`'s `findingsFolder` branch.
- `refuse_round_file`, `record_in_set`, `close_round`'s clearing, `start_round` / `start_record` and the `STATE` resume rules.

They match, apart from two departures. Each carries a `TODO: @claude` deferred-work marker naming what reverts it, and each is pinned by a test as it stands: the held-gate escalation in `round_gates._redispatch`, and the non-round findings file in `record_outcome`'s non-gate branch. Both citations were opened and say what the story index claims.

GraphScene's `rounds.record_gate` was read to confirm that a partly recorded set keeps `pending` a `DispatchSet`, so `_redispatch`'s `assert isinstance(current, DispatchSet)` holds. Every `graphscene` name the host imports is in `graphscene.__all__`, and the host reaches nothing below the public surface.

**Conventions.** Each new source module opens with *"The rule:"* and *"Deliberately not covered"*. Each new test file opens with *"The rule this file exists to enforce"*. Fixtures are planted under `tmp_path`, and the format-4 graph is read read-only. Gate 13's prose lists all eight new suites.

**Tests.** This review ran no suite and no probe; whether the suites pass is the Run gates phase's to establish.

**Pass 2.** `per_task_findings_root` does not exist on disk, so there was nothing to reconcile. The planning rounds' one incidental entry (`task_plan_reviews/…/review_2.md`) points at round 1's text, which the diff does not carry, so it raised no lead.

The two findings below are wording-only.

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 2** — Say "each of these" instead of "either" in the host README's `## Errors` closing sentence _(layer: devscene-flow-host)_
2. [ ] **Finding 1** — Drop the duplicated README link and the stray "and" from the `ROADMAP.md` GraphScene row _(layer: general)_

---

## Must Fix

_None._

---

## Should Fix

_None._

---

## Nice to Have

### 1. The `ROADMAP.md` GraphScene row links the host's README twice in one clause, and its list of what the host does now reads "and loads … reads … and resumes"
→ [finding_1.md](feat_flow_host_round_files_code_review/finding_1.md)

### 2. The host README's `## Errors` paragraph now names four failures but still says "Which exit status either becomes"
→ [finding_2.md](feat_flow_host_round_files_code_review/finding_2.md)

---

## Out of scope / verified-OK (intentional divergences / call-outs)

_Empty: `phases.parity` is `false`, so there is no reference implementation to diverge from._
