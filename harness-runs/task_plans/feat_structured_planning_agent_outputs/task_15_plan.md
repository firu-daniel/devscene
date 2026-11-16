### Task 15 — Update `docs/watcher.md` and `ARCHITECTURE.md`, and register the new suite in `devscene.config.json` → `treeGuards`

**Goal:** Bring the two remaining documents that describe how a planning node's decision is read in line with Tasks 10–11, and register Task 13's tree-reading suite so every unit whose change touches a file it reads runs it.

**Depends on:** Task 13, which adds `cli/test/agent-return-schemas.test.mjs` and names this task as its registering task (`plugin/instructions/unit_loop_core.md` → `## The test-run rule`, point 8): the suite reads `plugin/**/*.md`, `cli/templates/scripts/flows/task_plan_writing.graph.json` and `cli/templates/scripts/lib/planning-driver-lib.sh`. And Task 14, whose `docs/structured-agent-returns.md` is the decision of record these documents point at, and whose `docs/flow-graph-walker.md` → `### Not yet measured, and the hand step that measures it` now records the 2026-11-16 correction.

**How this catch-all task reads the conventions.** Its targets sit at the repository root, so it reads every configured layer's conventions document: `devscene.config.json` is the configuration contract (`.claude/context/conventions.md` → `## Configuration is the source of truth, and it is read at run time`) and `treeGuards` is an existing key, so no schema, model, check or `docs/config.md` row changes.

### Targets

- `devscene.config.json` → `treeGuards`
- `docs/watcher.md`
- `ARCHITECTURE.md`

**Work:**

- [ ] `devscene.config.json` → `treeGuards`: append two entries, both `"test": "test/agent-return-schemas.test.mjs"` — the argument the single-file test command takes, spelled as the existing entries spell theirs — one with `"covers": "plugin/**/*.md"` and one with `"covers": "cli/templates/scripts/**"`. Change nothing else in the file.
- [ ] `docs/watcher.md` → **What parks or pauses the driver, and what it retries.**: the infrastructure list's "a result with no decision object" becomes a return that carries no return block or fails its agent's `## Return schema`, retried like the rest. **The planning driver's unmeasured facts** (under `## 6. What a human must do, and what ships unexercised`): it no longer lists the node-session `structured_output` fact as unmeasured — the driver no longer reads it — and points at `docs/flow-graph-walker.md` → `### Not yet measured, and the hand step that measures it` and at `docs/structured-agent-returns.md` for what remains unmeasured (the orchestrating session's `Agent` result).
- [ ] `ARCHITECTURE.md` → the `cli/templates/scripts/lib/planning-node-lib.sh` → `pnl_agent_flags`, `pnl_launch` and `pnl_reap` row: drop "`--json-schema` with a schema built by `jq` from the planning graph" from the flag list, and replace "`structured_output` (else `.result | fromjson?`)" with the `result` text's return block, validated against the agent's `## Return schema` read from the pinned plugin; the coupling and seam cells say the same of the decision the script validates. Leave the remote mention control's row unchanged.

**Verification:**

- `devscene.config.json` still parses, carries the two new entries after the existing ones, and `git diff -- devscene.config.json` touches nothing outside `treeGuards`.
- `cli/test/agent-return-schemas.test.mjs` exists at the path the two entries name, relative to `cli/` as the existing entries are.
- `git grep -nE 'structured_output|json-schema|decision object' -- docs/watcher.md ARCHITECTURE.md` prints only lines about the remote mention control.
