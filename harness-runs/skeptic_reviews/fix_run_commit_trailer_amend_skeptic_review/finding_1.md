### 1. Six flow files still say the commit wrapper "enforces" no trailer, which the incident this branch fixes disproved

**Sites** (all under the `plugin` layer; each is the phrase `the wrapper enforces both`, found by quoted text):

1. `plugin/instructions/autonomous_pause_and_ledger.md` → `### 1.6 How to flip / create…`: "No `Co-Authored-By:` / trailer, no `--no-verify` — the wrapper enforces both."
2. `plugin/instructions/dispatch_discipline_instructions.md`, the commit paragraph beginning "Commit through the main checkout's copy of the wrapper": "No `Co-Authored-By:` / trailer and no `--no-verify` — the wrapper enforces both."
3. `plugin/instructions/plan_orchestration_instructions_autonomous.md`: "No `Co-Authored-By:` / trailer and no `--no-verify` / hook-skip flag — the wrapper enforces both: it builds the message from the positional args after `--` only (subject only here) and runs no commit hook."
4. `plugin/instructions/user_review_fixes_instructions_autonomous.md`: the same sentence as site 3.
5. `plugin/instructions/user_review_fix_plan_writing_instructions_autonomous.md`: "Fixed subject, no `Co-Authored-By:` / trailer, no `--no-verify` / hook-skip flag — the wrapper enforces both: it builds the message from the positional args after `--` only (subject only here) and runs no commit hook:"
6. `plugin/instructions/task_plan_writing_instructions_autonomous.md`, two occurrences: "Fixed subject `chore: Add UI-test plan for <branch>`, no `Co-Authored-By:` / trailer, no `--no-verify` / hook-skip flag — the wrapper enforces both: …" and "Make **one** commit with the fixed subject `chore: Add task plan for <branch>`, no `Co-Authored-By:` / trailer, no `--no-verify` / hook-skip flag — the wrapper enforces both: …".

**The problem.** These sentences tell the orchestrating session at each direct commit point that the commit wrapper *enforces* "no trailer". It does not. `cli/templates/scripts/commit-on-branch.sh`'s **MESSAGE ARGUMENTS** header says the opposite: *"THIS SCRIPT ENFORCES NONE OF THIS: it validates no message, rewrites no message, and passes each one to the commit exactly as given."* The task prompt's incident is the proof. The wrapper was handed `"Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"` as a body argument and committed it as `afdf238f`. Nothing refused or stripped it.

The `--no-verify` half is true: the wrapper commits by plumbing and runs no hook. The trailer half is the false guarantee, and it is about the very component and failure this branch exists to fix.

**Who reaches the wrong answer, and what it is.** The reader is the orchestrating session at one of these commit points, in a session whose system context still says *"End git commit messages with: Co-Authored-By: …"*. That happens in any session not launched on the run profile Task 2 changed. The profile's existing copies also keep the instruction until they are re-rendered (story index, **Manual setup required**). That session sees two instructions that conflict. The sentence settles the conflict wrongly: a trailer the session adds anyway "is enforced away" by the wrapper, so adding one looks harmless. The wrapper then commits it. That is the incident's first defect again, by the orchestrator instead of the committer.

**Why this is net-new, and why the plan's disposition does not cover it.** No committed review raised it. The story index's `## Scope register` kept these rows on purpose (rows 4, 5, 8, 9, 10 and 11, `no-change`). Its justification reads the sentence as *"the caller passes no trailer, and the wrapper adds none and runs no hook, both of which still hold."* The sentence does not say that. It says "the wrapper enforces both", and the cited source (the wrapper's own header) contradicts it. Under check 3 this is a misread citation, so it does not waive the fix.

It is graded **Should Fix**, not Must Fix. Each site's instruction ("no trailer") is still correct. Only the reason given for it is false, and Task 2's attribution switch removes the trailer's source in a run launched on a re-rendered profile.

**Fix.** Edit only the clause after the em dash at each site. Leave the rest of each sentence and its surrounding paragraph as they are. Use one wording per form, copied byte-for-byte into every site (`.claude/context/plugin.md` → `## Writing agent prose`, *"Each rule is stated once"*).

- **Short form** (sites 1 and 2). Replace `— the wrapper enforces both.` with:

  > — the wrapper adds neither and validates no message, so a trailer passed after `--` lands on the commit.

- **Long form** (sites 3, 4, 5 and both occurrences at site 6). Replace `— the wrapper enforces both: it builds the message from the positional args after `--` only (subject only here) and runs no commit hook` with:

  > — the wrapper adds neither and validates no message: it builds the message from the positional args after `--` only (subject only here), so a trailer passed there lands on the commit, and it runs no commit hook

  At site 5, keep the trailing `:` that introduces the code block that follows it.

No test pins the old phrase (`git grep -n "enforces both" -- cli/test test scripts docs` returns nothing), so this fix runs no suite of its own. The full suite runs in the Run gates phase.
