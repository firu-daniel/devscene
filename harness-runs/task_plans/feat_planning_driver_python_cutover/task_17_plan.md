### Task 17 — Act on each `RunExit` — hand-off, pause, halt, park — in `host/run_exits.py`

**Goal:** Port the part of the bash driver that acts on where a walk stopped: `pd_handoff`, `pd_stop_halt`, the cap halt, the PAUSE and undelivered pauses (`pd_partial`, `prl_pause`), `pd_ask_park`, `pd_escalate_park` and the walker-escalation park. As the task prompt's leads say, *"each arrives as a `RunExit` the driver acts on"*. `act_on_exit` returns the stop kind that Task 18 turns into the command's stdout line and status.

**Depends on:**
- **Task 10.** `host/run_records.py` → `write_park(repo_root, state_dir, branch, *, raised_by, title, body) -> str` and `write_pause(repo_root, state_dir, branch, *, phase, next_step, now)`.
- **Task 11.** `host/observations.py` → `Observations.add(category, problem, evidence, cost)`.
- **Task 16.** `host/planning_run.py` → `PlanningOutcome(kind, exit, consumed, last_round, pending_round, sessions)`. `kind` is `done`, `kill_switch`, `stop_file` or `run`. `sessions.return_document(node)` is a node's last return object.

**The exits, as GraphScene defines them.** `RunExit` is `End | Stop | Interrupt | Halt | Refused`:
- `End` is the `<terminal_handoff>`. It carries `reports` and `passed`.
- `Stop` is the `<escalate>` binding. It carries `node`, `agent`, `reason`, `summary`, `evidence`, `round_counts`, `held` and `closed_round`.
- `Interrupt` is the `<ask>` binding. It carries `node`, `agent`, `resume` and `resume_outcome`.
- `Halt(reason, detail)` has `reason` one of `stop`, `pause`, `cap` or `undelivered`.

**Where this task stops.** The convergence commits and the `P3` flip have already run as the `commit_convergence` hook before the `End` is returned, so this task makes none of them. Exit statuses and stdout are **Task 18's**.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/run_exits.py` (new)
- `devscene-flow-host/tests/test_run_exits.py` (new)

**Work:**

- [ ] **The entry point.** `async act_on_exit(outcome, *, repo_root, main_repo, state_dir, branch, wrapper, observations, narrate, now) -> StopKind`. `StopKind` is `Literal["handed_off", "park", "pause", "undelivered", "stop", "cap", "kill_switch"]`.
  - **`done` and `End`** return `handed_off`. For an `End`, first narrate the Done-summary lines `pd_handoff` logged, in its order:
    - `CONVERGED: <branch> — planning handed off`;
    - `tasks_count: <plan_writer's tasks_count, or not reported in this session>`;
    - the story index;
    - the per-task files;
    - the `ui_test:` line, for `passed`, `no_ui`, `qa-phase-off`, `run-mode-skipped` or not walked. It is read from the `End`'s `ui_test` report when present, else from the ledger and the UI-test index, as `pd_handoff` read them, with `ui_writer`'s `tests_count` / `reason`;
    - `passed without dispatch: …` when skips passed;
    - `📌 Dispatch additions: none`;
    - the `📌 Run mode:` line built as `pd_run_mode_line` built it from the ledger's `## Run mode`.
  - **`kill_switch`** returns `kill_switch`, and adds the `flow-efficiency` observation *"The global kill switch ended script-driven planning"*.
- [ ] **The halts.**
  - **`Halt("stop")` and `stop_file`** narrate `Halted by STOP file at <state_dir>/STOP. Delete the file and re-run /devscene:branch-start-plan-autonomous to continue.`, add *"A STOP file ended script-driven planning"*, and return `stop`.
  - **`Halt("cap")`** narrates the `MAX_TOTAL_DISPATCHES` halt text `pd_run_set` logged, verbatim with its paths, adds *"The dispatch cap halted script-driven planning"*, and returns `cap`.
  - **`Halt("pause")`** first makes the partial commit. The round number is `pending_round`, else `last_round`, else no commit and a narrated *"no round number is known for the interrupted dispatch: no partial commit"*. The commit is `commit_artifact(wrapper, repo_root, "plan-round-partial", round_number=n)`. It then calls `write_pause(…, phase="planning", next_step="dispatch <pending nodes>")`, adds *"A PAUSE request paused script-driven planning"*, and returns `pause`.
  - **`Halt("undelivered")`** makes the same partial commit, then `write_pause(…, phase="planning (API overload)", next_step="re-dispatch <nodes>; three consecutive dispatches undelivered: <detail>")`. It adds *"Sustained undelivered dispatches self-paused script-driven planning"* and returns `undelivered`.
- [ ] **The `<ask>` park, an `Interrupt`.**
  - **The body.** One `## Q<k> — <first line of item k>\n\n<item k>\n` per item of the return document's `questions` list, from `sessions.return_document(exit.node)`. When there are none, the body is ``The writer `<agent>` returned questions, but its return text was not captured in this session.``
  - **The park.** `write_park(raised_by=<agent or node>, title="Questions from <agent>", body)`.
  - **Then** narrate `PARKED: <branch> — 1 question(s) at <state_dir>/clarifications/<branch>/`, add *"A writer's questions parked script-driven planning"*, and return `park`.
- [ ] **The `<escalate>` park (a `Stop`) and a `Refused`.**
  - **`Stop`, the body:**
    - opens ``The planning walk escalated at `<node>`, reason `<reason>`.``;
    - then a fenced `text` block of the stop's summary, evidence and round counts;
    - then one `### `<gate>` — <outcome>` section per held gate. Each carries the agent, the reason from that node's `Launch` result, and its return text when a return document exists, else `not captured in this session`;
    - then `## Q1 — How should planning continue?` with ``The walker ended this walk at the escalation above and routes nowhere past it.``
  - **`Stop`, the partial commit.** When `held` is non-empty, the `plan-round-partial` commit is made first, as `pd_escalate_park` did. The round is the held gates' round number, else `last_round`.
  - **`Stop`, the park.** It is `write_park(raised_by=<agent or "plan_round">, title="Planning escalated at <node> (<reason>)")`, and it returns `park`.
  - **`Refused`** parks with `raised_by="plan_round"` and title `Planning walk refused a step`. The body names the refusal's reason in a `text` fence, then the same `## Q1 — How should planning continue?` section. It adds the `silent-failure` observation *"The planning walk refused a step during script-driven planning"* and returns `park`.
- [ ] **`tests/test_run_exits.py`.** It builds each exit by hand from GraphScene's public types, plants a fake wrapper and a minimal ledger, and uses a recording stand-in for `Observations` and the narration. Cases:
  - its header rule;
  - an `End` narrating the summary in order with `tasks_count` from a planted return document;
  - each halt's returned kind and its exact narration;
  - the pause's wrapper call `--artifact plan-round-partial --round 1`, and the pause files written;
  - the pause with no known round making no wrapper call;
  - the `<ask>` park's exact question file for two questions, matching the retired `planning-driver-control` case *"questions park as one Q<k> section per returned item"*;
  - the `<escalate>` park with a held gate committing the partial first;
  - one with no held gate committing nothing;
  - `Refused`'s park.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_run_exits.py` passes.
- Every literal the module narrates or writes is a module-level `Final` string or format, and the suite asserts each against a literal written in the test.
