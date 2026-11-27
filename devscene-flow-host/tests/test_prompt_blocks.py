"""The rule this file exists to enforce: `parse_prompt_source` accepts only
`<document> → ## <section> → ### <heading>` with a plugin-relative document, and
`read_prompt_blocks` returns a heading's fenced blocks as `pnl_core_scan` cuts them — scoped to its
section, fences hiding headings, CRs and trailing newlines stripped — raising `RecordError` with one
exact line, after `pnl_init`'s wording, for each document it cannot read.

Every case plants a document under `tmp_path` except one, which reads this checkout's tracked
planning core as read-only input. Every expected value is written from the task plan's rules or from
reading that core, never taken from the reader's output.

Deliberately not covered:
- An `OSError` other than a missing file, which propagates unwrapped: no portable way to plant one
  under `tmp_path`.
"""

from pathlib import Path

import pytest

from devscene_flow_host.records.errors import RecordError
from devscene_flow_host.records.prompt_blocks import (
    PromptSource,
    parse_prompt_source,
    read_prompt_blocks,
)

_CHECKOUT_PLUGIN = Path(__file__).resolve().parents[2] / "plugin"
_SOURCE = PromptSource(document="instructions/core.md", section="## Loop", heading="### 1. Spawn")


def _plant(plugin_dir: Path, data: bytes) -> Path:
    path = plugin_dir / "instructions" / "core.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def test_a_prompt_source_parses_into_its_three_parts() -> None:
    assert parse_prompt_source("instructions/core.md → ## Loop → ### 1. Spawn `a`") == PromptSource(
        document="instructions/core.md", section="## Loop", heading="### 1. Spawn `a`"
    )


@pytest.mark.parametrize(
    "value",
    [
        "instructions/core.md → ## Loop",
        "instructions/core.md → ## Loop → ### A → ### B",
        "instructions/core.md → Loop → ### A",
        "instructions/core.md → ## Loop → A",
        " → ## Loop → ### A",
        "/instructions/core.md → ## Loop → ### A",
        "instructions/../core.md → ## Loop → ### A",
    ],
    ids=[
        "two-parts",
        "four-parts",
        "section-without-prefix",
        "heading-without-prefix",
        "empty-document",
        "absolute-document",
        "dot-dot-segment",
    ],
)
def test_a_malformed_prompt_source_is_refused(value: str) -> None:
    with pytest.raises(ValueError) as error:
        parse_prompt_source(value)
    assert str(error.value) == (
        f"prompt source '{value}' is not '<document> → ## <section> → ### <heading>'"
    )


def test_two_blocks_under_one_heading_are_returned_in_order(tmp_path: Path) -> None:
    _plant(
        tmp_path,
        b"## Loop\n\n### 1. Spawn\n\nFirst:\n\n```\none\ntwo\n```\n\nThen:\n\n```\nthree\n```\n"
        b"\n### 2. Next\n\n```\nnot this\n```\n",
    )
    assert read_prompt_blocks(tmp_path, _SOURCE) == ("one\ntwo", "three")


def test_the_same_heading_under_another_section_is_not_matched(tmp_path: Path) -> None:
    _plant(
        tmp_path,
        b"## Other\n\n### 1. Spawn\n\n```\nother\n```\n\n"
        b"## Loop\n\n### 1. Spawn\n\n```\nmine\n```\n",
    )
    assert read_prompt_blocks(tmp_path, _SOURCE) == ("mine",)


def test_a_heading_line_inside_a_fence_is_not_read_as_a_heading(tmp_path: Path) -> None:
    _plant(tmp_path, b"## Loop\n\n### 1. Spawn\n\n```\n### 2. Next\n## Other\nkept\n```\n")
    assert read_prompt_blocks(tmp_path, _SOURCE) == ("### 2. Next\n## Other\nkept",)


def test_a_crlf_document_is_read_without_its_carriage_returns(tmp_path: Path) -> None:
    _plant(tmp_path, b"## Loop\r\n\r\n### 1. Spawn\r\n\r\n```\r\none\r\ntwo\r\n```\r\n")
    assert read_prompt_blocks(tmp_path, _SOURCE) == ("one\ntwo",)


def test_trailing_blank_lines_inside_a_fence_are_stripped(tmp_path: Path) -> None:
    _plant(tmp_path, b"## Loop\n\n### 1. Spawn\n\n```\none\n\n\n```\n")
    assert read_prompt_blocks(tmp_path, _SOURCE) == ("one",)


def test_a_missing_document_is_a_record_error(tmp_path: Path) -> None:
    with pytest.raises(RecordError) as error:
        read_prompt_blocks(tmp_path, _SOURCE)
    assert str(error.value) == (
        f"the prompt document '{tmp_path / 'instructions' / 'core.md'}' cannot be read"
    )


def test_a_document_that_is_not_utf8_is_a_record_error(tmp_path: Path) -> None:
    path = _plant(tmp_path, b"## Loop\n\xff\n")
    with pytest.raises(RecordError) as error:
        read_prompt_blocks(tmp_path, _SOURCE)
    assert str(error.value) == f"{path}: not UTF-8 text"


def test_a_missing_section_is_a_record_error(tmp_path: Path) -> None:
    path = _plant(tmp_path, b"## Other\n\n### 1. Spawn\n")
    with pytest.raises(RecordError) as error:
        read_prompt_blocks(tmp_path, _SOURCE)
    assert str(error.value) == f"the heading '## Loop' is not in '{path}'"


def test_a_section_without_the_heading_is_a_record_error(tmp_path: Path) -> None:
    path = _plant(tmp_path, b"## Loop\n\n### 2. Next\n\n## Other\n\n### 1. Spawn\n")
    with pytest.raises(RecordError) as error:
        read_prompt_blocks(tmp_path, _SOURCE)
    assert str(error.value) == f"the heading '### 1. Spawn' is not under '## Loop' in '{path}'"


def test_an_odd_number_of_fence_lines_is_a_record_error(tmp_path: Path) -> None:
    path = _plant(tmp_path, b"## Loop\n\n### 1. Spawn\n\n```\none\n```\n\n```\ntwo\n")
    with pytest.raises(RecordError) as error:
        read_prompt_blocks(tmp_path, _SOURCE)
    assert str(error.value) == (
        f"the heading '### 1. Spawn' carries 3 fence lines in '{path}', an unclosed block"
    )


def test_the_real_planning_core_yields_the_task_plan_writers_two_prompts() -> None:
    source = parse_prompt_source(
        "instructions/task_plan_writing_instructions_core.md → ## Loop → "
        "### 1. Spawn `task-plan-writer`"
    )
    blocks = read_prompt_blocks(_CHECKOUT_PLUGIN, source)
    assert len(blocks) == 2
    assert blocks[0].startswith("Write the task plan.")
    assert blocks[1].startswith("Revise the task plan per findings at")
