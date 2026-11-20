### 3. `load_graph` raises `TypeError` on a graph the schema accepts when an integer field is written as an integral float (`3.0`)

**File:** `graphscene/src/graphscene/model.py` (`_int`) — "if isinstance(value, bool) or not isinstance(value, int):"
**Class:** Wrong behaviour
**Failure:** If a caller passes `graphscene.load_graph` a parsed graph whose `counters.<name>.cap` is `3.0`, or whose round node's `convergingFrom` is `1.0`, then `load_graph` raises `TypeError: counters.<name>.cap: expected int`, or `TypeError: nodes.<id>.convergingFrom: expected int`. It neither returns a `FlowGraph` nor raises a `GraphError`.

The loader's contract (`graphscene/src/graphscene/loader.py`, module docstring) is that the schema check and the vocabulary check decide validity, and that every rejection is a `GraphError`. The builder's `TypeError` is reserved for "a shape the schema would have refused", which the docstring of `graphscene/src/graphscene/model.py` calls a programming error.

`Draft7Validator`, which the loader validates with, takes an integral float as an `integer`. The installed `jsonschema/_types.py` defines `draft6_type_checker` (and `draft7_type_checker = draft6_type_checker`) with `"integer"` redefined as `is_integer(checker, instance) or (isinstance(instance, float) and instance.is_integer())`. `ajv` accepts the same value too, because `JSON.parse("3.0")` is the number `3`. So a file holding `"cap": 3.0` passes both validators and the vocabulary check. `json.loads` returns that value as the Python `float` `3.0`. Then `build_flow_graph` → `_counter` → `_int` refuses it, because `isinstance(3.0, int)` is false. `_int` has exactly two callers, `cap` and `convergingFrom`, and those are the schema's only `"type": "integer"` fields. `formatVersion` is `const: 4` and is handled separately.

**Fix:**

1. In `graphscene/src/graphscene/model.py`, have `_int` accept what the schema accepts and normalise it to `int`:

   ```python
   def _int(value: object, path: str) -> int:
       if isinstance(value, float) and value.is_integer():
           return int(value)
       if isinstance(value, bool) or not isinstance(value, int):
           raise TypeError(f"{path}: expected int")
       return value
   ```

2. In the same file's module docstring, under *The mapping rules*, add this bullet after the *Absent keys* bullet:

   ```
   - Integers: a number the schema accepts as an integer, `3` or `3.0`, becomes an `int`.
   ```

3. In `graphscene/tests/test_loader.py`, add this case after `test_the_valid_generic_graph_loads`. `valid_generic.json` declares counter `attempt` with `cap` 3, and node `review_round` with `convergingFrom` 1.

   ```python
   def test_an_integral_float_where_the_schema_takes_an_integer_loads_as_an_int() -> None:
       graph = copy.deepcopy(_parsed("valid_generic.json"))
       counters = graph["counters"]
       assert isinstance(counters, dict)
       counters["attempt"]["cap"] = 3.0
       _node(graph, "review_round")["convergingFrom"] = 1.0
       loaded = load_graph(graph)
       assert type(loaded.counters["attempt"].cap) is int
       assert loaded.counters["attempt"].cap == 3
       review_round = loaded.nodes["review_round"]
       assert isinstance(review_round, RoundNode)
       assert type(review_round.converging_from) is int
       assert review_round.converging_from == 1
   ```

   Add `RoundNode` to that file's `from graphscene.model import FlowGraph` line, which becomes `from graphscene.model import FlowGraph, RoundNode`.

4. Extend the opening docstring of `graphscene/tests/test_loader.py`. Its first sentence currently ends "...and `valid_generic.json` loads." Make it end "...`valid_generic.json` loads; and a number the schema accepts as an integer, written `3.0`, loads as an `int`."

`graphscene/tests/test_loader.py` is the test file this fix edits, so it is the only test file the fix runs: `bash scripts/python-service.sh --package graphscene test tests/test_loader.py`.
