### Task 5 — Pin the watcher's side of the driver hand-off against a stub `uv`, locally and in job mode

**Goal:** Rewrite `cli/test/watcher-planning-driver.test.mjs` against the watcher Task 2 wrote. The suite keeps its present rule:
- **Key off or absent:** one engine session.
- **Key on and ready:** a setup session carrying `PLANNING IS SCRIPT-DRIVEN ON THIS LAUNCH`, then the driver, then the engine session only on its hand-off, in local and job mode alike.
- **On the hand-off:** exactly the answered pairs the driver consumed are archived.

The driver is now a process the watcher reaches through `uv`. A stub `uv` on `PATH` stands in for it. It records its argv and environment, and answers as the contract says. The suite pins the watcher's half without the Python command, which does not exist until Task 18.

**Depends on:** Task 2, which launches `devscene-planning-driver` through `hr_flow_host_exec` and maps the result:
- **`0` with `consumed: <i>…`:** archive the pairs, then run the engine session.
- **`3`:** no engine session. `stopped: undelivered` sets the pause detail.
- **Anything else:** `failed`.

**Where this task stops.** The driver's own behaviour (walk, parks, stops) is **Tasks 19–20's**, in `pytest`. This suite never runs Python.

### Targets

- `cli/test/watcher-planning-driver.test.mjs` — rewritten
- `cli/test/helpers/watcher.mjs` — only if the stub `uv` needs a fixture hook there (a `PATH` prefix). Add it as an option, and leave every existing caller unchanged.

**Work:**

- [ ] **The stub.** The fixture plants:
  - an environment under `<scripts_dir>/python/.venv`, with the `pyvenv.cfg` marker and an executable `bin/devscene-planning-driver`;
  - a stub `uv` first on the watcher's `PATH`.

  The stub writes its whole argv and the values of `DEVSCENE_MAIN_REPO`, `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS`, `UV_PROJECT_ENVIRONMENT` and `PYTHONPATH` to a calls log. It then plays one scripted answer: the exit status, the stdout line, and optionally the archive-relevant state.

  Keep the existing stub agent CLI for the setup and engine sessions. Every expected literal is written in this file. Rewrite the header to state the rule above and the stub's role.
- [ ] **The ready path, local.** The driver answers `0` with `consumed: 1`. Assert:
  - the order: setup session, then one `uv` call, then the engine session;
  - the `uv` argv: `run --frozen --no-sync --no-cache --project <scripts>/python/devscene-flow-host devscene-planning-driver --branch feat_x --worktree <wt> --main-repo <main> --plugin-dir <derived root> --flows <main scripts>/flows --log <log> --formatter <formatter>`, then `--`, then the agent CLI and the same shared flags the engine session got, minus `-p`, `--output-format` and `--verbose`;
  - `answer_1.md` / `question_1.md` archived, and no other pair archived.
- [ ] **The stops.**
  - The driver answers `3` with `stopped: park`: no engine session, and the run is classified from the park on disk.
  - It answers `3` with `stopped: undelivered`: the local `paused` notification carries `paused itself on API overload: three consecutive planning dispatches undelivered — `.
  - It answers `2`, or `0` with no `consumed:` line: the run is `failed`, and the log carries `planning driver failed for 'feat_x' (devscene-planning-driver exit <n>)`.
- [ ] **Not ready, and off.**
  - With no `bin/devscene-planning-driver`, the launch is one engine session. The log carries `planning driver off for 'feat_x': the flow host cannot run devscene-planning-driver (` followed by the cause.
  - With the key `false` or absent, there is no `uv` call and one engine session.
- [ ] **Job mode.** One case runs `autonomous-watcher.sh job` with a `directory`-sourced marketplace and the key on. It asserts the same three-step order and `uv` argv as the local ready case (`<state_dir>/lessons.md` → *"A recovery for an unattended run's failure covers every execution mode"*).

**Verification:**

- `npm test --workspace cli -- test/watcher-planning-driver.test.mjs` passes, every case above included.
- No case starts a real `uv` or Python process. The calls log shows only the stub.
