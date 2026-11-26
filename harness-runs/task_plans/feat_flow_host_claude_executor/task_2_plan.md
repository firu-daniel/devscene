### Task 2 — Judge a finished `stream-json` transcript into a `NodeResult` and usage fields in `host/session_stream.py`

**Goal:** Port the pilot's session judgement (`cli/templates/scripts/lib/planning-node-lib.sh` → `PNL_REAP_JQ`) to Python as a pure function. Given the text a `claude -p --output-format stream-json --verbose` session printed, the agent's contract and the session's working directory, it returns the node's GraphScene `NodeResult` together with the usage fields the session reported.

**Depends on:** Task 1, which defines `devscene_flow_host.records.plugin_contracts.AgentContract` with exactly these fields:

- `agent: str`;
- `tools: tuple[str, ...]`, the agent's declared `tools:` in line order;
- `return_schema: Mapping[str, object]`, the agent's `schemas/<agent>.return.json` object.

This task reads `tools` and `return_schema` and nothing else.

**Where this layer stops.** This module launches nothing, waits on nothing and keeps no state. It does not detect a stall. **Task 3**'s process supervisor does that, and **Task 4** replaces this module's result with the stall failure when the supervisor reports one. It does not call the usage sink and does not time the session (both **Task 4**). It does not check whether a `FAIL` or a round gate's `PASS` carries a findings file: that rule is the host's `record_outcome` (`devscene-flow-host/src/devscene_flow_host/host/round_gates.py`), and `Dispatch` cannot tell a round gate from a review loop's writer.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/session_stream.py` (new)
- `devscene-flow-host/tests/session_events.py` (new), a test-support module
- `devscene-flow-host/tests/test_session_stream.py` (new)

**Work:**

- [ ] `session_stream.py` defines `@dataclass(frozen=True) class SessionReading` with these fields:
  - `result: NodeResult`;
  - `session_id: str | None`, from the first `system`/`init` event;
  - `total_cost_usd: float | None`;
  - `cache_creation_input_tokens: int | None` and `cache_read_input_tokens: int | None`, from the `result` event's `usage` object;
  - `model_usage: Mapping[str, object]`, a `MappingProxyType` over `modelUsage`, or empty;
  - `permission_denials: int`, the length of `permission_denials` when it is a list, else `0`;
  - `withheld_tools: tuple[str, ...]`.

  `withheld_tools` holds the declared tools not starting `mcp__` that the `init` event's `tools` lacks, in declared order, and is empty when there is no `init` event. The usage fields are read whenever the event exists, on every classification, and a field of the wrong JSON type is `None`. Also define `DETAIL_FIELD: Final = "findings_file"` and the overload markers `("API Error: 500", "API Error: 503", "API Error: 529", "Overloaded")` as a `Final` constant.
- [ ] `judge_session(stream: str, contract: AgentContract, cwd: Path) -> SessionReading` keeps the pilot's order. First, split `stream` on newlines and keep the lines that parse as JSON objects; skip the others, as `fromjson? | objects` does. `init` is the first `type == "system"` and `subtype == "init"` event, and `result` is the **last** `type == "result"` event. Then classify; a reason is always one line, with every `\r` and `\n` turned into a space:
  1. No `init`: `Failed("infra", "the agent did not resolve: no init event")`.
  2. `init` tools the contract does not declare: `Failed("agent", "the init event grants tools the agent does not declare: [<t1>, <t2>]")`, in `init` order. This is the pilot's class, kept: a retry would launch with the same grant.
  3. No `result`: `Failed("undelivered", "no result event")`.
  4. `is_error` is `true` and the `result` text contains an overload marker: `Failed("undelivered", "API error: <first 200 characters of the one-lined result text>")`.
  5. `is_error` is `true`, or `subtype` is not `success`: `Failed("infra", "the session ended as <subtype, or 'no subtype'>")`, with `" with is_error"` appended when `is_error` is `true`.
  6. Then read the return block (next bullet). No block: `Failed("infra", "the result carries no return block")`.
  7. A block that is not one JSON object: `Failed("infra", "the return block is not one JSON object")`.
  8. `graphscene.return_violations(document, contract.return_schema)` is non-empty: `Failed("infra", "the return fails its schema: <str(first violation)>")`.
  9. `outcome` missing, not a string or empty: `Failed("infra", "the return carries no outcome")`.
  10. Otherwise return `Completed(outcome, detail)`. `detail` is the return's `findings_file` when it is a non-blank string, joined onto `cwd` when relative and kept as given when absolute; otherwise `None`.

  An outcome the node does not declare is still `Completed`. Refusing it is the walk's job (`graphscene/src/graphscene/model/execution.py` → *"never the executor's to check"*). This is one of the module's two departures from `PNL_REAP_JQ`; the other is that the findings-file presence check is left to `record_outcome`. The module docstring names both under *"Departures from `PNL_REAP_JQ`"*, opens with *"The rule:"*, and lists under *"Deliberately not covered"*: launching and stall detection (`host/session_process.py`), and the usage sink (`host/claude_executor.py`). A `ValueError` from `return_violations` propagates, because Task 4 refuses an invalid schema at construction.
- [ ] Return-block extraction keeps the pilot's rule:
  1. Normalise `\r\n` to `\n`.
  2. Prefix a `\n` and split on `\n```json\n`. Fewer than two parts means no block.
  3. Take the **last** part, prefix it with `\n`, and split on `\n````. Fewer than two parts means no block.
  4. The text after the first closing fence must hold only spaces, tabs, `\r` and `\n`; anything else means no block.
  5. The block is the text before that closing fence, parsed with `json.loads`.

  Prose before the block, and earlier `json` blocks, are tolerated, because the last opening fence is taken. Trailing text after the block is refused, as in the pilot (`harness-runs/lessons.md` → *"check every position the tool can put it"*).
- [ ] `tests/session_events.py` is a support module with a docstring opening *"The rule this module exists to enforce"*: every fake stream carries the fields a real 2.1.332 session's events carry. It exposes `init_event(tools: Sequence[str], session_id: str = "s-1") -> str`, a `system`/`init` JSON line with `tools` and `session_id`. It also exposes `result_event(text: str, *, subtype: str = "success", is_error: bool = False, total_cost_usd: float = 0.25, cache_creation_input_tokens: int = 1000, cache_read_input_tokens: int = 2000, model_usage: Mapping[str, object] | None = None, permission_denials: int = 0) -> str`. That returns a `type: "result"` JSON line carrying `result`, `session_id`, `total_cost_usd`, `usage.cache_creation_input_tokens`, `usage.cache_read_input_tokens`, `modelUsage` and a `permission_denials` list of that length, plus `return_block(document: Mapping[str, object], prose: str = "Done.") -> str`, prose followed by a fenced `json` block. **Task 4's test imports these three names; this task owns the module.**
- [ ] `tests/test_session_stream.py` has a docstring opening *"The rule this file exists to enforce"* and plants a minimal draft-07 schema in the test, one `oneOf` variant with `outcome` `const` `PASS` and a string `findings_file`. Include:
  - one case per numbered clause above, each asserting the exact `Failed` reason literal;
  - the withheld case: declared `Read, Glob, Grep, Bash, Write`, `init` `Read, Write, Bash`, so the result is `Completed` with `withheld_tools == ("Glob", "Grep")`;
  - a relative `findings_file` that becomes `cwd / <path>`, and an absolute one kept as given;
  - an undeclared outcome returned as `Completed` (with a schema that allows it);
  - prose plus two `json` blocks, where the last one is read;
  - trailing prose after the block, which gives no return block;
  - CRLF line endings;
  - a non-JSON line between events, which is skipped;
  - the usage fields read on a `Failed` session as well as a `Completed` one.

**Verification:**

- `tests/test_session_stream.py` passes. Every expected reason and field is a literal written from this file's rules, never taken from `judge_session`'s output.
- `bash scripts/typecheck.sh` reports nothing in the three targets. `session_stream.py` imports from `graphscene` only names in `graphscene.__all__`, and from this package only `devscene_flow_host.records.plugin_contracts`.
