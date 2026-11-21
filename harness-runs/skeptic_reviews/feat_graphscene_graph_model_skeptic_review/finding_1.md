### 1. `load_graph` accepts strings the schema's `pattern`s reject, because Python's `re` reads `$` and `.` differently from ECMA-262 and `ajv`

**File:** `graphscene/src/graphscene/loader.py` (`_validator`) — "return Draft7Validator(json.loads(resource.read_text(encoding=\"utf-8\")))"
**Class:** Wrong behaviour
**Failure:** If a caller passes `graphscene.load_graph` a parsed graph whose `flow` is `"article_review\n"` (or whose node id, outcome name, binding name, `start`, `to` or any other identifier ends with one newline), then `load_graph` returns a `FlowGraph`, while `node schemas/validate.mjs` (`ajv`, gate 3g) rejects the same document with `must match pattern "^[a-z][a-z0-9_]*$"`.

**Why it is wrong.** The loader's rule (`graphscene/src/graphscene/loader.py`, module docstring) is that "a returned graph has passed the format-4 schema this package ships". The story plan's second top risk is "The two validators disagreeing". `docs/development.md` → **Gate 3** now says that "`ajv` and the loader are held to the same fixtures". A JSON Schema `pattern` is an ECMA-262 regular expression, and `ajv` compiles it as one. `node_modules/ajv/dist/vocabularies/code.js` → `usePattern` calls `regExp(pattern, u)`, the default `new RegExp`, and `schemas/validate.mjs` builds `new Ajv()` with no options. In ECMA-262 without the `m` flag, `$` matches only at the end of the input, and `.` matches no line terminator (`\n`, `\r`, ` `, ` `).

`jsonschema` does not translate. `graphscene/.venv/.../jsonschema/_keywords.py` → `pattern` is `not re.search(patrn, instance)`, with the pattern passed to Python's `re` verbatim. In Python, `$` also matches **just before a trailing newline**, and `.` matches `\r`, ` ` and ` `.

Every anchored pattern in `graphscene/src/graphscene/schemas/flow-graph.schema.json` ends in `$`: `identifier`, `outcomeName`, `bindingName`, `predicateName`, `reasonName`, a predicate's `records`, `agent`, `findingsFolder`, `ledger` and a report value. So a value with one trailing `\n` passes every one of them in Python. `propertyNames` descends into the same `pattern` keyword (`_keywords.py` → `propertyNames`), so node ids and every other declared name are affected too. `findingsFolder` (`^\{state_dir\}/.+/$`) also accepts `"{state_dir}/a\rb/"` through its `.`. The vocabulary check and `build_flow_graph` never look at a name's characters, so the graph comes back typed. The branch's tests miss this because every committed `schema_negative_*.json` fixture differs from `valid_generic.json` in structure, never in a trailing line terminator.

This is net-new. The code review's Finding 3 is the integral-float `type` mismatch between the builder and `jsonschema`. This finding is a `pattern` mismatch between `jsonschema` and `ajv`, and that fix does not touch it.

**Fix:**

1. In `graphscene/src/graphscene/loader.py`, add these two helpers above `_validator`:

   ```python
   _ECMA_DOT = "[^\\n\\r\\u2028\\u2029]"


   def _ecma_pattern(pattern: str) -> str:
       """Rewrite `pattern` so Python's `re` reads it as ECMA-262 does: an unescaped `$` outside a
       character class matches only at the very end, and an unescaped `.` outside one matches no
       line terminator."""
       out: list[str] = []
       in_class = False
       index = 0
       while index < len(pattern):
           char = pattern[index]
           if char == "\\":
               out.append(pattern[index : index + 2])
               index += 2
               continue
           if in_class:
               in_class = char != "]"
               out.append(char)
           elif char == "[":
               in_class = True
               out.append(char)
           elif char == "$":
               out.append("\\Z")
           elif char == ".":
               out.append(_ECMA_DOT)
           else:
               out.append(char)
           index += 1
       return "".join(out)


   def _ecma_patterns(node: object) -> object:
       """Return a copy of the schema `node` with every `pattern` keyword rewritten by
       `_ecma_pattern`."""
       if isinstance(node, dict):
           return {
               key: (
                   _ecma_pattern(child)
                   if key == "pattern" and isinstance(child, str)
                   else _ecma_patterns(child)
               )
               for key, child in node.items()
           }
       if isinstance(node, list):
           return [_ecma_patterns(child) for child in node]
       return node
   ```

2. Replace the body of `_validator` with:

   ```python
       resource = files("graphscene") / "schemas" / "flow-graph.schema.json"
       schema = _ecma_patterns(json.loads(resource.read_text(encoding="utf-8")))
       assert isinstance(schema, dict)
       return Draft7Validator(schema)
   ```

   The shipped schema file stays unchanged. Only the in-memory copy the validator holds is rewritten, so `ajv` and `test_the_shipped_schema_is_a_valid_draft_7_schema` still read the file as written. A pattern-violation message now quotes the rewritten pattern, for example `... does not match '^[a-z][a-z0-9_]*\\Z'`. No existing test asserts a pattern message (`grep -rn "does not match" graphscene/src graphscene/tests` finds none).

3. In the same file's module docstring, add this paragraph directly after the paragraph that opens "The rule: a returned graph has passed the format-4 schema":

   ```
   A schema `pattern` is matched as ECMA-262, as `ajv` matches it: its `$` only at the very end of
   the string, never before a trailing newline, and its `.` against no line terminator.
   ```

4. In `graphscene/tests/test_loader.py`, add these two cases after `test_a_missing_required_field_names_the_node`. `valid_generic.json` declares `"flow": "article_review"`, and its node `draft` is a dispatch node without `findingsFolder`.

   ```python
   def test_a_trailing_newline_does_not_satisfy_an_anchored_pattern() -> None:
       graph = copy.deepcopy(_parsed("valid_generic.json"))
       graph["flow"] = "article_review\n"
       with pytest.raises(GraphError) as raised:
           load_graph(graph)
       assert raised.value.stage == "schema"
       assert [violation.path for violation in raised.value.violations] == ["flow"]


   def test_a_pattern_dot_does_not_match_a_line_terminator() -> None:
       graph = copy.deepcopy(_parsed("valid_generic.json"))
       _node(graph, "draft")["findingsFolder"] = "{state_dir}/a\rb/"
       with pytest.raises(GraphError) as raised:
           load_graph(graph)
       assert raised.value.stage == "schema"
       assert [violation.path for violation in raised.value.violations] == [
           "nodes.draft.findingsFolder"
       ]
   ```

5. Extend the opening docstring of `graphscene/tests/test_loader.py`. Its first sentence ends "...loads as an `int`." Make it end "...loads as an `int`; and a schema `pattern` is matched as ECMA-262 matches it, so a trailing newline or a `.` against a line terminator is rejected."

`graphscene/tests/test_loader.py` is the test file this fix edits, so it is the only test file the fix runs: `bash scripts/python-service.sh --package graphscene test tests/test_loader.py`.
