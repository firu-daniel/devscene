### 1. The freshness sentences claim a stale `origin/<default_branch>` widens the diff only after a merge, but a branch cut from an unpushed local `<default_branch>` widens it too

**File:** `plugin/instructions/plan_orchestration_instructions_core.md` (`## Resolved values`, the `<default_branch>` row) — "it widens only when the branch merged a `<default_branch>` commit the ref does not carry"
**Second site:** `plugin/instructions/improvement_observations_instructions.md` (`## Dispositioned units — an entry per unit closed without a fix`, the **Bound the set to this run before writing anything.** paragraph) — "where `origin/<default_branch>` is behind a `<default_branch>` commit the branch merged,"

**Problem.** Both sentences say a stale `origin/<default_branch>` widens the range in only one case: the branch *merged* a `<default_branch>` commit the ref does not carry. The core's row adds that the three-dot diff "still starts at the branch's fork point". There is a second case. A branch cut on top of a local `<default_branch>` that holds unpushed commits carries those commits from its fork point, with no merge. The merge base of `origin/<default_branch>` and `HEAD` is then the ref's own tip, not the fork point, so `origin/<default_branch>...HEAD` and `origin/<default_branch>..HEAD` both take in the unpushed commits.

`refresh-branch.sh`'s own header names this state as real: *"`--local` is for the state where the local base is AHEAD of the remote one — commits landed in the main checkout and were not pushed"* (`cli/templates/scripts/refresh-branch.sh`). A run copy cannot reach it, because `create-worktree.sh` cuts the branch "from the commit origin reports, never from a local ref" (`cli/templates/scripts/create-worktree.sh`). A branch a person cuts by hand in the main checkout or a linked worktree can reach it.

**Probe run:** `bash scripts/scratch-run.sh harness-runs/scratch/stale_origin_probe.mjs`. It made a throwaway bare remote and clone under the system temp directory, pushed one `dev` commit, committed `unpushed.txt` on local `dev` without pushing, then cut `feat` from local `dev` and committed `feat.txt`. Output:

```
bare base   : "feat.txt"
origin base : "feat.txt\nunpushed.txt"
log origin  : "feat\nunpushed on dev"
```

Both sentences describe the project and give no step, so this is a Should Fix, not a Must Fix. Each still states an invariant that is false. The core row is also the only place the branch's freshness analysis is recorded.

**Fix.** Replace the two clauses. Change no other text in either file.

1. In `plugin/instructions/plan_orchestration_instructions_core.md`, `<default_branch>` row, replace:

   > A three-dot diff against a stale `origin/<default_branch>` still starts at the branch's fork point; it widens only when the branch merged a `<default_branch>` commit the ref does not carry, which `refresh-branch.sh`'s default mode cannot cause because it fetches `origin/<base>` before merging.

   with:

   > A diff or range against a stale `origin/<default_branch>` widens to every `<default_branch>` commit the branch carries and the ref does not — one merged by `refresh-branch.sh --local`, or one the branch was cut on top of from a local `<default_branch>` holding unpushed commits. `refresh-branch.sh`'s default mode cannot cause it, because it fetches `origin/<base>` before merging, and a run copy cannot, because its branch is cut from the commit origin reports.

2. In `plugin/instructions/improvement_observations_instructions.md`, **Bound the set to this run before writing anything.** paragraph, replace:

   > where `origin/<default_branch>` is behind a `<default_branch>` commit the branch merged,

   with:

   > where `origin/<default_branch>` is behind a `<default_branch>` commit the branch carries — one it merged, or one it was cut on top of —

Both files are under `plugin/**/*.md`, so the loop selects the `test/diff-base-corpus.test.mjs` tree guard on its own. Neither replacement adds or removes a `..HEAD` range or the fallback sentence.
