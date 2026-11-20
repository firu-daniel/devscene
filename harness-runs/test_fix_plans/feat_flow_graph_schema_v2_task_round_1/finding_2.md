### 2. Gate 13f: `mypy` rejects `name = node.get("binding")` in `vocabulary.py`

**Site:** `graphscene/src/graphscene/vocabulary.py` → `_node_violations`, the terminal-node block `if node.get("kind") == "terminal":` / `name = node.get("binding")` (near line 150).

**Failing test:** none — `run-gates.sh` leg `13f GraphScene typecheck` (`mypy` strict over `graphscene/src` and `graphscene/tests`)

**Class:** Wrong behaviour

**Failure:** If gate 13f type-checks the `graphscene` package, then `mypy` fails with `src/graphscene/vocabulary.py:150: error: Incompatible types in assignment (expression has type "object", variable has type "str")  [assignment]`.

**Failure as logged:**

```
  FAIL  13f GraphScene typecheck (exit 1, 3 s)
        src/graphscene/vocabulary.py:150: error: Incompatible types in assignment (expression has type "object", variable has type "str")  [assignment]
        Found 1 error in 1 file (checked 5 source files)
```

**Diagnosis:** Earlier in `_node_violations`, the loop `for name, edge_value in routes.items():` binds `name`. `routes` is `_mapping(...)`, typed `dict[str, object]`, so `mypy` infers `name: str` for the rest of the function. The terminal block then reuses the same variable: `name = node.get("binding")`, where `node` is `Mapping[str, object]`, so the value is `object`. Under `strict = true` (`graphscene/pyproject.toml` → `[tool.mypy]`, and `.claude/context/graphscene.md` → `## The stack, in the words the rules below use`), assigning `object` to a variable already typed `str` is an `[assignment]` error. The code behaves correctly at runtime, because the `isinstance(name, str)` guard narrows the value before use, but the typecheck leg fails. The leg's own lint (13e) and tests (13g) pass.

**Fix:**

- [ ] In the terminal block of `_node_violations`, use a variable name that is new to the function: `binding_name = node.get("binding")`, `if isinstance(binding_name, str):`, `binding = bindings.get(binding_name)`, then `_undeclared_binding(node_path, binding_name)` and `f"{node_path}.binding: binding '{binding_name}' is not an end"`.
- [ ] Do not change the messages the function returns or the order it returns them in (the module docstring states that order).
- [ ] Do not add a `# type: ignore`, a `cast` or an `object` annotation on the loop variable.
- [ ] Check that `binding` is not already bound in that function with a type that conflicts. Today it is assigned only inside this block, so it keeps its `_Binding | None` type.
