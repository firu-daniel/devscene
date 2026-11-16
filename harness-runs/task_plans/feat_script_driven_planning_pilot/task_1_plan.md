### Task 1 — Add `lib/planning-node-lib.sh`: one node session's prompt, schema, launch and validated result

**Goal:** Ship the library that turns one walker dispatch block into one headless node session, and reads that session back as exactly one of these:
- a declared outcome the walker can record;
- `error`;
- `undelivered`, meaning the session did not return.

The library launches nothing on its own and decides no routing.

**Where this library stops.**
- **The walk is Task 3's.** Which node runs next, when a set is launched, STOP, PAUSE, the cap, recording with `flow-walker.sh next`, retries and the stall kill all belong to Task 3 (`lib/planning-driver-lib.sh`).
- **Every durable write is Task 2's.** That includes commits, the ledger, question files and observations (`lib/planning-record-lib.sh`).
- **The flag vector is Task 6's.** The binary, `--settings`, `--permission-mode`, `--model`, `--effort`, `--add-dir`, the environment scrub and the main-checkout anchor export all live in the watcher function `session_exec`. This library calls that function by the name in `PD_SESSION_EXEC` and appends only the per-node flags listed below.
- **The row is Task 4's.** This task adds no `OUTER_LOOP_SCRIPTS` row.

### Targets

- `cli/templates/scripts/lib/planning-node-lib.sh` (new): the sourced library, functions prefixed `pnl_`.
- `cli/test/planning-node-lib.test.mjs` (new): its suite.

**Work:**

- [ ] **Header and floors.**
  - Open on `#!/usr/bin/env bash` and a `# planning-node-lib.sh — …` header stating what the library owns and the rule it exists to enforce: *a node's result is a declared outcome, `error` or `undelivered`, never a guess.* Add a `REPRO` block that runs each public function against a throwaway fixture.
  - It is a sourced library, so it sets no shell options. Hold to bash 3.2 and `jq` 1.5: no associative arrays and no `mapfile`.
  - Give every `mktemp` an explicit `"${TMPDIR:-/tmp}/<name>.XXXXXX"` template and never `-t`.
  - Put every temporary file the library makes (a filtered MCP config, a `return` text, a friction list) under one directory that `pnl_init` creates with `mktemp -d`. `pnl_cleanup` removes that directory and only that directory: `rm -f` on its files, then `rmdir` on it, as `run-analytics.sh` → `cleanup` does, never a recursive removal (`.claude/context/conventions.md` → `## Shell assets`). The directory holds files only, never a subdirectory. Task 3's `pd_drive` calls it on every return path.
  - Never name the main-checkout anchor environment variable outside a comment. Its export belongs to the watcher's `session_exec`.
  - Read the graph at `<worktree>/<scriptsDir>/flows/task_plan_writing.graph.json`, resolving `scriptsDir` and `stateDir` through `lib/harness-run-lib.sh`, which the caller has already sourced.
- [ ] **`pnl_init <plugin_dir> <worktree>`.** It returns 0, or 2 with one `planning-driver: <cause>` line on stderr. It sets:
  - `PNL_PLUGIN_NAME`, from `<plugin_dir>/.claude-plugin/plugin.json` → `.name`, which must be non-empty;
  - `PNL_MAX_DISPATCHES`, the integer on the `MAX_TOTAL_DISPATCHES = <n>` line of `<plugin_dir>/instructions/task_plan_writing_instructions_core.md` → `## Setup (once per session)` step 4;
  - the eight dispatch blocks of that same core, each the text between the fences of the fenced block under its heading, keyed on the `##` section and then the `###` heading:
    - `## Loop` → `` ### 1. Spawn `task-plan-writer` ``: the first fence is `plan_writer` `initial`, the second `plan_writer` `revision`;
    - `### 2. Business-parity review (plan-review mode)` → `business_parity_review`;
    - `### 3. Architecture review (plan-review mode)` → `architecture_review`;
    - `` ### 4. Spawn `task-plan-reviewer` `` → `plan_review`;
    - `## UI-test-plan write loop` → `` ### 1. Spawn `ui-tests-plan-writer` ``: `ui_writer` `initial` and `revision`;
    - `` ### 2. Spawn `ui-tests-plan-reviewer` `` → `ui_review`.

  A heading not found, a section with the wrong fence count, or no `MAX_TOTAL_DISPATCHES` integer is exit 2, naming the heading or line. The heading strings sit in one declared list at the top of the file, which Task 5's suite reads.
- [ ] **`pnl_prompt`, `pnl_schema` and the per-node flags.**
  - **`pnl_prompt <node> <variant> <branch> <iteration> <review_mode> [findings_file…]`** prints the block with these placeholders filled:
    - `<branch>`;
    - `<state_dir>`: `stateDir` with no trailing `/`;
    - `<prompt_path>`: `<state_dir>/task_prompts/<branch>_task_prompt.md`;
    - `<iteration>` and `<review_mode>`;
    - `<findings_files>`: the findings files in walker order, joined by `, `;
    - `<findings_file>`: the single findings file.

    Every other `<…>`, `task_<N>_plan.md`'s `<N>` among them, is left literal, as the core's own `## The walker` → **`action: dispatch`** fills only those values. Nothing is appended. Task 3 appends answered pairs on a writer resume.
  - **`pnl_schema <node>`** prints a JSON Schema built by `jq` from the graph's `.nodes.<node>.outcomes` keys:
    - `outcome`: required, an enum of exactly those keys;
    - `findings_file`: string;
    - `return`: string, the agent's whole return as its own `## Output contract` states it;
    - `harness_friction`: an array of strings.
  - **`pnl_agent_flags <node> <agent>`** prints the per-node flags, one per line:
    - `--agent <PNL_PLUGIN_NAME>:<agent>`;
    - `--plugin-dir <plugin_dir>`;
    - `--add-dir <plugin_dir>`;
    - `--json-schema <schema>`;
    - the MCP flags. When the agent file's `tools:` line, `<plugin_dir>/agents/<agent>.md`, names no `mcp__` tool, they are `--disallowedTools mcp__*`. When it names some, they are `--strict-mcp-config --mcp-config <file>`, where `<file>` is a temporary JSON written from the worktree's `.mcp.json` keeping only the servers its `mcp__<server>__` entries name, or `{"mcpServers":{}}` when there is no such file.
- [ ] **`pnl_launch` and `pnl_reap`.**
  - **`pnl_launch <seq> <node> <agent> <prompt> <log_path>`** starts, in the background, a subshell that runs `"$PD_SESSION_EXEC" "<prompt>" <per-node flags>` piped into `tee` to `${log_path%.log}.planning/<seq>-<node>.stream.jsonl`, then into `"$PD_FORMATTER"`, appended to `<log_path>`. It records a handle (pid, stream path, start epoch) the caller keeps.
  - **`pnl_reap <handle>`** runs after the pid has exited. It first appends the node's whole stream file once to the run's `${log_path%.log}.stream.jsonl`. Reaps are sequential in the driver loop, so no two sessions' lines interleave, and the usage gate and the run-analytics script read node sessions there as they read any session, late by one node. It then prints `key=value` lines: `kind=returned|error|undelivered`, `outcome=`, `findings=`, `return_file=` (the `return` text in a temp file), `friction_file=`, `cost=` (`total_cost_usd`), `duration_secs=`, `denials=` (the length of the `result` event's `permission_denials`) and `reason=`. It decides in this order:
    1. **No `system`/`init` event** → `error`, reason `the agent did not resolve: no init event`.
    2. **Tools mismatch** → `error`. Every non-MCP tool of the agent's `tools:` line must be in the `init` `tools` list, and every `init` tool must be in the agent's list. An agent MCP entry missing from `init` is allowed.
    3. **No `result` event, or `is_error` with an API 500, 503 or 529 / `Overloaded` in `result`** → `undelivered`.
    4. **`is_error` true or `subtype` other than `success`** → `error`.
    5. **Read the decision.** Take `.structured_output` when it is an object, else `.result | fromjson?` when that is an object, else `error`.
    6. **`outcome` not a key of the node's outcomes** → `error`, reason `undeclared outcome <value>`.
    7. **A missing `findings_file`** → `error`. It is required for `FAIL` at any node, and for `PASS` at a node listed in some `round` node's `gates`.
    8. **`questions` with a blank `return`** → `error`.
    9. **Otherwise** → `returned` with the outcome.
- [ ] **`cli/test/planning-node-lib.test.mjs`.**
  - Open it with the rule it enforces.
  - Each case copies `lib/harness-run-lib.sh`, this library and the shipped graph from `cli/templates/scripts/` into a fixture under the system temp directory. It sources them in one `bash` process, with `PD_SESSION_EXEC` naming a stub function that runs `$DEVSCENE_AGENT_CLI -p "$1" "${@:2}"`, and with a stub agent CLI printing canned `stream-json` lines.
  - Cover one case per `pnl_reap` rule, plus a declared `PASS`/`FAIL`/`returned`/`questions`.
  - Cover `pnl_schema`'s enum for `plan_writer` and for `plan_review`.
  - Cover `pnl_init` against a core copy with one heading renamed: exit 2 naming it.
  - Cover the `pnl_agent_flags` MCP split.
  - Never aim a case at this checkout.

**Verification:**

- `cli/test/planning-node-lib.test.mjs` passes. Its undeclared-outcome case returns `kind=error` and leaves the stub's other output unread, and its no-`init` case reports `error` for a stub that exits 0 with empty stdout, which is the measured unknown-agent shape (`docs/orchestrator-cost-measurement.md` → `## 4.`).
- `grep` the new library for the main-checkout anchor variable's name and find it only inside comments.
- `grep` the new library for `mktemp`, and find every call names a `"${TMPDIR:-/tmp}/…XXXXXX"` template.
