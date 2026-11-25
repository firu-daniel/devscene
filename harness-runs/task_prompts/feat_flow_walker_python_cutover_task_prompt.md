`feat_flow_walker_python_cutover` switches the harness from the bash walker to GraphScene's and retires the bash walker. Bringing the Python packages and their `uv` requirement to adopters is #478, ordered before this branch. Part of #376.

## Decided (2026-11-23)

- **A full cutover, with no bash fallback.** `flow-walker.sh` runs the Python walker, `devscene-flow-host`'s compatibility command (#465, split out of #418 on 2026-11-23), for every caller: orchestrator sessions (autonomous, started by the watcher or from a terminal, and semi-autonomous), the user-review fix flow's `check-round-file`, and the script driver. The bash walker is retired in this branch once the `flow-walker*` suites pass against Python. This replaces the leads' "perhaps with the bash walker behind a flag for a while".
- **Shipping to adopters is #478** _(split out 2026-11-24)_. The npm package carrying the sources, provisioning, the `doctor` check, `setup-uv` and the README requirement land there, before this branch. This branch's `flow-walker.sh` hand-off reaches the package where #478 puts it.
- **Two axes, kept apart.** This branch decides which walker runs. Who drives the walk, an orchestrator session or the watcher's script driver, is #424's opt-in, and #425 makes the graph driver the default for headless runs.
- **The v3 bridge's retirement is split out to #459**, together with the port of `check-flow-graph.sh`'s checks 4–7 and the checker comparison. This branch ships the v4 graph, which the Python walker reads.

## Decided (2026-11-24)

- **A change under `.github/workflows/` is pushed by hand.** If this branch changes a file under the repository's `.github/workflows/`, the run parks **before** the push that would carry it. The park's question asks for that push. The user pushes by hand, then drops an answer acknowledging it, and the run resumes. The unattended push guard refuses such a push, and a refused push fails the run.

## Decided (2026-11-24, after #478)

- **The suites test the branch's Python, not main's.** In a run copy, `setup-worktree.sh` step 6 builds `<scriptsDir>/python/.venv` from the **main checkout's** packages, as wheels (`--no-editable`), never from the copy's own tree (#478, a security choice that stays). So the `flow-walker*` suites, and anything else this branch runs through the walker, put the copy's own sources first on `PYTHONPATH` — `<copy>/devscene-flow-host/src:<copy>/graphscene/src` — over that main-built environment, so a `devscene-flow-host` change made on the branch is the code the suites exercise. How the hand-off or the test helper sets it is this branch's choice; the fixture repositories have no `<scriptsDir>/python/`, so the helper names the project and environment explicitly.
- **A host without `uv` fails, and `init` provisions by default.** With the walker needed:
  - `doctor`'s `uv` check, a warning since #478, becomes a failure;
  - `setup-worktree.sh` step 6 fails the bootstrap where it printed `SKIPPED` and passed (no `uv`, or no project);
  - `init` builds the environment by default instead of behind `--provision-python`. The flag's fate (kept as a no-op, inverted to an opt-out, or removed) and what a run that cannot be prompted does are this branch's to settle.
- **Per-call startup cost: measure and record, no threshold.** The cutover goes ahead whatever the number is; the measurement goes into `docs/flow-graph-walker.md` so later improvements have a baseline.
- **This repository's re-render is a post-merge user step**, not a run task: the run never runs `init --upgrade` or the self-adopt re-render on the main checkout.
- **A leftover bash state file is deleted.** A flat file at `<stateDir>/.flow_walker_state` is removed and the walk starts fresh, the orchestrator's `current` → exit 1 → `start` recovery (#464). Not moved aside, not migrated.

## Leads to check (2026-11-23)

_Raised with the decision above, for the planning session to confirm or refute._

- **`uv` inside a session's sandbox** _Measured 2026-11-24 on macOS, under a run's per-run profile, through `scratch-run.sh`._ `uv` runs. `uv run --frozen --no-sync --no-cache --project devscene-flow-host devscene-flow-walker start` and `current` exited `0` and wrote the walk's state and locks. Without `--no-cache`, `uv run` exits `2` with `Failed to initialize cache at ~/.cache/uv`, because the sandbox refuses the cache. So the hand-off needs `--no-cache`, as `python-service.sh`'s gate legs pass it. The Linux leg is owed in #317.
- **An unprovisioned checkout:** the walker refuses with a clear remedy, naming the provisioning command, the way gate 13 grades `BLOCKED`, instead of failing obscurely. That covers terminal runs in the main checkout as well as run copies. _From #478 (2026-11-24):_ the command to name is `bash <scriptsDir>/flow-host-provision.sh`, run outside the sandbox — the same remedy #478's `SKIPPED` line and `doctor`'s `flow-host` check already print.
- **Per-call startup cost** of `uv run` and Python, measured, since a run makes many walker calls.
- ~~**Byte-for-byte output**~~ _Superseded by #465 → **Decided (2026-11-24)**._ The bar is now the wire grammar wherever a caller parses it (`planning-driver-lib.sh`, `planning-node-lib.sh`, `plugin/instructions/task_plan_writing_instructions_core.md`, `user_review_fix_plan_writing_instructions_core.md`): the keys, their order, the exit codes and the actions. Where the host routes better, the host's way wins. Every place the command answers differently is listed for this branch in `devscene-flow-host/README.md` → `## Differences from flow-walker.sh`, together with the `flow-walker*` suite cases that change with it.
- **The v4 graph shipped to adopters:** `cli/src/generators/outerLoopScripts.ts` ships only `task_plan_writing.graph.json` (v3) today. Whether the v4 file ships beside it or replaces it is this branch's choice; anything v3 left after that is #459's.
- **What #465 left for this branch** _From #465's branch (2026-11-24)._
  - **The command is `devscene-flow-walker`.** It takes `flow-walker.sh`'s flags plus one of its own, `--flows <dir>`, the directory holding `<flow>.v4.graph.json`, because it cannot find its graph beside itself as bash does. `flow-walker.sh`'s hand-off passes it. ~~The launch line is `uv run --frozen --no-sync --project devscene-flow-host …`; the console script is installed by `bash scripts/python-service.sh provision`.~~ _Superseded by #478, see **What #478 left for this branch** below._ `bash scripts/python-service.sh run` is still not a route to it.
  - **The suite changes are listed, not left to be rediscovered.** `## Differences from flow-walker.sh` → **Chosen** names each `flow-walker*` case that pins bash's behaviour and has to change. Among them:
    - the other-branch refusal in `flow-walker-ui-and-reentry.test.mjs` (11);
    - the stale-lock cases in `flow-walker-concurrency.test.mjs` (2)–(4), since the command's `flock` locks die with their process;
    - the cause regexes in `flow-walker-fan-out.test.mjs` (5) and (6);
    - `cli/test/helpers/walker.mjs` → `WALKER_GRAPH_PATH`, which points at the v3 graph.
  - **Nothing is still open there** _(from #475, 2026-11-24)_. #472 settled the held-gate escalation. #475 made `current` re-print what its step printed, through a host record `PrintedReadsStore`, and found the third difference (`evidence.open:` under a repeated heading) was never one. The `current` cases (`flow-walker-ui-and-reentry.test.mjs` (4) and (10), `flow-walker-resume.test.mjs` (1), (2) and (4), `flow-walker.test.mjs` (3)) are now expected to hold unchanged. None of them has been run against the command yet.
- **What #478 left for this branch** _From #478's branch (2026-11-24)._
  - **The layout** (every name owned by `cli/src/flowHost/layout.ts`): the packages sit at `<scriptsDir>/python/graphscene/` and `<scriptsDir>/python/devscene-flow-host/`, siblings; the walker's environment is `<scriptsDir>/python/.venv`, separate from the dev `.venv`s `python-service.sh` keeps in each package. In this repository the two package paths are committed relative symlinks to the root `graphscene/` and `devscene-flow-host/`, so the same path resolves here.
  - **The launch line** is `UV_PROJECT_ENVIRONMENT=<scriptsDir>/python/.venv uv run --frozen --no-sync --project <scriptsDir>/python/devscene-flow-host devscene-flow-walker <verb> …`, plus `--no-cache` inside the sandbox. Checked end to end on 2026-11-24 from a packed tarball in a scratch repository: `check-round-file --findings <missing path>` exits `3`.
  - **Provisioning** is `bash <scriptsDir>/flow-host-provision.sh` (library function `hr_flow_host_provision`): `uv sync --frozen --no-dev --no-editable`, outside the sandbox. It is reached from `init --provision-python`, `setup-worktree.sh` step 6 (local run copies and the remote job's `Bootstrap the checkout`), and by hand. Because the packages install as wheels, a merge that changes either package needs a re-provision of the main checkout; `doctor`'s `flow-host` check reports the drift.
  - **Remote jobs:** `devscene-run.yml` (template) carries a pinned `astral-sh/setup-uv` step before the bootstrap, so the job provisions itself; `devscene-control.yml` has none. The job-surfaces check refuses a branch whose commits changed `<scriptsDir>/python/` (here, only the two symlinks), not the root packages.
  - **Write protection:** the main checkout's `<scriptsDir>/python/`, and in this repository the link targets `graphscene/` and `devscene-flow-host/`, are write-protected in the unattended profile.
  - **What #478 left switched off for this branch:** see **Decided (2026-11-24, after #478)** above.

- **A bash-format state file left at cutover** _Raised 2026-11-23; restated after #418 merged (#467)._ The bash walker's state is a flat file at `<stateDir>/.flow_walker_state`. #418 made that path a **directory**: each branch's walk is a `FileStateStore` at `<stateDir>/.flow_walker_state/<quote(branch, safe="")>.json` (`devscene-flow-host/src/devscene_flow_host/host/store.py`). A leftover bash file therefore no longer reaches `FileStateStore.read`'s `ValueError`. Every read and lock under the path raises `NotADirectoryError`, an `OSError` the host propagates unchanged (`store.py` → *"Deliberately not covered"*). A naive mapping turns that into a blocking exit 2. _From #465's branch (2026-11-24):_ that is what the command does today. `commands/flow_walker.py` → `failure` maps every `OSError` to exit `2`, and `next` / `current` read the walk store before anything else, so a leftover flat file blocks them rather than answering *"no saved walk"*. _Seen 2026-11-24 in a run copy:_ with the flat file present, `start` exits `2` with `[Errno 20] Not a directory: …/.flow_walker_state/round_refusals`, and `current` exits `2` the same way on `…/<branch>.json`. It should count as a lost state, so the orchestrator's `current` → exit 1 → `start` recovery runs (#464): ~~the flat file is moved aside or removed~~ the flat file is deleted (decided 2026-11-24), then the walk starts. "A run in progress isn't resumed across state formats" below says what happens, but not how the old file is treated.
- _The lock-path clash raised on 2026-11-23 no longer holds after #418 (#467)._ The Python lock is now `<stateDir>/.flow_walker_state/<branch file>.lock`, inside the directory, so it never meets bash's `<stateDir>/.flow_walker_state.lock` directory, which is a sibling. A stale bash lock directory is left-over debris, not a blocker.
- **Two places still assume the flat file** _From #418 as merged (#467, 2026-11-23); #418's plan handed them to the cutover._
  - Gate 6a's anchored filter `grep -v '^\./harness-runs/\.flow_walker_state:'` (`scripts/check-machine-paths.sh`) does not match the files inside the directory, `./harness-runs/.flow_walker_state/<branch>.json:…`.
  - The remote bundle copies `<state_dir>/.flow_walker_state` as one file, `<bundle>/flow_walker_state` (`cli/templates/scripts/lib/harness-run-lib.sh` → `HR_REMOTE_WALKER_FILE`). A directory needs a recursive copy, or one branch's files: `<branch>.json` and its records under `round_refusals/`, `revision_findings/` and `printed_reads/` (#475). Without `printed_reads/`, `current` falls back to re-reading the files.
  
  The prose that describes the flat file goes with them: `docs/flow-graph-walker.md`'s state and lock *Decision.*s, `docs/remote-execution.md` → **The walker state.** and `cli/templates/scripts/README.md`.

## Leads

_The leads below are starting points from #376 and the discussion that split it, not requirements. The planning session decides what holds when this branch is planned._

- The `flow-walker*` suites pass against the Python walker, needing #411 to run in a run copy.
- `flow-walker.sh` hands off to `devscene-flow-host`'s compatibility command (#465, split out of #418; the package itself is #451, renamed by #455) through `uv run --frozen --no-sync`, perhaps with the bash walker behind a flag for a while. Its callers keep calling `flow-walker.sh` unchanged.
- A run in progress isn't resumed across state formats.
- _Moved to #459 on 2026-11-23: the v3 bridge's retirement, the port of checks 4–7 and the two checkers' comparison._
- _Moved to #478 on 2026-11-24: shipping the Python packages and `uv` to adopters._
- This repo's re-render. _Decided 2026-11-24: a post-merge user step (see above)._

## Depends on

#411, #415, #418, #464, #465, #472, #475, #478
