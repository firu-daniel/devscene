### Task 8 — Document the two drivers in `docs/flow-graph-walker.md` and the pilot in `docs/watcher.md`

**Goal:** Record the pilot where a maintainer looks for it:
- **`docs/flow-graph-walker.md`** says that the walker now has two drivers, which one runs when, and how each runs a parallel round, each following the contract #370 wrote in `### Item 8 — a round's gates fan out, and the round node joins`. It also records which facts about a node session are not yet measured, beside the one hand step that measures them.
- **`docs/watcher.md`** carries the libraries, the switch, the launch sequence and the per-execution-mode answer.

**Depends on:**
- **Task 6:** the switch `PLANNING_DRIVER_PLUGIN_DIR` (empty means off, read in local mode only); the readiness conditions; the setup → driver → engine sequence; `session_exec`; and the node stall threshold of `max(STALL_WARN_SECS, STALL_KILL_SECS − POLL_INTERVAL_SECS)`, `0` when `STALL_CHECK_ENABLED` is not `1`.
- **Task 3:** `pd_drive`'s `0` / `3` / `2` returns, and STOP per block, PAUSE once per set and the cap over the whole set.
- **Task 1:** the prompts read from the pinned core; the schema keys `outcome`, `findings_file`, `return` and `harness_friction`; the `init` check; the MCP flags; and the node stream path `${log_path%.log}.planning/<seq>-<node>.stream.jsonl`, appended to the run's `.stream.jsonl` at reap.
- **Task 7:** the clause literal `PLANNING IS SCRIPT-DRIVEN ON THIS LAUNCH` and the engine command's step 4a.

Every fact here is cited to the file and symbol that owns it rather than restated in full (`.claude/context/conventions.md` → `## Documents of record`).

### Targets

- `docs/flow-graph-walker.md`: its **What it owns.** paragraph, `### Item 4 …`, `### Item 8 …`, and a new section.
- `docs/watcher.md`: `## 2. The scripts` (its table and a new subsection), `## 4. Pausing, parking and the usage gate` → *"Its policy knobs, by name"*, and `## 6. What a human must do, and what ships unexercised`.

**Work:**

- [ ] **`docs/flow-graph-walker.md`: the second driver, in place.**
  - Extend **What it owns.** to cover the second driver.
  - In `### Item 4 — STOP, the counter and PAUSE stay orchestrator steps`, add a closing **On the script-driven path.** paragraph: there they are the driver's, per set, exactly as **A set.** words them, and the halt messages are the core's with `<reentry_command>` resolved to the autonomous fork's value.
  - After `### Item 8`'s **What a second driver must do.**, add one sentence: that driver is built, and the new section below records it.
- [ ] **`docs/flow-graph-walker.md`: a new `## 5. The two drivers`.** Write it in this file's decision / reason / cost form. It covers:
  - **Which runs when.** The orchestrator is the default and every mode's driver. The script driver runs only when the switch is set, in a local run of the task engine whose planning is not finished.
  - **How each runs a parallel round.** The orchestrator runs it as one message of foreground `Agent` calls. The driver runs one headless session per block, launched at once and recorded with `next --node` in finish order. `action: wait` is nothing to do; a held `error` or `blocker`, and a stalled session the driver killed, come back as one binding after the last outcome; siblings are never cancelled.
  - **Why the driver is three watcher-sourced libraries** and not a script: one producer of the launch vector, no new agent reach, and the full environment for the wrappers.
  - **Why the prompts come from the pinned plugin's core** at run time: the core stays the one owner of every dispatch block.
  - **The schema-from-graph rule**, and the `init` check that answers the three gaps of `docs/orchestrator-cost-measurement.md` → `## 4.`
  - **The cost.** The setup session per launch, the node streams' one-node delay into the run stream, and no `context_notes:` on this path.
  - **What the follow-up measures**, by pointing at `ROADMAP.md` → the `Script-driven planning pilot` row (#159). No figure taken under a stub is cited as evidence of a saving.
- [ ] **`docs/flow-graph-walker.md`: the unmeasured facts.** Add `### Not yet measured, and the hand step that measures it` under the new section. It names the three facts:
  - whether a `stream-json` session's closing `result` event carries `structured_output` under `--json-schema`;
  - whether the `init` tools under `--json-schema` are the agent's allowlist and nothing more;
  - whether an installed plugin copy shadows `--plugin-dir` for a scoped `--agent`.

  Then the hand step: one real planning run with the switch set, from a terminal outside any agent session. Give one fenced block, one command per line, holding:
  - the `watcher.env` line;
  - the `restart-watcher.sh` call;
  - three `jq` reads over `<log>.planning/1-plan_writer.stream.jsonl`, for the `init` event's `tools`, the `init` event's `plugins` and the `result` event's `structured_output` keys.

  Close with the rule that each fact is recorded with its command, its exact output, the Claude Code version and the date, as this tree's documents of record require.
- [ ] **`docs/watcher.md`.**
  - **§2 table.** Add three rows for `lib/planning-node-lib.sh`, `lib/planning-record-lib.sh` and `lib/planning-driver-lib.sh`: what each owns; *"sourced by the watcher for the opt-in planning driver; never executed, and it ships without an executable bit"*; and `no` in the allow-entry column.
  - **A new `### Script-driven planning (opt-in pilot)` subsection under §2** covering:
    - the switch and how to set it, in a fenced block;
    - the readiness conditions and the `planning driver off for '<branch>'` log line;
    - the clause and the three-session sequence;
    - how the driver's `0` / `3` / `2` maps onto `classify_run_exit`;
    - the node stall rule and why it fires before the run-level watchdog;
    - where node streams land;
    - the per-execution-mode answer: a local watcher run takes the driver when ready, and a remote job always takes the orchestrated path because no `devscene-run.yml` `env:` block maps the switch and job mode ignores it.
  - **§4.** Add `PLANNING_DRIVER_PLUGIN_DIR` to *"Its policy knobs, by name"*.
  - **§6.** Add one bullet pointing at the unmeasured facts in `docs/flow-graph-walker.md`.

**Verification:**

- `git grep -n "PLANNING_DRIVER_PLUGIN_DIR" -- docs` finds the switch in both files, and `docs/watcher.md` states its local-only scope and the remote job's orchestrated path in one place.
- Every command an adopter or maintainer is told to run in the two files sits alone on its own line in a fenced block, as `harness-runs/lessons.md` → *Adopter-facing documentation* requires.
- No line in either file states a saving, a cost or a duration measured by the branch's tests or its own sessions (`harness-runs/lessons.md` → *Evidence and measurement*).
