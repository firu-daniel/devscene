### 2. `typos` flags the awk array name `nd` in the planning record library

**Site:** `cli/templates/scripts/lib/planning-record-lib.sh`, inside the single-quoted awk program assigned to `PRL_REWRITE_AWK=` (navigation hint: lines 310–338). The hits are the arrays `nd` and `kd` in its `BEGIN` block, e.g. `n++; nd[n] = ENVIRON["PRL_N_WT"]; kd[n] = "worktree"`, and in its main rule, `$0 = rewrite($0, nd[i], kd[i])`. Grep-verified: `nd[` appears 10 times in the file, all inside this program. That matches the log's 10 `— nd` lines.

**Failing test:** none — 6f shipped files pass typos (`scripts/check-typos.sh`)

**Failure (from the log):**

```
FAIL  6f shipped files pass typos (exit 1, 0 s)
      check-typos: cli/templates/scripts/lib/planning-record-lib.sh — nd
```

(The same line is printed 10 times, once per occurrence.)

**Diagnosis.** Gate 6f runs `typos` 1.51.1 with its default configuration over `cli/templates`, `plugin`, `schemas` and `cli/src`. It fails on any flagged word outside the deliberate set in `scripts/check-typos.sh`'s header (`ines`, `Ein`, `fo`, each keyed to one file). `typos` reads the identifier `nd` as a misspelling of "and". The planning record library is new on this branch, and it names the needle array `nd` and the parallel kind array `kd`. `kd` is not flagged, but renaming the pair together keeps them consistent. The program's meaning does not depend on these names: they are global awk arrays used only in `BEGIN` and in the main rule. The `rewrite()` function receives values through its own parameters (`needle`, `kind`), so it never reads the arrays directly.

**Fix.** Rename both arrays throughout the `PRL_REWRITE_AWK` program and change nothing else:

- [ ] `nd` → `needles` and `kd` → `kinds`, in every occurrence on the three `if (ENVIRON["PRL_N_…"] != "")` lines, on the sort line (`if (length(nd[j]) > length(nd[i])) { t = nd[i]; … }`) and in the main rule `{ for (i = 1; i <= n; i++) $0 = rewrite($0, nd[i], kd[i]); print }`. Do not reuse `needle` or `kind`: those are `rewrite()`'s parameter names, and a global with the same name would be shadowed there and would read as the same variable.
- [ ] Leave the `rewrite()` function, the `delim()` helper, the sort logic and the shell quoting of the program unchanged. Check that the program text still contains no `'` character, since it sits inside a single-quoted shell string.
- [ ] Do not add `nd` to `scripts/check-typos.sh`'s deliberate set. A renamed identifier is the fix. That set is reserved for words that cannot be respelled, such as a regular expression or a flag string.
- [ ] Confirm with a grep that `nd[` and `kd[` no longer appear in the file.
