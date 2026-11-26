### Task 5 — Document the executor in `devscene-flow-host/README.md` and the package docstring

**Goal:** Make the package's own documentation say what this branch added. The flow host now holds the harness's `claude` executor, not only executor configuration: the README's statement of what the package is, its layers table and a new `## The executor` section, and the package root's docstring.

**Depends on:** Task 4, which ships these, as named:

- `ClaudeExecutor` in `src/devscene_flow_host/host/claude_executor.py`, with `SessionUsage`, `UsageSink`, `NODE_INACTIVITY_LIMIT_SECONDS` (2685.0) and `KILL_GRACE_SECONDS`;
- `judge_session` in `host/session_stream.py` (Task 2);
- `run_session` in `host/session_process.py` (Task 3);
- `read_agent_contract`, `read_plugin_name` and `AgentContract` in `records/plugin_contracts.py` (Task 1).

This task documents those names and the rules their module docstrings state, and changes no code. Each docstring's *"The rule:"* paragraph is the source; the README restates no rule a docstring does not hold.

### Targets

- `devscene-flow-host/README.md`
- `devscene-flow-host/src/devscene_flow_host/__init__.py`: the module docstring only

**Work:**

- [ ] `README.md` → `## What it is`: replace "configuration, records, predicates, executor configuration and hooks" with wording that says the package holds the harness's executor, `ClaudeExecutor`, which runs each dispatched node as one headless `claude` session. Add one sentence saying that nothing in production calls it until the run loop (#484) and the planning cutover (#424). This is scope-register row 4.
- [ ] `README.md` → `## The layers`: in the `host` row, add `judge_session` (`host/session_stream.py`), `run_session` (`host/session_process.py`) and `ClaudeExecutor`, `UsageSink` and `SessionUsage` (`host/claude_executor.py`). In the `records` row, add `read_plugin_name`, `read_agent_contract` and `AgentContract` (`records/plugin_contracts.py`). This is scope-register row 7. Leave the import rule text unchanged: no contract changes.
- [ ] `README.md`, a new `## The executor` section after `## What it reads, answers and keeps`. It covers:
  - what the constructor takes and from whom;
  - the flags the executor adds, and that it refuses host flags that carry them;
  - the classification order with each `Failed` class;
  - the two departures from `PNL_REAP_JQ`;
  - `findings_file` becoming an absolute `detail`;
  - the inactivity limit's value and where it comes from;
  - group kill on stall and on cancellation;
  - the usage sink's once-before-return rule and the pairing it gives the host.

  It states the measured fact that `--json-schema` is not applied under `--agent` the way `.claude/context/conventions.md` → `## Documents of record` requires a measured fact to be stated: what was measured, the version (Claude Code 2.1.332, 2026-11-26), the command (`claude -p --output-format stream-json --verbose --model haiku` with `--plugin-dir <plugin> --agent devscene:prompt-injection-reviewer --json-schema <its return schema>`), and the observation (no `StructuredOutput` tool in the `init` tools, and no `structured_output` key on the `result` event). It quotes no wall-clock figure (`harness-runs/lessons.md` → *"A wall-clock figure in a document of record is never one a run measured inside its own session"*).
- [ ] `src/devscene_flow_host/__init__.py`: in the docstring's first paragraph, replace "executor configuration" with the harness's executor, as in the README's `## What it is`. Leave the rule paragraphs and `__all__` unchanged.

**Verification:**

- Re-run the story index's two scope-register derivation commands. `git grep -n "executor configuration" -- '*.md' ':!harness-runs' ':!examples'` must report no hit under `devscene-flow-host/`. Its remaining hits must all be rows the register lists as `no-change`. `git grep -n "host/walking.py" -- '*.md' ':!harness-runs' ':!examples'` must report no site that is not a register row.
- Every name the README adds resolves to a definition in the module it cites: grep each module for the name.
- `bash scripts/typecheck.sh` reports nothing in `src/devscene_flow_host/__init__.py`.
