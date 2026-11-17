### Task 21 — Replace the committer's wrapper-call suite with one that pins the commit step's call shape

**Goal:** `cli/test/committer-wrapper-calls.test.mjs` reads `plugin/agents/committer.md` when the module loads, so it throws now that Task 20 has deleted that file. Replace it with `cli/test/commit-step-calls.test.mjs`, a source guard over the call shape the commit step now has. It keeps the one case that still holds, §1.6's once-alone rule, and adds cases for the unit loop's step 5 and the four forks' `<commit_call>` bindings.

**Why this `cli` task ships after the plugin tasks.** It asserts plugin prose that Tasks 9, 11, 12, 13 and 20 write. A source guard ships after the text it pins, as `fix_untrusted_input_framing_subagents` Task 8 did. It is the one place this plan leaves the configured `cli` → `plugin` order.

**Depends on:**

- **Task 9.** `unit_loop_core.md` → `## The unit loop` step 5 carries the line `<commit_call> --unit <the row's commit unit> --plan <the row's readiness index> --id <K> <the row's commit extra args>`. It also carries, byte-for-byte, the definition `**Once, alone** means its own Bash call holding that one command and nothing else — no `cd`, `;`, `&&`, `||`, pipe, `echo "exit $?"`, `$(…)` or shell variable before or after it.`
- **Tasks 11 and 12.** The two autonomous forks bind `<commit_call>` to `` `bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root> --push` ``.
- **Task 20.** The two semi-autonomous forks bind it to `` `bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root>` ``, and it deletes `committer.md`.
- **Task 13.** It keeps `autonomous_pause_and_ledger.md`'s heading `### 1.6 How to flip / create — direct `commit-on-branch.sh`, NEVER a committer dispatch`, its sentence `Call each wrapper once, alone.` and the same definition, all byte-for-byte.

### Targets

- `cli/test/committer-wrapper-calls.test.mjs` (deleted).
- `cli/test/commit-step-calls.test.mjs` (new) — this task's own test file.

**Work:**

- [ ] **Delete `cli/test/committer-wrapper-calls.test.mjs`**, with a plain `rm` naming that one tracked path.
- [ ] **Header.** It opens with the rule: every commit step is one literal call of the main checkout's wrapper, issued once, alone, with no `$`, and the forks' `<commit_call>` values differ only by `--push`. It states that this is a source guard, the last resort `.claude/context/conventions.md` → `## The testing bar` permits, and why: no behavioural test starts an orchestrator session. It names what it deliberately does not cover: whether a live session issues one Bash call per commit.
- [ ] **Cases.** Use the same `section()` slicing helper as the deleted suite, with `DEFINITION` kept as a literal and never read from a plugin file:
  - **(a)** the unit loop's step 5 carries the call line and `DEFINITION`;
  - **(b)** §1.6 still carries `Call each wrapper once, alone.` and `DEFINITION`, carries no `newline-separated`, and names `--artifact ledger-flip --entry`;
  - **(c)** each autonomous fork's `## Mode contract — bindings` table has a `<commit_call>` row containing the `--push` value;
  - **(d)** each semi-autonomous fork's row contains the value without `--push`;
  - **(e)** no file under `plugin/` names `agents/committer.md` or carries `<committer_push>`.
- [ ] **Registration.** Cases (a)–(d) read six fixed files. Case (e) reads the `plugin/` tree as text, which makes this suite a tree-reading test under `unit_loop_core.md` → `## The test-run rule` point 8. **Task 24** adds its `treeGuards` entry (`test/commit-step-calls.test.mjs`, covering `plugin/**/*.md`) to `devscene.config.json`. Do not edit `devscene.config.json` here.
- [ ] **Red once, recorded in the header.** In the working tree only, delete `--push` from one autonomous fork's `<commit_call>` row, run the suite, and record the failing case and its message with the date. Then restore the file byte-identical.

**Verification:**

- `npm test --workspace cli -- test/commit-step-calls.test.mjs`, from the repository root as one plain foreground command, exits zero with `fail 0`.
- `git ls-files cli/test/committer-wrapper-calls.test.mjs` prints nothing after the commit, and `git grep -n 'committer-wrapper-calls' -- cli docs` prints nothing.
- After the red-once restore, `git status --short -- plugin` prints nothing.
