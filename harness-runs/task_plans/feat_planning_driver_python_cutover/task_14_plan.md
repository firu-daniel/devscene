### Task 14 — Build the session args, per-agent MCP flags and session environment in `host/agent_flags.py`

**Goal:** Build the three inputs `ClaudeExecutor` takes from the host, as the task prompt's leads give them:
- `session_args`: the watcher's shared flags passed through unchanged, plus `--add-dir <plugin_dir>` unless the shared vector already carries it;
- `agent_args`: each agent's MCP flags as `pnl_agent_flags` built them;
- `env`: the session environment.

The environment is the driver's own, minus the variables the flow host's `uv` launch adds, so no node session inherits the flow host's Python environment. That is the story index's second `Top risks:` entry.

**Where this task stops.** It builds values. Constructing `ClaudeExecutor` with them is **Task 16's**. The `ClaudeExecutor` constructor refuses a host flag it sets itself (`EXECUTOR_FLAGS`), so nothing here passes one.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/agent_flags.py` (new)
- `devscene-flow-host/tests/test_agent_flags.py` (new)

**Work:**

- [ ] **`session_args(shared: Sequence[str], plugin_dir: Path, *, plugin_dir_added: bool) -> tuple[str, ...]`.** It returns `shared` unchanged, followed by `--add-dir <plugin_dir>` unless `plugin_dir_added`. A token of `shared` that is an `EXECUTOR_FLAGS` member, bare or as `<member>=`, raises `ValueError` naming it, before any session.
- [ ] **`agent_args(contracts: Mapping[str, AgentContract], worktree: Path, scratch: Path) -> dict[str, tuple[str, ...]]`.** It reads each agent's declared `tools` off its `AgentContract`, as `records/plugin_contracts.py` reads them.
  - **No server named.** When no tool matches `mcp__<server>__…`, the agent's args are `("--disallowedTools", "mcp__*")`.
  - **Servers named.** Otherwise they are `("--strict-mcp-config", "--mcp-config", "<scratch>/mcp-<agent>.json")`.
    - The file holds `{"mcpServers": {…}}`: the worktree's `.mcp.json` `mcpServers`, cut to the named servers.
    - When there is no `.mcp.json`, the file holds `{"mcpServers": {}}`.
    - A `.mcp.json` that is not a JSON object is a `RecordError` naming it.
- [ ] **`session_env(environ: Mapping[str, str], *, venv: Path | None) -> dict[str, str]`.** It returns `environ` without `VIRTUAL_ENV`, `UV_PROJECT_ENVIRONMENT`, `PYTHONPATH`, `PYTHONDONTWRITEBYTECODE` and `PYTHONHOME`, the `FLOW_HOST_LAUNCH_VARIABLES` `Final` tuple. When `venv` is given, the `PATH` entries equal to `<venv>/bin` are removed. Every other variable, `DEVSCENE_MAIN_REPO` and `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS` among them, is kept.
- [ ] **Module docstring.** *"The rule:"* names `pnl_agent_flags` and `PD_PLUGIN_DIR_ADDED`, retired, and cites `cli/templates/scripts/lib/harness-run-lib.sh` → `hr_flow_host_exec` for the five variables. *"Deliberately not covered"*: removing the scratch directory, which is its owner's; the watcher's shared flags themselves.
- [ ] **`tests/test_agent_flags.py`:**
  - its header rule;
  - `session_args` with and without `plugin_dir_added`;
  - a shared `--agent` and a shared `--output-format=json` each refused with exact text;
  - an agent with no `mcp__` tool;
  - an agent naming two servers of three in a planted `.mcp.json`, whose exact JSON written is a literal;
  - no `.mcp.json`;
  - a malformed `.mcp.json`'s `RecordError` text;
  - `session_env` dropping the five variables and the `<venv>/bin` entry while keeping `DEVSCENE_MAIN_REPO` and a `PATH` order otherwise unchanged.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_agent_flags.py` passes.
- Every file `agent_args` writes sits under `scratch`, asserted by listing `tmp_path`.
