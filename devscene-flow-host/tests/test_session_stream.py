"""The rule this file exists to enforce: `judge_session` classifies a finished `stream-json`
transcript in `PNL_REAP_JQ`'s order — one case per clause, each asserting the exact `Failed`
reason — reads the last fenced `json` block followed by nothing but whitespace as the return,
resolves a relative `findings_file` against the session's directory, returns an undeclared outcome
as `Completed`, and reads the usage fields on every classification.

Every stream is built from `session_events`, and every expected reason and field is a literal
written from the task plan's rules, never taken from `judge_session`'s output.

Deliberately not covered:
- A `ValueError` from an invalid return schema: `graphscene.return_violations`' own suite covers
  it, and it propagates through `judge_session` unchanged.
"""

from collections.abc import Mapping
from pathlib import Path
from types import MappingProxyType

from graphscene import Completed, Failed

from devscene_flow_host.host.session_stream import judge_session
from devscene_flow_host.records.plugin_contracts import AgentContract
from session_events import init_event, result_event, return_block

_SCHEMA: Mapping[str, object] = MappingProxyType(
    {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "oneOf": [
            {
                "type": "object",
                "required": ["outcome"],
                "additionalProperties": False,
                "properties": {
                    "outcome": {"const": "PASS"},
                    "findings_file": {"type": "string"},
                },
            }
        ],
    }
)
_OPEN_SCHEMA: Mapping[str, object] = MappingProxyType(
    {"$schema": "http://json-schema.org/draft-07/schema#", "type": "object"}
)
_TOOLS = ("Read", "Write")
_CWD = Path("/work/run")


def _contract(
    tools: tuple[str, ...] = _TOOLS, schema: Mapping[str, object] = _SCHEMA
) -> AgentContract:
    return AgentContract(agent="writer", tools=tools, return_schema=schema)


def _stream(*lines: str) -> str:
    return "\n".join(lines) + "\n"


def _passing(text: str = return_block({"outcome": "PASS"})) -> str:
    return _stream(init_event(list(_TOOLS)), result_event(text))


def test_clause_1_no_init_event_is_infra() -> None:
    reading = judge_session(
        _stream(result_event(return_block({"outcome": "PASS"}))), _contract(), _CWD
    )
    assert reading.result == Failed("infra", "the agent did not resolve: no init event")
    assert reading.withheld_tools == ()
    assert reading.session_id is None


def test_clause_2_an_undeclared_granted_tool_is_agent() -> None:
    stream = _stream(
        init_event(["Read", "Bash", "Write", "WebFetch"]),
        result_event(return_block({"outcome": "PASS"})),
    )
    reading = judge_session(stream, _contract(), _CWD)
    assert reading.result == Failed(
        "agent", "the init event grants tools the agent does not declare: [Bash, WebFetch]"
    )


def test_clause_3_no_result_event_is_undelivered() -> None:
    reading = judge_session(_stream(init_event(list(_TOOLS))), _contract(), _CWD)
    assert reading.result == Failed("undelivered", "no result event")
    assert reading.total_cost_usd is None
    assert reading.cache_creation_input_tokens is None
    assert reading.cache_read_input_tokens is None
    assert reading.model_usage == {}
    assert reading.permission_denials == 0


def test_clause_4_an_overloaded_error_is_undelivered_with_the_one_lined_text() -> None:
    text = "API Error: 529\r\n" + "x" * 300
    stream = _stream(init_event(list(_TOOLS)), result_event(text, subtype="success", is_error=True))
    reading = judge_session(stream, _contract(), _CWD)
    expected = "API error: " + ("API Error: 529  " + "x" * 300)[:200]
    assert reading.result == Failed("undelivered", expected)


def test_clause_4_each_marker_is_recognised() -> None:
    for marker in ("API Error: 500", "API Error: 503", "Overloaded"):
        stream = _stream(init_event(list(_TOOLS)), result_event(marker, is_error=True))
        reading = judge_session(stream, _contract(), _CWD)
        assert reading.result == Failed("undelivered", f"API error: {marker}")


def test_clause_5_is_error_without_a_marker_is_infra() -> None:
    stream = _stream(init_event(list(_TOOLS)), result_event("boom", is_error=True))
    reading = judge_session(stream, _contract(), _CWD)
    assert reading.result == Failed("infra", "the session ended as success with is_error")


def test_clause_5_a_subtype_other_than_success_is_infra() -> None:
    stream = _stream(init_event(list(_TOOLS)), result_event("", subtype="error_max_turns"))
    reading = judge_session(stream, _contract(), _CWD)
    assert reading.result == Failed("infra", "the session ended as error_max_turns")


def test_clause_5_a_missing_subtype_reads_as_no_subtype() -> None:
    stream = _stream(
        init_event(list(_TOOLS)), '{"type": "result", "is_error": false, "result": "x"}'
    )
    reading = judge_session(stream, _contract(), _CWD)
    assert reading.result == Failed("infra", "the session ended as no subtype")


def test_clause_6_no_fenced_block_is_infra() -> None:
    reading = judge_session(_passing("All done, no block."), _contract(), _CWD)
    assert reading.result == Failed("infra", "the result carries no return block")


def test_clause_6_an_unclosed_block_is_infra() -> None:
    reading = judge_session(_passing('Done.\n```json\n{"outcome": "PASS"}\n'), _contract(), _CWD)
    assert reading.result == Failed("infra", "the result carries no return block")


def test_clause_6_trailing_prose_after_the_block_gives_no_return_block() -> None:
    text = return_block({"outcome": "PASS"}) + "\nOne more thing.\n"
    reading = judge_session(_passing(text), _contract(), _CWD)
    assert reading.result == Failed("infra", "the result carries no return block")


def test_clause_7_a_block_that_is_not_one_object_is_infra() -> None:
    for body in ('["PASS"]', '{"outcome": "PASS"} {"outcome": "PASS"}', "not json"):
        reading = judge_session(_passing(f"Done.\n```json\n{body}\n```"), _contract(), _CWD)
        assert reading.result == Failed("infra", "the return block is not one JSON object")


def test_clause_8_a_return_failing_its_schema_is_infra() -> None:
    reading = judge_session(_passing(return_block({"outcome": "FAIL"})), _contract(), _CWD)
    assert reading.result == Failed(
        "infra",
        "the return fails its schema: (root): {'outcome': 'FAIL'} is not valid under any of the "
        "given schemas",
    )


def test_clause_9_a_return_without_a_non_empty_string_outcome_is_infra() -> None:
    for document in ({}, {"outcome": 3}, {"outcome": ""}):
        reading = judge_session(
            _passing(return_block(document)), _contract(schema=_OPEN_SCHEMA), _CWD
        )
        assert reading.result == Failed("infra", "the return carries no outcome")


def test_clause_10_a_valid_return_is_completed_without_detail() -> None:
    reading = judge_session(_passing(), _contract(), _CWD)
    assert reading.result == Completed("PASS", None)


def test_a_blank_findings_file_gives_no_detail() -> None:
    reading = judge_session(
        _passing(return_block({"outcome": "PASS", "findings_file": " \t"})), _contract(), _CWD
    )
    assert reading.result == Completed("PASS", None)


def test_a_relative_findings_file_is_joined_onto_cwd() -> None:
    text = return_block({"outcome": "PASS", "findings_file": "reviews/r1.md"})
    reading = judge_session(_passing(text), _contract(), _CWD)
    assert reading.result == Completed("PASS", "/work/run/reviews/r1.md")


def test_an_absolute_findings_file_is_kept_as_given() -> None:
    text = return_block({"outcome": "PASS", "findings_file": "/elsewhere/r1.md"})
    reading = judge_session(_passing(text), _contract(), _CWD)
    assert reading.result == Completed("PASS", "/elsewhere/r1.md")


def test_an_undeclared_outcome_is_still_completed() -> None:
    reading = judge_session(
        _passing(return_block({"outcome": "MAYBE"})), _contract(schema=_OPEN_SCHEMA), _CWD
    )
    assert reading.result == Completed("MAYBE", None)


def test_declared_tools_the_init_event_lacks_are_withheld_in_declared_order() -> None:
    declared = ("Read", "Glob", "Grep", "Bash", "Write")
    stream = _stream(
        init_event(["Read", "Write", "Bash"]), result_event(return_block({"outcome": "PASS"}))
    )
    reading = judge_session(stream, _contract(tools=declared), _CWD)
    assert reading.result == Completed("PASS", None)
    assert reading.withheld_tools == ("Glob", "Grep")


def test_a_declared_mcp_tool_is_never_withheld() -> None:
    declared = ("Read", "Write", "mcp__docs__search_docs")
    reading = judge_session(_passing(), _contract(tools=declared), _CWD)
    assert reading.withheld_tools == ()


def test_the_last_of_two_json_blocks_is_read() -> None:
    text = 'Draft:\n```json\n{"outcome": "FAIL"}\n```\n\nFinal:\n' + return_block(
        {"outcome": "PASS", "findings_file": "f.md"}
    )
    reading = judge_session(_passing(text), _contract(), _CWD)
    assert reading.result == Completed("PASS", "/work/run/f.md")


def test_crlf_line_endings_are_read() -> None:
    text = 'Done.\r\n\r\n```json\r\n{"outcome": "PASS"}\r\n```\r\n'
    stream = init_event(list(_TOOLS)) + "\r\n" + result_event(text) + "\r\n"
    reading = judge_session(stream, _contract(), _CWD)
    assert reading.result == Completed("PASS", None)
    assert reading.session_id == "s-1"


def test_a_non_json_line_between_events_is_skipped() -> None:
    stream = _stream(
        init_event(list(_TOOLS), session_id="s-9"),
        "warning: not an event",
        "[1, 2]",
        result_event(return_block({"outcome": "PASS"})),
    )
    reading = judge_session(stream, _contract(), _CWD)
    assert reading.result == Completed("PASS", None)
    assert reading.session_id == "s-9"


def test_the_last_result_event_is_judged() -> None:
    stream = _stream(
        init_event(list(_TOOLS)),
        result_event("", subtype="error_during_execution"),
        result_event(return_block({"outcome": "PASS"})),
    )
    reading = judge_session(stream, _contract(), _CWD)
    assert reading.result == Completed("PASS", None)


def test_the_usage_fields_are_read_on_a_completed_session() -> None:
    stream = _stream(
        init_event(list(_TOOLS), session_id="s-7"),
        result_event(
            return_block({"outcome": "PASS"}),
            total_cost_usd=1.5,
            cache_creation_input_tokens=11,
            cache_read_input_tokens=22,
            model_usage={"claude-opus": {"inputTokens": 5}},
            permission_denials=2,
        ),
    )
    reading = judge_session(stream, _contract(), _CWD)
    assert reading.result == Completed("PASS", None)
    assert reading.session_id == "s-7"
    assert reading.total_cost_usd == 1.5
    assert reading.cache_creation_input_tokens == 11
    assert reading.cache_read_input_tokens == 22
    assert reading.model_usage == {"claude-opus": {"inputTokens": 5}}
    assert reading.permission_denials == 2


def test_the_usage_fields_are_read_on_a_failed_session() -> None:
    stream = _stream(
        init_event(list(_TOOLS)),
        result_event("boom", is_error=True, total_cost_usd=0.75, permission_denials=1),
    )
    reading = judge_session(stream, _contract(), _CWD)
    assert reading.result == Failed("infra", "the session ended as success with is_error")
    assert reading.session_id == "s-1"
    assert reading.total_cost_usd == 0.75
    assert reading.cache_creation_input_tokens == 1000
    assert reading.cache_read_input_tokens == 2000
    assert reading.model_usage == {}
    assert reading.permission_denials == 1


def test_a_usage_field_of_the_wrong_type_is_none() -> None:
    stream = _stream(
        init_event(list(_TOOLS)),
        '{"type": "result", "subtype": "success", "is_error": false, "result": "x",'
        ' "total_cost_usd": "0.5", "usage": {"cache_creation_input_tokens": 1.5,'
        ' "cache_read_input_tokens": true}, "modelUsage": [], "permission_denials": 3}',
    )
    reading = judge_session(stream, _contract(), _CWD)
    assert reading.total_cost_usd is None
    assert reading.cache_creation_input_tokens is None
    assert reading.cache_read_input_tokens is None
    assert reading.model_usage == {}
    assert reading.permission_denials == 0
