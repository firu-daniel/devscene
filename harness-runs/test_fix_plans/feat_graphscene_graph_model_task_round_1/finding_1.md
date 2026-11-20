### 1. `loader.py` puts two blank lines between its imports and `_ECMA_DOT`, failing `ruff` `I001`

**File:** `graphscene/src/graphscene/loader.py` (module top level) — between "from graphscene.vocabulary import vocabulary_violations" and "_ECMA_DOT = " (around lines 29–32, a navigation hint only)

**Failing test:** none — 13e GraphScene lint

**Class:** Broken contract

**Failure:** If the Run gates phase runs gate 13's leg `13e GraphScene lint` (`ruff` over `graphscene/`, rule set `I` selected in `graphscene/pyproject.toml` → `[tool.ruff.lint]`), then it exits 1 with "help: Organize imports" over `loader.py`'s import block and "Found 1 error.", failing the test gate.

**Failure quoted from the log** (gate `test`, leg `13e`; class: new this round — round 1, no earlier log):

```
  FAIL  13e GraphScene lint (exit 1, 0 s)
           |
        17 |   """
        18 |
        19 | / import json
        20 | | import os
        21 | | from collections.abc import Iterable
        22 | | from functools import cache
        23 | | from importlib.resources import files
        24 | |
        25 | | from jsonschema import Draft7Validator
        26 | |
        27 | | from graphscene.errors import GraphError, Violation
        28 | | from graphscene.model import FlowGraph, build_flow_graph
        29 | | from graphscene.vocabulary import vocabulary_violations
           | |_______________________________________________________^
        help: Organize imports
           |
        30 |
           -
        31 | _ECMA_DOT = "[^\\n\\r\\u2028\\u2029]"
           |

        Found 1 error.
        [*] 1 fixable with `--fix`.
        13 files already formatted
```

**Diagnosis.** Checked against the current tree: the three import groups themselves are already in `I001` order (standard library, then `jsonschema`, then first-party `graphscene`, each alphabetised and separated by one blank line), so the order is not what fails. What fails is the gap after the block: the current file has **two** blank lines between `from graphscene.vocabulary import vocabulary_violations` and `_ECMA_DOT = "[^\\n\\r\\u2028\\u2029]"`. `ruff`'s isort rule runs with the default `lines-after-imports` (automatic), which wants two blank lines only when the next statement is a `def`, `class` or decorator, and one before any other statement — here a module-level assignment. The help hunk's `-` marks exactly that one surplus blank line for removal. The formatter half of the leg passed (`13 files already formatted`), and a single blank line there is also format-clean, so removing the line satisfies both halves. Every other leg of gate 13 (`13a`–`13c`, `13f`, `13g`) passed, so nothing else in `graphscene/` is implicated. The gap came in with Skeptic review finding 1's change, which inserted `_ECMA_DOT` and `_ecma_pattern` directly after the imports.

**Fix.**

- [ ] In `graphscene/src/graphscene/loader.py`, delete one of the two blank lines between `from graphscene.vocabulary import vocabulary_violations` and `_ECMA_DOT = "[^\\n\\r\\u2028\\u2029]"`, leaving exactly one blank line there.
- [ ] Leave the two blank lines between `_ECMA_DOT = …` and `def _ecma_pattern(` as they are, and change nothing else in the file — no import is reordered, renamed or removed.
