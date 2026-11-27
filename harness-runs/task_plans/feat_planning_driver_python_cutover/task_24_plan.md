### Task 24 — Record the cutover in `docs/flow-graph-walker.md`

**Goal:** `docs/flow-graph-walker.md` is the decision record for script-driven planning (scope register row 13). Bring it up to date, as the task prompt's lead *"`docs/flow-graph-walker.md` brought up to date"* asks. The bash driver's decisions are marked superseded with the date and branch, and the Python driver's decisions are recorded in the document's own **Decision.** / **Reason.** / **Cost.** form.

**Depends on:** Tasks 2, 16, 17 and 18. They fix what is decided:
- **Task 2.** The watcher launches `devscene-planning-driver` through `hr_flow_host_exec`, passing the shared session vector after `--`.
- **Task 16.** The driver walks in run mode with `ClaudeExecutor`, `CorePromptBuilder`, `PlanningHooks` and `decide_planning_entry`, under `ExecutionLimits(max_concurrent_dispatches=5, max_attempts=3, backoff_seconds=60.0, dispatch_cap=MAX_TOTAL_DISPATCHES)`.
- **Task 15.** The round-file refusal becomes an `infra` failure.
- **Task 17.** The pause's partial commit and the parks are the driver's.

**Where this task stops.** This document only. The other `docs/` pages and `ARCHITECTURE.md` are **Task 25's**. The document's first-line statement of who reads it and what it owns stays as it is, unless it names the bash libraries.

### Targets

- `docs/flow-graph-walker.md`

**Work:**

- [ ] **`## 5. The two drivers`.** The script-driven driver is `devscene-flow-host`'s `devscene-flow-host/src/devscene_flow_host/commands/planning_driver.py`, run in GraphScene's run mode. Mark the decision that names `lib/planning-node-lib.sh`, `lib/planning-record-lib.sh` and `lib/planning-driver-lib.sh` as the driver **Superseded 2026-11-27 (`feat_planning_driver_python_cutover`)**, with a pointer to the new entry. Mark the bash-floor cost (*"polls the set once a second with `kill -0`"*) superseded the same way.
- [ ] **New decisions, each with its reason and cost:**
  - the driver walks in-process, and runs no `flow-walker.sh`;
  - the launch vector still has one producer, the watcher's shared array, passed after `--`;
  - at most 5 dispatches at once, as a flow-host constant, not a configuration key;
  - the walk stays in the file store, with no ledger-backed store. A pause, a stop or a crash leaves it in place, a remote job carries `.flow_walker_state` in its `harness-state` bundle, and `decide_planning_entry` rebuilds an unusable one;
  - the round-file refusal is an `infra` failure retried alone, held `error` on the third attempt;
  - `corpus_staleness` is still dropped, pending the follow-up per-run summary file, as the task prompt decides.
- [ ] **The other bash-driver sentences.** Every other decision or cost that names `pnl_init`, `pnl_reap`, `PNL_CORE_BLOCKS` or `PD_*` gets the same superseded marker. That includes the core-headings decision under *"At every drive, `pnl_init` reads …"*, now held by the graph's `promptSource` and `test_core_agreement.py` check 10, and the node-stream decision. Each marker names its replacement in one sentence.
- [ ] **The `Changed 2026-11-25 (#459)` and `Changed 2026-11-26 (feat_graphscene_node_hooks)` entries.** Where they say the bash driver reads the graph, add a dated `Changed 2026-11-27 (feat_planning_driver_python_cutover)` line saying no bash reader of the graph remains.
- [ ] Re-run scope register entries A and D. Neither lists `docs/flow-graph-walker.md` for a live sentence: every hit left is inside a superseded entry or names retired code as retired.

**Verification:**

- `git grep -nE 'planning-(driver|node|record)-lib|pnl_[a-z_]+|PNL_CORE_BLOCKS' -- docs/flow-graph-walker.md` prints only lines inside an entry marked **Superseded** or naming the code as retired.
- Every new decision cites a path and symbol that exists after Tasks 1–18, such as `host/run_control.py` → `MAX_CONCURRENT_DISPATCHES`, by symbol and never by line number.
