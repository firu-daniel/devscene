### 2. A missing package directory is reported as "is git on PATH?", after git has already answered

**File:** `scripts/python-service.sh` (the per-package `cd` just above `export_locations "$package"`): "if ! cd \"$repo_root/$package\"; then"

The branch split the old combined resolve-and-`cd` check into two parts. The first is the `git rev-parse` check, and its message correctly asks whether git is on `PATH`. The second is a `cd` into the selected package, which runs only after `repo_root` has resolved. That second check reuses the first one's text unchanged:

```
echo "python-service: could not resolve ${package}/ from '${script_dir}' (is git on PATH?)" >&2
```

By the time the `cd` runs, git has already answered. The only failure left is that the table row's directory is missing (or cannot be entered) under the repository root. So the parenthetical sends the reader to check the one thing that is known to work. No step fails because of this, so it is graded Nice to Have.

**Fix:** replace that `echo` line in the per-package `cd` block, and leave the earlier `[ -z "$repo_root" ]` block's message as it is:

```bash
if ! cd "$repo_root/$package"; then
  echo "python-service: no ${package}/ directory under the repository root '${repo_root}'" >&2
  exit 1
fi
```

`cli/test/python-service.test.mjs` asserts no text for this path, so the fix edits no test file and runs no test. The full suite runs later, in the Run gates phase.
