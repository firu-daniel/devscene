### Task 14 — Move the observations commit onto `--artifact` and read the records from any message line

**Goal:** Rewrite `plugin/instructions/improvement_observations_instructions.md`. Its own commit becomes one `--artifact observations --push` call. Its two history readers then follow the records to where the commit step now writes them: a **body line**, never the subject. The **Index-only commit** trip-wire moves its `mark … done — ` frame from the subject to any message line. The parsed substrings stay byte-for-byte.

**Depends on:**

- **Task 1**, whose `ucl_body_record` writes at most one lower-case body line per unit commit, in this precedence:
  1. `record disposition of <unit token> — <cause>`, when the unit's detail file carries `## Disposition`;
  2. `mark <unit token> already passing — <cause>`, when it carries `## Already passing`;
  3. `mark <unit token> done — <staged set>`, when the stage set is index-only.
  
  `<unit token>` is `Task K` or `Finding K`. The subject is always `<prefix>: <unit label> — <short title>`. So the disposition and index-only frames never co-occur on one commit, and neither is ever in the subject.
- **Task 3**, whose `--artifact observations --push` commits `<state_dir>/improvement_observations/<branch>.md` under `chore: Log improvement observations for <branch>` and pushes.

### Targets

- `plugin/instructions/improvement_observations_instructions.md`

**Work:**

- [ ] **The Index-only commit row and note (d).**
  - **The row.** It reads: a unit's commit staged nothing but the readiness index and the unit's own detail file, which its message records on a body line as `mark <unit token> done — <staged set>`.
  - **Note (d).** Match "a **line** framed `mark ` … ` done — `" in the same `git log --format='%h %s%n%b'` output, instead of "a subject framed". Its case rule becomes "a body line is lower-case, and the match stays case-insensitive on the leading word, so a commit made before this change still counts".
  - **The co-occurrence sentence.** Replace "the committer puts a `disposition` argument in the subject when …" with: the commit step writes one body record per commit, so a `mark … done — ` line is by construction the no-disposition case.
- [ ] **`## Dispositioned units` (b).**
  - **The record's source.** Replace "That is the record `${CLAUDE_PLUGIN_ROOT}/agents/committer.md` → `## Commit-message policy` puts on a commit … in the **subject** … and in a commit **body line** when …". The new text: the record the commit step writes as a body line whenever the unit's detail file carries `## Disposition`, citing `<scripts_dir>/commit-on-branch.sh` → **THE SUBJECT AND ITS RECORD**.
  - **What stays.** Keep "any line of whose message" and the whole three-rule parse byte-for-byte.
  - **The case rule.** Keep **The match's one case rule.**, but replace its "the committer binds it to `<commit_conventions>`'s capitalisation" reason. The new reason: the leading word is lower-case on a body line, and a commit made before this change may carry it capitalised in its subject.
  - **The sanitised cause.** "the committer's wrapper-safe subject rule" → "the commit step's normaliser".
- [ ] **The commit section.**
  - **The commit.** Rewrite **Direct wrapper, never a `committer` dispatch.**, **No committer mode fits.** and **Exact staging + commit.** around the one call `bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root> --artifact observations --push`, spelled literally. Cite `autonomous_pause_and_ledger.md` §1.6 by its unchanged heading.
  - **The exit paragraph.** Rewrite **Wrapper exit status (surface the error).** around the printed `error:` line and exit. The landed exit 1 is re-synced inside the wrapper and reported as `index_sync:`.
  - **The separate push.** Delete it.
  - **The rows.** Keep the `<MAIN_REPO>` row byte-for-byte; the `<scripts_dir>` row names the one wrapper.
- [ ] **The remaining mention.** In the `## The entry format` examples, "a tracked artifact omitted from the committer's explicit path list" → "… from the commit step's explicit path list".

**Verification:**

- `git grep -n -e 'committer' -- plugin/instructions/improvement_observations_instructions.md` prints nothing.
- `git grep -n -F 'record disposition of ' -- plugin/instructions/improvement_observations_instructions.md` still matches, and `git grep -n -F 'any line of whose message' -- plugin/instructions/improvement_observations_instructions.md` still matches.
- `git grep -n -F -e '--artifact observations --push' -- plugin/instructions/improvement_observations_instructions.md` shows the one call, and `git grep -n -F 'chore: Log improvement observations for' -- plugin/instructions/improvement_observations_instructions.md` prints nothing.
- `git diff -- plugin/instructions/improvement_observations_instructions.md` changes no heading line.

**Deviations from plan:**

- **First-write branch-moved exit 1.** The old re-stage call passed the parent directory `<state_dir>/improvement_observations` so a deleted new file was staged away. `--artifact observations` stages only the file path, and a deleted path is skipped (`commit-on-branch.sh` → **STAGING POLICY, AND THE ONE TRAP IN IT**), so no `--artifact` call can clear the staged addition. Implemented: a later write still reverts and re-issues the same call (exit 3); a first write deletes nothing and reports the path as left staged. `## Surfacing it in the Done summary` was updated to match. This leaves a tracked-dirty tree in that rare race where the old procedure left it clean.
- **`## Push` kept as a heading.** The plan said to delete the separate push. The section heading stays because the verification bar forbids heading changes and `## Where it runs & the non-blocking rule` cites `## Push`. Its body now describes the in-call `--push`, the same shape `clarification_digest_instructions.md` → `## Push` took in Task 13.
- **The headless-trap citation.** The old `## Push` cited `autonomous_pause_and_ledger.md` §1.6 for the `if …; then … fi` trap. Task 13 removed that text from §1.6, so the new body states the trap in one clause and does not cite §1.6 for it.
- **Further stale mentions fixed in the same file.** `## Where it is written` (the commit wrapper is now handed no path, and the driver's subject is now named through the `observations` kind so the subject literal does not appear), `## Dispositioned units` (b)'s `disposition:`-argument sentence (now points to `unit_loop_core.md` → `### The dispositioned outcome`), and `## Ledger / resume`'s "unconditional push" clause.
