### 2. `next`'s `--node` and `--detail` flags are never exercised by the command line's suite

**File:** `graphscene/tests/facade/test_cli.py` (`test_a_walk_starts_refuses_an_unanswered_skip_and_steps_with_an_answer`) — "\"next\", _GRAPH, state, \"--outcome\", \"done\""

`graphscene/src/graphscene/facade/cli.py` → `_walk` passes `args.node` and `args.detail` to `walker.next(outcome, node, detail)`. `graphscene/README.md` → `## The command line` documents both flags in the `next` row. No case in `graphscene/tests/facade/test_cli.py` passes either one: every `next` call gives only `--outcome` and, in one case, `--answer`. Two kinds of drift would go unnoticed:

- The two flags swapped, for example `walker.next(outcome, detail, node)`.
- `--detail` dropped, so that a gate's record carries `null`.

Both would leave the whole suite green, and a host that names the gate in a round and passes a findings path would get the wrong record. The current code is correct. A probe confirmed it:

- **Command:** `bash scripts/python-service.sh --package graphscene probe harness-runs/scratch/branch_review_cli_node_detail.py graphscene/tests/fixtures/flow_graph/valid_generic.json`, which runs `start`, then `next --outcome done --answer stage_disabled=false`, then `next --node edit_check --outcome rejected --detail findings/edit_0.md`.
- **Result:** exit `0`, and a `draft` dispatch whose `closed_round` is `[{"gate": "edit_check", "outcome": "rejected", "detail": "findings/edit_0.md"}]`. A further `next --node nope --outcome rejected` exited `3` with `"'nope' is not the pending node 'draft'"`.

So this is missing coverage of documented flags, not a wrong result.

**Fix:** add two cases to `graphscene/tests/facade/test_cli.py`, under `# a walk`. Hand-write their expected values from the flags passed and from the library's refusal text, as the module docstring requires:

```python
def test_next_records_the_named_gate_with_its_detail(tmp_path: Path) -> None:
    state = str(tmp_path / "walk.json")
    assert _run("start", _GRAPH, state)[0] == 0
    assert _run("next", _GRAPH, state, "--outcome", "done", "--answer", "stage_disabled=false")[0] == 0

    status, out, _ = _run(
        "next", _GRAPH, state,
        "--node", "edit_check", "--outcome", "rejected", "--detail", "findings/edit_0.md",
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
```

Wrap the lines at `ruff`'s 100-column limit. Then run only that file, from the repository root, as one plain foreground command:

```
bash scripts/python-service.sh --package graphscene test tests/facade/test_cli.py
```
