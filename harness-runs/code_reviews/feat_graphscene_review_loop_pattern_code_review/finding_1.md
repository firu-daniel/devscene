### 1. Two schema dependency clauses the branch adds are never exercised: a writer-less round carrying `plan`, `revisionNote`, `counter` or `convergingFrom`, and a writer with no `convergingFrom`

**File:** `graphscene/src/graphscene/schemas/flow-graph.schema.json` (`definitions.roundNode.dependencies`) — `"plan": ["writer"]`; tests go in `graphscene/tests/facade/test_loading.py` (beside `test_a_schema_negative_is_rejected_at_the_schema_stage`)

The branch adds five `dependencies` entries to `roundNode`: `"writer": ["counter", "convergingFrom"]`, `"counter": ["writer"]`, `"convergingFrom": ["writer"]`, `"plan": ["writer"]`, `"revisionNote": ["writer"]`. The story index states two rules on them (`## Context`: the three keys are "present together or absent together", and "`plan` and `revisionNote` are allowed only on a round that declares `writer`"). Only one clause is tested: `schema_negative_writer_without_counter.json` drops `counter` from a round that keeps `writer`. Nothing tests the four reverse entries or the `convergingFrom` half of the `writer` entry. If any of those lines were deleted, every test in the suite would still pass. A writer-less round carrying `counter` or `plan` would then load as a plain round and silently drop keys its author meant to opt in with. The task plan did not ask for these cases, so this is a coverage gap, not a plan violation.

Confirmed by reading only. I searched the branch diff and `graphscene/tests/` for a case that adds any of the four keys to a writer-less round, or drops `convergingFrom` from a round that keeps `writer`, and found none. I did not run the suggested test. The expected violation path (`nodes.checks` / `nodes.review_round`, the object that carries the triggering key) is inferred from the existing `("schema_negative_writer_without_counter.json", "nodes.review_round")` entry in `_SCHEMA_NEGATIVES`, which is the same kind of `dependencies` failure.

**Fix:** in `graphscene/tests/facade/test_loading.py`, add these two tests after `test_a_schema_negative_is_rejected_at_the_schema_stage`. Then add one clause to the module docstring's rule sentence: "a round that does not declare `writer` but carries `counter`, `convergingFrom`, `plan` or `revisionNote`, and a round declaring `writer` without `convergingFrom`, are rejected at the schema stage".

```python
@pytest.mark.parametrize(
    ("key", "value"),
    [("counter", "attempt"), ("convergingFrom", 1), ("plan", ["article"]), ("revisionNote", "article")],
)
def test_a_review_loop_key_on_a_round_without_a_writer_is_rejected_at_the_schema_stage(
    key: str, value: object
) -> None:
    graph = copy.deepcopy(_parsed("valid_plain_round.json"))
    nodes = graph["nodes"]
    assert isinstance(nodes, dict)
    nodes["checks"][key] = value
    with pytest.raises(GraphError) as raised:
        load_graph(graph)
    assert raised.value.stage == "schema"
    assert "nodes.checks" in [violation.path for violation in raised.value.violations]


def test_a_writer_without_converging_from_is_rejected_at_the_schema_stage() -> None:
    graph = copy.deepcopy(_parsed("valid_generic.json"))
    nodes = graph["nodes"]
    assert isinstance(nodes, dict)
    del nodes["review_round"]["convergingFrom"]
    with pytest.raises(GraphError) as raised:
        load_graph(graph)
    assert raised.value.stage == "schema"
    assert "nodes.review_round" in [violation.path for violation in raised.value.violations]
```

These tests are planted in place, not committed fixtures, so they need no `package.json` or `_FIXTURE_NAMES` wiring. This fix edits only that one test file, so run only that file, from the repository root:

```
bash scripts/python-service.sh --package graphscene test tests/facade/test_loading.py
```
