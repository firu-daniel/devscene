### Task 1 — Add the atomic `replace-if-changed` write policy and `gitCommonDir`

**Goal:** Give the write engine the one new re-run contract `init --upgrade` needs: create a missing file, keep a current one, and replace a changed one by rename after a backup outside the working tree.

**Where this task stops.** It adds the policy and the git probe. No generator uses the policy yet: Tasks 5 and 6 enqueue requests with it, and Task 10 supplies `backupDir` and calls the plan.

### Targets

- `cli/src/core/writer.ts`
- `cli/src/core/git.ts`
- `cli/test/write-plan-replace.test.mjs` (new)

**Work:**

- [ ] `writer.ts`: add `'replace-if-changed'` to `WritePolicy` and handle it in `resolveRequests` and `planWrite`. An absent target is `created`. A target whose bytes and permission bits both match is `kept`. Compare bytes as buffers, so a file that is not valid UTF-8 is compared correctly. Changed bytes give `backed-up-and-replaced`. A mode-only difference is replaced with no backup, because its bytes do not change. `--force` is not consulted. Add `WriteContext.backupDir?: string`, and throw `internal()` if a backup is due and it is absent.
- [ ] `writer.ts` → `commitWrite`: for this policy, create the temporary file in the target's directory with a random name and exclusive creation (`wx`), write it, set its mode, flush it, and `renameSync` it over the target. Use `request.mode` when given, otherwise the existing file's permission bits, otherwise `0o644`. Remove the temporary file on every failure path. Before replacing, copy the old file to `<backupDir>/<repo-relative path>` with `COPYFILE_EXCL`, creating parent directories `0o700`, and refuse a symlink on that path. The backup directory is created only when the first backup is written. `backupPath` on the result is that path.
- [ ] `writer.ts` header: update "four values" and "four policies", add the policy to the structural guarantees without moving any mutating call outside `commitWrite`, and update the re-run table. The permission-profile row becomes `create-if-absent` for `init` and `replace-if-changed` under `init --upgrade`, with the reason that the file is generated and additions live in `.claude/settings.autonomous.local.json`. Add a row for the outer-loop scripts with the same two policies, and a row stating that `init` never writes the local additions file.
- [ ] `git.ts`: add `gitCommonDir(repoRoot: string): string | undefined`, a fixed-argv `rev-parse --git-common-dir` resolved against `repoRoot`, returning `undefined` when git does not answer.
- [ ] `write-plan-replace.test.mjs`: import `WritePlan` from `../dist/core/writer.js` and `gitCommonDir` from `../dist/core/git.js`, with a `Reporter` given capturing sinks. Cover create, keep, replace with backup, mode-only replacement with no backup, `--dry-run` leaving the tree and backup directory byte-identical, a symlink target refused, preserved mode when the request has none, no temporary file left after a success or a forced failure, a replacement keeping an already-open file's old inode, and `gitCommonDir` from a main checkout and a linked worktree.

**Verification:**

- `cli/test/write-plan-replace.test.mjs` passes.
- A second `apply` of the same plan reports only `kept` for these requests and creates no backup directory.
- Every `chmodSync`, `copyFileSync`, `mkdirSync`, `openSync`, `renameSync` and `rmSync` that serves a plan in `writer.ts` is inside `commitWrite` or a helper only it calls.
