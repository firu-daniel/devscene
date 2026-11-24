### 1. The test header points at "`round_gates`' rule above", but that rule is in another file

**File:** `devscene-flow-host/tests/test_round_gates.py` (the module docstring): "from `round_gates`' rule above and"

The header that Task 1 rewrote now says the held-gate cases' expected values are written "from `round_gates`' rule above and `flow-walker.sh` → `OUTPUT`'s `<escalate>` grammar". Nothing above that sentence in `test_round_gates.py` states the held-gate rule. The header's first paragraph covers the refused-file rule, and its third paragraph gives a one-sentence summary of the held-gate order. The rule the cases are written from is the bullet in `devscene-flow-host/src/devscene_flow_host/host/round_gates.py`'s module docstring, under *"The rule:"*: "A held gate at a join whose only gates out are refused ones does not escalate there". Everywhere else, this branch cites that bullet by file and heading, as in `devscene-flow-host/README.md` (`host/round_gates.py` → *"The rule:"*). The word "above" therefore sends a reader to the wrong place, and the header is the only spot that cites the rule without naming its file.

This is a docstring wording fix. It changes no behaviour.

**Fix:** in the module docstring of `devscene-flow-host/tests/test_round_gates.py`, replace

```
`revision_findings` writers, and, for the held-gate cases, from `round_gates`' rule above and
```

with

```
`revision_findings` writers, and, for the held-gate cases, from `host/round_gates.py` →
*"The rule:"* and
```

Then re-wrap the rest of that sentence so that no line goes over 100 characters (`ruff` `line-length = 100`). Do not change any other line of the docstring, and do not touch any test body.
