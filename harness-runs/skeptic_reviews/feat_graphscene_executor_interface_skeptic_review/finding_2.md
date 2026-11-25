### 2. The comment justifying the `Any` cast in `return_violations` claims a non-JSON value is reported as a violation, and it is not

**File:** `graphscene/src/graphscene/adapters/return_schema.py` (`return_violations`) — "the runtime accepts any object and reports a non-JSON value as a violation"

**Why this is a finding.** The comment justifies widening `document` to `Any` before it reaches `iter_errors`:

```python
    # The `Validator` protocol's stub narrows `instance` to JSON types; the runtime accepts any
    # object and reports a non-JSON value as a violation.
    instance: Any = document
```

The second clause is false. jsonschema reports a non-JSON value only where a keyword such as `type` checks that position. A non-JSON value anywhere else passes with no violation.

The reader who gets this wrong is the maintainer of `return_violations`, or an executor author (#421) reading this function to decide whether it guards a parsed return. They will conclude that a document carrying a non-JSON value is always rejected, so they will add no check of their own. But a document like that is accepted.

**Evidence (probe run).** `bash scripts/python-service.sh --package graphscene probe harness-runs/scratch/skeptic_probe.py`, run against this branch's tree, printed `non-JSON doc -> [] []` for `return_violations({"a": object()}, {"type": "object"})`: no violation.

**Fix.** In `graphscene/src/graphscene/adapters/return_schema.py`, replace the two comment lines above `instance: Any = document` with:

```python
    # The `Validator` protocol's stub narrows `instance` to JSON types; the runtime accepts any
    # object, and reports a non-JSON value only where a keyword such as `type` checks it.
```

No code or test change. This edit runs no test file.
