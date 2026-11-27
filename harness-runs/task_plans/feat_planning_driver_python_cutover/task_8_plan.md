### Task 8 — Remove the issue numbers from GraphScene's run loop, set execution and command line

**Goal:** As the task prompt decides, *"When this branch completes, no code in `graphscene/` or `devscene-flow-host/` mentions an issue number."* The three GraphScene sites lose their number. Each sentence keeps what it says.

**Where this task stops.** GraphScene's sites only. The `devscene-flow-host` sites are **Task 22's** (source and tests) and **Task 23's** (README). Behaviour does not change: these are docstring edits.

### Targets

- `graphscene/src/graphscene/engine/run_loop.py` — *"An inactivity timeout: the executor's (#421)."*
- `graphscene/src/graphscene/engine/set_execution.py` — *"… returns that stall as `Failed("infra", …)` (#421)."*
- `graphscene/src/graphscene/facade/cli.py` — *"DevScene's `key: value` wire, which is #418's."*

**Work:**

- [ ] `run_loop.py`: *"An inactivity timeout: the executor's."*
- [ ] `set_execution.py`: drop ` (#421)`. The sentence already says the executor detects the stall.
- [ ] `facade/cli.py`: *"DevScene's `key: value` wire, which is its flow host's command's."* The flow host stays unnamed, so GraphScene still names no harness module (`.claude/context/graphscene.md` → `## What it may depend on`).

**Verification:**

- `git grep -nE '#[0-9]+' -- graphscene` prints nothing.
- `git grep -n devscene -- graphscene/src/graphscene/facade/cli.py` prints no new `devscene`-prefixed name. The boundary test's forbidden literal is not introduced.
- `commands.typecheck` exits zero. Its `ruff` and `mypy` legs cover the three edited docstrings.
