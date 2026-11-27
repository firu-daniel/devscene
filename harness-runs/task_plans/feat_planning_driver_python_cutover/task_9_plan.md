### Task 9 — Read the planning core's dispatch cap and a branch's highest question index as records

**Goal:** Add two record readers the driver needs, each read the way the bash reader of that record reads it:
- `read_max_total_dispatches(plugin_dir)`, the `MAX_TOTAL_DISPATCHES` the planning core's `## Setup (once per session)` declares, as `pnl_init` reads it;
- `max_question_index(repo_root, state_dir, branch)`, the highest `question_<n>.md` index under the branch's clarification directory, as `hr_max_question_index` reads it.

**Where this layer stops.** The readers return values and decide nothing (`.claude/context/devscene-flow-host.md` → `## Records, and which one is the truth`). Using the cap as `ExecutionLimits.dispatch_cap` is **Task 12's** and **Task 16's**. Writing a park at `max + 1` is **Task 10's**.

### Targets

- `devscene-flow-host/src/devscene_flow_host/records/core_limits.py` (new)
- `devscene-flow-host/src/devscene_flow_host/records/clarifications.py` — `max_question_index`
- `devscene-flow-host/tests/test_core_limits.py` (new)
- `devscene-flow-host/tests/test_clarifications.py` — the new reader's cases

**Work:**

- [ ] `records/core_limits.py`:
  - **Constants.** `Final` constants `CORE_DOCUMENT = "instructions/task_plan_writing_instructions_core.md"`, `SETUP_HEADING = "## Setup (once per session)"` and `MAX_DISPATCHES_MARKER = "MAX_TOTAL_DISPATCHES = "`.
  - **`read_max_total_dispatches(plugin_dir: Path) -> int`.** It reads as the retired `pnl_init` did: under the setup heading only, up to the next `## ` heading, the first line containing the marker, then the run of digits after it, as a base-10 int.
  - **Errors.** `RecordError` messages are each one line naming the file:
    - a missing core: `the planning core '<path>' does not exist`;
    - non-UTF-8: `<path>: not UTF-8 text`;
    - no marker under the heading: `no 'MAX_TOTAL_DISPATCHES = <n>' line under '## Setup (once per session)' in '<path>'`.
  - **Docstring.** It carries *"The rule:"* naming `pnl_init` as the reader it reads as, plus *"Deliberately not covered"*. That section covers using the value, and the reader that cuts the prompt blocks, which is `records/prompt_blocks.py`'s.
- [ ] `records/clarifications.py`: add `max_question_index(repo_root, state_dir, branch) -> int`.
  - It returns the highest `n` of a regular file named `question_<n>.md` directly in `<state_dir>/clarifications/<branch>/`, reusing the module's `_QUESTION_NAME` pattern, or `0` when there is none or the directory is absent. Sub-directories such as `answered/` are not read, as `hr_max_question_index` reads only the top level.
  - Extend the module docstring's rule.
- [ ] `tests/test_core_limits.py`:
  - header *"The rule this file exists to enforce"*;
  - one case per clause: the value read; a marker outside the setup section ignored; each of the three `RecordError` texts asserted exactly; a value with leading zeros read base-10;
  - one case reading the real `plugin/instructions/task_plan_writing_instructions_core.md` read-only, asserting the literal `40` written from reading that file.
- [ ] `tests/test_clarifications.py`: cases for `max_question_index`:
  - no directory gives `0`;
  - `question_1.md` and `question_3.md` give `3`;
  - a `question_9.md` under `answered/` is not counted;
  - a non-matching name is ignored.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_core_limits.py` passes.
- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_clarifications.py` passes.
- `records/core_limits.py` imports no `graphscene` (the `devscene-flow-host-graphscene-outside-records` contract).
