# Skeptic Review: fix_default_branch_diff_base

## Context

**Branch:** `fix_default_branch_diff_base`
**Date:** 2026-11-21
**Reviewed:** the whole branch diff against `origin/dev`, 13 files with 116 insertions and 33 deletions, after the two code-review fixes. That covers the `diff_base: origin/<default_branch>` dispatch blocks and their quoted copies, the branch, skeptic and review-plan reviewers' diff commands, the `git log` ranges and their mentions, the new suite `cli/test/diff-base-corpus.test.mjs`, and its `treeGuards` entry. This run copy has no local `dev`: a bare `git diff dev...HEAD` failed with `fatal: bad revision 'dev...HEAD'`, so the review used `origin/dev`. 14 run-artifact files excluded from the reviewed diff.

**De-duplicated against:** `harness-runs/code_reviews/fix_default_branch_diff_base_code_review.md` and its two findings: the freshness sentences, and the `ALLOWED_LITERAL` scope. Both are applied on the branch. No business-parity branch review exists, because `phases.parity` is `false`. No architecture branch review was written for this branch. No planning round recorded an incidental finding.

**Adversarial checks, first-hand.**

- **Check 1 (wiring).** `git grep` over `plugin/` finds no bare `<default_branch>...HEAD`, `<default_branch>..HEAD` or `diff_base: <default_branch>` outside D.2's sanctioned `git rev-list --count` fallback. No `diff_base` dispatch exists outside the two core blocks, and no graph or script prompt passes one. The fallback sentence appears exactly once in each of the eight files whose `git diff` or `git log` runs against the base, and those eight are exactly the files the suite's `DIFF_SITE` selects. The suite is under `cli/test/`, which `node --test` discovers, and its `treeGuards` entry follows the form of its siblings.
- **Check 2 (runtime address).** `origin/<default_branch>` resolves in a run copy: this copy carries `refs/remotes/origin/dev`. `create-worktree.sh` mirrors the pushed refs into the clone, and `refresh-branch.sh` mirrors the fetched `refs/remotes/origin/<base>` into a clone target (`hr_copy_sync_out_var`), so the copy's ref follows a default-mode refresh. The parity leg is inert.
- **Check 3 (citations).** These were opened and confirmed: `plugin/agents/README.txt` → "Port-time corrections" (byte-identical quoted blocks), `.claude/context/plugin.md` → `## Writing agent prose` ("An agent's growth is paid for by behaviour"), and the `refresh-branch.sh` header ("Default mode fetches and merges `origin/<base>`"). The suite's RED ONCE record names a real line, but as a line coordinate (Finding 1).
- **Checks 4 and 5.** No divergence is marked intentional. The widened range against a stale `origin/<default_branch>` is the task prompt's own decision, and code-review Finding 1 already raised it, so it is not re-raised here.

**Headline.** The base change is complete and wired. One net-new Should Fix remains.

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 1** — Replace the line coordinate in the suite's RED ONCE record with a heading anchor _(layer: cli)_

---

## Must Fix

_None._

---

## Should Fix

### 1. The suite's RED ONCE record locates its failing site by a line coordinate
→ [finding_1.md](fix_default_branch_diff_base_skeptic_review/finding_1.md)

---

## Nice to Have

_None._

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from and this section is empty.
