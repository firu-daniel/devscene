### Task 6 — Run the main checkout's walker from the unsandboxed planning driver

**Goal:** The watcher's planning driver runs the walker outside the sandbox. It runs the **main checkout's** `flow-walker.sh`, with the run copy as its working directory, instead of the run copy's own `flow-walker.sh`. That way the walker script, the environment it executes and the graph it reads are the ones `cli/src/generators/writeProtection.ts` write-protects:
- that module's rule is *"anything that runs outside the sandbox must not be writable from inside it"*;
- its set names *"the main checkout's outer-loop scripts and their library, the main checkout's `<scriptsDir>/python/`"*;
- it leaves a run copy's environment writable *"since no unsandboxed step builds from it"*.

After the cutover, the run copy's walker would execute the run copy's `<scriptsDir>/python/.venv`, which is an unsandboxed step running from a writable environment. This task closes that route instead of widening it (`<state_dir>/lessons.md` → *"Never drop a protection because another route 'can already' reach the same target until that route is measured"*).

**Depends on:**
- **Task 1.** The hand-off resolves its environment, project and `--flows` directory beside itself unless `DEVSCENE_FLOW_HOST_ENV` / `DEVSCENE_FLOW_HOST_PROJECT` are set. Run from the main checkout, it therefore uses `<main>/<scriptsDir>/python/.venv`, `<main>/<scriptsDir>/python/devscene-flow-host` and `<main>/<scriptsDir>/flows`. It finds the repository root from its working directory, so the walk's state stays in the run copy.
- **Task 2.** `cli/test/helpers/planning-driver.mjs` builds the driver fixture's environment with `walkerEnv()` merged in. Its fixture also takes a `mainRepo` directory, passed to the driver as `PD_MAIN_REPO` and defaulting to the fixture's own directory.
- **Task 5.** It grades an unprovisioned main-checkout environment as a `doctor` failure where `execution.scriptDrivenPlanning` is on, which is the consequence of this task.

**Where this task stops.** The driver's other reads from the run copy are data and stay where they are: `PNL_GRAPH`'s node list from `lib/planning-node-lib.sh`, and the ledger and round files. The driver's logged call text `flow-walker.sh <verb> …` is unchanged, so `cli/test/planning-driver-control.test.mjs`'s `[plan-drive] walker: flow-walker.sh start ` match holds.

### Targets

- `cli/templates/scripts/lib/planning-driver-lib.sh` — `pd_main`'s `PD_WALKER`, and the header's walker paragraph and `REPRO`.
- `cli/test/planning-driver-walk.test.mjs` — one new case.

**Work:**

- [ ] `planning-driver-lib.sh`:
  - set `PD_WALKER="$PD_MAIN_REPO/$(hr_scripts_dir "$PD_MAIN_REPO")/flow-walker.sh"`, resolved once in `pd_main` with the same fault handling as `PNL_SCRIPTS_DIR`'s resolution — a `planning-driver: <cause>` fault and status `2` when it does not resolve;
  - keep `pd_walk`'s `cd "$PD_WORKTREE" && bash "$PD_WALKER" …`;
  - add a header paragraph: the walker is the main checkout's because it runs unsandboxed, citing `writeProtection.ts`'s rule;
  - update the `REPRO` step *"copy `flow-walker.sh`, `flows/` and the five libraries under "$r/m/s/""* to say the walker run is `$r/m`'s.
- [ ] `planning-driver-walk.test.mjs`, new case: build a second `walkerFixture` as the main checkout, pass it as Task 2's `mainRepo` option, and replace the worktree fixture's own `<scriptsDir>/flow-walker.sh` with a script that prints nothing and exits `9`. Drive the walk to its first set, and assert the drive did not fault on the walker. Its log carries the real walker's `action: dispatch` lines, so the walker that ran is the main checkout's. State the rule in the case's comment.

**Verification:**

- Run `commands.typecheck`; it must exit 0.
- Run `npm test --workspace cli -- test/planning-driver-walk.test.mjs`.
- `git grep -n 'PD_WALKER=' -- cli/templates/scripts` shows only the main-checkout form.
