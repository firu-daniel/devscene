### Task 9 — Describe the hand-off in the `cli` package's own READMEs

**Goal:** The `cli` package's prose says what Tasks 1 and 3 made true. `flow-walker.sh` is a hand-off to `devscene-flow-walker`. The gate library is gone. `flows/task_plan_writing.v4.graph.json` is written into `scriptsDir` beside the format-3 graph. The walker's state is a per-branch directory at `<state_dir>/.flow_walker_state/`.

**Depends on:** Task 1 (the hand-off and the shipped set) and Task 3 (`hr_flow_host_provision` now fails without `uv` or a project). This task restates only what those files now do, and changes no behaviour.

### Targets

- `cli/templates/scripts/README.md` — the paragraph opening *"The other family in this directory is not generated."*
- `cli/templates/README.md` — the paragraph opening *"One file here is not written by `init`"*.
- `cli/README.md` — the shipped-script list naming *"the flow walker (`flow-walker.sh`) and its gate library (`lib/flow-walker-gates.sh`)"*.

**Work:**

- [ ] `cli/templates/scripts/README.md`:
  - in the shipped-family list, replace *"the flow walker `flow-walker.sh` with its gate library `lib/flow-walker-gates.sh` and the planning flow's graph `flows/task_plan_writing.graph.json`"* with: the walker `flow-walker.sh`, which hands each call to `devscene-flow-walker` in `<scriptsDir>/python/.venv`; its graph `flows/task_plan_writing.v4.graph.json`; and the format-3 graph `flows/task_plan_writing.graph.json` the planning driver reads;
  - replace the sentence that says the format-4 file *"is **not** written into `scriptsDir`"*;
  - make *"keeps machine-local state at `<state_dir>/.flow_walker_state`"* the per-branch directory;
  - in the `flow-host-provision.sh` sentence, add that `setup-worktree.sh`'s step 6 now fails a bootstrap with no `uv` or no project.
- [ ] `cli/templates/README.md`: the format-4 graph is now written by `init`. Drop the paragraph's claim, keeping any other file it names.
- [ ] `cli/README.md`: drop the gate library from the list, and add the format-4 graph.

**Verification:**

- `git grep -n -e 'flow-walker-gates' -e 'not\*\* written into' -- cli/README.md cli/templates/README.md cli/templates/scripts/README.md` prints nothing.
- Every command these READMEs hand a reader still sits in its own fenced block, one per line (`<state_dir>/lessons.md` → *"Every command an adopter is meant to run sits in a fenced block"*).
