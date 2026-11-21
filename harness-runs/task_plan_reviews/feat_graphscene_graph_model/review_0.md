# Task plan review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **`task_1_plan.md` and `task_2_plan.md` — the immutability cases do not say how to pass `mypy` `strict`.**
   - Task 1's `test_errors.py` asks that "assigning `path` raises `dataclasses.FrozenInstanceError`". Task 2's `test_model.py` asks the same for an attribute, and adds that "item assignment on `graph.nodes` raises `TypeError`".
   - Written plainly (`v.path = "y"`, `graph.nodes["x"] = …`), those statements are rejected by `mypy` `strict`, which `graphscene/pyproject.toml` → `[tool.mypy]` runs over `tests`:
     - assigning to a frozen-dataclass attribute is `[misc]` ("Property … is read-only");
     - indexed assignment on a `Mapping` is `[index]`.
   - The obvious workaround, `setattr(v, "path", …)`, trips `ruff`'s `B010`, which is in the configured `B` set.
   - Neither task's unit run reaches `mypy` (`.claude/context/graphscene.md` → `## Tests`: graded only by gate 13's leg `13f`). Both files say only that "full annotations" leave those legs "nothing to find", so the break would first show up in the Run gates phase.
   - **Fix:** in each of the two files, name the form these cases take, e.g. a targeted `# type: ignore[misc]` / `# type: ignore[index]` on the one offending line inside the `pytest.raises` block. That ignore is a used ignore, so strict's `warn_unused_ignores` stays quiet.
   - Graded Should Fix rather than Must Fix: an implementer who knows `mypy` can still write it correctly, so I cannot say for certain that the failure will happen.

## Nice to Have

1. **`task_1_plan.md` — the `test_vocabulary.py` docstring goes partly stale after Task 3.**
   - Its *"Deliberately not covered"* item says the fixtures are validated against the schema "from the repository root". After Task 3 they are also validated through `graphscene.loader`.
   - Task 3 updates the matching sentence in `test_flow_graph_schema.py` but not this one. Task 1 already rewrites this docstring, so it could add a pointer to `tests/test_loader.py`. It is a docstring only.
2. **`task_1_plan.md` to `task_3_plan.md` — the `__all__` entries land in Task 4 instead of with each module.**
   - `.claude/context/graphscene.md` → `## What accompanies a new module` says a public name "lands with its `__all__` entry".
   - The plan puts all of `__init__.py` in Task 4 to keep one owner per file, so `Violation`, the model types and `load_graph` are not root-exported for three commits. Nothing fails in between, and the branch ends correct.
   - One sentence in the story index's `## Context` saying this split is deliberate would stop a later reader from taking it for an omission.
