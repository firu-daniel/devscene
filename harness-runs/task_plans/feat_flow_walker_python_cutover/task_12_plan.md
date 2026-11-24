### Task 12 — Widen gate 6a's walker-state filter to the per-branch directory

**Goal:** Gate 6a's anchored filter in `scripts/check-machine-paths.sh` drops the hits inside the Python walker's state directory, `./harness-runs/.flow_walker_state/<file>:…`, as well as the bash walker's flat file `./harness-runs/.flow_walker_state:…`. The task prompt names this as one of *"Two places still assume the flat file"*. The flat file stays covered because this repository's self-adopted `scripts/flow-walker.sh` is the bash walker until the post-merge re-render (story index `## Context`).

**Depends on:** Task 1, whose hand-off makes `<state_dir>/.flow_walker_state` a directory whose `revision_findings/` records keep findings paths as the orchestrator passed them, absolute ones included. That is the reason the filter exists.

### Targets

- `scripts/check-machine-paths.sh` — the third `grep -v` and the header paragraph `THE WALKER-STATE FILTER.` (hand-written; not an `init` output).
- `docs/development.md` → gate 6a's paragraph, the sentence on *"the third anchored `grep -v`"*.

**Work:**

- [ ] `check-machine-paths.sh`: replace `grep -v '^\./harness-runs/\.flow_walker_state:'` with one anchored filter that matches exactly two shapes: `./harness-runs/.flow_walker_state:<line>:` and `./harness-runs/.flow_walker_state/<path without a colon>:<line>:`. For example, `grep -v '^\./harness-runs/\.flow_walker_state\(/[^:]*\)\{0,1\}:'`, written in basic regex so both GNU and BSD `grep` read it alike. A same-named path anywhere else, such as under `examples/notes-app/devscene/`, is still printed. Rewrite the header paragraph: it now names the per-branch directory, and points its *"machine-local"* citation at `devscene-flow-host/README.md` → `## What it reads, answers and keeps` instead of `scripts/flow-walker.sh`'s `STATE —` header.
- [ ] `docs/development.md` gate 6a: rewrite the sentence so it states the two shapes the third filter drops, and why both: the directory now, and the flat file until this repository's re-render. Point its citation away from `scripts/flow-walker.sh`'s `STATE —` header, as above.

**Verification:**

- In a throwaway directory under the system temp directory, plant `harness-runs/.flow_walker_state/feat_x.json`, `harness-runs/.flow_walker_state/revision_findings/feat_x.json`, a flat `harness-runs/.flow_walker_state` in a second copy, and `examples/notes-app/devscene/.flow_walker_state`, each holding the value of `$HOME`. Run `bash <this checkout>/scripts/check-machine-paths.sh` there. Only the `examples/notes-app/…` hit is printed.
- `git grep -n 'STATE —' -- scripts/check-machine-paths.sh docs/development.md` prints nothing.
