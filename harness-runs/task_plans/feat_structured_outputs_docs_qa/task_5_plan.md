### Task 5 — Make the schema suite fail an agent definition with no return schema

**Goal:** `cli/test/agent-return-schemas.test.mjs` fails any `plugin/agents/*.md` agent definition that has no `plugin/schemas/<agent>.return.json`. Today the suite skips such an agent by design, so agents could adopt the mechanism one at a time; with every agent adopted, the skip becomes a rule that a new agent lands with its schema. The new check is exported like the suite's others and is run once on an inline bad sample it must reject, so it cannot pass vacuously.

**Depends on:** Tasks 1–4, which add the last five schema files — `qa-tester`, `qa-tester-mobile-maestro`, `qa-tester-mobile-mcp`, `docs-writer` and `docs-reviewer`. With them landed, every definition under `plugin/agents/` has a schema file; before them this task's own real-tree case would fail. That is why this `cli` task ships after the `plugin` tasks rather than in the configured layer order (story index `## Context`). This task changes no plugin file and no schema file; Task 6 rewords the decision record to the rule this task puts in force.

**Where this task stops.** The suite enumerates agents from the directory listing, never from a count: the task prompt's *"all 22 agents"* is today's tree, and a baked-in number would break on the next agent added. `README.txt` in `plugin/agents/` is not an agent: the suite's `allAgentFiles` already filters on `.md`.

### Targets

- `cli/test/agent-return-schemas.test.mjs` — the header comment, one new exported check, one real-tree case replacing the *"at least one agent has a …"* case, and one bad-sample case. This suite is already registered in `devscene.config.json` → `treeGuards`, so no registration is owed (`plugin/instructions/unit_loop_core.md` → `## The test-run rule`, point 8).

**Work:**

- [ ] **The check.** Beside `checkSchemaOwners`, add and export `checkSchemaCoverage(agentNames, schemaNames)`: it returns one problem per agent name with no schema name, worded `` `${AGENTS_DIR}/${n}.md has no ${SCHEMAS_DIR}/${n}${SCHEMA_SUFFIX}` ``, mirroring `checkSchemaOwners`' wording in the other direction. Give it a one-line doc comment in the style of its neighbours (*"Every agent definition has a schema file."*).
- [ ] **The real-tree case.** Replace `` test(`at least one agent has a ${SCHEMAS_DIR}/<agent>${SCHEMA_SUFFIX}`, …) `` with `` test(`every agent definition has a ${SCHEMAS_DIR}/<agent>${SCHEMA_SUFFIX}`, …) ``, which asserts `allAgentFiles.length > 0` (so it cannot pass on an empty directory) and `assert.deepEqual(checkSchemaCoverage(allAgentFiles.map((f) => agentName(f.path)), [...schemaTexts.keys()]), [])`. Leave `agentFiles`, the per-agent loop and every other real-tree case as they are: a definition with no schema now fails this one case, by name, rather than every per-agent check at once.
- [ ] **The bad sample.** Beside `bad samples: a schema file with no agent definition is rejected`, add `bad samples: an agent definition with no schema file is rejected`, asserting that `checkSchemaCoverage(['sample-agent', 'unschemaed-agent'], ['sample-agent'])` returns exactly one problem naming `plugin/agents/unschemaed-agent.md`, and that `checkSchemaCoverage(['sample-agent'], ['sample-agent'])` returns none.
- [ ] **The header.** In the opening rule sentence, *"every agent with a `plugin/schemas/<agent>.return.json` declares its return there"* becomes *"every agent under `plugin/agents/` has a `plugin/schemas/<agent>.return.json`, declares its return there"*. Replace *"An agent with no schema file is skipped by design, so agents adopt the mechanism one at a time (#380); a schema file with no agent definition beside it fails."* with *"An agent definition with no schema file fails, as does a schema file with no agent definition beside it, so a new agent lands with its schema."* Keep every other header sentence.

**Verification:**

- `npm test --workspace cli -- test/agent-return-schemas.test.mjs`, from the repository root as one plain foreground command, passes, and its output lists the case `every agent definition has a plugin/schemas/<agent>.return.json` and the case `bad samples: an agent definition with no schema file is rejected` — the task's own edited test file, per `## The test-run rule` point 3.
- `grep -nE 'skipped by design|one at a time|#380|at least one agent has' cli/test/agent-return-schemas.test.mjs` has no hit.
- `grep -nE '\b2[0-9]\b agents|length, 2[0-9]' cli/test/agent-return-schemas.test.mjs` has no hit: no agent count is baked in.
- The new check's problem wording names the definition path and the missing schema path, so a reader knows which file to add.
