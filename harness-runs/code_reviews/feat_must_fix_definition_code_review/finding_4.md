### 4. The walker header's `--skipped` line lost its column alignment

**File:** `cli/templates/scripts/flow-walker.sh` (the `USAGE` header comment) — "#   --skipped the run mode's skipped ids"; the same line in `scripts/flow-walker.sh`

The edit that extended the `--findings` description also removed one space from the `--skipped` line. Its description now starts one column left of those on the `--node` and `--findings` lines.

**Fix:** in both copies, change the start of that line to:

```bash
#   --skipped  the run mode's skipped ids; read only when no flow-progress
```
