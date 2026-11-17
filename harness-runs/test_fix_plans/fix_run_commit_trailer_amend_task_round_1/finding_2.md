### 2. Probe's `git` leg declaration disagrees with Gate 15's restated leg table

**Site:** `scripts/lib/sandbox-probe/core.sh`, the `sp_leg_declare git "CS3,CL5" \` call (around lines 77–79, navigation hint only), whose second argument begins `"ordinary git in the clone succeeds under the real per-run profile, git fetch origin is refused`. The restated row it must equal is `docs/development.md`, the `| \`git\` | CS3, CL5 |` row of the table headed `| Leg | Rows | Expected | Recorded in |` (around line 2620).

**Failing test:** `cli/test/sandbox-probe-git-and-legs.test.mjs` — `Gate 15's restated leg table matches --list, row for row`

**Failure (from the log, gate 4 `npm test`):**

```
not ok 1675 - Gate 15's restated leg table matches --list, row for row
  location: 'cli/test/sandbox-probe-git-and-legs.test.mjs:436:1'
  error: |-
    Expected values to be strictly deep-equal:
    + actual - expected
    +   'git\tCS3,CL5\tordinary git in the clone that writes only the index and objects succeeds under the real per-run profile, while the calls that move refs/heads, packed-refs or HEAD (commit, stash push/pop, switch -c) are expected to be refused since fix_run_commit_trailer_amend, which CS16 measures (owed); until the leg is moved, a CS3 fail naming only those calls is that expectation, not a regression (docs/sandbox-verification.md §5 PD32); git fetch origin is refused by the network allowlist as the clone layout intends, each CL5 write is refused or written as recorded, and a call refused at the permission layer is not run\t§2 The clone layout (owed) (CS3); §2 The per-run clone (2026-10-19) (CL5)',
    -   'git\tCS3,CL5\tordinary git in the clone succeeds under the real per-run profile, git fetch origin is refused by the network allowlist as the clone layout intends, each CL5 write is refused or written as recorded, and a call refused at the permission layer is not run\t§2 The clone layout (owed) (CS3); §2 The per-run clone (2026-10-19) (CL5)',
  code: 'ERR_ASSERTION'
```

In this test `actual` is the table restated in `docs/development.md` (via `restatedTable`, backticks stripped) and `expected` is the probe's `--list` output; every other row matched.

**Classification:** new this round (round 1; no earlier logs). Fixable on the branch.

**Diagnosis:** This branch's Task 6 (commit `1ca61ada`, "Record attribution, ref-deny row and guard decisions") rewrote the `git` row's Expected cell in `docs/development.md` to state that, since `fix_run_commit_trailer_amend` write-denies the clone's `.git/refs/heads`, `.git/packed-refs` and `.git/HEAD`, CS3's `commit`, `stash push`/`pop` and `switch -c` are expected to be refused, and that a CS3 `fail` naming only those calls is not a regression (`docs/sandbox-verification.md` §5 PD32). The probe's own declaration of that leg in `scripts/lib/sandbox-probe/core.sh` was not changed, so `bash scripts/sandbox-probe.sh --list` still prints the old sentence. The test exists to hold the doc's restatement equal to `--list` row for row, so one of the two must move. The doc's new wording is the intended, reviewed statement of the leg's expectation (it is mirrored by the CS3, CS3 (Linux), CS16 and PD32 entries in `docs/sandbox-verification.md`), and it is phrased as the probe's own declared expectation ("until the leg is moved"); the probe's declaration is the source `--list` reads, so it is the side to update. PD32 defers moving the *grading* of those calls out of `scripts/lib/sandbox-probe/legs-protection.sh` → `sp_leg_git` under roadmap item 21; changing the declared Expected text does not change any grading and does not implement that deferral.

**Fix:**

- [ ] In `scripts/lib/sandbox-probe/core.sh`, replace the second argument of `sp_leg_declare git "CS3,CL5"` with exactly this string (the doc row's Expected cell with backticks stripped, as the test compares it):

  ```
  ordinary git in the clone that writes only the index and objects succeeds under the real per-run profile, while the calls that move refs/heads, packed-refs or HEAD (commit, stash push/pop, switch -c) are expected to be refused since fix_run_commit_trailer_amend, which CS16 measures (owed); until the leg is moved, a CS3 fail naming only those calls is that expectation, not a regression (docs/sandbox-verification.md §5 PD32); git fetch origin is refused by the network allowlist as the clone layout intends, each CL5 write is refused or written as recorded, and a call refused at the permission layer is not run
  ```

  Keep it inside double quotes on its own continuation line, as the neighbouring declarations are; it contains no `"`, `$`, backtick or backslash, so no escaping is needed. Leave the rows argument `"CS3,CL5"` and the third argument (`"§2 The clone layout (owed) (CS3); §2 The per-run clone (2026-10-19) (CL5)"`) unchanged.
- [ ] Leave `docs/development.md` unchanged, and do not change `sp_leg_git`'s grading in `scripts/lib/sandbox-probe/legs-protection.sh` (deferred by PD32 under roadmap item 21).
- [ ] Check that no other declaration's text was edited and that `sp_leg_declare`'s tab-joined output for the `git` leg still has exactly four fields (the new text contains no tab).
