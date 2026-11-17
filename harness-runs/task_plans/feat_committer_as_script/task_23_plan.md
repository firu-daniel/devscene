### Task 23 — Re-point the analyze, development and remote-execution documents and the plan-shape grader at the commit step

**Goal:** Four root-level documents state a fact about the `committer` agent that stops being true once Task 20 deletes it. Restate each about **the commit step** — the `commit-on-branch.sh --unit` / `--artifact` call — and leave every measured row and dated record untouched.

**Depends on:**

- **Task 20**, which deletes `plugin/agents/committer.md`.
- **Task 4**, which makes the adopter's conventions skeleton say that no agent reads the commit-message policy: the wrapper builds its own subjects.

**Catch-all task.** Its implementer reads every configured layer's conventions document, because the sentences describe both shipped halves.

### Targets

- `docs/analyze.md`
- `docs/development.md`
- `docs/remote-execution.md`
- `evals/plan-shape/graders/plan-shape.md`

**Work:**

- [ ] **`docs/analyze.md`.**
  - **The agent set.** "plus `plugin/agents/committer.md` for the commit policy" in the derived agent set goes: no agent reads the commit policy now.
  - **"No committer" sentences.** "a setup run has no branch, no committer and no run-control tree" → "… no commit step …". "there is no committer behind a `/devscene:analyze` run" → "there is no commit step behind a `/devscene:analyze` run".
- [ ] **`docs/development.md`.** In the Gate 8 pass criteria, drop "plus `plugin/agents/committer.md` for the commit policy" from the derived agent set. Keep the grep command and its count wording, and change nothing in any measured table or dated paragraph.
- [ ] **`docs/remote-execution.md`.** "each `committer` dispatch carries `push: true`, and each direct commit is followed by a single `push-branch.sh` call" becomes the fact as it now is. Every unit and fixed-subject commit point is one `commit-on-branch.sh` call carrying `--push`, and only the docs flows keep a separate `push-branch.sh` call.
- [ ] **`evals/plan-shape/graders/plan-shape.md`.** "the orchestrator and the committer key off the exact string" → "the orchestrator and the commit step key off the exact string".

**Verification:**

- `git grep -n -w committer -- docs/analyze.md docs/development.md docs/remote-execution.md evals/plan-shape/graders/plan-shape.md` prints nothing.
- `git diff --stat -- docs/development.md` shows only the one sentence's edit, and no table row in that file changed.
