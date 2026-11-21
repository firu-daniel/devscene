### Task 2 — Base the branch, skeptic and review-plan reviewers' diffs on `origin/<default_branch>`

**Goal:** Three end-of-branch reviewers compute `git diff <default_branch>...HEAD` themselves, with no `diff_base` argument. That fails in a run copy, which carries no local `<default_branch>`. Rebase every such diff on `origin/<default_branch>`, and give each agent the fallback sentence for an adoption with no `origin` remote.

**Where this task stops.** These three agents receive no `diff_base` key, so no dispatch block changes here. The `diff_base` wire is **Task 1's**, and the commit ranges and the docs-phase diff are **Task 3's**. `branch-reviewer.md`'s `git show <default_branch>:.claude/review-sweep.md` is a row read, not a diff (story index `## Context` → *Out of scope*). It keeps the local-first rule `review-sweep.sh` applies: this task moves that rule into the row and leaves the `## Read first` line unchanged. **Task 4**'s test then holds this task's text to two rules: no bare `<default_branch>...HEAD` anywhere, and the fallback sentence present verbatim in every file that runs `git diff` against `origin/<default_branch>`.

### Targets

- `plugin/agents/branch-reviewer.md`
- `plugin/agents/skeptic-reviewer.md`
- `plugin/agents/review-plan-reviewer.md`

**Work:**

- [ ] **The shared row.** Write one replacement `<default_branch>` row for `## Resolved values` and use it word for word in all three files: `` `defaultBranch` — the branch work starts from and merges into. Never a remembered branch name. Every `git diff` in this file is based on its remote-tracking ref `origin/<default_branch>`, which every checkout carries, a run copy included. `` followed by the fallback sentence quoted in the story index `## Context`. In `branch-reviewer.md` only, append one more sentence in place of today's run-copy clause: `git show <default_branch>:.claude/review-sweep.md` reads the local `<default_branch>`, and in a run copy, which carries none (a bare `git rev-parse --verify --quiet refs/heads/<default_branch>` prints nothing), reads `origin/<default_branch>` instead.
- [ ] `branch-reviewer.md`: in `### Pass 1 — Independent review (always)` (the step 3 `--stat` / `--shortstat` block and step 4's `-U15` diff) and in `### Pass 0 — the deterministic sweep` (**Exit `1`.**'s `-U15` diff and **(b)**'s export-enumeration diff), change every `<default_branch>...HEAD` to `origin/<default_branch>...HEAD`. Leave the pathspecs and flags unchanged.
- [ ] `skeptic-reviewer.md` → `## Process`: change the `--stat` / `--shortstat` block and the `-U15` hunk rule to `origin/<default_branch>...HEAD`.
- [ ] `review-plan-reviewer.md` → `## Process` step 3: change both the `--name-only` diff and the `-U15` diff to `origin/<default_branch>...HEAD`.

**Verification:**

- `git grep -nE '(^|[^/])<default_branch>\.\.\.?HEAD' -- plugin/agents/branch-reviewer.md plugin/agents/skeptic-reviewer.md plugin/agents/review-plan-reviewer.md` prints nothing.
- `git grep -nF "re-issue that command once with \`<default_branch>\` in its place and say which base you used." -- plugin/agents/branch-reviewer.md plugin/agents/skeptic-reviewer.md plugin/agents/review-plan-reviewer.md` hits each file once.
- The three `<default_branch>` rows are identical up to `branch-reviewer.md`'s extra `git show` sentence. Compare the three lines from `git grep -n '^| .<default_branch>. |' -- <the three files>`.
- `branch-reviewer.md` → `## Read first`'s `git show <default_branch>:.claude/review-sweep.md` line is unchanged (`git diff` shows no hunk there).
