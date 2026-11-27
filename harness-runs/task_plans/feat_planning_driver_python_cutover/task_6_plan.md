### Task 6 — Describe the Python planning driver in the `cli` package's two READMEs

**Goal:** `cli/README.md` and `cli/templates/scripts/README.md` stop naming the bash driver's three libraries. They say what the script-driven path runs now: `devscene-planning-driver`, launched by the watcher from `<scriptsDir>/python/` through the library route `hr_flow_host_exec`.

**Depends on:** Tasks 2 and 3. Task 2 launches the driver through `hr_flow_host_exec`, and Task 3 removed the libraries from the shipped set.

**Where this task stops.** Prose only, in this layer's two READMEs. `docs/` is **Task 25's**.

### Targets

- `cli/README.md` — the outer-loop paragraph (scope register row 5)
- `cli/templates/scripts/README.md` — its opening paragraph (scope register row 6)

**Work:**

- [ ] `cli/README.md`: replace *"the planning driver's three libraries (`lib/planning-*-lib.sh`), which the run watcher sources for the opt-in script-driven planning pilot"* with the planning driver `devscene-planning-driver`. It is a console script of the shipped `devscene-flow-host` package, which the run watcher launches from `<scriptsDir>/python/` through `uv` for the opt-in script-driven planning pilot. Replace *"the planning driver's libraries read for its node list"* with *"the planning driver walks"*.
- [ ] `cli/templates/scripts/README.md`:
  - drop the three library names from the list of shipped assets;
  - the graph's second reader is the planning driver;
  - replace *"the watcher's planning driver, not the orchestrating session, runs `flow-walker.sh`"* with the fact as it now stands: the driver walks the graph in-process, and runs no `flow-walker.sh`.

**Verification:**

- `git grep -nE 'planning-(driver|node|record)-lib' -- cli/README.md cli/templates/scripts/README.md` prints nothing.
- Each new sentence names only things that exist after Tasks 1–3: `hr_flow_host_exec`, the console script name, and `<scriptsDir>/python/`.
