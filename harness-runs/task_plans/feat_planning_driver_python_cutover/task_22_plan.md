### Task 22 — Point the host's docstrings at the run driver and remove their issue numbers

**Goal:** Fix the host docstrings that defer a responsibility to *"the run driver's (#424)"* or to the planning driver *"not yet merged"*. They now name the module that owns it, which Tasks 12–17 added. Remove every remaining issue number from `devscene-flow-host/src` and `devscene-flow-host/tests`, as the task prompt decides. Each sentence keeps what it says, minus the number.

**Depends on:** Tasks 13, 15, 16 and 17, which own what these docstrings defer:
- **Task 16.** `host/planning_run.py` acts on the entry decision, builds the prompt builder over the pairs, and clears the revision findings on a round's close.
- **Task 15.** `host/planning_executor.py` keeps `RevisionFindingsStore` filled in run mode.
- **Task 17.** `host/run_exits.py` makes the pause's partial commit and the parks.
- **Task 13.** `host/node_sessions.py` pairs usage with `Launch` rows and writes each node's stream.

**Where this task stops.** Docstrings and comments only. No behaviour changes. The README is **Task 23's**.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/agent_prompts.py` — *"Keeping `RevisionFindingsStore` filled in run mode: the run driver's (#424)."*
- `devscene-flow-host/src/devscene_flow_host/host/planning_entry.py` — *"Acting on the decision … the run driver's (#424)."*
- `devscene-flow-host/src/devscene_flow_host/host/planning_hooks.py` — *"A pause's `plan-round-partial` commit and the `<ask>` / `<escalate>` parks: the run driver's (#424) …"*
- `devscene-flow-host/src/devscene_flow_host/host/claude_executor.py` — the two *"the flow host's script-driven planning driver's, not yet merged"* items
- `devscene-flow-host/src/devscene_flow_host/host/round_gates.py` — *"this order is the host's, chosen in #472"*
- `devscene-flow-host/tests/test_planning_entry.py` — *"variant (#325)"*
- `devscene-flow-host/tests/test_round_gates.py` — *"chosen over bash's in #472"*

**Work:**

- [ ] `agent_prompts.py`: the item becomes *"Keeping `RevisionFindingsStore` filled in run mode: `host/planning_executor.py`'s."*
- [ ] `planning_entry.py`: *"… the run driver's, `host/planning_run.py`."* `planning_hooks.py`: *"… the run driver's, `host/run_exits.py`, because each is a `RunExit` and not a node or round event."*
- [ ] `claude_executor.py`: the pairing item names `host/node_sessions.py` → `NodeSessions`, and the stream item names the same class. Drop *"not yet merged"*.
- [ ] `round_gates.py` and `test_round_gates.py`: *"this order is the host's"* and *"chosen over bash's"*, with no number. `test_planning_entry.py`: the clause keeps what the variant does, without `(#325)`.
- [ ] Re-run `git grep -nE '#[0-9]+' -- devscene-flow-host/src devscene-flow-host/tests` and fix any further hit the same way.

**Verification:**

- `git grep -nE '#[0-9]+' -- devscene-flow-host/src devscene-flow-host/tests` prints nothing.
- `git grep -n 'not yet merged' -- devscene-flow-host/src` prints nothing.
- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_planning_entry.py` passes, as does `… test tests/test_round_gates.py`. Only their docstrings changed.

**Deviations from plan:**
- The first `git grep` check still prints five lines: `tests/test_node_sessions.py` (the `"#1 plan_writer …"` and `"#2 plan_review …"` literals) and `tests/test_planning_driver_walk.py` (`"[plan-drive] #1 plan_writer …"`). These are run-log sequence numbers inside expected-value string literals, not issue numbers, so they were kept. Removing them would change what those tests assert. No issue number remains in `devscene-flow-host/src` or `devscene-flow-host/tests`.
- `host/session_process.py` also deferred stream writing to the planning driver *"not yet merged"*, and it is not in the Targets list. It now names `host/node_sessions.py` → `NodeSessions`, so the second `git grep` check prints nothing.
