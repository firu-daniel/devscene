# Task plan review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **`task_2_plan.md` — the declared `Mapping[str, object]` schema type is wider than the reused translator walks.** The contract block declares `def return_violations(document: object, schema: Mapping[str, object]) -> list[Violation]`. The Work bullet then reuses `graphscene/src/graphscene/adapters/schema.py` → `_ecma_patterns`, whose body rewrites only `isinstance(node, dict)` and `isinstance(node, list)` nodes and returns any other node unchanged. A `Mapping` that is not a `dict` is therefore not walked. One example is a `types.MappingProxyType`, which `.claude/context/graphscene.md` → `## The model and its wire forms` makes this package's own mapping type. Its `pattern` keywords stay untranslated, or the implementer's `assert isinstance(schema, dict)` (as `_validator` does) fails on an input the signature admits. No test case covers a non-`dict` schema, because every case plants a dict literal.
   **Fix:** narrow the parameter to the JSON shape the translator handles, `dict[str, object]` as `json.loads` returns it, and say so in the docstring's *"The rule:"*. Alternatively, copy the schema into plain `dict`s and `list`s before `_ecma_patterns` and add a case that passes a `MappingProxyType` schema carrying `"pattern": "^a$"` and asserts `"a\n"` fails.

## Nice to Have

1. **Story index (`feat_graphscene_executor_interface_story_plan.md`) → `Top risks:`, first bullet.** It reads *"The three tasks drift apart on the contract"*, but the plan has four tasks, and the same bullet goes on to name Tasks 2–4. *"The tasks drift apart"* would match the readiness list.
