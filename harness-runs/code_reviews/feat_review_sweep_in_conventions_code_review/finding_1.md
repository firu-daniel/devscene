### 1. `review-sweep.sh` refuses every run copy, because a run copy has no local `<default_branch>`

**File:** `cli/templates/scripts/review-sweep.sh` (the default-branch resolution) — "git -C \"$top\" rev-parse --verify --quiet \"$default_branch^{commit}\""; its self-adopted twin `scripts/review-sweep.sh` (same substring); `plugin/agents/branch-reviewer.md` → `## Resolved values`, the `<default_branch>` row, and `## Read first`, the bullet opening "`.claude/review-sweep.md` as `<default_branch>` holds it"

**The problem.** The design (story `## Context` → "The sweep script") is that `branch-reviewer` runs the main checkout's copy as `bash <MAIN_REPO>/<scripts_dir>/review-sweep.sh --repo <repo_root>`, where `<repo_root>` is the run copy in an autonomous run. The script then resolves `<default_branch>` **as a local branch inside `--repo`**:

```bash
git -C "$top" rev-parse --verify --quiet "$default_branch^{commit}" >/dev/null 2>&1 \
  || rs_fail "default branch $default_branch does not resolve in $top"
```

and uses the same bare name for `git show "$default_branch:$RS_SWEEP_PATH"` and for `git diff "$default_branch...HEAD"`.

A run copy carries no local default branch. `create-worktree.sh` creates the working copy "from origin/$default_branch" (`cli/templates/scripts/create-worktree.sh`, the "has no 'origin' remote" refusal). The run copy this review ran in has exactly three refs: `refs/heads/feat_review_sweep_in_conventions`, `refs/remotes/origin/dev` and `refs/remotes/origin/feat_review_sweep_in_conventions`. In it, `git rev-parse --verify --quiet 'dev^{commit}'` exits 1, and `git diff dev...HEAD` fails with `fatal: bad revision 'dev...HEAD'`. So in every semi-autonomous and autonomous review, which is where this branch's feature is meant to run, the script exits `2` with `default branch dev does not resolve in <run copy>`. Half (a) of Pass 0 never runs there, and the reviewer reports a "configuration gap" that no edit to the configuration or the sweep document can close.

`cli/test/review-sweep.test.mjs` does not catch it. Every case runs the script against the fixture it lives in, where `main` is a local branch. No case sets up the deployed shape: the script in a main checkout and `--repo` aimed at a clone of it.

The same bare `<default_branch>` reaches the reviewer's own new `## Read first` bullet (`git show <default_branch>:.claude/review-sweep.md`) and the Pass 0 hit-verification command (`git diff -U15 <default_branch>...HEAD -- <path>`). Both fail the same way in a run copy. The first one would also report the sweep document as unreadable, a configuration gap, when it is in fact committed.

These two are not the only sites. The pre-existing diff commands in `branch-reviewer.md` fail the same way in a run copy: the Pass 1 step 1 `--stat` and `--shortstat` commands, the step 4 `git diff -U15 <default_branch>...HEAD -- <segment files>`, and the Pass 0 half (b) export enumeration. This review had to diff against `origin/dev` for exactly that reason. Fix step 3 therefore edits the `<default_branch>` row in `## Resolved values` rather than the two added sites. The choice is deliberate: one row-level rule covers every place the file uses `<default_branch>` as a git revision. Patching only the added lines would leave the older commands broken in the same run copy.

**Fix.**

1. In `cli/templates/scripts/review-sweep.sh`, replace the resolution block above with one that falls back to the remote-tracking ref, and use the resolved ref everywhere the script names the base:

   ```bash
   if git -C "$top" rev-parse --verify --quiet "refs/heads/$default_branch^{commit}" >/dev/null 2>&1; then
     base_ref=$default_branch
   elif git -C "$top" rev-parse --verify --quiet "refs/remotes/origin/$default_branch^{commit}" >/dev/null 2>&1; then
     base_ref=origin/$default_branch
   else
     rs_fail "default branch $default_branch does not resolve in $top, as a local branch or as origin/$default_branch"
   fi

   doc=$(git -C "$top" show "$base_ref:$RS_SWEEP_PATH" 2>/dev/null) \
     || rs_fail "$RS_SWEEP_PATH is not committed on $base_ref"
   ```

   Replace `$default_branch` with `$base_ref` in the skeleton message ("on $default_branch is still an untouched skeleton"), in the `no '## Sweep rows' heading` message, and in the `git diff … "$default_branch...HEAD"` call and its failure message. In the header comment, extend the `WHO RUNS IT` paragraph's `git show <default_branch>:.claude/review-sweep.md` sentence with: "— or `origin/<default_branch>` when `--repo` carries no local `<default_branch>`, as a run copy does". Make the same sentence change to the EXIT MAP's "`<default_branch>` not resolvable" clause.
2. Copy the edited template byte for byte to `scripts/review-sweep.sh`.
3. In `plugin/agents/branch-reviewer.md` → `## Resolved values`, append to the `<default_branch>` row's cell: "In a run copy, which carries no local `<default_branch>` (a bare `git rev-parse --verify --quiet refs/heads/<default_branch>` prints nothing), write `origin/<default_branch>` wherever this file uses `<default_branch>` as a git revision."
4. In `docs/analyze.md` → `## 13. The review-sweep document`, paragraph **(f)**, after "The script reads the document as `git show <default_branch>:.claude/review-sweep.md`", add "— `origin/<default_branch>` in a run copy, which has no local default branch —".
5. Add a case to `cli/test/review-sweep.test.mjs` that reproduces the deployed shape. First fix the imports: add `mkdtemp` and `rm` to the `node:fs/promises` import, so it reads `import { mkdir, mkdtemp, rm, writeFile } from 'node:fs/promises';`, and add `import { tmpdir } from 'node:os';`. Build the fixture with `sweepFixture(t, { [SWEEP]: sweepDoc([CONSOLE_ROW]) })`, write `src/a.js` holding `console.log(1);\n` and `commitAll` it. Then clone the fixture into a fresh directory from `mkdtemp(join(tmpdir(), 'review-sweep-clone-'))`, removed in `t.after` with an in-process `rm(…, { recursive: true, force: true })`. Run it as `runGit(dir, ['clone', '--quiet', dir, clone])`. The clone checks out `feat` and carries only `origin/main`. Assert that `git -C <clone> rev-parse --verify --quiet refs/heads/main` fails, so the case proves something. Then run `sweep(dir, ['--repo', clone])` and expect `assertHits(…, ['src/a.js:1: Raw console'])`. Keep the existing "unresolvable default branch" case: its `/default branch main does not resolve/` pattern still matches the new message.

This fix edits `cli/test/review-sweep.test.mjs`, so that is the one test file it runs: `npm test --workspace cli -- test/review-sweep.test.mjs`, from the repository root, as one plain foreground command. The self-adoption byte-identity test and the full suite run later, in the Run gates phase.
