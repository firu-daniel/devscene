### Task 13 — Rewrite the walker's decisions of record and ship the startup-cost measurement

**Goal:** `docs/flow-graph-walker.md` records the cutover:
- the walker is `devscene-flow-host`'s command behind `flow-walker.sh`'s hand-off;
- its state is a per-branch directory;
- its locks are `flock`s that die with their process;
- the format-4 graph is the one it reads and ships;
- the bash and `jq` floor no longer bounds the walker.

It also gains the per-call startup-cost section the task prompt asks for (*"measure and record, no threshold"*). Following `<state_dir>/lessons.md` → *"A wall-clock figure in a document of record is never one a run measured inside its own session"*, the section ships the measurement commands and a figure slot, and the user fills it by hand. `docs/converging-plan-reviews.md`'s citation of the bash header's `STATE` paragraph is repointed, because Task 1 removes that paragraph.

**Depends on:**
- **Task 1.** The hand-off launches `UV_PROJECT_ENVIRONMENT=<scriptsDir>/python/.venv uv run --frozen --no-sync --no-cache --project <scriptsDir>/python/devscene-flow-host devscene-flow-walker …` with `--flows <scriptsDir>/flows`. It refuses an unprovisioned checkout with exit `2` naming `bash <scriptsDir>/flow-host-provision.sh`. It deletes a leftover flat state file. Its header keeps `USAGE`, `ROUNDS`, `A REFUSED ROUND FILE`, `OUTPUT` and `EXIT CODES`, and drops `STATE`, `CONCURRENCY` and the bash floors.
- **Task 6.** The planning driver runs the main checkout's walker.

### Targets

- `docs/flow-graph-walker.md`:
  - `### Item 3a — walker state is machine-local, and a re-entry continues it`;
  - `### Item 6 — the walker and graph ship into scriptsDir, and the graph is found beside the walker`;
  - `### Item 8 — a round's gates fan out, and the round node joins` (its lock and mechanics sentences);
  - `### Item 9 — a round file is checked before its verdict is recorded` (its `fw_round_file_check` citation);
  - `### The runtime — bash 3.2 and jq 1.5`;
  - a new per-call startup section.
- `docs/converging-plan-reviews.md` — the *"`cli/templates/scripts/flow-walker.sh` → the header's `STATE` paragraph"* citation.

**Work:**

- [ ] Items 3a and 8: write the state's new **Decision.**
  - the walk is `<state_dir>/.flow_walker_state/<percent-encoded branch>.json`, with its records in subdirectories;
  - a different branch is never refused;
  - a leftover flat file from the bash walker is deleted and the walk starts fresh (task prompt, decided 2026-11-24).

  Replace the lock sentence (*"`start` and `next` hold the lock `<state_dir>/.flow_walker_state.lock`"*) with the two `flock`s in `RefusalStore`-then-walk order. Repoint *"The mechanics are `flow-walker.sh` → `ROUNDS`, `OUTPUT`, `STATE` and `CONCURRENCY`"* to the header sections Task 1 keeps, plus `devscene-flow-host/README.md` → `## What it reads, answers and keeps`. Keep each item's existing **Decision.** / **Reason.** shape, and record the change with this branch's date rather than rewriting history silently.
- [ ] Item 6 and Item 9:
  - **Item 6:** `flow-walker.sh` and `flows/task_plan_writing.v4.graph.json` ship into `scriptsDir`, and the hand-off passes that directory as `--flows`; the format-3 graph still ships for the planning driver's node list, until #459; `lib/flow-walker-gates.sh` no longer ships;
  - **Item 9:** the round-file check is now `devscene-flow-host/src/devscene_flow_host/records/round_files.py` → `round_file_problem`, which reads as the retired `fw_round_file_check` did.
- [ ] `### The runtime — bash 3.2 and jq 1.5`: add a dated **Superseded.** paragraph. The walker is Python run through `uv`. The hand-off itself stays bash-3.2-safe and needs `jq` only through `lib/harness-run-lib.sh`'s `stateDir` read. A host without `uv` is refused by the walker, failed by `doctor` and failed at `setup-worktree.sh` step 6. A run's planning driver runs the main checkout's walker, because the driver runs unsandboxed (Task 6).
- [ ] New section *"Per-call startup cost"*:
  - **what is measured:** the wall-clock time of one walker call whose work is negligible — `check-round-file` on a path that does not exist — so the figure is the hand-off, `uv run` and Python start-up;
  - **the commands,** each in its own fenced block, one per line: `time bash scripts/flow-walker.sh check-round-file --findings harness-runs/no-such-review.md`, run ten times, plus `uv --version`;
  - **how to read it:** the median of the ten `real` figures, the `uv` version, the host and the date; no threshold, because the cutover was decided whatever the figure (task prompt);
  - **a slot** reading *"Not yet measured — taken by hand after this branch merges and this repository is re-rendered, outside any headless session, on an otherwise idle machine"*.

  Fill no figure.
- [ ] `docs/converging-plan-reviews.md`: point the citation at `devscene-flow-host/README.md` → `## What it reads, answers and keeps` → **Resuming a round.**, which states the same counter-versus-round-number rule for the command.

**Verification:**

- `git grep -n -e 'flow_walker_state\.lock' -e 'flow-walker-gates' -e "header's \`STATE\`" -- docs/flow-graph-walker.md docs/converging-plan-reviews.md` prints only lines that are explicitly dated history or **Superseded.** text.
- The measurement section carries no figure, and every command in it sits in its own fenced block (`<state_dir>/lessons.md` → *"Every command an adopter is meant to run sits in a fenced block"*).
