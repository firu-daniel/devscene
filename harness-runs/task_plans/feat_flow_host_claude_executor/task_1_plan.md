### Task 1 — Read the plugin's name and each agent's `AgentContract` in `records/plugin_contracts.py`

**Goal:** Give the flow host a record reader for the plugin directory. It reads the plugin's name from `.claude-plugin/plugin.json`, and one agent's declared `tools:` and return schema into a frozen `AgentContract`, as the pilot's bash readers do. With this reader the host can build the executor's per-agent contracts, and the executor itself never opens a plugin file.

**Where this layer stops.** This task reads values and decides nothing with them. It does not validate a schema against JSON Schema: `graphscene.return_violations` does that, `records` never imports `graphscene`, and **Task 4** runs that check when it constructs `ClaudeExecutor`. It does not compare tools with a session's `init` event (**Task 2**). It does not build any flag from the tools list: the per-agent flags, the pilot's MCP-config flags among them, are host input to **Task 4**.

### Targets

- `devscene-flow-host/src/devscene_flow_host/records/plugin_contracts.py` (new)
- `devscene-flow-host/src/devscene_flow_host/records/__init__.py`: the layer docstring's list of records it reads
- `devscene-flow-host/tests/test_plugin_contracts.py` (new)

**Work:**

- [ ] `plugin_contracts.py`, the constants and the value. Add module-level `Final` constants for the fixed names this module reads, under `## Shared code and constants` of `.claude/context/devscene-flow-host.md`: `PLUGIN_MANIFEST` (`.claude-plugin/plugin.json`), `AGENTS_DIRECTORY` (`agents`) and `SCHEMAS_DIRECTORY` (`schemas`). Write the per-agent suffixes `.md` and `.return.json` inline in the two path functions `agent_definition_path(plugin_dir: Path, agent: str) -> Path` and `return_schema_path(plugin_dir: Path, agent: str) -> Path`. Add `@dataclass(frozen=True) class AgentContract` with exactly these fields:
  - `agent: str`;
  - `tools: tuple[str, ...]`, in `tools:` line order;
  - `return_schema: Mapping[str, object]`, a `MappingProxyType` over the parsed top-level object, read-only at the top level as `HarnessConfig.phases` is.

  An agent name that does not match `^[a-z0-9][a-z0-9-]*$` raises `ValueError(f"not an agent name: {agent!r}")` before any path is built. A name like that is a caller's defect, not an unreadable record.
- [ ] `read_plugin_name(plugin_dir: Path) -> str`, as `pnl_init` reads `.name | strings` from the manifest (`cli/templates/scripts/lib/planning-node-lib.sh`). Each unreadable shape is a one-line `RecordError` naming the file:
  - no file: `no .claude-plugin/plugin.json under <plugin_dir>`;
  - bytes that are not UTF-8 JSON: `<file>: not valid JSON`;
  - not an object: `<file>: not a JSON object`;
  - no non-empty string `name`: `<file>: carries no non-empty name`.

  Only `FileNotFoundError` becomes a `RecordError`. Every other `OSError` propagates (`.claude/context/devscene-flow-host.md` → `## Errors`).
- [ ] `read_agent_contract(plugin_dir: Path, agent: str) -> AgentContract` reads two files.
  - **The tools**, as `pnl_agent_tools_var` does. The file's first line must be `---`. Scan until the closing `---` for the first line starting `tools:`, split its remainder on `,`, trim spaces and tabs, drop empty items, and strip a trailing `\r` from every line. Refusals:
    - no definition: `no agent definition at <file>`;
    - no opening fence, no `tools:` line before the closing fence, or an empty list: `<file>: carries no tools: line`.
  - **The schema**, as `pnl_load_schemas` does. Refusals:
    - no file: `no return schema at <file>`;
    - not UTF-8 JSON, or not one JSON object: `<file>: is not one JSON object`;
    - no top-level `oneOf` array: `<file>: carries no top-level oneOf array`.

  The module docstring opens with *"The rule:"*. It names `pnl_init`, `pnl_agent_tools_var` and `pnl_load_schemas` as the bash readers it reads like, and states that it re-reads both files on every call. Under *"Deliberately not checked"* it lists: whether the schema is valid JSON Schema (Task 4's construction check, through `graphscene.return_violations`), every other frontmatter key, and the plugin manifest's other keys.
- [ ] `records/__init__.py`: add the plugin's manifest, agent definitions and return schemas to the docstring's list of records the layer reads. Leave its rule paragraph unchanged.
- [ ] `tests/test_plugin_contracts.py`: a module docstring opening *"The rule this file exists to enforce"* and typed `-> None` test functions. Include:
  - one planted-plugin case under `tmp_path` for each `RecordError` message above, asserting the exact text, and the `ValueError` for a bad agent name;
  - one clean planted case: a `tools:` line with spaces, an `mcp__` tool and a CRLF line ending, read to the exact tuple;
  - one case reading this checkout's own tracked files as read-only input, from a path built off `__file__`: `plugin/.claude-plugin/plugin.json` gives `devscene`, and `plugin/agents/task-plan-reviewer.md` with `plugin/schemas/task-plan-reviewer.return.json` gives the tools `("Read", "Glob", "Grep", "Bash", "Write", "mcp__devscene-docs__search_docs")`, which is the literal on that file's `tools:` line, and a schema whose `$schema` is the draft-07 URI. In the same case, `graphscene.return_violations({}, contract.return_schema)` returns a non-empty list and does not raise. That proves Task 4's construction check accepts a shipped schema.

  These are named fixed files, not a tree of files, so this test is no tree guard and needs no `treeGuards` entry.

**Verification:**

- `tests/test_plugin_contracts.py` passes, and every expected message and tuple in it is a literal written from this file's rules or from reading the named plugin files, never one taken from the reader's output.
- `bash scripts/typecheck.sh` reports nothing in the three targets. `plugin_contracts.py` imports only the standard library and `devscene_flow_host.records`.
