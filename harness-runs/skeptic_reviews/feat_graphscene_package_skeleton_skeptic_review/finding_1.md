### 1. The boundary test flags a relative dynamic import as an outside import with an empty name

**File:** `graphscene/tests/test_boundary.py`, in `_dynamic_import_target`, at "if isinstance(first, ast.Constant) and isinstance(first.value, str):". Its consumer is `scan`, at "top = module.split(\".\")[0]".

**Problem.** For a static import, the scanner skips a relative import on purpose. `_imported_modules` returns `[]` for an `ast.ImportFrom` whose `level` is not `0`, and `test_a_clean_module_produces_no_violation` pins that `from . import sibling` and `from .sibling import thing` pass. Rule (b) has no such skip. `_dynamic_import_target` returns any string-constant first argument as it is. Two relative dynamic imports therefore reach `scan`'s allowed-set check as if they were absolute:

- **`importlib.import_module(".engine", __package__)`.** The target is `".engine"`, so `top = ".engine".split(".")[0]` is `""`. The empty string is not in `sys.stdlib_module_names | {"graphscene"}`, so the scanner records `__init__.py:<line>: imports , outside the allowed set`. The violation names no module.
- **`__import__("engine", globals(), None, [], 1)`, or the same call with `level=1`.** This is a relative import of the sibling `graphscene.engine`. The target is `"engine"`, which is not in the allowed set, so the scanner records `imports engine, outside the allowed set`.

Both forms stay inside the package, just as `from . import engine` does. The test's own rule statement in the module docstring is about what the library *reaches outside* itself.

**Runtime symptom.** The tree does not trigger this yet: `src/graphscene/__init__.py` holds no import. It is reachable as soon as the engine is added. If an engine module under `src/graphscene/` loads a sibling with `importlib.import_module(".<name>", __package__)`, then `test_the_real_library_stays_inside_its_boundary` fails, and gate 13's leg 13g fails with it. The failure message, `imports , outside the allowed set`, names no module, so it does not point at the cause.

**Proof.** In `_dynamic_import_target`, the only filters are "the call is a recognised importer" and "the first positional argument is a `str` constant". Nothing reads the argument's leading `.` or the call's `level`. In `scan`, `".engine".split(".")[0] == ""`, and `""` is not a member of `sys.stdlib_module_names` or of the declared-dependency names, so the `top not in allowed` branch appends the violation. Code review finding 4 covered the opposite gap: dynamic-import forms the scanner *misses*. This false positive is not covered by any committed review.

**Fix.** All edits are in `graphscene/tests/test_boundary.py`. Keep every line within the package's 100-column `ruff` limit. The lines below already are.

1. Replace the tail of `_dynamic_import_target`, from `first = call.args[0]` to the end of the function, with:

   ```python
       first = call.args[0]
       if isinstance(first, ast.Constant) and isinstance(first.value, str):
           if first.value.startswith(".") or _relative_level(call):
               return None
           return first.value
       return None
   ```

2. Add this function directly after `_dynamic_import_target`, separated from it and from the next function by two blank lines:

   ```python
   def _relative_level(call: ast.Call) -> bool:
       level: ast.expr | None = call.args[4] if len(call.args) > 4 else None
       for keyword in call.keywords:
           if keyword.arg == "level":
               level = keyword.value
       return isinstance(level, ast.Constant) and isinstance(level.value, int) and level.value != 0
   ```

   `__import__`'s fifth positional parameter is `level`. `import_module` takes at most two positional arguments and no `level` keyword, so the check never fires for it.

3. Add this test directly after `test_rule_b_flags_a_constant_dynamic_import_outside_the_allowed_set`, separated by two blank lines:

   ```python
   def test_a_relative_dynamic_import_is_not_flagged(tmp_path: Path) -> None:
       sources = {
           "dotted": 'import importlib\n\nimportlib.import_module(".engine", __package__)\n',
           "positional_level": '__import__("engine", globals(), None, [], 1)\n',
           "keyword_level": '__import__("engine", globals(), level=1)\n',
       }
       for name, source in sources.items():
           package = _plant(tmp_path / name, source)
           _, violations = scan(package, _STDLIB_AND_SELF)
           assert violations == [], name
   ```

   The existing rule (b) case `"dunder": '__import__("yaml")\n'` must still flag `yaml`: it passes no `level`.

4. In the module docstring, replace the paragraph that begins "`scan` parses every module" with:

   ```
   `scan` parses every module under `src/graphscene/` with `ast` and flags (a) an `import` or an
   absolute `from ... import` of a top-level name outside the allowed set; (b) a call to
   `importlib.import_module`, `import_module` or `__import__` with an absolute string-constant module
   name outside it (a relative one, with a leading `.` or a non-zero constant `level`, is skipped, as
   a relative `from` import is); (c) any top-level name from (a) or (b) starting with `devscene`,
   allowed or not; and (d) any string constant containing `devscene.config.json`.
   ```

This fix runs no test. No conventions document states a single-file command for a Python test, so this file's run is gate 13's leg 13g in the Run gates phase.
