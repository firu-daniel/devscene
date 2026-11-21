### 1. `_ecma_pattern` translates only `$` and `.` and silently passes every other construct, so a later schema `pattern` can make `load_graph` and gate 3g's `ajv` disagree again

**File:** `graphscene/src/graphscene/loader.py` (`_ecma_pattern`, `_ecma_patterns`) — "def _ecma_pattern(pattern: str) -> str:"

**Problem.** `_ecma_patterns` rewrites every `pattern` keyword of the shipped `graphscene/src/graphscene/schemas/flow-graph.schema.json` through `_ecma_pattern` before `_validator` hands the schema to `jsonschema.Draft7Validator`. `_ecma_pattern` rewrites only an unescaped `$` (to `\Z`) and an unescaped `.` outside a class (to `_ECMA_DOT`). It copies every other character unchanged, and copies any backslash plus its next character as-is ("out.append(pattern[index : index + 2])"). That is correct for the eleven patterns the schema carries today. They use only literals, `^`, `$`, `.`, `*`, `+`, character classes with literal ranges (`[a-z0-9_]`, `[A-Za-z0-9.]`), and the escaped syntax characters `\{` and `\}`.

Nothing refuses a construct the translator does not handle, though. `schemas/validate.mjs` builds `new Ajv()` with default options, and ajv compiles a schema `pattern` as an ECMA-262 `RegExp` with the `u` flag. Python's `re`, on a `str` pattern, reads several constructs differently:

- `\d`, `\w`, `\s` and `\b` (and their negations) are Unicode-aware in Python and ASCII-only (or a different set) in ECMA-262.
- `\p{…}` is a Unicode property escape in ECMA `u` mode and an error in Python `re`.
- Python has no POSIX class: `[[:alpha:]]` reads as a nested `[`.
- Inline flags `(?i)`, named groups `(?P<…>)` / `(?<…>)` and lookbehind `(?<=…)` / `(?<!…)` differ in support or syntax.
- `\A`, `\Z` and a lone `{` are an anchor, an anchor and a literal in Python, and an identity escape or a syntax error under ECMA `u`.

A schema change that adds any of these would make `load_graph` accept or reject a graph that gate 3g (`npm run validate:graphscene-schema`) judges the other way, with no test failing. The skeptic review's Finding 1 closed exactly that divergence for `$` and `.`. The translator's docstring also does not say which constructs it supports.

The user asked for a guard that walks every `pattern` in the shipped schema and fails on any unhandled construct, naming the pattern and its schema path, and for a docstring stating the supported set. The fix below builds the refusal into the translator, so it fires whenever the validator is built, and adds tests that hold it.

**Fix:**

- [ ] **Make `_ecma_pattern` refuse what it does not translate.** In `graphscene/src/graphscene/loader.py`, change `_ecma_pattern` to take the pattern's schema path, `_ecma_pattern(pattern: str, path: tuple[str | int, ...]) -> str`. Give `_ecma_patterns` a matching `path: tuple[str | int, ...] = ()` parameter. It extends `path` with each dict key or list index as it recurses, and passes `path + ("pattern",)` when it rewrites a `pattern` string. Keep the existing `isinstance(child, str)` guard, so a property *named* `pattern` whose value is a subschema is still recursed. `_ecma_pattern` accepts **only** this set, read with the existing `in_class` scan, and raises `ValueError` on the first character sequence outside it:
  - Outside a character class:
    - a literal character that is not a metacharacter;
    - `^`, `$`, `.`, `|`, `*`, `+`, `?`;
    - a `{` that opens a well-formed quantifier `{n}`, `{n,}` or `{n,m}` (digits only), together with its closing `}`;
    - `(` not followed by `?`, the non-capturing opener `(?:`, and `)`;
    - `[`, opening a class.
  - Inside a class:
    - a literal character;
    - a leading `^`;
    - a `-` range between two literals;
    - the closing `]`.
    - A `[` inside a class is refused, which covers POSIX classes like `[[:alpha:]]`.
  - In either position: a backslash followed by one ECMA-262 syntax character, `^ $ \ . * + ? ( ) [ ] { } | /`. Inside a class only, `\-` too. These identity escapes read the same in both engines.

  Everything else is refused, in particular:
  - a backslash followed by a letter or digit (`\d \D \w \W \s \S \b \B \p \P \u \x \c \k \A \Z \n \t \1` …);
  - `(?` followed by anything but `:` (inline flags, named groups, lookahead and lookbehind);
  - an unescaped `{` that does not open a well-formed quantifier, and an unescaped `}` or `]` outside a class;
  - a trailing lone backslash.

  The error message is exactly:

  ```python
  f"{_render(path)}: schema pattern {pattern!r} uses {construct!r}, which _ecma_pattern does not translate to ECMA-262"
  ```

  `construct` is the refused sequence as written: the two-character escape, the `(?` plus its next character, the `[` inside a class, or the lone `{`, `}` or `]`. `_render` is the module's existing helper, already defined below `_validator`. Move it above `_ecma_pattern`, unchanged, so a refused identifier pattern reads `definitions.identifier.pattern: schema pattern …`. `_validator` keeps calling `_ecma_patterns(json.loads(...))` with no path argument, so a shipped-schema change that adds an unhandled construct raises the moment the validator is first built.

- [ ] **State the supported set in the docstrings.** Rewrite `_ecma_pattern`'s docstring to list the accepted constructs above in one or two sentences. Keep its current statement of the `$` and `.` rewrites, and add that any other construct raises `ValueError` naming the pattern's schema path, so a schema change forces a decision about the translator. In the module docstring, after "and its `.` against no line terminator.", add one sentence: a `pattern` using any construct outside the translator's supported set is refused when the validator is built, never passed to `re` untranslated.

- [ ] **Hold it with tests** in `graphscene/tests/test_loader.py`. Follow the layer's scanner-rule shape: one planted case per refused class, each asserting the exact message, plus a clean case and a run against the real tree. Import `_ecma_patterns` from `graphscene.loader`. Add these tests:
  - `test_every_shipped_schema_pattern_is_translatable`: `_ecma_patterns(json.loads(...))` over the shipped schema (read as `test_the_shipped_schema_is_a_valid_draft_7_schema` reads it) returns without raising.
  - One parametrized test, `test_an_untranslatable_pattern_construct_is_refused`. Each case passes `{"definitions": {"x": {"pattern": <p>}}}` and asserts `pytest.raises(ValueError)` with the exact message for path `definitions.x.pattern`, pattern `<p>` and the construct named. Cover at least: `^\d+$` (`\d`), `^\w+$` (`\w`), `^\s$` (`\s`), `\bx` (`\b`), `^\p{L}$` (`\p`), `(?<=a)b` (`(?<`), `(?i)abc` (`(?i`), `^[[:alpha:]]$` (`[`), `^a{x$` (`{`), and `^a]$` (`]`).
  - `test_a_refusal_names_a_nested_schema_path`: a pattern under a list and a dict (for example `{"anyOf": [{"properties": {"name": {"pattern": "\\d"}}}]}`) names `anyOf[0].properties.name.pattern`.
  - `test_supported_constructs_translate_unchanged_but_for_dollar_and_dot`: `^\{state_dir\}/.+/$`, `^[A-Za-z0-9][A-Za-z0-9.]*$`, `^(?:ab|c){2,3}$` and `^[^\]a-z]?$` come back with only the `$` and out-of-class `.` rewrites applied.

  Extend the module docstring's rule sentence ("and a schema `pattern` is matched as ECMA-262 matches it, …") with: "and a `pattern` using a construct the translator does not handle is refused, naming its schema path". The unit runs only this edited test file, through `bash scripts/python-service.sh --package graphscene test tests/test_loader.py`.
