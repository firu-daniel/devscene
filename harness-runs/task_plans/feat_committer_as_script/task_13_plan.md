### Task 13 — Move the ledger, dispatch-additions, digest and re-screened-input commits onto `--artifact`

**Goal:** Rewrite the four shared autonomous modules whose commit points spell a fixed subject and a path set in prose. Each becomes one literal `--artifact … --push` call, and each loses its "this is not a committer dispatch" argument. The four commit points are:

- the flow-progress ledger's create and flip form;
- the dispatch-additions record;
- the clarification digest;
- the prompt-injection screen's re-screened edit.

**Depends on:**

- **Task 3.** Its front end takes `bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root> --artifact <kind> [--entry <id>] [--path <p>]… --push`.
  - **What the call does.** It commits the table's paths under the table's fixed subject, re-syncs a landed exit 1 itself, and pushes after exit 0 or exit 3.
  - **What it prints.** The return block, or `error: <line>`: exit 1 for a refusal, 2 for protected, 3 for `error: nothing to commit`.
- **Task 1's kinds used here:**
  - `ledger` → `chore: Add flow-progress ledger for <branch>`;
  - `ledger-flip` with `--entry <id>`, `<id>` in `[A-Za-z0-9.]+` → `chore: Flow progress <entry-id> for <branch>`;
  - `dispatch-additions` → `chore: Log dispatch additions for <branch>`, path `<state_dir>/dispatch_additions/<branch>.md`;
  - `clarification-digest` → `chore: Record clarification digest for <branch>`, path `<state_dir>/clarification_digests/<branch>.md`;
  - `rescreened-input` → `chore: Commit re-screened input edit for <branch>`, paths from repeated `--path`.

**What must not move.** The heading `### 1.6 How to flip / create — direct `commit-on-branch.sh`, NEVER a committer dispatch` stays byte-for-byte. Other forks cite it (Tasks 11, 12 and 15), and so do `cli/test/flow-walker-resume.test.mjs` and Task 21's suite. Its sentence `Call each wrapper once, alone.` and the **Once, alone** definition stay byte-for-byte too. Its "NEVER a committer dispatch" remains literally true.

### Targets

- `plugin/instructions/autonomous_pause_and_ledger.md`
- `plugin/instructions/dispatch_discipline_instructions.md`
- `plugin/instructions/clarification_digest_instructions.md`
- `plugin/instructions/prompt_injection_screen.md`

**Work:**

- [ ] **`autonomous_pause_and_ledger.md` §1.6.**
  - **The form.** "Edit the ledger file, then commit and push via the wrapper" becomes: edit the ledger file, then issue `bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root> --artifact ledger-flip --entry <entry-id> --push`, or `--artifact ledger --push` for creation. That is one call, which commits and pushes.
  - **What stays.** Keep `Call each wrapper once, alone.`, the definition and the literal-spelling paragraph. Keep the `chore: Flow progress A1.5f for <branch>` worked example as the subject the call produces.
  - **What goes.** Delete the ⚠️ two-calls-and-no-exit-gate warning; one call has nothing to gate. Delete the **One exit 1 is a landed commit.** re-sync instructions: the wrapper re-syncs and prints `index_sync:`.
  - **The three-reasons block.** Replace "This is **NOT** a `committer` agent dispatch, for three reasons" with one sentence: the flip is a Bash call costing zero dispatches.
  - **Idempotency.** Keep it: a re-flip prints `error: nothing to commit`, exits 3, and still pushes.
- [ ] **`autonomous_pause_and_ledger.md` elsewhere.**
  - "implementers, reviewers, committers stay single-purpose" → "implementers and reviewers stay single-purpose".
  - The §2.2 **Dirty-tracked** bullets: "a unit is mid-commit, between an implementer and its committer" → "between an implementer and its commit call". "a bounded committer dispatch" → "a bounded commit call".
  - The later "pending committer", "next committer dispatch", "its committer's" and "`committer` closing a unit" become the commit call's.
  - Change no heading.
- [ ] **`dispatch_discipline_instructions.md`.**
  - **`## Commit mechanics`.** The dispatch-additions commit becomes `bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root> --artifact dispatch-additions --push`. The "exit 1 or exit 2 … Revert the block" paragraph reads the printed `error:` line and the exit.
  - **Rationale.** **No committer mode fits.** and **Why this is not a `committer` dispatch** collapse into the §1.6 pointer.
  - **The dispatch-class lists.** "implementer, reviewer, writer, committer alike" → "implementer, reviewer and writer alike". "the implementer, reviewer or committer contracts" → "the implementer or reviewer contracts". "every implementer, every writer, `committer`" → "every implementer, every writer". The pre-dispatch-rule sentence's "three dispatches it owns — implementer, per-unit reviewer, committer" → "two dispatches it owns — implementer, per-unit reviewer".
  - **`<scripts_dir>` row.** Its `## Resolved values` row keeps naming the two scripts; push is now `--push`. Keep its `<MAIN_REPO>` row byte-for-byte.
- [ ] **`clarification_digest_instructions.md` and `prompt_injection_screen.md`.**
  - **The digest commit.** It becomes `… --artifact clarification-digest --push`. "Direct wrapper, never a `committer` dispatch" → "Direct wrapper call, never a bare `git add` / `git commit`", still citing §1.6.
  - **The screen's step 4.** It commits every held modified tracked path in one call, `… --artifact rescreened-input --path <path> --path <path>… --push`, with no separate push line. Its exit bullet reads: exit 0 or 3 goes on; exit 1 or 2 halts as step 0 states. Delete the landed-exit-1 clause, because the wrapper re-syncs. Keep its `<MAIN_REPO>` literal-spelling sentence byte-for-byte.

**Verification:**

- `git grep -n -w -e 'committer' -e 'committers' -- plugin/instructions/autonomous_pause_and_ledger.md plugin/instructions/dispatch_discipline_instructions.md plugin/instructions/clarification_digest_instructions.md plugin/instructions/prompt_injection_screen.md` prints only the §1.6 heading line.
- `git grep -n -F -e '--artifact ledger-flip --entry' -e '--artifact dispatch-additions --push' -e '--artifact clarification-digest --push' -e '--artifact rescreened-input --path' -- plugin/instructions` shows one call per module.
- `git grep -n -F 'Call each wrapper once, alone.' -- plugin/instructions/autonomous_pause_and_ledger.md` still matches, and `git diff -- plugin/instructions/autonomous_pause_and_ledger.md` changes no heading line.
