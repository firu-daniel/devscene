### Task 5 — Rename the package in the supply-chain workflow, then park for the maintainer's push

**Goal:** Make the nightly `uv-audit` job audit the renamed package's lock. `.github/workflows/supply-chain.yml` names `devscene-runtime` twice: in its header comment, and in the `uv-audit` job's `working-directory: devscene-runtime` step. After merge, the job would `cd` into a directory that no longer exists and fail every night.

**Depends on:** Task 1 and Task 4.

- Task 1 moved the lock to `devscene-flow-host/uv.lock`.
- Task 4 updated `docs/development.md` → `## 8. The nightly supply-chain audit`, which now states that `uv-audit` runs `uv audit --preview-features audit-command --frozen` *"once each from `docs-retrieval-service/`, `graphscene/` and `devscene-flow-host/`"*.

This task makes the workflow match that sentence and changes nothing else.

**Why this task is last, and what happens after its commit.** `push-branch.sh` refuses every unattended push whose commits change a path under `.github/workflows/`. It prints a `refusing to push:` line and exits `0` (`cli/templates/scripts/push-branch.sh` → `NO UNATTENDED PUSH CHANGES A WORKFLOW FILE`). So once this commit lands, the run's push of the branch is refused. **The run parks and asks the maintainer to push it**, and it resumes once the maintainer answers that the push is done (story index `## Context`, manual steps 1 and 2). Neither this task nor its implementer pushes, retries the push, splits the commit, or works around the refusal in any other way. Every earlier task's commit was pushed before this one, which is why it ships last.

### Targets

- `.github/workflows/supply-chain.yml`

**Work:**

- [ ] In the header comment, change `devscene-runtime/uv.lock` to `devscene-flow-host/uv.lock`. Re-wrap only the comment lines that change: `docs-retrieval-service/uv.lock, graphscene/uv.lock and` / `devscene-flow-host/uv.lock), zizmor-online (the`.
- [ ] In the `uv-audit` job, change the third step's `working-directory: devscene-runtime` to `working-directory: devscene-flow-host`. Its `run:` line, the step order, the pinned action SHAs and every other job stay exactly as they are.

**Verification:**

- `git grep -n -i "devscene-runtime" -- .github/workflows/supply-chain.yml` prints nothing. `git grep -n "working-directory: devscene-flow-host" -- .github/workflows/supply-chain.yml` prints one line.
- `git diff HEAD -- .github/workflows/supply-chain.yml` changes the header comment and the one `working-directory` line, and nothing else.
- The commit lands through the unit loop as usual. The refused push that follows is the expected park, not a failure of this task.
