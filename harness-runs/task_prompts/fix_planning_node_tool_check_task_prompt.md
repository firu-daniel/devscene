`fix_planning_node_tool_check` stops the planning driver from refusing every node whose agent declares `Bash` beside `Glob` or `Grep`, a refusal Claude Code itself causes by leaving those two tools out of the session.

## What happened

The first real run with `execution.scriptDrivenPlanning` on, `fix_run_commit_trailer_amend` (2026-11-16, Claude Code 2.1.325), parked after its first node. The `task-plan-writer` session wrote the whole plan (a story index and seven task files; `success`, 103 turns, about $7.77, 16 minutes). Then `pnl_reap` decided its result as:

```
[plan-drive] #1 plan_writer: error (the agent tools do not match its init event: missing [Glob, Grep], extra [])
```

That is an agent-class `error`, so the walker escalated at `plan_writer` and the run parked with `question_1.md`. The plan files were left uncommitted in the run copy.

The agent's `tools:` line is `Read, Write, Edit, Bash, Glob, Grep, mcp__devscene-docs__search_docs`. The session's `init` event listed `["Read","Write","Edit","Bash"]`.

## Measured, 2026-11-16, Claude Code 2.1.325

Headless sessions launched as the driver launches them (`claude -p --output-format stream-json --verbose --plugin-dir <main checkout>/plugin --agent devscene:<agent>`), reading the `system`/`init` event's `tools`:

| Agent | `tools:` line | `init` tools |
|---|---|---|
| `task-plan-writer` (the run's node 1) | `Read, Write, Edit, Bash, Glob, Grep, mcp__devscene-docs__search_docs` | `Read, Write, Edit, Bash` |
| `architecture-reviewer` | `Read, Glob, Grep, Bash, Write, mcp__devscene-docs__search_docs` | `Read, Bash, Write` |
| `committer` | `Bash, Read, Edit` | `Bash, Read, Edit` |
| `prompt-injection-reviewer` | `Read, Grep, Glob` | `Read, Grep, Glob` |

The run's orchestrator session, launched with no `--agent`, has no `Glob` or `Grep` in its `init` tools either, beside `Bash`.

So in this Claude Code version a session that has `Bash` is given neither `Glob` nor `Grep`, whatever the agent declares. A session without `Bash` keeps them. No session was given a tool its agent does not declare.

Two more facts from the same node-1 `init` event, which `docs/flow-graph-walker.md` → `### Not yet measured, and the hand step that measures it` lists as unmeasured:

- **Plugins loaded:** `devscene` once, `{"name":"devscene","path":"<main checkout>/plugin","source":"devscene@inline","version":"0.7.1"}`, beside Claude Code's built-in plugins. No installed copy was loaded beside the `--plugin-dir` one.
- **`init` tools under `--json-schema`:** `--json-schema` added no tool. The only difference from the `tools:` line is the `Glob`/`Grep` omission above.

The third fact in that section, `structured_output` under `--json-schema`, is not this issue's. It belongs to `feat_structured_agent_outputs` (#379), which replaces how a node's decision is read.

> ⚠️ **Find every anchor in this prompt by its quoted text, heading or function name, never by line number.**

## What to read first

- `cli/templates/scripts/lib/planning-node-lib.sh` → `PNL_REAP_JQ`, the rule that builds `$missing` and `$extra` and decides `the agent tools do not match its init event`; `pnl_agent_tools_var`; the module header's account of the `init` check.
- `cli/test/planning-node-lib.test.mjs`: the cases asserting `missing [Grep], extra []` and `missing [], extra [Edit]`.
- `docs/flow-graph-walker.md` → `## 5. The two drivers`: the paragraph on the `init` check ("a session whose `init` tools carry anything that line does not name is refused"), and `### Not yet measured, and the hand step that measures it`.
- `docs/orchestrator-cost-measurement.md` → `## 4. Does a session's main agent keep its \`tools:\` allowlist?`, which the check answers.

## The goal

1. A node session whose `init` tools are its agent's `tools:` line, less tools Claude Code itself withholds, is not refused.
2. A session given any tool its agent does not declare is still refused at once, as an agent-class `error`. That is the protection the check exists for.
3. `docs/flow-graph-walker.md` records the measurements above in the form its documents of record require, and no longer lists the plugins and `init`-tools facts as unmeasured.

## Proposals — for planning to settle, not constraints

- **Refuse on `extra` only.** A missing tool cannot widen what a session does. An agent that truly needs a withheld tool fails in its own work, visibly. The docs already describe the check this way.
- **Or tolerate a named set.** Accept `Glob` and `Grep` missing only when `Bash` is present, and keep refusing any other missing tool. This is tighter, but it ties the driver to one Claude Code version's behaviour.
- Either way, a missing tool is worth one `[plan-drive]` log line or an observation, so a future change in what Claude Code withholds is visible.

## Constraints

- No new permission in any profile.
- Bash 3.2 and jq 1.5 floors, as the libraries' headers state.
- `bash scripts/typecheck.sh` and `scripts/run-gates.sh` pass.
- **No measured result is invented.** The table above is the record. Anything else the change relies on is either already recorded or added as unmeasured.
