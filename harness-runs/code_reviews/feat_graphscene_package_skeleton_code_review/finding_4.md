### 4. The boundary test's "Deliberately not covered" list omits the dynamic-import forms its scanner cannot see

**File:** `graphscene/tests/test_boundary.py` (module docstring): "Deliberately not covered:"

Rule (b) recognises a dynamic import in three forms only:
- the attribute call `importlib.import_module(...)`;
- the bare names `import_module` / `__import__`;
- a call whose module name is the first positional argument and a string constant.

The docstring's "Deliberately not covered" list names only "An import whose module name is computed at run time". Three more constant-name forms also go unflagged, and the list does not say so:
- an aliased importer, `from importlib import import_module as load` then `load("yaml")`;
- a keyword argument, `import_module(name="yaml")`;
- another route, `builtins.__import__("yaml")` or `importlib.__import__("yaml")`.

Someone who later extends the library would reasonably take the list as complete.

**Fix:** add one bullet to the docstring's "Deliberately not covered:" list, after the existing two:

```
- A constant-name dynamic import the scanner does not recognise as one: an importer bound to
  another name (`from importlib import import_module as load`), a module name passed by keyword
  (`import_module(name=...)`), or `__import__` reached through a module (`builtins.__import__`).
```

This is a docstring-only edit, so the fix runs no test.
