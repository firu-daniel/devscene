### 1. Each planning agent's return JSON schema is inlined in its definition, so every dispatch pays for a block only the driver and the suite read

**File:** `plugin/agents/task-plan-writer.md` → `## Return schema` — "\"title\": \"task-plan-writer return\"" (the same `## Return schema` section sits at the end of `plugin/agents/task-plan-reviewer.md`, `plugin/agents/architecture-reviewer.md`, `plugin/agents/business-parity-reviewer.md`, `plugin/agents/ui-tests-plan-writer.md` and `plugin/agents/ui-tests-plan-reviewer.md`); reader: `cli/templates/scripts/lib/planning-node-lib.sh` (`pnl_load_schemas`) — "f=\"$PNL_PLUGIN_DIR/agents/$agent.md\""

**Problem.** Verified in the current tree. Each of the six agent definitions carries its return contract twice: a `## Return schema` fenced `json` block placed directly after `## Output contract`, and the `### Return fields` prose inside `## Output contract`. Measured (`sed -n '<range>p' <file> | wc -w -c`, ranges from `grep -n '^## '`):

| Agent | `## Return schema` section, words / chars | `### Return fields`, words | Whole definition today, words / chars |
|---|---|---|---|
| `task-plan-writer` | 278 / 2,484 | 385 | 4,859 / 33,344 |
| `task-plan-reviewer` | 184 / 1,633 | 54 | 5,001 / 33,717 |
| `architecture-reviewer` | 203 / 1,745 | 75 | 4,891 / 34,418 |
| `business-parity-reviewer` | 229 / 1,945 | 88 | 5,456 / 38,007 |
| `ui-tests-plan-writer` | 317 / 2,791 | 111 | 4,902 / 33,457 |
| `ui-tests-plan-reviewer` | 180 / 1,568 | 65 | 3,964 / 26,154 |
| **Total** | **1,391 / 12,166** | **778** | **29,073 / 199,097** |

The schemas are about 12 KB, paid on every dispatch of every one of the six. The model acts on `### Return fields`, not on the schema. The schema is read only by machines: `planning-node-lib.sh` → `pnl_agent_schema_scan` (an awk scan for the first ```` ```json ```` block under the `## Return schema` heading) and `pnl_load_schemas` (which writes it to `<PNL_TMP>/schema-<node>.json` for `PNL_REAP_JQ`), `cli/test/agent-return-schemas.test.mjs` (`checkSchemaBlock`, `hasSchemaSection`), and the driver test stub in `cli/test/helpers/planning-driver.mjs` (`agentText.indexOf('## Return schema')`).

The recorded reason for keeping the schema inline, `docs/structured-agent-returns.md` → `### The schema lives in the agent's own definition`, weighs only a file under the repository-root `schemas/`, which the installed plugin does not carry. It does not weigh a file inside `plugin/`, which ships with the plugin and is under the same `--plugin-dir` root `pnl_init` already reads `agents/` and `instructions/` from.

**Fix.** Move each schema into its own file inside the plugin, read only by the driver and the suites, and keep a short `### Return fields` in the agent as the only return description the model sees.

- [ ] **The schema files.** Create `plugin/schemas/<agent>.return.json` for each of the six agents. Each holds the JSON object from that agent's current `## Return schema` block, byte-for-byte except for whitespace, in the same closed dialect. Use a new `plugin/schemas/` directory, not `plugin/agents/`: `plugin/agents/` is the component-discovery directory, and `plugin/agents/README.txt` already exists because of what may sit beside the definitions there. Then delete the `## Return schema` section from all six definitions.
- [ ] **The canonical sentence.** Every agent has a `## Output contract` sentence ending "valid against `## Return schema` below". Replace it in the module and in all six agents with one sentence that points at `### Return fields`, for example: "End your reply with your return object: one fenced code block whose info string is `json`, holding one JSON object with exactly the fields `### Return fields` below lists for your outcome, with nothing after its closing fence." Keep the opening `End your reply with your return object: ` (the suite asserts it). Copy the new sentence byte-for-byte into `plugin/instructions/agent_return_contract.md` → `## The return block` and all six agents.
- [ ] **`### Return fields` carries what the model needs to write a valid object, and nothing else.** One bullet per schema property, opening with the backticked name. Annotate every property whose JSON type is not `string` right after the name: `(integer)`, `(boolean)` or `(array of strings)`. The model no longer sees the schema, so a `tasks_count` written as `"3"` would otherwise fail the driver's check and cost a re-dispatch. Keep each bullet's per-outcome presence and its lower bounds ("at least 1"). Cut whatever restates another file, and cut caller-side rationale. In `task-plan-writer` (385 words today, aim for at most about 200):
  - Drop "The caller writes these entries to the branch's improvement-observations intake and the closing Done summary. Every entry is a recommendation, never a task." (where the caller writes the entries is the caller's concern).
  - Drop "`doctor`'s `layer-drift` check reports the same directories."
  - Compress the `undescribed-layer` remedy to the instruction it gives.
  - Keep the two entry types, what each entry names, and the "never the `--yes` spelling" edge case. The lesson ledger's `## Agent prose` rule binds this: cut restatement or rationale, never a definition or edge case the agent acts on.

  Trim the other five the same way where an Output contract sentence already says which outcome carries which field. Finding 2 owns any wider rewording of those agents, so here make only the cuts that come from the move.
- [ ] **The driver reads the file.** In `cli/templates/scripts/lib/planning-node-lib.sh`:
  - Delete `pnl_agent_schema_scan`.
  - Have `pnl_load_schemas` read `$PNL_PLUGIN_DIR/schemas/$agent.return.json`. A missing or unreadable file, a file that is not one JSON object, and an object with no top-level `oneOf` array each stay a `pnl_fail` naming the file.
  - Reword the header comment ("the `## Return schema` its agent's return object must satisfy, read out of the pinned plugin's agent file"), the `pnl_load_schemas` comment and the `PNL_REAP_JQ` comment ("the closed dialect of the plugin's `agent_return_contract.md` → `## The return schema`") to name the schema file.
  - Update the `REPRO` lines the move affects.

  Also update the comment in `cli/templates/scripts/lib/planning-driver-lib.sh` that names "`## Return schema`" and the one in `cli/templates/scripts/autonomous-watcher.sh` ("against its agent's `## Return schema`").
- [ ] **The static suite.** Edit `cli/test/agent-return-schemas.test.mjs`:
  - **Which agents are in scope.** An agent is schema-carrying when `plugin/schemas/<agent>.return.json` exists. This replaces `hasSchemaSection`.
  - **`checkSchemaBlock` becomes a parse of that file.** It must hold one JSON object.
  - **Checks to drop.** Drop `checkOutputContract`'s "`## Return schema` does not directly follow `## Output contract`" check.
  - **Checks to add.** A schema file whose agent has no `plugin/agents/<agent>.md` fails. An agent definition that still carries a `## Return schema` section or any fenced `json` block in `## Output contract` fails, so the schema cannot be re-inlined. A `### Return fields` bullet's type annotation must agree with the property's schema `type`, and a non-string property with no annotation fails.
  - **Checks to keep.** Keep the property-for-property check between `### Return fields` and the schema, the canonical-sentence check, the outcome-backtick check, the graph, `pd_ret_field`, citation and roster checks.
  - **Bad samples.** Rework the bad samples so `sampleAgent()` carries no `## Return schema` and the schema is passed alongside. Replace the "not directly after" sample with the new "re-inlined schema" and "missing type annotation" samples. Rewrite the renamed-`findings_file` sample to mutate the schema object instead of the agent text.
  - **Header comment.** Update the file's header comment to match.

  Also edit `cli/test/planning-node-lib.test.mjs`. Its fixture agent files (`schemaSection`) and its `pnl_init refuses an agent file with no usable ## Return schema, naming it` cases move to fixture `schemas/<agent>.return.json` files: the file is missing, it is not one JSON object, or it has no top-level `oneOf`. Then edit `cli/test/helpers/planning-driver.mjs`:
  - The fixture plugin build (`for (const agent of PLANNING_AGENTS)`) also copies `schemas/<agent>.return.json`.
  - The stub reads its schema from `join(pluginDir, 'schemas', agent + '.return.json')` instead of scanning the agent text.
  - Update its header comment ("built from the `## Return schema` of the fixture plugin's copy of the real agent").
- [ ] **The tree guard.** `devscene.config.json` → `treeGuards` registers `test/agent-return-schemas.test.mjs` for `plugin/**/*.md` and `cli/templates/scripts/**` only. Add a third entry with `"covers": "plugin/schemas/**"`, so that editing a schema file alone still triggers the suite.
- [ ] **Prose that names the old location.** Update every sentence that says the schema is the agent's `## Return schema` section:
  - **`plugin/instructions/agent_return_contract.md`.** In `## The return schema`, the schema is the file `${CLAUDE_PLUGIN_ROOT}/schemas/<agent>.return.json`, never read by the agent. In `## Return fields`, `### Return fields` is the only return description the agent carries, with the type annotation rule. In `## Adopting it for another agent`, step 1 creates the file. In `## Reading a return`, the driver applies the schema file.
  - **`plugin/instructions/plan_review_rounds.md` → `## The round file`.** Change "The reviewer's own `## Return schema` owns the shape." so it names the reviewer's `### Return fields`. Reviewer agents read this module on every dispatch, so it must not send them to a section that no longer exists.
  - **`docs/structured-agent-returns.md`.** Rewrite `### The schema lives in the agent's own definition` as a decision of record:
    - **Decision.** The schema lives in `plugin/schemas/<agent>.return.json`, read by `pnl_load_schemas` and the suite and never by the model.
    - **Alternatives.** Both are weighed: inline in the definition (what this branch first shipped), and the root `schemas/` directory, which is not in the installed plugin.
    - **Reason.** Name the 12,166 characters / 1,391 words that every dispatch of the six agents carried.
    - **Cost.** The model writes the object from prose alone. The suite holds the prose to the schema, including types, so the two cannot drift. A schema-only edit is a tree-guard trigger through the new `treeGuards` entry.

    In that same document, update `### Everything a caller routes or records on is a field` ("each per the agent's own `## Return schema`"), `### Validation on each path, and why no validator script`, and `## 2. Adopting it for another agent`.
  - **Driver-side documents.** Change "its agent's `## Return schema`" to name the schema file in `docs/flow-graph-walker.md` (the `### How each runs a parallel round` decision and the `pnl_reap` decision that cites `pnl_load_schemas`), `docs/watcher.md` (the two sentences naming "its agent's `## Return schema`"), and `ARCHITECTURE.md` (the `planning-node-lib.sh` row, "validated by the script against the agent's `## Return schema` read from the pinned plugin").
  - **Where the new asset kind goes.** Add a row to `.claude/context/plugin.md` → `## Where a new asset goes`: "an agent's return schema, read by the planning driver and the static suite, never by the agent" → `plugin/schemas/<agent>.return.json`. Add a `Plugin agent return schema` row to `.claude/CLAUDE.md` → `## File naming conventions` (`plugin/schemas/<agent>.return.json`, example `plugin/schemas/task-plan-writer.return.json`).

**Verification:**
- Run `bash scripts/typecheck.sh`.
- Run the test files this fix edits, through the configured single-file command: `cli/test/agent-return-schemas.test.mjs` and `cli/test/planning-node-lib.test.mjs`.
- Each of the six definitions carries no `## Return schema` and no ```` ```json ```` fence: `grep -c '^## Return schema' plugin/agents/*.md` prints 0 for every file.
- `grep -rn "## Return schema" plugin docs cli/templates ARCHITECTURE.md` prints no line that describes the schema's location as the agent definition.
- Re-measure the six definitions with `wc -w -c plugin/agents/<agent>.md`. Each falls by at least its `## Return schema` figure in the table above (projected total about 27,682 words / 186,931 characters, before any `### Return fields` trim).
