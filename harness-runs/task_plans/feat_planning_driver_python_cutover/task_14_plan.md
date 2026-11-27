### Task 14 — Read the worktree's MCP servers as a record, and build the session args, per-agent MCP flags and session environment in `host/agent_flags.py`

**Goal:** Build the three inputs `ClaudeExecutor` takes from the host, as the task prompt's leads give them:
- `session_args`: the watcher's shared flags passed through unchanged, plus `--add-dir <plugin_dir>` unless the shared vector already carries it;
- `agent_args`: each agent's MCP flags as `pnl_agent_flags` built them;
- `env`: the session environment.

The environment is the driver's own, minus the variables the flow host's `uv` launch adds, so no node session inherits the flow host's Python environment. That is the story index's second `Top risks:` entry.

**Where this task stops.** It builds values. Constructing `ClaudeExecutor` with them, and calling `read_mcp_servers(worktree)` to hand `agent_args` its servers, is **Task 16's**. The `ClaudeExecutor` constructor refuses a host flag it sets itself (`EXECUTOR_FLAGS`), so nothing here passes one. The record read and the host work are split along the layer line (`.claude/context/devscene-flow-host.md` → `## The internal layers`: *"Reading a record into a value is `records`"*): `records/mcp_servers.py` reads the worktree's `.mcp.json` into a plain value; `host/agent_flags.py` reads no file but the contracts it is handed, and only cuts that value and writes the per-agent scratch files.

### Targets

- `devscene-flow-host/src/devscene_flow_host/records/mcp_servers.py` (new)
- `devscene-flow-host/tests/test_mcp_servers.py` (new)
- `devscene-flow-host/src/devscene_flow_host/host/agent_flags.py` (new)
- `devscene-flow-host/tests/test_agent_flags.py` (new)

**Work:**

- [ ] **`records/mcp_servers.py` → `read_mcp_servers(worktree: Path) -> Mapping[str, object]`**, and `tests/test_mcp_servers.py`.
  - **Constant.** `MCP_CONFIG_FILENAME: Final = ".mcp.json"`.
  - **The value**, read as `pnl_agent_flags` (`cli/templates/scripts/lib/planning-node-lib.sh`) read it through `jq '.mcpServers // {}'`: the file's `mcpServers` object as a read-only `MappingProxyType`, server name to its configuration, in file order. An absent file, and an absent or `null` `mcpServers`, are each an empty mapping.
  - **Unreadable shapes**, each a one-line `RecordError` naming the path, as `records/config.py` spells its own: non-UTF-8 bytes or text that is not JSON, `f"{path}: not valid JSON"`; a top level that is not an object, `f"{path}: not a JSON object"`; an `mcpServers` that is neither `null` nor an object, `f"{path}: mcpServers is not a JSON object"`.
  - **The docstring.** *"The rule:"* names `pnl_agent_flags` as the bash reader it reads as (readable in that file's history once Task 4 deletes it). *"Deliberately not covered"*: which servers an agent may use, and writing any file, both `host/agent_flags.py`'s; each server entry's own shape, which `claude` checks.
  - **The cases**, each against literals: three servers read in order; no file; `mcpServers` absent, and `null`; each of the three `RecordError` texts exactly; the returned mapping refusing assignment.
- [ ] **`session_args(shared: Sequence[str], plugin_dir: Path, *, plugin_dir_added: bool) -> tuple[str, ...]`.** It returns `shared` unchanged, followed by `--add-dir <plugin_dir>` unless `plugin_dir_added`. A token of `shared` that is an `EXECUTOR_FLAGS` member, bare or as `<member>=`, raises `ValueError` naming it, before any session.
- [ ] **`agent_args(contracts: Mapping[str, AgentContract], mcp_servers: Mapping[str, object], scratch: Path) -> dict[str, tuple[str, ...]]`.** It reads each agent's declared `tools` off its `AgentContract`, as `records/plugin_contracts.py` reads them. `mcp_servers` is `read_mcp_servers(worktree)`'s value; this function opens no `.mcp.json` and raises no `RecordError`.
  - **No server named.** When no tool matches `mcp__<server>__…`, the agent's args are `("--disallowedTools", "mcp__*")`.
  - **Servers named.** Otherwise they are `("--strict-mcp-config", "--mcp-config", "<scratch>/mcp-<agent>.json")`.
    - The file holds `{"mcpServers": {…}}`: `mcp_servers` cut to the named servers, in `mcp_servers`' order.
    - When `mcp_servers` is empty, the file holds `{"mcpServers": {}}`.
- [ ] **`session_env(environ: Mapping[str, str], *, venv: Path | None) -> dict[str, str]`.** It returns `environ` without `VIRTUAL_ENV`, `UV_PROJECT_ENVIRONMENT`, `PYTHONPATH`, `PYTHONDONTWRITEBYTECODE` and `PYTHONHOME`, the `FLOW_HOST_LAUNCH_VARIABLES` `Final` tuple. When `venv` is given, the `PATH` entries equal to `<venv>/bin` are removed. Every other variable, `DEVSCENE_MAIN_REPO` and `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS` among them, is kept.
- [ ] **`host/agent_flags.py`'s module docstring, and `tests/test_agent_flags.py`.**
  - **The docstring.** *"The rule:"* names `pnl_agent_flags` and `PD_PLUGIN_DIR_ADDED`, retired, and cites `cli/templates/scripts/lib/harness-run-lib.sh` → `hr_flow_host_exec` for the five variables. *"Deliberately not covered"*: reading `.mcp.json`, which is `records/mcp_servers.py`'s; removing the scratch directory, which is its owner's; the watcher's shared flags themselves.
  - **The cases:**
    - its header rule;
    - `session_args` with and without `plugin_dir_added`;
    - a shared `--agent` and a shared `--output-format=json` each refused with exact text;
    - an agent with no `mcp__` tool;
    - an agent naming two servers of a three-server `mcp_servers` mapping built in the test, whose exact JSON written is a literal;
    - an empty `mcp_servers` mapping;
    - `session_env` dropping the five variables and the `<venv>/bin` entry while keeping `DEVSCENE_MAIN_REPO` and a `PATH` order otherwise unchanged.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_mcp_servers.py` passes.
- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_agent_flags.py` passes.
- `host/agent_flags.py` names neither `MCP_CONFIG_FILENAME` nor `RecordError`: `grep -nE 'mcp\.json|RecordError' devscene-flow-host/src/devscene_flow_host/host/agent_flags.py` prints no hit outside its docstring.
- Every file `agent_args` writes sits under `scratch`, asserted by listing `tmp_path`.
