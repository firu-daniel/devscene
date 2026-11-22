### 2. `test_review_loop.py` and `review_loop.py` still say the three review-loop fields are required, which Task 4 made false

**File:** `graphscene/tests/engine/test_review_loop.py` (module docstring) — "the schema, the model and the builder require them"; and `graphscene/src/graphscene/engine/review_loop.py` (`_loop`) — "# Typed optional so this module needs no edit when the three fields become optional."

Task 1 wrote both texts while `RoundNode.writer`, `.counter` and `.converging_from` were still required. Task 4 then made them optional in the schema, the model and the builder. The test module's `Deliberately not covered:` bullet still says *"A built round node lacking the three fields: the schema, the model and the builder require them, so the absent case is pinned through `_loop` directly."* That is now false: `build_flow_graph` builds a writer-less round (`valid_plain_round.json`, which `test_builder.py` builds). A maintainer reading the header will think `review_loop` cannot be tested on a built plain round, so it never is. As a result, `review_loop(node)` on a real writer-less `RoundNode` has no case in its own suite. The code comment in `_loop` talks about a future that has already arrived. Both are durable code-level texts that no longer hold, so this is a Should Fix.

**Fix:**

1. In `graphscene/src/graphscene/engine/review_loop.py` → `_loop`, delete the line `    # Typed optional so this module needs no edit when the three fields become optional.`.
2. In `graphscene/tests/engine/test_review_loop.py`, replace the module docstring's second paragraph and its `Deliberately not covered:` section with:

```python
Graphs are built through `graphscene.adapters.builder.build_flow_graph`, from
`valid_generic.json`, `valid_plain_round.json` or a graph planted through
`graphscene/tests/engine/walk_support.py` → `planted`; every expected value is hand-written from
reading the graph. A round lacking only one or two of the three fields, which the schema refuses,
is pinned through `_loop` directly.
"""
```

3. Add this case after `test_the_fixture_round_is_a_review_loop`:

```python
def test_the_plain_round_fixture_is_no_review_loop() -> None:
    parsed: object = json.loads((_FIXTURES / "valid_plain_round.json").read_text(encoding="utf-8"))
    assert isinstance(parsed, dict)
    graph = build_flow_graph(parsed)
    node = graph.nodes["checks"]
    assert isinstance(node, RoundNode)
    assert review_loop(node) is None
    assert review_loops(graph) == ()
```

This fix edits one test file and one source module that file tests, so run only that file, from the repository root:

```
bash scripts/python-service.sh --package graphscene test tests/engine/test_review_loop.py
```
