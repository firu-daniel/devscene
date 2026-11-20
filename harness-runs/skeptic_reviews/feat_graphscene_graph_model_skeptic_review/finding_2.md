### 2. `load_graph_file` raises `UnicodeDecodeError`, not a parse-stage `GraphError`, on a file that is not UTF-8

**File:** `graphscene/src/graphscene/loader.py` (`load_graph_file`) — "with open(path, encoding=\"utf-8\") as handle:"

**Problem.** `load_graph_file` opens the file in text mode with `encoding="utf-8"` and the default `errors="strict"`. So `handle.read()` raises `UnicodeDecodeError` on any byte sequence that is not valid UTF-8, such as a Latin-1 `é` (`0xE9`) in a `description`. `UnicodeDecodeError` is neither of the two outcomes the branch's own text promises:

- `graphscene/src/graphscene/loader.py`, module docstring: the loader turns "parsed or on-disk data into the typed `FlowGraph` model, or into a `GraphError`".
- `graphscene/README.md` → `## What it is`, the `loader.py` row: `load_graph` and `load_graph_file` "return a `FlowGraph` or raise `GraphError`".
- `load_graph_file`'s docstring carves out only "an `OSError` propagates unchanged". `UnicodeDecodeError` is a `ValueError`, not an `OSError`.

A caller that catches `GraphError` to report a bad graph file therefore crashes on a mis-encoded one. The branch has a `parse` stage for exactly this case: bytes on disk that are not a JSON document. It is reached today only through `json.JSONDecodeError` (`test_a_file_that_is_not_json_is_rejected_at_the_parse_stage`).

**Fix:**

1. In `graphscene/src/graphscene/loader.py`, replace the first two statements of `load_graph_file`, the `with open(...)` block, with a binary read and a checked decode. The `try: parsed ... json.loads` block after them stays as it is.

   ```python
       with open(path, "rb") as handle:
           data = handle.read()
       try:
           text = data.decode("utf-8")
       except UnicodeDecodeError as error:
           reason = f"not valid UTF-8: {error.reason} (byte {error.start})"
           raise GraphError("parse", [Violation("", reason)]) from error
   ```

   Change the function's docstring to: `"""Read `path` as UTF-8 JSON and load it; a file that is not UTF-8 or not JSON is a parse-stage `GraphError`, and an `OSError` propagates unchanged."""`

2. In `graphscene/tests/test_loader.py`, add this case after `test_a_file_that_is_not_json_is_rejected_at_the_parse_stage`. In `b'{"flow": "\xe9"}'`, byte 10 is `0xE9`, a three-byte lead byte, and the byte after it is `"`, so UTF-8 decoding stops there with "invalid continuation byte".

   ```python
   def test_a_file_that_is_not_utf_8_is_rejected_at_the_parse_stage(tmp_path: Path) -> None:
       path = tmp_path / "graph.json"
       path.write_bytes(b'{"flow": "\xe9"}')
       with pytest.raises(GraphError) as raised:
           load_graph_file(path)
       assert raised.value.stage == "parse"
       assert raised.value.violations == (
           Violation("", "not valid UTF-8: invalid continuation byte (byte 10)"),
       )
   ```

`graphscene/tests/test_loader.py` is the test file this fix edits, so it is the only test file the fix runs: `bash scripts/python-service.sh --package graphscene test tests/test_loader.py`.
