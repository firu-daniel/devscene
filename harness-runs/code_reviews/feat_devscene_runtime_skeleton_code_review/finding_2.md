### 2. The requirement-name parser is copied into both `devscene-runtime` test files

**File:** `devscene-runtime/tests/test_graphscene_dependency.py` (`_dependency_name`, `_REQUIREMENT_NAME`) — "def _dependency_name(requirement: str) -> str:"; its twin is `devscene-runtime/tests/test_boundary.py` (`_dependency_name`, `_REQUIREMENT_NAME`).

**Problem.** Both test files in this suite define the same regex, `_REQUIREMENT_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")`, and the same `_dependency_name` body, character for character. `.claude/context/conventions.md` → `### Where a new responsibility goes` says "Before adding a copy of anything, grep for it", and `.claude/context/graphscene.md` → `## Tests` gives this repository's shape for code one package's suites share: a support module beside the tests (`graphscene/tests/engine/walk_support.py`). `docs-retrieval-service/tests/` does the same with `fakes.py` and `ts_bridge.py`, which its test files import by bare module name (`from fakes import …`), under the same `mypy` `files = ["src", "tests"]` / `mypy_path = "src"` settings this package uses. Today the two copies agree. But both tests depend on this normalisation: the boundary test's allowed set and the lock-staleness comparison. If someone changes one copy and not the other (Finding 1 already adds requirement parsing beside one of them), the two tests will name the same dependency differently.

**Fix.** Move the parser into one support module and import it in both files.

1. Create `devscene-runtime/tests/requirement_names.py`:

```python
"""The rule this module exists to enforce: this suite turns a PEP 508 requirement string into a
dependency name in one place, so the boundary test and the lock test always normalise a name the
same way (lower-cased, `-` as `_`).
"""

import re

_REQUIREMENT_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


def dependency_name(requirement: str) -> str:
    match = _REQUIREMENT_NAME.match(requirement.strip())
    if match is None:
        raise ValueError(f"unparseable dependency: {requirement!r}")
    return match.group(0).lower().replace("-", "_")
```

2. In `devscene-runtime/tests/test_boundary.py`:
   - Delete `_REQUIREMENT_NAME` and `_dependency_name`.
   - Add `from requirement_names import dependency_name` after `import graphscene`, as its own import block. It is first-party under `[tool.ruff] src = ["src", "tests"]`.
   - In `_declared_dependencies`, change `_dependency_name(entry)` to `dependency_name(entry)`.
   - Remove `import re` if nothing else in the file uses it.

3. In `devscene-runtime/tests/test_graphscene_dependency.py`:
   - Delete `_REQUIREMENT_NAME` and `_dependency_name`.
   - Add the same import.
   - Change every `_dependency_name(` call to `dependency_name(`.
   - Remove `import re` unless another regex in the file still uses it. Finding 1's `_REQUIREMENT` does, if it has landed.

The two test files this fix edits are the only tests it runs, each through `bash scripts/python-service.sh --package devscene-runtime test tests/<file>.py`.
