### Task 11 — Record the launch route and the retired bash walker in `devscene-flow-host`

**Goal:** `devscene-flow-host`'s README and the two module docstrings that defer to #419 state what the cutover settled:
- callers reach `devscene-flow-walker` through `flow-walker.sh`'s hand-off;
- the bash walker is retired;
- a leftover flat `<stateDir>/.flow_walker_state` is deleted by the hand-off before the command runs.

The bash function names cited across this package's docstrings stay as provenance. One README sentence says they name the retired walker's functions, which are readable in the history of `cli/templates/scripts/flow-walker.sh` and `cli/templates/scripts/lib/flow-walker-gates.sh` before this branch merged. No docstring is rewritten for that.

**Depends on:** Task 1, whose hand-off:
- launches `UV_PROJECT_ENVIRONMENT=<scriptsDir>/python/.venv uv run --frozen --no-sync --no-cache --project <scriptsDir>/python/devscene-flow-host devscene-flow-walker …`;
- passes `--flows <scriptsDir>/flows` to the walk verbs;
- names the environment and project through `DEVSCENE_FLOW_HOST_ENV` / `DEVSCENE_FLOW_HOST_PROJECT` when set;
- refuses an unprovisioned checkout with exit `2`;
- deletes a regular file at `<stateDir>/.flow_walker_state` for `start`, `next` and `current`.

Also Task 7, which moved the suite cases `## Differences from flow-walker.sh` named.

**Where this task stops.** No behaviour change in this package. Only docstrings change under `src/`. Where the conventions document's rules are falsified, the story's return records it as `stale-rule` entries; this task does not touch any `.claude/context/` file.

### Targets

- `devscene-flow-host/README.md`:
  - `## What it is`;
  - `## The command line`, its closing paragraph *"How an adopter launches it is #419's"*;
  - `## What it reads, answers and keeps` → **The walk.**;
  - `## Differences from flow-walker.sh`, its `**Who reads this:**` line and **The walk's state.** entry. The heading text stays byte-identical, because `.claude/context/devscene-flow-host.md` cites it.
- `devscene-flow-host/src/devscene_flow_host/commands/flow_walker.py` — the module docstring's *"Deliberately not covered"* list.
- `devscene-flow-host/src/devscene_flow_host/host/store.py` — the module docstring's *"Deliberately not covered"* item on the flat file.

**Work:**

- [ ] README `## The command line`: replace *"How an adopter launches it is #419's."* with the launch route — every caller runs `bash <scriptsDir>/flow-walker.sh <verb> …`, which hands off with the line above — and keep the existing fenced launch commands for this repository. In `## What it is`, say the command is reached through `flow-walker.sh`, which no longer carries a bash walker.
- [ ] README **The walk.**: replace *"The bash walker's own state, a flat file at that same path, is not this package's."* with: a flat file there, left by the retired bash walker, is deleted by `flow-walker.sh` before this command runs, and the walk starts fresh through the caller's `current` → exit 1 → `start`.
- [ ] README `## Differences from flow-walker.sh`:
  - rewrite the `**Who reads this:**` line: a record of how the command answers differently from the bash walker #419 retired, and which `cli/test/flow-walker*.test.mjs` cases #419 changed for each — every listed suite move is now done;
  - add the sentence on docstring citations of bash function names;
  - **Chosen** entries stay as the record.
- [ ] Docstrings:
  - `commands/flow_walker.py`: *"The launch route and `uv`: #419's."* becomes *"The launch route and `uv`: `cli/templates/scripts/flow-walker.sh`'s."*; the flat-file item becomes *"A flat bash state file at `<stateDir>/.flow_walker_state`: `flow-walker.sh` deletes it before this command runs."*;
  - `host/store.py`'s flat-file item keeps that this package lets the `OSError` propagate, and adds that `flow-walker.sh` removes such a file first.

**Verification:**

- Run `commands.typecheck`; it must exit 0.
- `git grep -n "#419's" -- devscene-flow-host` prints nothing.
- `git grep -n '## Differences from flow-walker.sh' -- devscene-flow-host/README.md .claude/context` still shows the heading and its two citations, byte-identical.
