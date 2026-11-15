# Test Fix Plan: feat_script_driven_planning_pilot — task round 1

## Context

**Branch:** `feat_script_driven_planning_pilot`
**Test log:** `harness-runs/test_run_logs/feat_script_driven_planning_pilot/task_round_1.log` (machine-local, uncommitted; every line this plan relies on is quoted in the per-finding files or below)
**Summary:** The typecheck gate passed and the test gate failed on two gates: gate 6a, because three tracked plan-round artifacts name absolute paths under the running user's home directory, and gate 6f, because `typos` flags the awk array name `nd` in `cli/templates/scripts/lib/planning-record-lib.sh`. Gates 13a–13c were BLOCKED on an unprovisioned Python environment, which no change on the branch can fix. Gates 13d and 14d were SKIPPED; a skip is not a failure, so neither is listed below.

---

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the per-item fix loop.** The loop walks the `[ ]` entries below top to bottom, and only the committing role flips a marker to `[x]`. `[ ]` markers anywhere else, such as sub-step bullets inside the per-finding files, are informational only. Each entry resolves to one self-contained `finding_<K>.md` in `feat_script_driven_planning_pilot_task_round_1/`.

1. [ ] **Finding 1** — Replace the home-directory paths in three plan-round artifacts with machine-neutral forms. _(layer: general)_
2. [ ] **Finding 2** — Rename the awk arrays `nd` / `kd` in `PRL_REWRITE_AWK` so `typos` no longer flags them. _(layer: cli)_

---

## Must Fix

### 1. Three tracked plan-round artifacts name machine paths under the home directory
→ [finding_1.md](feat_script_driven_planning_pilot_task_round_1/finding_1.md)

### 2. `typos` flags the awk array name `nd` in the planning record library
→ [finding_2.md](feat_script_driven_planning_pilot_task_round_1/finding_2.md)

---

## Not fixable on this branch

- **Gates 13a Python lint, 13b Python typecheck and 13c Python tests (gate 13, BLOCKED).** Each one was reported as

  ```
  BLOCKED 13a Python lint — uv or the synced Python environment is missing; run bash scripts/python-service.sh sync (0 s)
        python-service: not provisioned: no synced environment at <home>/.cache/devscene-docs-retrieval/venvs/602766304; run bash scripts/python-service.sh sync
  ```

  (13b and 13c carry the same `not provisioned` line.) **Reason:** the cause is on the host, not in the tree. The docs-retrieval service's synced Python environment is missing from the machine's cache directory. The log's own `== gates this script cannot run` section lists gate 13 as running unattended "once bash scripts/python-service.sh sync has provisioned its environment". **Operator's remedy:** run `bash scripts/python-service.sh sync` on the gate host, then rerun the gates. `run-gates` counts these three as neither failed nor passed (`run-gates: 2 failed, 22 passed`).

---

## Source failures

The prompt named no earlier-round logs, so every failure is classed *first round (no earlier log to compare)*.

| Log line (rewritten per step 5) | Gate | Maps to | Class |
|---|---|---|---|
| `FAIL  6a no machine paths (printed output, which is the finding, 2 s)` | test (gate 6) | Finding 1 | first round |
| `FAIL  6f shipped files pass typos (exit 1, 0 s)` | test (gate 6) | Finding 2 | first round |
| `BLOCKED 13a Python lint — uv or the synced Python environment is missing; …` | test (gate 13) | Not fixable on this branch | first round |
| `BLOCKED 13b Python typecheck — uv or the synced Python environment is missing; …` | test (gate 13) | Not fixable on this branch | first round |
| `BLOCKED 13c Python tests — uv or the synced Python environment is missing; …` | test (gate 13) | Not fixable on this branch | first round |

The typecheck gate reported `PASS: typecheck` and `gate typecheck exited 0`, so it has no failures to list.
