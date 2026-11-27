### Task 9 — Read the planning core's dispatch cap, a branch's highest question index and the configured `scriptsDir` as records

**Goal:** Add the record reads the driver needs, each read the way the bash reader of that record reads it:
- `read_max_total_dispatches(plugin_dir)`, the `MAX_TOTAL_DISPATCHES` the planning core's `## Setup (once per session)` declares, as `pnl_init` reads it;
- `max_question_index(repo_root, state_dir, branch)`, the highest `question_<n>.md` index under the branch's clarification directory, as `hr_max_question_index` reads it;
- `HarnessConfig.scripts_dir`, the `scriptsDir` key of `devscene.config.json`, read by the existing `read_config` as `hr_scripts_dir` reads it (through `hr_config_dir`, after `hr_config_load`).

**Where this layer stops.** The readers return values and decide nothing (`.claude/context/devscene-flow-host.md` → `## Records, and which one is the truth`). Using the cap as `ExecutionLimits.dispatch_cap` is **Task 12's** and **Task 16's**. Writing a park at `max + 1` is **Task 10's**. Building the commit wrapper's path `<main_repo>/<scripts_dir>/commit-on-branch.sh` from `scripts_dir` is **Task 16's**; this task reads the value only.

### Targets

- `devscene-flow-host/src/devscene_flow_host/records/core_limits.py` (new)
- `devscene-flow-host/src/devscene_flow_host/records/clarifications.py` — `max_question_index`
- `devscene-flow-host/src/devscene_flow_host/records/config.py` — `HarnessConfig.scripts_dir`, `DEFAULT_SCRIPTS_DIR`, and the docstring's rule
- `devscene-flow-host/tests/test_core_limits.py` (new)
- `devscene-flow-host/tests/test_clarifications.py` — the new reader's cases
- `devscene-flow-host/tests/test_config.py` — the `scriptsDir` cases

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
- [ ] `records/config.py` and `tests/test_config.py`: read `scriptsDir`.
  - **The value.** `HarnessConfig` gains `scripts_dir: str`, repo-relative with no trailing `/`, set by a `_scripts_dir(document, path)` that reads as `_state_dir` does and as `hr_scripts_dir` → `hr_config_dir` reads: an absent or `null` key is `DEFAULT_SCRIPTS_DIR`; every trailing `/` is stripped; a value left empty after stripping is `DEFAULT_SCRIPTS_DIR`.
  - **The constant.** `DEFAULT_SCRIPTS_DIR: Final = "devscene-scripts"`, commented as the schema's default `devscene-scripts/`, normalised as `hr_config_dir` normalises it.
  - **Its unreadable shape.** A `scriptsDir` that is not a string is `RecordError(f"{path}: scriptsDir is not a string")`.
  - **The docstring.** The rule's *"`read_config` reads two keys, `stateDir` and `phases`"* becomes three keys, adding *"`scriptsDir` as `hr_scripts_dir`"* to the list of bash readers. *"Deliberately not checked"* gains *"Whether `scriptsDir` is a safe repo-relative path, which is the schema's"*. Nothing else in the module changes.
  - **The cases**, in `tests/test_config.py`, one per shape: an absent `scriptsDir` and a `null` one each give `devscene-scripts`; `"tools/scripts/"` gives `tools/scripts`; `"//"` gives `devscene-scripts`; a non-string's `RecordError` text asserted exactly; and the existing full-configuration case asserting `scripts_dir` too.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_core_limits.py` passes.
- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_clarifications.py` passes.
- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_config.py` passes, every existing case unchanged but the full-configuration one.
- `records/core_limits.py` imports no `graphscene` (the `devscene-flow-host-graphscene-outside-records` contract).

**Deviations from plan:**
- Plan said `max_question_index` reads only the top level, "as `hr_max_question_index` reads only the top level", and asked for a case asserting a `question_9.md` under `answered/` is not counted. `cli/templates/scripts/lib/harness-run-lib.sh` → `hr_max_question_index` globs `"$clar_dir"/question_*.md "$clar_dir"/answered/question_*.md` and its comment says "top level and answered/ together"; this layer's conventions require reading as the bash reader does. Implemented as top level plus `answered/`, and the case asserts `answered/question_9.md` gives `9`. This also keeps Task 10's park at `max + 1` from reusing an archived pair's index.
- Plan said "a regular file named `question_<n>.md`"; the bash reader tests `[ -e "$q" ]`, so any entry that resolves counts (a dangling symlink does not). Implemented as `exists()`.
- An extra `max_question_index` case reads a zero-padded `question_010.md` as `10`, per the bash reader's forced base 10.
