### Task 4 — Describe the script-built subject and the body-line records in the adopter's conventions and CLAUDE templates

**Goal:** Rewrite what an adopter's conventions skeleton asks about commit messages, now that no agent reads the commit-message policy and the wrapper builds every unit and artifact subject itself. Update the always-loaded `CLAUDE.md` template's sentence about who reads that policy, and the `init` test that pins the skeleton's fragments.

**Depends on:** Task 3, which makes `commit-on-branch.sh` build the subject `<prefix>: <unit label> — <short title>`, at most 72 bytes.

- **Prefix.** The branch-name token for a story task, `fix` for the review-fix rows, and the severity mapping for a user-review item.
- **Body records.** It writes the lower-case body records `record disposition of <unit token> — <cause>`, `mark <unit token> already passing — <cause>` and `mark <unit token> done — <staged set>`.
- **Fixed-form subjects.** It emits `review_plan_file` → `chore: add code review for <branch>`, `ui_test_pass` → `chore: Mark UI test K passing for <branch>`, and the fixed subjects of `lib/unit-commit-lib.sh`'s artifact table.
- **Trailers.** It adds no attribution trailer.

### Targets

- `cli/templates/claude/context/conventions.md` — the **The commit-message policy** bullet under **What belongs here**.
- `cli/templates/claude/CLAUDE.md` — the sentence "the committer reads exactly one section of one of them".
- `cli/test/init.test.mjs` — the test `the shared conventions skeleton carries the commit-policy section the committer resolves against` and its doc comment.

**Work:**

- [ ] **The commit-message policy bullet.**
  - **The opening.** Replace "which is the whole of what the committer agent reads from this document". The new opening says that the harness builds every unit and artifact commit subject itself, through `<scripts_dir>/commit-on-branch.sh` and its `lib/unit-commit-lib.sh`. This section therefore states the policy those built subjects follow, and the policy for the commits a person or a flow makes by other means.
  - **What the bullet keeps asking.** The prefix vocabulary, capitalisation, the subject-length cap, the attribution-trailer stance, and the probe-derived fixed-form list with its exemption. Keep the existing probe command byte-for-byte.
  - **The wire sentence.** Replace "`review_plan_file` and `ui_test_pass` are the committer's own commit modes and the dispatching flow files quote both" with a sentence saying those two subjects and the artifact table's subjects are owned by `lib/unit-commit-lib.sh`. Changing one is an edit to the library and to every flow file that names it.
  - **What the adopter now answers.** Replace the "which is what the committer's `commit_prefix` argument spells as the literal `none`" clause. State the subject shape the wrapper builds, and that the unit-commit prefix per class is the harness's: the branch-name token for new work, `fix` for a fix to existing work, the severity mapping for a user-review item. Say what an adopter answers instead: whether their own other commits follow it.
  - **Body records.** State that disposition, already-passing and index-only records are body lines in lower case, and that the harness adds no attribution trailer to a commit it builds.
- [ ] **`cli/templates/claude/CLAUDE.md`.** Reword "the committer reads exactly one section of one of them — the commit-message policy in the shared cross-layer conventions document — and nothing else" to say that no agent reads these files on a commit: the commit wrapper builds its own subjects. Keep the paragraph's other sentences byte-for-byte.
- [ ] **`cli/test/init.test.mjs`.** Rename the test so it no longer names the committer, and rewrite its doc comment around the rule it now enforces: the skeleton still carries a commit-policy section that names the wrapper-built subject and the body-line records. Replace the fragment list with literals from the new bullet: keep `commit-message policy`, `attribution-trailer` and `Per commit class`, add `body line` and `commit-on-branch.sh`, and drop `review_plan_file`, `ui_test_pass` and `carries no prefix at all` only where the new bullet no longer carries them.

**Verification:**

- `npm test --workspace cli -- test/init.test.mjs`, from the repository root as one plain foreground command, exits zero with `fail 0`.
- `git grep -n -w committer -- cli/templates/claude` prints nothing.
- The fixed-form-subject probe command in the bullet is byte-identical to the one `git show HEAD:cli/templates/claude/context/conventions.md` carries.
