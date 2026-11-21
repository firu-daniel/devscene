### Task 4 — Add the diff-base corpus test over `plugin/**/*.md`

**Goal:** Add a `cli` corpus test that holds the plugin corpus to this branch's rule. Every end-of-branch diff and commit range is based on `origin/<default_branch>`, and every file that runs `git diff` or `git log` against that base carries the one fallback sentence, byte for byte. This is the static check the lessons ledger requires whenever several agent definitions carry one rule (`harness-runs/lessons.md` → `## Agent prose`, *"When a change makes agent definitions state one rule in two places … the same change ships the static check that holds the two aligned"*).

**Depends on:** Tasks 1, 2 and 3. The test asserts the text they write, so it lands after them and its own run passes. It relies on these contracts:
- the dispatch and quoted lines read `diff_base: origin/<default_branch>` (Task 1);
- no plugin `*.md` carries a bare `<default_branch>...HEAD` or `<default_branch>..HEAD`, except the D.2 fallback literal `git rev-list --count <default_branch>..HEAD` in `plan_orchestration_instructions_core.md` and `user_review_fixes_instructions_core.md` (Tasks 1–3 leave both untouched);
- the fallback sentence, quoted in the story index `## Context`, appears verbatim in `architecture-reviewer.md`, `business-parity-reviewer.md` (Task 1), `branch-reviewer.md`, `skeptic-reviewer.md`, `review-plan-reviewer.md` (Task 2), `statistics-plan-writer.md`, `improvement_observations_instructions.md` and `docs_phase_instructions.md` (Task 3).

**Registration.** This test reads a tree of repository files, so it is a tree guard (`${CLAUDE_PLUGIN_ROOT}/instructions/unit_loop_core.md` → `## The test-run rule`, point 8). **Task 5** adds its `treeGuards` entry to `devscene.config.json`. This task does not edit that file, because it sits outside the `cli` layer's path.

### Targets

- `cli/test/diff-base-corpus.test.mjs` (new)

**Work:**

- [ ] **Header.** Open the file with a header modelled on `cli/test/untrusted-input-corpus.test.mjs`. It states, first, *"The rule this suite exists to enforce"*: every end-of-branch diff and commit range in `plugin/**/*.md` is based on `origin/<default_branch>`, and each file that runs one carries the fallback sentence verbatim. It records *"Registered as a tree guard by Task 5 of `fix_default_branch_diff_base`"*. It names what is deliberately not covered: whether a sentence sits in the right row, and `git show` row reads, which keep `review-sweep.sh`'s local-first rule.
- [ ] **Case `no-bare-base`.** Walk `plugin/` recursively for `*.md` from `WORKSPACE_ROOT` (`cli/test/helpers/fixture.mjs`), with `node:fs` and `node:path` only. In each file's text, remove every occurrence of the one allowed literal `git rev-list --count <default_branch>..HEAD`. Then collect every match of `/(?<!origin\/)<default_branch>\.\.\.?HEAD/` and of `/diff_base: <default_branch>/` as `<repo-relative path>:<line>`. Assert the collected list `deepEqual` to `[]`, so a failure names every offending site.
- [ ] **Case `fallback-sentence`.** Hold the sentence as one exported constant, `FALLBACK_SENTENCE`, equal to the story index's quoted sentence character for character. Select every `plugin/**/*.md` file with a line matching `/git (diff|log)\b[^\n`]*(origin\/<default_branch>|<diff_base>)\.\.\.?HEAD/`. Assert that the list of selected files lacking `FALLBACK_SENTENCE` `deepEqual`s `[]`. Also assert the selected set is non-empty, so a broken regex cannot pass vacuously.
- [ ] **Red once.** In the working tree only, revert one site of each rule (for example, put a bare `<default_branch>...HEAD` back in `plugin/agents/skeptic-reviewer.md`, then delete the fallback sentence from `plugin/instructions/docs_phase_instructions.md`). Run the file and confirm each case fails naming that file. Restore both edits, and record each red run in the header's `RED ONCE` lines, as the model suite does.

**Verification:**

- `npm test --workspace cli -- test/diff-base-corpus.test.mjs` passes, run from the repository root as one plain foreground command. This is this task's own new test file. Read the exit status and the pass/fail counts.
- The two red runs above are recorded in the header with their date and the failure each printed.
- After the restore, `git status --short` shows the new, untracked `cli/test/diff-base-corpus.test.mjs` and no modified file under `plugin/`.
