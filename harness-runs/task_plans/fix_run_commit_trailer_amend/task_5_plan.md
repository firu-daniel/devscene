### Task 5 — Committer reads back the landed commit and reports, never repairs, one that went wrong

**Goal:** Make the committer, and every orchestrator commit point that calls the wrapper directly, check the commit that actually landed. If it is wrong, report it so the run parks, and never repair it by rewriting history. This is the contract half of the incident, where a committer saw its own commit carry a trailer and ran `git commit --amend` in the run copy.

**Depends on:** Task 2, which switches off the session's attribution instruction in the run profile. Two things follow for this task. The trailer rule below no longer competes with an instruction telling the session to add one. And no raw `git commit` is granted, so the amend this task forbids in prose is refused by the profile too. Task 4 keeps the plugin guard from vouching for it.

**Where this layer stops.** Prose contracts only. The divergence a raw rewrite leaves behind is reported by the wrappers' refusal, which is **Task 3's**. A landed-wrong `error:` parks through the callers' existing mapping: a `committer` returning `error:` goes to `<escalate>` (`plugin/instructions/plan_orchestration_instructions_core.md`, `plugin/instructions/user_review_fixes_instructions_core.md`), and no caller changes.

### Targets

- `plugin/agents/committer.md` — `## Commit-message policy` → **Attribution trailer**, `## Process` steps 4–6, `## Output contract`.
- `plugin/instructions/autonomous_pause_and_ledger.md` — `### 1.6 How to flip / create — direct `commit-on-branch.sh`, NEVER a committer dispatch`.

**Work:**

- [ ] `committer.md` → **Attribution trailer**: keep the rule and add only its edge case. A trailer that anything other than `<commit_conventions>` asks for — a session's own instruction to end commit messages with an attribution line included — is not `<commit_conventions>` requiring one, and is never passed.
- [ ] `committer.md` step 5 **Verify:** change the second call to `git log -1 --format=%h%n%B`. Keep the step's words *"as two separate calls, each once, alone"* byte-for-byte, because `cli/test/committer-wrapper-calls.test.mjs` matches them. The second call's first line must match `<short_sha>`. The rest must be exactly the message arguments step 4 passed after `--`, one paragraph each, with no line step 4 did not pass and no trailer `<commit_conventions>` does not require. On a mismatch, return `error: commit <short_sha> landed wrong — <what is wrong>; not repaired` and stop. There is then no step 6 push, and `<what is wrong>` is normalised per **Wrapper-safe subjects** clause (a). `ui_test_pass` step g already defers to step 5 and inherits this.
- [ ] `committer.md` `## Process`: add one rule, stated once, under step 4's exit mapping. A commit that landed — exit 0, or the landed exit 1 — is never amended, reset, rebased, recommitted or moved with `git update-ref`, whatever is wrong with it. It is reported through step 5's `error:`.
- [ ] `committer.md` `## Output contract`: add `error: commit <short_sha> landed wrong — <what is wrong>; not repaired` to the named `error:` returns, and note that it is the one `error:` returned after a commit landed.
- [ ] `autonomous_pause_and_ledger.md` §1.6: after the **One exit 1 is a landed commit.** paragraph, add one paragraph. A wrapper commit that landed with a subject, body line or trailer the commit point did not mean is never repaired: no `git commit --amend`, `git reset`, `git rebase`, `git update-ref` or second commit in its place. The commit point halts and hands off through the flow's existing `<escalate>` binding, naming the commit and what is wrong with it. Use that exact phrasing, as §1.8 does. Do not reword the paragraph's surrounding sentences, which other files quote.

**Verification:**

- `grep -n "landed wrong" plugin/agents/committer.md` shows the error in step 5 and in `## Output contract`. The two spellings are byte-identical.
- `grep -n "as two separate calls, each once, alone" plugin/agents/committer.md` still hits step 5.
- `grep -rn "git commit --amend" plugin/agents/committer.md plugin/instructions/autonomous_pause_and_ledger.md` shows it only inside a prohibition.
- `committer.md`'s frontmatter is unchanged (`tools: Bash, Read, Edit`), and its word count grows only by the sentences above.
