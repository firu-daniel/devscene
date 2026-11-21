`fix_default_branch_diff_base` makes every end-of-branch diff and commit range use `origin/<default_branch>` as its base, as the Done summary's delivery count already does, so an agent in a run copy stops failing on a ref the copy does not carry.

## Why

A run copy is a clone holding only the run branch locally; the default branch exists there only as `refs/remotes/origin/<default_branch>`. The diff base handed to agents is the bare `<default_branch>`, so `git diff dev...HEAD` and `git log dev..HEAD` fail with "bad revision" / "unknown revision", and each agent falls back to `origin/dev` on its own. Nothing has broken yet, because every agent improvised the right base, but each dispatch spends a failed command and an improvised base, and the fallback is not in any contract.

Reported in the improvement observations of at least six runs: `fix_agent_python_probes` (5 dispatches: architecture-reviewer A2, branch-reviewer B, review-plan-reviewer B.2, skeptic-reviewer C2, statistics-plan-writer D.1), `feat_flow_graph_schema_v2`, `chore_remove_legacy_worktree_arm`, `chore_sandbox_honesty_paragraphs`, `chore_gate12_unroutable_sandbox_rows`, `chore_devscene_github_surface`.

## Decided (2026-11-21)

- The base is `origin/<default_branch>`, the same form `plan_orchestration_instructions_core.md` → `### D.2 Done summary` and `user_review_fixes_instructions_core.md` already use for the delivery count. No local default-branch ref is created in the run copy.

## Leads

_Starting points, not requirements; planning decides what holds._

- **Bare-base sites today** (`git grep -nE "<default_branch>\.\.\.?HEAD|diff_base: <default_branch>" -- plugin`):
  - `plugin/instructions/plan_orchestration_instructions_core.md` — the two `diff_base: <default_branch>` dispatch blocks (architecture and business-parity branch reviews), and its `<default_branch>` resolved-values row, which already names the remote-tracking ref for D.2;
  - `plugin/agents/branch-reviewer.md`, `skeptic-reviewer.md`, `review-plan-reviewer.md` — `git diff <default_branch>...HEAD` directly, not through a `diff_base` argument;
  - `plugin/agents/architecture-reviewer.md`, `business-parity-reviewer.md` — the `diff_base: <default_branch>` example blocks;
  - `plugin/agents/statistics-plan-writer.md` and `plugin/instructions/improvement_observations_instructions.md` — `git log … <default_branch>..HEAD`;
  - `plugin/instructions/docs_phase_instructions.md` — the changed-files and content diffs;
  - `plugin/samples/sample_statistics.md` — the `<default_branch>..HEAD` mention.
- **A token or a literal.** Either each site writes `origin/<default_branch>`, or a new resolved value (e.g. `<diff_base_ref>`) is declared once per file. The second keeps the "never a remembered branch name" rule in one place per file; planning weighs it against the corpus's citation rules.
- **Freshness.** In a run copy `origin/<default_branch>` is the ref the clone was made from. In a supervised session in the main checkout or a linked worktree it is as fresh as the last fetch. Check whether any flow step fetches before the end-of-branch reviews, and whether a stale `origin/<default_branch>` can widen the diff after a merge into the default branch mid-branch.
- **The graph engine.** The planning driver (`scripts/lib/planning-driver-lib.sh`) runs only plan-mode nodes, which take no diff base, so it needs no change today. When implementation phases move onto graphs (#425 and after), a node prompt that carries a diff base should carry `origin/<default_branch>`.

## Depends on

Nothing.
