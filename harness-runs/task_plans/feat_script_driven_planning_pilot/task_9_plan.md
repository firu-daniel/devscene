### Task 9 — Add the node-session launch site to `ARCHITECTURE.md` §5 and the libraries to `docs/cli.md`'s outer-loop list

**Goal:** Keep two inventories true:
- `ARCHITECTURE.md` → `## 5. Where the engine is reached — the launch path`, whose own derivation command now reaches the planning driver's node-session launch;
- `docs/cli.md` → *"Two families land in `scriptsDir`, and only one of them is generated."*, which lists every outer-loop file `init` copies and says which an agent may run.

**Depends on:**
- **Task 1** (`cli/templates/scripts/lib/planning-node-lib.sh`). `pnl_agent_flags` appends these to the shared vector:
  - `--agent <plugin name>:<agent>`;
  - `--plugin-dir <pinned dir>`;
  - `--add-dir <pinned dir>`;
  - `--json-schema <schema built by jq from the graph>`;
  - either `--disallowedTools mcp__*` or `--strict-mcp-config --mcp-config <filtered .mcp.json>`.

  `pnl_reap` reads the `init` event's `tools`, and the `result` event's `subtype`, `is_error`, `structured_output` (else `.result | fromjson?`), `total_cost_usd` and `permission_denials`.
- **Task 6** (`cli/templates/scripts/autonomous-watcher.sh` → `session_exec`), now the one producer of the shared flag vector for the engine session and every node session.
- **Task 4**, which ships the three libraries as `agentInvocable: false` rows with no `DENY_SCRIPT_BASENAMES` entry.

### Targets

- `ARCHITECTURE.md`: `## 5. Where the engine is reached — the launch path`.
- `docs/cli.md`: the *"Two families land in `scriptsDir`"* paragraph.

**Work:**

- [ ] **`ARCHITECTURE.md` §5, the derivation.** Run the section's own derivation command, verbatim, from the checkout root:

  ```
  grep -rnE 'DEVSCENE_AGENT_CLI|AGENT_CLI|ENGINE_COMMAND_|--output-format|--permission-mode|--settings|--add-dir|rate_limit_event|PIPESTATUS' cli/templates/scripts/ cli/src/
  ```

  Then hold its covering invariant: every site the command reaches is a row of the table or is dispositioned in the paragraph before it. Never narrow the command to fit the table.
- [ ] **`ARCHITECTURE.md` §5, the edits.**
  - Amend the `spawn_engine` row's **Site** cell to name `session_exec` as the function that now carries the flag string.
  - Add a row for `cli/templates/scripts/lib/planning-node-lib.sh` → `pnl_agent_flags` / `pnl_launch` / `pnl_reap`, called by `lib/planning-driver-lib.sh` → `pd_drive`, with all four columns:
    - **What it binds:** the per-node flags above on top of `session_exec`'s vector, and the `init` and `result` fields above. The `init` event's tools are compared with the agent file's `tools:` line, and a missing `init` event is an `error`.
    - **How engine-bound:** tightly, and by name, since every flag is one CLI's spelling and the outcome is read out of that CLI's result envelope.
    - **What a second runtime must supply:** a headless session that adopts a named agent's tool restriction from a pinned plugin source, reports the tools it granted, and returns one structured object the script validates.
  - Extend the paragraph's *"Remote execution added one launch site"* sentence with the planning driver's, local mode only.
  - Keep the column markers: **[shipped]** on the first three columns and **[designed]** on the fourth, as the table's own legend states.
- [ ] **`docs/cli.md`.**
  - In the *"Two families land in `scriptsDir`"* paragraph's outer-loop list, add *"the planning driver's three libraries, which the run watcher sources for the opt-in script-driven planning pilot"*.
  - In the same paragraph's account of what is allow-listed, add one clause: the three libraries are `agentInvocable: false` and carry no deny-list entry, because run directly each only defines functions, and the watcher that runs the driver is itself withheld.

**Verification:**

- Re-run the §5 derivation command above, and read every file it reaches against the table: each is a row or is named in the dispositioning paragraph, `lib/planning-node-lib.sh` and `session_exec` among them.
- `grep -n "planning driver" docs/cli.md ARCHITECTURE.md` finds the new list entry, the allow-list clause and the new row.

**Deviations from plan:** The §5 derivation command also reaches `cli/templates/scripts/lib/harness-run-lib.sh` (the `--add-dir` mention in the comment on `hr_job_absent_file`, from `1a41540c`), which no row or disposition covered; to hold the covering invariant it is now dispositioned in the paragraph, whose "Six of the files" count was reworded to "The remaining files" so it carries no count. The new row is placed last, so the mention-session sentence now says "the last row but one below".
