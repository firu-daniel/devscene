### Task 17 — Act on each `RunExit` — hand-off, pause, halt, park — in `host/run_exits.py`

**Goal:** Port the part of the bash driver that acts on where a walk stopped: `pd_handoff`, `pd_stop_halt`, the cap halt, the PAUSE and undelivered pauses (`pd_partial`, `prl_pause`), `pd_ask_park`, `pd_escalate_park` and the walker-escalation park. As the task prompt's leads say, *"each arrives as a `RunExit` the driver acts on"*. `act_on_exit` returns the stop kind that Task 18 turns into the command's stdout line and status.

**Depends on:**
- **Task 10.** `host/run_records.py` → `write_park(repo_root, state_dir, branch, *, raised_by, title, body) -> str` and `write_pause(repo_root, state_dir, branch, *, phase, next_step, now)`. Also `records/ledger.py` → `read_run_mode_entries(repo_root, state_dir, branch) -> RunModeEntries`, a frozen `RunModeEntries(skipped: str, ignored: tuple[IgnoredEntry, ...])` with `IgnoredEntry(text: str, reason: str | None)`: `skipped` is the `## Run mode` section's `- skipped:` value with its `   (…)` comment cut, `""` when absent; each `reason` is verbatim with its closing parenthesis.
- **Task 11.** `host/observations.py` → `Observations.add(category, problem, evidence, cost)`.
- **Task 16.** `host/planning_run.py` → `PlanningOutcome(kind, exit, consumed, last_round, pending_round, sessions)`. `kind` is `done`, `kill_switch`, `stop_file` or `run`. `sessions.return_document(node)` is a node's last return object.

**The exits, as GraphScene defines them.** `RunExit` is `End | Stop | Interrupt | Halt | Refused`:
- `End` is the `<terminal_handoff>`. It carries `reports` and `passed`.
- `Stop` is the `<escalate>` binding. It carries `node`, `agent`, `reason`, `summary`, `evidence`, `round_counts`, `held` and `closed_round`.
- `Interrupt` is the `<ask>` binding. It carries `node`, `agent`, `resume` and `resume_outcome`.
- `Halt(reason, detail)` has `reason` one of `stop`, `pause`, `cap` or `undelivered`.

**The existing readers this task also uses**, each with its present signature: `records/ledger.py` → `read_planning_marks(repo_root, state_dir, branch) -> PlanningMarks` and `DONE_VALUE` / `SKIPPED_VALUE`; `records/config.py` → `read_config(repo_root).phases`; and `host/paths.py` → `render_path(template, state_dir, branch)` over the graph's path named by `host/planning_hooks.py` → `UI_TEST_INDEX_PATH` (imported, not re-spelled, as `host/planning_entry.py` imports it), as `host/planning_hooks.py` → `PlanningHooks._ui_test_plan_written` builds it.

**Where this task stops.** The convergence commits and the `P3` flip have already run as the `commit_convergence` hook before the `End` is returned, so this task makes none of them. Exit statuses and stdout are **Task 18's**. Reading any ledger or configuration line is `records`'; this module formats the values the readers above return and parses no record itself.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/run_exits.py` (new)
- `devscene-flow-host/tests/test_run_exits.py` (new)

**The return fields it reads, exported for Task 21.** Every return-document key and every node this module reads one from is a module-level `Final` of `host/run_exits.py`, and the code reads through these names, never an inline key. Task 21 imports them:
  - nodes: `PLAN_WRITER_NODE: Final = PLAN_WRITER_ENTRY`, `UI_WRITER_NODE: Final = UI_WRITER_ENTRY` — re-exports of the owner's constants, imported from `devscene_flow_host.host.planning_entry` (which defines `PLAN_WRITER_ENTRY: Final = "plan_writer"` and `UI_WRITER_ENTRY: Final = "ui_writer"`), the same way `UI_TEST_INDEX_PATH` is imported rather than re-spelled. They are the planning graph's two `<ask>`-bound nodes (`cli/templates/scripts/flows/task_plan_writing.graph.json`, the `questions` outcomes bound to `<ask>`). `run_exits.py` writes no string literal for either node id: `git grep -n '"plan_writer"\|"ui_writer"' -- devscene-flow-host/src/devscene_flow_host/host/run_exits.py` returns no hits;
  - fields: `QUESTIONS_FIELD: Final = "questions"`, `TASKS_COUNT_FIELD: Final = "tasks_count"`, `TESTS_COUNT_FIELD: Final = "tests_count"`, `REASON_FIELD: Final = "reason"`;
  - `QUESTION_NODES: Final = (PLAN_WRITER_NODE, UI_WRITER_NODE)` — the nodes whose `Interrupt` it reads `QUESTIONS_FIELD` from;
  - `RETURN_FIELD_READS: Final[tuple[tuple[str, str], ...]]` — every `(node, field)` read the module makes: `(PLAN_WRITER_NODE, QUESTIONS_FIELD)`, `(UI_WRITER_NODE, QUESTIONS_FIELD)`, `(PLAN_WRITER_NODE, TASKS_COUNT_FIELD)`, `(UI_WRITER_NODE, TESTS_COUNT_FIELD)`, `(UI_WRITER_NODE, REASON_FIELD)`. A read added to the module is added here in the same change.
  - The `Interrupt` body reads `QUESTIONS_FIELD` from `sessions.return_document(exit.node)`; an `exit.node` outside `QUESTION_NODES` is narrated and parked with the not-captured body, never read.

**Work:**

- [ ] **The entry point**, with the return-field constants above defined first. `async act_on_exit(outcome, *, graph, repo_root, main_repo, state_dir, branch, wrapper, observations, narrate, now) -> StopKind`. `graph` is the loaded planning `FlowGraph`. `StopKind` is `Literal["handed_off", "park", "pause", "undelivered", "stop", "cap", "kill_switch"]`.
  - **`done` and `End`** return `handed_off`. For an `End`, first narrate the Done-summary lines `pd_handoff` logged, in its order:
    - `CONVERGED: <branch> — planning handed off`;
    - `tasks_count: <plan_writer's tasks_count, or not reported in this session>`;
    - the story index;
    - the per-task files;
    - the `ui_test:` line, for `passed`, `no_ui`, `qa-phase-off`, `run-mode-skipped` or not walked, with `ui_writer`'s `tests_count` / `reason`. It is read from the `End`'s `ui_test` report when present. Otherwise it falls back as `pd_handoff` did, through the readers above: `read_planning_marks(…).p2` `SKIPPED_VALUE` gives `run-mode-skipped` when `read_config(repo_root).phases["qa"]` is `True`, else `qa-phase-off`; `DONE_VALUE` gives `passed` when the UI-test index at `render_path(graph.paths[UI_TEST_INDEX_PATH], state_dir, branch)` exists under `repo_root`, else `no_ui`; any other mark gives not walked;
    - `passed without dispatch: …` when skips passed;
    - `📌 Dispatch additions: none`;
    - the `📌 Run mode:` line, formatted as `pd_run_mode_line` formatted it from `read_run_mode_entries(repo_root, state_dir, branch)`'s value: each `IgnoredEntry` becomes ` | ignored: "<text>"`, followed by ` (<reason>` when `reason` is not `None`; a `skipped` of `""` or `none` gives `📌 Run mode: none<ignored…>`; any other gives `📌 Run mode: skipped <skipped> — authority <state_dir>/flow_progress/<branch>_progress.md ## Run mode<ignored…>`.
  - **`kill_switch`** returns `kill_switch`, and adds the `flow-efficiency` observation *"The global kill switch ended script-driven planning"*.
- [ ] **The halts.**
  - **`Halt("stop")` and `stop_file`** narrate `Halted by STOP file at <state_dir>/STOP. Delete the file and re-run /devscene:branch-start-plan-autonomous to continue.`, add *"A STOP file ended script-driven planning"*, and return `stop`.
  - **`Halt("cap")`** narrates the `MAX_TOTAL_DISPATCHES` halt text `pd_run_set` logged, verbatim with its paths, adds *"The dispatch cap halted script-driven planning"*, and returns `cap`.
  - **`Halt("pause")`** first makes the partial commit. The round number is `pending_round`, else `last_round`, else no commit and a narrated *"no round number is known for the interrupted dispatch: no partial commit"*. The commit is `commit_artifact(wrapper, repo_root, "plan-round-partial", round_number=n)`. It then calls `write_pause(…, phase="planning", next_step="dispatch <pending nodes>")`, adds *"A PAUSE request paused script-driven planning"*, and returns `pause`.
  - **`Halt("undelivered")`** makes the same partial commit, then `write_pause(…, phase="planning (API overload)", next_step="re-dispatch <nodes>; three consecutive dispatches undelivered: <detail>")`. It adds *"Sustained undelivered dispatches self-paused script-driven planning"* and returns `undelivered`.
- [ ] **The parks: `<ask>` (an `Interrupt`), `<escalate>` (a `Stop`) and a `Refused`.**
  - **`Interrupt`, the body.** One `## Q<k> — <first line of item k>\n\n<item k>\n` per item of the return document's `questions` list, from `sessions.return_document(exit.node)`. When there are none, the body is ``The writer `<agent>` returned questions, but its return text was not captured in this session.``
  - **`Interrupt`, the park.** `write_park(raised_by=<agent or node>, title="Questions from <agent>", body)`. Then narrate `PARKED: <branch> — 1 question(s) at <state_dir>/clarifications/<branch>/`, add *"A writer's questions parked script-driven planning"*, and return `park`.
  - **`Stop`, the body:**
    - opens ``The planning walk escalated at `<node>`, reason `<reason>`.``;
    - then a fenced `text` block of the stop's summary, evidence and round counts;
    - then one `### `<gate>` — <outcome>` section per held gate. Each carries the agent, the reason from that node's `Launch` result, and its return text when a return document exists, else `not captured in this session`;
    - then `## Q1 — How should planning continue?` with ``The walker ended this walk at the escalation above and routes nowhere past it.``
  - **`Stop`, the partial commit.** When `held` is non-empty, the `plan-round-partial` commit is made first, as `pd_escalate_park` did. The round is the held gates' round number, else `last_round`.
  - **`Stop`, the park.** It is `write_park(raised_by=<agent or "plan_round">, title="Planning escalated at <node> (<reason>)")`, and it returns `park`.
  - **`Refused`** parks with `raised_by="plan_round"` and title `Planning walk refused a step`. The body names the refusal's reason in a `text` fence, then the same `## Q1 — How should planning continue?` section. It adds the `silent-failure` observation *"The planning walk refused a step during script-driven planning"* and returns `park`.
- [ ] **Module docstring.**
  - *"The rule:"* — each `RunExit` is acted on as the retired bash acted on where its walk stopped, and the module names the functions it reads as: `pd_handoff` (with `pd_run_mode_line`), `pd_stop_halt`, `pd_partial`, `pd_ask_park` and `pd_escalate_park` in `cli/templates/scripts/lib/planning-driver-lib.sh`, retired and readable in that file's history once Task 4 deletes it. It formats values the `records` readers return and reads no record line itself.
  - *"Deliberately not covered"* — the convergence commits and the `P3` flip, which the `commit_convergence` hook runs before an `End` is returned (`host/planning_hooks.py`); exit statuses and the stdout line, which are Task 18's `commands/planning_driver.py`; the observation flush, also Task 18's; and reading the ledger or the configuration, which is `records`'.
- [ ] **`tests/test_run_exits.py`.** It builds each exit by hand from GraphScene's public types, loads the real planning graph read-only, plants a fake wrapper, a minimal ledger and a `devscene.config.json`, and uses a recording stand-in for `Observations` and the narration. Cases:
  - its header rule;
  - an `End` narrating the summary in order with `tasks_count` from a planted return document;
  - the `📌 Run mode:` line for a planted ledger with a skipped value and two `- ignored:` entries, one with a reason, and for one whose `- skipped:` is `none`, each against a literal;
  - the `ui_test:` fallback with no `ui_test` report: `P2` `-` with `qa` on and off, and `P2` `x` with and without a planted UI-test index;
  - each halt's returned kind and its exact narration;
  - the pause's wrapper call `--artifact plan-round-partial --round 1`, and the pause files written;
  - the pause with no known round making no wrapper call;
  - the `<ask>` park's exact question file for two questions, matching the retired `planning-driver-control` case *"questions park as one Q<k> section per returned item"*;
  - the `<escalate>` park with a held gate committing the partial first;
  - one with no held gate committing nothing;
  - `Refused`'s park;
  - `QUESTION_NODES` equals the set of nodes in the real planning graph with an outcome bound to `<ask>`, so a new `<ask>` node cannot go unread.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_run_exits.py` passes.
- Every literal the module narrates or writes is a module-level `Final` string or format, and the suite asserts each against a literal written in the test.

**Deviations from plan:**
- The pause's `dispatch <pending nodes>`, the cap's `MAX_TOTAL_DISPATCHES (<n>)` and a held `Stop`'s round had no source in the planned `PlanningOutcome`, and no `Halt` or `Stop` field carries them. `host/planning_run.py` now also returns `pending_nodes` (read from the same `walker.current()` call as `pending_round`), `dispatch_cap`, and `dispatched_round` (the round number of the last dispatch that carried one, recorded by a `_RoundRecorder` executor wrapper). All three default, so earlier callers are unchanged. A held `Stop` commits for `dispatched_round`, falling back to `last_round`. `tests/test_planning_run.py` asserts the new fields.
- A held gate's reason comes from its last `Launch` result, and `NodeSessions` had no way to read one. It now has `launch_result(node)`, asserted in `tests/test_node_sessions.py`.
- These follow the retired bash, which the plan does not list. Every park narrates `PARKED: …` and every pause narrates `PAUSED: <branch> — <phase>`, as `prl_park` and `prl_pause` logged them. The kill switch narrates `halted: the global kill switch <path> is present`, as `pd_main` did. A `Stop` adds `pd_escalate_park`'s observation *"A walker escalation parked script-driven planning"*. A `Stop` with no held gate and reason `error` or `blocker` carries the stop node's own session section, as `pd_escalate_park` did.
- The `Refused` body opens `The planning walk refused a step:` above its `text` fence. A `Stop`'s fence lists `summary:`, `evidence:` (the rendered path) and `round_counts:`, with `none` when a value is absent.
