### 1. Rename the `fo` local in `record_in_set()` so typos stops flagging it

**Site:** `cli/templates/scripts/flow-walker.sh`, function `record_in_set()`. The local declaration is `local rn="$1" g="$A_NODE" n edge i=0 h first="" fo="" held=""` (around line 871), and `fo` is used three more times in the same function: `first="$GV"; fo="$SV"` in the join loop, `g_need "nodes.$first.outcomes.$fo.binding"`, and `reason: $fo$NL$held` in the `OUT=` binding action. The repository's self-adopted copy, `scripts/flow-walker.sh`, is byte-identical today and has the same four sites.

**Failing test:** none — `6f shipped files pass typos` (run by `scripts/check-typos.sh`).

**Failure (from the log):**

```
  FAIL  6f shipped files pass typos (exit 1, 0 s)
        check-typos: cli/templates/scripts/flow-walker.sh — fo
        check-typos: cli/templates/scripts/flow-walker.sh — fo
        check-typos: cli/templates/scripts/flow-walker.sh — fo
        check-typos: cli/templates/scripts/flow-walker.sh — fo
```

**Diagnosis:** `scripts/check-typos.sh` runs `typos 1.51.1` with its default dictionary over `cli/templates`, `plugin`, `schemas` and `cli/src`. Any hit fails the gate unless its `(path, word)` pair is in the script's short allowlist of deliberate words. `typos` reads `fo` as a misspelling of `of`/`for`. The only allowlisted `fo` is `plugin/hooks/lib/harness-config-lib.sh|fo`, the `--fo` option-prefix example. The four hits are the four occurrences of the shell local `fo` (short for "first held outcome") that Task 3 (`1bfba6ca`) added to `record_in_set()`. The variable is an abbreviation that can be renamed, not a deliberate word, so the right fix is a rename. Adding an allowlist entry would be wrong. `scripts/flow-walker.sh` sits outside the scanned trees and is not flagged, but it is the same script, and changing only one copy would make the two drift apart.

**Fix:**

- [ ] In `cli/templates/scripts/flow-walker.sh` → `record_in_set()`, rename the local `fo` to `first_outcome` at all four sites: the `local` declaration (`fo=""` → `first_outcome=""`), the assignment in the join loop (`fo="$SV"` → `first_outcome="$SV"`), the `g_need "nodes.$first.outcomes.$fo.binding"` lookup, and the `reason: $fo$NL$held` field of the `OUT=` line. Change nothing else, so behaviour and output stay identical.
- [ ] Apply the same rename to `scripts/flow-walker.sh` so the two files stay byte-identical. That copy is the `general` layer's part of this finding.
- [ ] Do not add `fo` for `flow-walker.sh` to the allowlist in `scripts/check-typos.sh`. That list is reserved for deliberate words.
  - **Deviations from plan:** (`cli` layer) The finding names no test file (`none — 6f shipped files pass typos`), so the row-`G.4` check took the fix-site fallback. Reading `record_in_set()` in `cli/templates/scripts/flow-walker.sh` showed all four `fo` sites still there, so the fix was not already in place, and the rename to `first_outcome` was applied at all four. The `6f` gate (`scripts/check-typos.sh`) was not run, because a unit never runs a gate script. The closing claim rests on two things. First, the four sites listed in the Site section were read before the edit and re-read after it. Second, `grep -n '\bfo\b\|first_outcome'` was run over the file before the edit. The Run gates phase's `commands.test` run verifies the typos gate. `bash scripts/typecheck.sh` passed (`check-shell-parse: 125 files checked … 0 failed`, `PASS: typecheck`). The `scripts/flow-walker.sh` copy is outside the `cli` path scope and was left for the `general` layer.
  - **Deviations from plan:** (`general` layer) This finding names no test file, so the row-`G.4` check again took the fix-site fallback. Running `grep -n '\bfo\b\|first_outcome'` over `scripts/flow-walker.sh` showed all four `fo` sites still in place, so the rename to `first_outcome` was applied at the four sites. `cmp scripts/flow-walker.sh cli/templates/scripts/flow-walker.sh` then exited 0, so the two copies are byte-identical. `grep -c '\bfo\b'` over `scripts/flow-walker.sh` now returns `0`. The `6f` gate (`scripts/check-typos.sh`) was not run, because a unit never runs a gate script. The Run gates phase's `commands.test` run verifies it. `bash scripts/typecheck.sh` passed (`check-shell-parse: 125 files checked … 0 failed`, `PASS: typecheck`). Three tree guards were selected and all passed: `test/shipped-scripts-mktemp.test.mjs` (1/1), `test/watcher-main-anchor.test.mjs` (3/3) and `test/no-container-home-paths.test.mjs` (1/1).
