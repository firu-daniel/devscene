### Task 1 — Hand `flow-walker.sh` to `devscene-flow-walker`, ship the format-4 graph and retire the gate library

**Goal:** Replace the bash walker's body in `cli/templates/scripts/flow-walker.sh` with a hand-off to `devscene-flow-host`'s compatibility command. Ship `flows/task_plan_writing.v4.graph.json` into `scriptsDir` beside the walker. Retire `lib/flow-walker-gates.sh` from the template tree and from the shipped table.

**Where this task stops.** This task owns the hand-off script and the shipped set. It does **not** edit any test file:
- Task 2 points the walker-driving helpers at this hand-off.
- Task 3 updates `cli/test/outer-loop-scripts.test.mjs` → `WALKER_FILES` to the shipped set this task leaves.
- Task 7 moves the suite cases that pinned bash.
- Task 8 adds the suite for the hand-off's own contract.

It does not touch this repository's self-adopted `scripts/flow-walker.sh`, `scripts/lib/flow-walker-gates.sh` or `scripts/flows/`: the user re-renders those after merge (story index `## Context`).

### Targets

- `cli/templates/scripts/flow-walker.sh` — rewritten as the hand-off.
- `cli/templates/scripts/lib/flow-walker-gates.sh` — deleted.
- `cli/src/generators/outerLoopScripts.ts` — `OUTER_LOOP_SCRIPTS`: the format-4 graph row added and the gate-library row removed; the module header's set description.

**The interface this task defines, which Tasks 2, 6 and 8 restate:**

- **Environment and project.** The environment is `DEVSCENE_FLOW_HOST_ENV` when set and non-empty, else `<this script's dir>/python/.venv`. The project is `DEVSCENE_FLOW_HOST_PROJECT` when set and non-empty, else `<this script's dir>/python/devscene-flow-host`. Both are absolute paths once resolved.
- **The unprovisioned refusal.** The hand-off exits `2` with exactly one stderr line, nothing on stdout, and runs nothing, when any of these holds: `uv` is not on `PATH`; `<env>/pyvenv.cfg` is absent; `<env>/bin/devscene-flow-walker` is not executable. The line opens `flow-walker: ` and names the command `bash <scriptsDir>/flow-host-provision.sh`, with the words `outside the sandbox`. `<scriptsDir>` is the walker's own directory as given. This is the remedy #478's `SKIPPED` line and `doctor`'s `flow-host` check already print, so the advice and the refusal share one predicate (`<state_dir>/lessons.md` → *"A remedy never sends an adopter to a place the CLI refuses"*).
- **The leftover bash state file.** For `start`, `next` and `current` only, the hand-off resolves the root with `hr_repo_root` and `stateDir` with `hr_state_dir`, both from `lib/harness-run-lib.sh`. It then deletes `<root>/<stateDir>/.flow_walker_state` when that path is a regular file and not a symbolic link, and prints nothing about it. If either value does not resolve, it deletes nothing and leaves the cause to the command.
- **An old library.** A `lib/harness-run-lib.sh` that cannot be sourced, or defines no `hr_repo_root` or `hr_state_dir`, is refused with exit `2` and the existing words `flow-walker: <file> predates this walker`. This happens before anything else runs, and for every verb except `check-round-file`, which needs no library.
- **The launch.** The script unsets `VIRTUAL_ENV`, then runs `UV_PROJECT_ENVIRONMENT=<env> exec uv run --frozen --no-sync --no-cache --project <project> devscene-flow-walker "$@"`. It appends `--flows <this script's dir>/flows` for `start`, `next` and `current` only, because `check-round-file` refuses a flag it does not take. Every other argument is passed through unchanged, and the command's stdout, stderr and exit status are the caller's answer.

**Work:**

- [ ] `flow-walker.sh` body:
  - resolve its own directory from `${BASH_SOURCE[0]}`;
  - source `lib/harness-run-lib.sh` from beside itself and apply the old-library refusal above, for every verb but `check-round-file`;
  - delete the leftover flat state file for `start` / `next` / `current`;
  - apply the unprovisioned refusal;
  - launch as above.

  Keep the body bash-3.2-safe under `set -u`: an empty `--flows` array must expand without an unbound-variable error, as in `${flows[@]+"${flows[@]}"}`. No `jq` call, no graph read and no state write remain in the script.
- [ ] `flow-walker.sh` header. Keep the caller-facing sections that callers cite by name — `USAGE`, `ROUNDS`, `A REFUSED ROUND FILE`, `OUTPUT` and `EXIT CODES` (`cli/templates/scripts/lib/planning-driver-lib.sh` cites *"`flow-walker.sh`'s own `ROUNDS`, `OUTPUT`, `EXIT CODES`"*) — restated to what the command does:
  - `EXIT CODES` lists exit `1` and exit `2` as `devscene-flow-host/README.md` → `## The command line` does, plus this script's own exit-`2` refusals;
  - `ROUNDS` takes the held-gate order from `## Differences from flow-walker.sh` → **The held-gate escalation.**;
  - the graph is `<this script's dir>/flows/<flow>.v4.graph.json`.

  Replace `STATE`, `CONCURRENCY` and `BASH 3.2 AND JQ 1.5 ARE THE FLOORS` with a `HAND-OFF` section. It states the launch line, the two variables and why they exist (a caller that names the environment and project explicitly — the `cli` suites over the branch's own sources), why `--no-cache` is always passed, the leftover-file deletion, and that the walk's state, locks and records are the command's, pointing at `devscene-flow-host/README.md` → `## What it reads, answers and keeps`. Close with a `REPRO` block, run in a throwaway fixture, for: a provisioned `start`; the unprovisioned refusal; `check-round-file` with a missing file (exit `3`); and a planted flat state file removed by `current`.
- [ ] Delete `cli/templates/scripts/lib/flow-walker-gates.sh`. Its readers are ported into `devscene-flow-host/src/devscene_flow_host/records/round_files.py`, `records/round_evidence.py` and `records/index_evidence.py`, and pinned by `devscene-flow-host/tests/test_round_files.py`, `test_round_evidence.py` and `test_index_evidence.py`.
- [ ] `outerLoopScripts.ts` → `OUTER_LOOP_SCRIPTS`:
  - remove the `flow-walker-gates.sh` row and its comment;
  - add `Object.freeze({ file: 'task_plan_writing.v4.graph.json', subdir: 'flows', mode: 0o644, agentInvocable: false })` before the `flow-walker.sh` row, with a comment saying the hand-off passes this directory as `--flows`;
  - reword the format-3 row's comment: it stays shipped because `lib/planning-node-lib.sh` and `lib/planning-driver-lib.sh` read its node list, and its retirement is #459's.

  Update the module header's list (*"the flow walker with its gate library and flow graph"*) to the new set. No `cli/src/core/writer.ts` row is owed: its row *"The outer-loop scripts and their `lib/` files"* already covers every `OUTER_LOOP_SCRIPTS` file, the format-3 graph included.

**Verification:**

- Run `commands.typecheck`; it must exit 0.
- In a throwaway `git init` fixture under the system temp directory, run `init` against the built CLI and confirm:
  - `scripts/flows/task_plan_writing.v4.graph.json` landed byte-identical to the template, with mode `0644`;
  - `scripts/lib/flow-walker-gates.sh` was not written.
- Walk the header's `REPRO` block in that fixture. To get a provisioned environment there, set `DEVSCENE_FLOW_HOST_ENV` to this checkout's provisioned `scripts/python/.venv` and `DEVSCENE_FLOW_HOST_PROJECT` to this checkout's `devscene-flow-host`. Each outcome must print what the block says:
  - `start` prints an `action: dispatch` block;
  - an empty `DEVSCENE_FLOW_HOST_ENV` directory gives exit `2` and the remedy line;
  - `check-round-file` on a missing path exits `3` with no `--flows` error;
  - a planted flat `<stateDir>/.flow_walker_state` makes `current` exit `1` with `no walk in progress at …`, and leaves the path absent.
- `git grep -n 'flow-walker-gates' -- cli/src cli/templates` prints only the deleted file's mentions in Task 9's READMEs, which Task 9 owns.
