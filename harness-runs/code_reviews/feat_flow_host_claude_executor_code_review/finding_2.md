### 2. `agent_definition_path` and `return_schema_path` are public but nothing outside their own module calls them

**File:** `devscene-flow-host/src/devscene_flow_host/records/plugin_contracts.py` (`agent_definition_path`, `return_schema_path`): "def agent_definition_path(plugin_dir: Path, agent: str) -> Path:"

**The problem.** The two functions are module-level public names, but only `read_agent_contract` in the same file calls them. No other module, and no test under `devscene-flow-host/tests/`, calls them. The branch's caller check covered every `layers[].path` scope and found no call site outside `records/plugin_contracts.py`. Neither function is in the README's `## The layers` → `records` row, which names `read_plugin_name`, `read_agent_contract` and `AgentContract` as the module's surface. The functions are wired, because `read_agent_contract` uses them, so no wrong result follows. The problem is that the module offers two entry points nothing uses and nothing documents, and a later caller could start depending on them without a review noticing. This is Should Fix, because no failure sentence can be completed.

**Fix.** In `devscene-flow-host/src/devscene_flow_host/records/plugin_contracts.py`:

- rename `agent_definition_path` to `_agent_definition_path`;
- rename `return_schema_path` to `_return_schema_path`;
- update the two calls in `read_agent_contract` to match:

```python
def read_agent_contract(plugin_dir: Path, agent: str) -> AgentContract:
    definition = _agent_definition_path(plugin_dir, agent)
    schema = _return_schema_path(plugin_dir, agent)
```

No test names either function, so no test file changes and no test runs for this fix.
