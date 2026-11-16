### Task 13 — Move the ledger, dispatch-additions, digest and re-screened-input commits onto `--artifact`

**Goal:** Rewrite the four shared modules whose commit points spell a fixed subject and a path set in prose. Each commit point becomes one literal `--artifact` call, and each loses its "this is not a committer dispatch" argument. The commit points are:

- the flow-progress ledger's create and flip form;
- the planning-pause partial commit (§2.2 → **Planning artifacts only**, reused by §2.5 step 0);
- the dispatch-additions record — the one point here in a **family-neutral** module, so its push follows the activating flow (see the `dispatch_discipline_instructions.md` bullet);
- the clarification digest;
- the prompt-injection screen's re-screened edit.

Every point but the dispatch-additions record sits in an autonomous-only module and carries `--push` unconditionally.

**Depends on:**

- **Task 3.** Its front end takes `bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root> --artifact <kind> [--entry <id>] [--path <p>]… --push`.
  - **What the call does.** It commits the table's paths under the table's fixed subject, re-syncs a landed exit 1 itself, and pushes after exit 0 or exit 3.
  - **What it prints.** The return block, or `error: <line>`: exit 1 for a refusal, 2 for protected, 3 for `error: nothing to commit`.
- **Task 1's kinds used here:**
  - `ledger` → `chore: Add flow-progress ledger for <branch>`;
  - `ledger-flip` with `--entry <id>`, `<id>` in `[A-Za-z0-9.]+` → `chore: Flow progress <entry-id> for <branch>`;
  - `dispatch-additions` → `chore: Log dispatch additions for <branch>`, path `<state_dir>/dispatch_additions/<branch>.md`;
  - `clarification-digest` → `chore: Record clarification digest for <branch>`, path `<state_dir>/clarification_digests/<branch>.md`;
  - `rescreened-input` → `chore: Commit re-screened input edit for <branch>`, paths from repeated `--path`;
  - `plan-round-partial` with `--round <n>` → `chore: Plan round <n> partial for <branch>`, `plan-round`'s six paths;
  - `fix-plan-round-partial` with `--round <N> --iteration <k>` → `chore: Fix plan <N> round <k> partial for <branch>`, `fix-plan-round`'s paths.

**Where this task stops.** §2.2 states the one-call form with the kind and its round flags left to the fork. Task 15 binds each fork's kind and flags in that fork's pause and self-pause paragraphs, and Task 11 rewrites the clean-tree entries 17 and 19 that register these points.

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
- [ ] **`autonomous_pause_and_ledger.md` §2.2 → **Planning artifacts only (the two plan-writing forks)**.**
  - **The lead-in.** "(the fork names its set and its partial subject)" → "(the fork names its planning path set and its partial artifact kind with the kind's round flags)". The dirty-tree test still reads the fork's planning path set, which is the kind's table row.
  - **Steps 1 and 2 become one step.** Commit the round so far with `bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root> --artifact <the fork's partial kind> <the fork's round flags> --push`, the round flags carrying the round of the dispatch the pause interrupts — for a set, the set's round. It is the call's only command, spelled as §1.6 spells it, with no shell expansion. Keep: untracked planning artifacts are committed by this same call, and exit 3 (nothing to commit) is normal and still pushes. Replace "a landed exit 1 counts as committed, as §1.6 states" with: the wrapper re-syncs a landed exit 1 itself and exits 0. Delete the separate `push-branch.sh` step. Renumber "Honour the pause now" as step 2.
  - **§2.5 step 0.** It reuses the step by reference ("exactly as §2.2's bullet of that name states"), so it needs no edit and stays true: it now names one call that commits and pushes. Its "local `git` work and a push" stays true too.
  - **What stays.** The bullet's bold label, **A round's set.** and its "its **Planning artifacts only** commit exiting 3", and §2.3's references to the partial commit, all byte-for-byte.
- [ ] **`autonomous_pause_and_ledger.md` elsewhere.**
  - "implementers, reviewers, committers stay single-purpose" → "implementers and reviewers stay single-purpose".
  - The §2.2 **Dirty-tracked** bullets: "a unit is mid-commit, between an implementer and its committer" → "between an implementer and its commit call". "a bounded committer dispatch" → "a bounded commit call".
  - The later "pending committer", "next committer dispatch", "its committer's" and "`committer` closing a unit" become the commit call's.
  - Change no heading.
- [ ] **`dispatch_discipline_instructions.md`.** This module is **mode-free and family-neutral**: its `## Activation` names the mode-free cores, which also run in the semi-autonomous flows, whose forks leave their commits unpushed for the human merge step (Task 20's semi-autonomous `<commit_call>` binding carries no `--push` for that reason). So the push stays conditional on the activating flow, and exactly one push mechanism is named.
  - **`## Commit mechanics`.** The dispatch-additions commit becomes one call: `bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root> --artifact dispatch-additions --push` in a flow that pushes its commits, and `bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root> --artifact dispatch-additions` (no `--push`) in a flow that pushes none. Show both literals; state that `## Push` decides which. The literal is written out, never `<commit_call>`: two of the activating cores (`task_plan_writing_instructions_core.md`, `user_review_fix_plan_writing_instructions_core.md`) bind no `<commit_call>`. The "exit 1 or exit 2 … Revert the block" paragraph reads the printed `error:` line and the exit; its landed-exit-1 exception goes, because the wrapper re-syncs that case itself and exits 0.
  - **`## Push` — kept as a heading, reduced to the family-neutral rule.** `plan_orchestration_instructions_autonomous.md` → **Post-commit push.** cites this heading, so its text does not change. Its body becomes the single statement of the rule: in a flow that pushes its commits, the `## Commit mechanics` call carries `--push`, which pushes in the same call immediately after the commit (exit 0 or exit 3), best-effort; in a flow that pushes none, the call carries no `--push` and nothing here pushes. Keep the "this step pushes exactly where the flow it runs in pushes, which is what keeps it family-neutral" sentence and the "A phase that owes no block skips the step whole" sentence. Delete the separate `bash <MAIN_REPO>/<scripts_dir>/push-branch.sh <repo_root>` block, its literal-spelling paragraph (now covered by `## Commit mechanics`'s), and the unconditional-call / no-exit-code-gate paragraph, since there is no second call to gate. Keep the **Why it is issued here, and where the rationale lives.** paragraph byte-for-byte: its argument against leaving the push to a later step is now the reason the call carries `--push`, and its pointer to `plan_orchestration_instructions_autonomous.md` stays.
  - **Rationale.** **No committer mode fits.** and **Why this is not a `committer` dispatch** collapse into the §1.6 pointer.
  - **The dispatch-class lists.** "implementer, reviewer, writer, committer alike" → "implementer, reviewer and writer alike". "the implementer, reviewer or committer contracts" → "the implementer or reviewer contracts". "every implementer, every writer, `committer`" → "every implementer, every writer". The pre-dispatch-rule sentence's "three dispatches it owns — implementer, per-unit reviewer, committer" → "two dispatches it owns — implementer, per-unit reviewer".
  - **`## Resolved values` and the mode-free note.** The `<scripts_dir>` row names one script by path, `commit-on-branch.sh` in `## Commit mechanics`, and states that its `--push` runs the `push-branch.sh` beside it; it no longer names `push-branch.sh` "in `## Push`". The **Mode-free and family-neutral.** paragraph stays byte-for-byte: `## Push` still cites the fork document as its rationale source. Keep the `<MAIN_REPO>` row byte-for-byte.
- [ ] **`clarification_digest_instructions.md` and `prompt_injection_screen.md`.**
  - **The digest commit.** It becomes `… --artifact clarification-digest --push`. "Direct wrapper, never a `committer` dispatch" → "Direct wrapper call, never a bare `git add` / `git commit`", still citing §1.6.
  - **The screen's step 4.** It commits every held modified tracked path in one call, `… --artifact rescreened-input --path <path> --path <path>… --push`, with no separate push line. Its exit bullet reads: exit 0 or 3 goes on; exit 1 or 2 halts as step 0 states. Delete the landed-exit-1 clause, because the wrapper re-syncs. Keep its `<MAIN_REPO>` literal-spelling sentence byte-for-byte.

**Verification:**

- `git grep -n -w -e 'committer' -e 'committers' -- plugin/instructions/autonomous_pause_and_ledger.md plugin/instructions/dispatch_discipline_instructions.md plugin/instructions/clarification_digest_instructions.md plugin/instructions/prompt_injection_screen.md` prints only the §1.6 heading line.
- `git grep -n -F -e '--artifact ledger-flip --entry' -e '--artifact dispatch-additions' -e '--artifact clarification-digest --push' -e '--artifact rescreened-input --path' -e '--artifact <the fork' -- plugin/instructions` shows the call at each commit point, with `dispatch_discipline_instructions.md` showing both its `--push` and its no-`--push` literal.
- `git grep -n -F 'push-branch.sh <repo_root>' -- plugin/instructions/dispatch_discipline_instructions.md` prints nothing, and in `autonomous_pause_and_ledger.md` no match falls inside §2.2: each commit point names one push mechanism.
- `git grep -n -F '## Push' -- plugin/instructions/dispatch_discipline_instructions.md plugin/instructions/plan_orchestration_instructions_autonomous.md` still shows the heading and its citer.
- `git grep -n -F 'Call each wrapper once, alone.' -- plugin/instructions/autonomous_pause_and_ledger.md` still matches, and `git diff -- plugin/instructions/autonomous_pause_and_ledger.md` changes no heading line.
