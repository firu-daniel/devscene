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
