"""The rule this file exists to enforce: the `graphscene` command line prints one ASCII-only JSON
document and a newline on stdout for every command, and exits 0 for a loaded graph or a returned
action, 1 for a rejected graph with its check document, 2 for usage, 3 for a `Refused` and 4, with
one `graphscene: ` line on stderr and nothing on stdout, for an input it could not read or use; and
`graphscene/pyproject.toml` declares it as the console script `graphscene`.

This facade suite names `graphscene.facade.cli` rather than importing from `graphscene`: the
command's Python entry is deliberately not public, and its real caller is a process, which the
subprocess case runs.

Every expected value is hand-written from reading `valid_generic.json`, the `static_negative_*.json`
and `schema_negative_*.json` fixtures and the library's refusal texts, never taken from the
command's output. The check document's own cases are
`graphscene/tests/adapters/test_check_json.py`'s; this suite checks that the command prints it and
exits as the contract says.
"""

import io
import json
import subprocess
import sys
import tomllib
from pathlib import Path

from graphscene.facade.cli import main

_ROOT = Path(__file__).parents[2]
_FIXTURES = _ROOT / "tests" / "fixtures" / "flow_graph"
_GRAPH = str(_FIXTURES / "valid_generic.json")
_STATIC_NEGATIVE = str(_FIXTURES / "static_negative_node_known.json")
_SCHEMA_NEGATIVE = str(_FIXTURES / "schema_negative_no_vocabulary.json")

_DRAFT: dict[str, object] = {
    "kind": "dispatch",
    "node": "draft",
    "agent": "article-writer",
    "prompt": None,
    "counters": {"attempt": 0},
    "round_number": 0,
    "converging": None,
    "closed_round": [],
    "passed": [],
}


def _editor_set(number: int) -> dict[str, object]:
    return {
        "kind": "set",
        "round": "review_round",
        "number": number,
        "dispatches": [
            {
                "kind": "dispatch",
                "node": "edit_check",
                "agent": "article-editor",
                "prompt": None,
                "counters": {"attempt": 0},
                "round_number": number,
                "converging": False,
                "closed_round": [],
                "passed": [],
            }
        ],
        "passed": [],
    }


def _run(*argv: str) -> tuple[int, str, str]:
    stdout, stderr = io.StringIO(), io.StringIO()
    status = main(list(argv), stdout=stdout, stderr=stderr)
    return status, stdout.getvalue(), stderr.getvalue()


def _document(text: str) -> object:
    assert text.endswith("\n")
    assert text.count("\n") == 1
    return json.loads(text)


# check


def test_check_of_a_valid_graph_exits_0_with_the_empty_document() -> None:
    status, out, err = _run("check", _GRAPH)
    assert (status, err) == (0, "")
    assert _document(out) == {"stage": None, "violations": []}


def test_check_of_a_static_negative_exits_1_with_its_check_split_off() -> None:
    status, out, err = _run("check", _STATIC_NEGATIVE)
    assert (status, err) == (1, "")
    assert _document(out) == {
        "stage": "static",
        "violations": [
            {
                "path": "nodes.draft.outcomes.done.to",
                "check": "node-known",
                "reason": "'review' is not a node",
            }
        ],
    }


def test_check_of_a_schema_negative_exits_1_with_a_null_check() -> None:
    status, out, err = _run("check", _SCHEMA_NEGATIVE)
    assert (status, err) == (1, "")
    assert _document(out) == {
        "stage": "schema",
        "violations": [
            {"path": "", "check": None, "reason": "'vocabulary' is a required property"}
        ],
    }


def test_check_of_a_file_that_is_not_json_is_a_parse_stage_rejection(tmp_path: Path) -> None:
    graph = tmp_path / "graph.json"
    graph.write_text("{", encoding="utf-8")
    status, out, err = _run("check", str(graph))
    assert (status, err) == (1, "")
    assert _document(out) == {
        "stage": "parse",
        "violations": [
            {
                "path": "",
                "check": None,
                "reason": "not valid JSON: Expecting property name enclosed in double quotes "
                "(line 1, column 2)",
            }
        ],
    }


def test_check_of_a_missing_file_exits_4_on_stderr_only(tmp_path: Path) -> None:
    missing = tmp_path / "absent.json"
    status, out, err = _run("check", str(missing))
    assert (status, out) == (4, "")
    assert err.startswith("graphscene: ")
    assert str(missing) in err
    assert err.count("\n") == 1 and err.endswith("\n")


# a walk


def test_a_walk_starts_refuses_an_unanswered_skip_and_steps_with_an_answer(
    tmp_path: Path,
) -> None:
    state = str(tmp_path / "walk.json")

    status, out, _ = _run("start", _GRAPH, state)
    assert status == 0
    assert _document(out) == _DRAFT

    status, out, _ = _run("next", _GRAPH, state, "--outcome", "done")
    assert status == 3
    assert _document(out) == {
        "kind": "refused",
        "reason": "the host cannot answer predicate 'stage_disabled' for node 'edit_check'",
    }

    status, out, _ = _run(
        "next", _GRAPH, state, "--outcome", "done", "--answer", "stage_disabled=false"
    )
    assert status == 0
    assert _document(out) == _editor_set(0)

    status, out, _ = _run("current", _GRAPH, state)
    assert status == 0
    assert _document(out) == _editor_set(0)

    assert sorted(path.name for path in tmp_path.iterdir()) == ["walk.json", "walk.json.lock"]


def test_next_records_the_named_gate_with_its_detail(tmp_path: Path) -> None:
    state = str(tmp_path / "walk.json")
    assert _run("start", _GRAPH, state)[0] == 0
    answered = _run("next", _GRAPH, state, "--outcome", "done", "--answer", "stage_disabled=false")
    assert answered[0] == 0

    status, out, _ = _run(
        "next",
        _GRAPH,
        state,
        "--node",
        "edit_check",
        "--outcome",
        "rejected",
        "--detail",
        "findings/edit_0.md",
    )
    assert status == 0
    document = _document(out)
    assert isinstance(document, dict)
    assert document["node"] == "draft"
    assert document["closed_round"] == [
        {"gate": "edit_check", "outcome": "rejected", "detail": "findings/edit_0.md"}
    ]


def test_next_naming_a_node_that_is_not_pending_is_refused(tmp_path: Path) -> None:
    state = str(tmp_path / "walk.json")
    assert _run("start", _GRAPH, state)[0] == 0

    status, out, _ = _run("next", _GRAPH, state, "--node", "nope", "--outcome", "done")
    assert status == 3
    assert _document(out) == {"kind": "refused", "reason": "'nope' is not the pending node 'draft'"}


# refusals and environment failures


def test_start_at_a_node_that_is_not_an_entry_is_refused(tmp_path: Path) -> None:
    status, out, _ = _run("start", _GRAPH, str(tmp_path / "walk.json"), "--entry", "edit_check")
    assert status == 3
    assert _document(out) == {
        "kind": "refused",
        "reason": "'edit_check' is not an entry of flow 'article_review'",
    }


def test_current_before_any_start_is_refused(tmp_path: Path) -> None:
    status, out, _ = _run("current", _GRAPH, str(tmp_path / "walk.json"))
    assert status == 3
    assert _document(out) == {"kind": "refused", "reason": "no walk has started"}


def test_a_malformed_state_file_exits_4(tmp_path: Path) -> None:
    state = tmp_path / "walk.json"
    state.write_text("not a state", encoding="utf-8")
    status, out, err = _run("current", _GRAPH, str(state))
    assert (status, out) == (4, "")
    assert err.startswith(f"graphscene: {state}: ")


def test_a_malformed_resume_file_exits_4_naming_its_path(tmp_path: Path) -> None:
    resume = tmp_path / "resume.json"
    resume.write_text("{}", encoding="utf-8")
    status, out, err = _run("start", _GRAPH, str(tmp_path / "walk.json"), "--resume", str(resume))
    assert (status, out) == (4, "")
    assert err.startswith(f"graphscene: {resume}: ")


def test_a_valid_resume_enters_its_round_at_its_number(tmp_path: Path) -> None:
    resume = tmp_path / "resume.json"
    resume.write_text(
        json.dumps({"round": "review_round", "number": 2, "records": []}), encoding="utf-8"
    )
    status, out, _ = _run(
        "start",
        _GRAPH,
        str(tmp_path / "walk.json"),
        "--entry",
        "review_round",
        "--resume",
        str(resume),
        "--answer",
        "stage_disabled=false",
    )
    assert status == 0
    assert _document(out) == _editor_set(2)


def test_a_walk_on_a_rejected_graph_prints_the_check_document_and_writes_no_state(
    tmp_path: Path,
) -> None:
    status, out, _ = _run("start", _STATIC_NEGATIVE, str(tmp_path / "walk.json"))
    assert status == 1
    document = _document(out)
    assert isinstance(document, dict)
    assert document["stage"] == "static"
    assert list(tmp_path.iterdir()) == []


# usage


def test_an_answer_that_is_neither_true_nor_false_is_usage(tmp_path: Path) -> None:
    status, out, err = _run(
        "start", _GRAPH, str(tmp_path / "walk.json"), "--answer", "stage_disabled=maybe"
    )
    assert (status, out) == (2, "")
    assert err.startswith("usage: graphscene start")
    assert list(tmp_path.iterdir()) == []


def test_a_predicate_answered_twice_is_usage(tmp_path: Path) -> None:
    status, out, err = _run(
        "start",
        _GRAPH,
        str(tmp_path / "walk.json"),
        "--answer",
        "stage_disabled=true",
        "--answer",
        "stage_disabled=false",
    )
    assert (status, out) == (2, "")
    assert "given twice" in err


def test_no_sub_command_is_usage() -> None:
    status, out, err = _run()
    assert (status, out) == (2, "")
    assert err.startswith("usage: graphscene")


def test_help_goes_to_stdout_and_exits_0() -> None:
    status, out, err = _run("--help")
    assert (status, err) == (0, "")
    assert out.startswith("usage: graphscene")


# output


def test_a_lone_surrogate_is_escaped_in_ascii_output(tmp_path: Path) -> None:
    status, out, _ = _run("start", _GRAPH, str(tmp_path / "walk.json"), "--entry", "\udcff")
    assert status == 3
    assert out.isascii()
    assert "\\udcff" in out


# declaration and process


def test_the_console_script_is_declared() -> None:
    pyproject = tomllib.loads((_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert pyproject["project"]["scripts"]["graphscene"] == "graphscene.facade.cli:main"


def test_the_module_runs_as_a_process_and_writes_to_the_real_stdout(tmp_path: Path) -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "graphscene.facade.cli", "check", _GRAPH],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert (completed.returncode, completed.stderr) == (0, "")
    assert completed.stdout == '{"stage": null, "violations": []}\n'
