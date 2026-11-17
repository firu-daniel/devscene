### Task 1 — Write-deny the run copy's branch-ref store and HEAD in the profile and the per-run copy

**Goal:** Make a sandboxed command in a run copy unable to move that copy's branch, whatever spelling it uses: a raw `git commit` or `--amend`, `git update-ref` run through a scratch script, a rewrite of `packed-refs`, or a switch of `HEAD`. Every other route is closed so that the only thing left able to move the branch is the excluded commit, push and refresh wrappers, which run outside the sandbox.

**Where this layer stops.** This task changes the protected set and its two declared mirrors. It does not change the profile template `cli/templates/claude/settings.autonomous.json` at all: its `permissions` lists, its `attribution` key and its `_README` paragraphs, the **FOUR COMMANDS RUN OUTSIDE THE SANDBOX…** paragraph's clone clause included, are **Task 2's**, which ships after this one and cites the three rows below. That task's assertions sit in a different suite. It does not document the change, which is **Tasks 6 and 7's**: those tasks cite the three rows below by exactly these paths and kinds. It adds no probe leg: the measurement row CS16 is **Task 6's**, graded `owed`.

**The three rows this task adds**, appended after `.git/objects/info/http-alternates`, in this order:

| path | kind | bubblewrapDenyWrite |
|---|---|---|
| `.git/HEAD` | `file` | `true` |
| `.git/refs/heads` | `directory` | `true` |
| `.git/packed-refs` | `file` | `true` |

Why these three:

- **`refs/heads`** holds the loose branch ref, and every git ref update takes `refs/heads/<branch>.lock` first.
- **`packed-refs`** holds a branch that has been packed. Git rewrites it through `packed-refs.lock` in `.git` and then renames that onto it.
- **`HEAD`** names which branch the copy is on, and the wrappers' clone check reads the branch from it.

None of the three is the whole `.git`, which the module header forbids for a run copy (`docs/sandbox-verification.md` CL4). `refs/heads` and `HEAD` exist in every clone when a sandbox starts. `packed-refs` exists in every clone `git clone` wrote refs into. Where it is absent on a bubblewrap host, the exact entry mounts the documented placeholder, and the per-run copy's absent-path manifest and sweep already handle that.

### Targets

- `cli/src/generators/writeProtection.ts` — `COPY_GIT_PATHS`, its module header, and the `_README` line it renders.
- `cli/templates/scripts/autonomous-watcher.sh` — the declared mirror `RUN_PROFILE_COPY_GIT_PATHS` and the header comment above it.
- `cli/test/profile.test.mjs` — the pinned `COPY_GIT_PATHS` list and the bubblewrap comment.

**Work:**

- [ ] `writeProtection.ts` → `COPY_GIT_PATHS`: append the three rows in the table above, with these `reason` clauses:
  - `.git/HEAD`: *"it names the branch that run copy is on, which only the excluded wrappers may move"*;
  - `.git/refs/heads`: *"it holds the run branch's ref, which only the excluded commit, push and refresh wrappers may move"*;
  - `.git/packed-refs`: *"a branch packed there moves when it is rewritten"*.

  Each clause renders into the profile's `_README` and into `doctor`'s message as it stands.
- [ ] `writeProtection.ts` module header: extend the set description and the **A run copy's `.git` must never be covered as a whole** paragraph. Under the sibling-run-copy glob the protected `.git` paths are now the trust files **and** the branch-ref store — `HEAD`, `refs/heads` and `packed-refs` — so that a run copy's branch moves only through the excluded wrappers, which read and swap that ref outside the sandbox (`cli/templates/scripts/lib/harness-run-lib.sh` → `hr_copy_sync_in_var`, `hr_copy_ref_swap_var`). State the accepted cost: a sandboxed `git commit`, `git switch`, branch creation and `git stash push` are refused in a run copy, and no flow issues them. Mark the stash refusal as derived rather than measured: it runs `git reset --hard`, which locks `refs/heads/<branch>`. Point at `docs/sandbox-verification.md` row CS16, owed. Wherever the generator's rendered `_README` line (`WHAT RUNS OUTSIDE THE SANDBOX CANNOT BE WRITTEN…`) enumerates the run copy's protected `.git` paths, it must name the three new ones.
- [ ] `autonomous-watcher.sh` → `RUN_PROFILE_COPY_GIT_PATHS`: append `.git/HEAD file deny`, `.git/refs/heads directory deny` and `.git/packed-refs file deny`, in that order. This is the declared mirror, held equal by `cli/test/watcher-run-profile.test.mjs`. In the `# THE PER-RUN PROFILE.` header block, adjust any wording that counts or lists the rows so it no longer says six.
- [ ] `cli/test/profile.test.mjs`: extend the `assert.deepEqual` pin of `COPY_GIT_PATHS.map(({ path, kind }) => [path, kind])` with `['.git/HEAD', 'file']`, `['.git/refs/heads', 'directory']` and `['.git/packed-refs', 'file']`. Keep the bubblewrap `omit` list pin unchanged, at the trio alone, and change its comment *"the base keeps all six"* to state the new count. The existing per-row `assertProtected` loop then covers the new rows. If `cli/test/watcher-run-profile.test.mjs`, `cli/test/doctor-profile-sandbox.test.mjs` or `cli/test/doctor.test.mjs` pins the row count or the six-row list literally, edit that pin in this task too. Those files then become this task's own edited test files.

**Verification:**

- `npm test --workspace cli -- test/profile.test.mjs` passes, and so does each other test file this task edited, run the same way.
- `bash scripts/typecheck.sh` exits 0.
- A fixture's rendered base profile carries, under the sibling glob, a `denyWrite` entry and its `Edit` rules for each new row: `Edit(/<glob>/.git/HEAD)`, `Edit(/<glob>/.git/refs/heads/**)` and `Edit(/<glob>/.git/packed-refs)`. Its `denyWrite` still holds no entry for `<glob>/.git` as a whole.
- `RUN_PROFILE_COPY_GIT_PATHS` in `cli/templates/scripts/autonomous-watcher.sh` lists exactly the paths, kinds and `deny`/`omit` columns of `COPY_GIT_PATHS`, in its order, ending with the three new rows, each marked `deny`.
  - **Deviations from plan:** The mirror-equality bullet rests on reading the two declarations side by side, not on execution: its held-equal suite `cli/test/watcher-run-profile.test.mjs` was not edited by this task, so under the test-run rule it is not run here and is deferred to the Run gates phase. None of `cli/test/watcher-run-profile.test.mjs`, `cli/test/doctor-profile-sandbox.test.mjs` or `cli/test/doctor.test.mjs` pins the six-row list or the row count literally (`grep -n "six\|http-alternates\|COPY_GIT_PATHS"` over the three): each pins only the bubblewrap `omit` trio, which is unchanged, so none was edited. The `# THE PER-RUN PROFILE.` header block neither counts nor lists the rows, so only the mirror itself changed there. The fixture-profile bullet is met by `cli/test/profile.test.mjs`'s per-row `assertProtected` loop over `COPY_GIT_PATHS`, which passed.
