# Story: Every end-of-branch diff and commit range is based on `origin/<default_branch>`

## Context

This branch moves every end-of-branch diff and commit range the plugin corpus hands an agent from the bare `<default_branch>` to its remote-tracking ref `origin/<default_branch>`. That is the form `plugin/instructions/plan_orchestration_instructions_core.md` → `### D.2 Done summary` and `plugin/instructions/user_review_fixes_instructions_core.md` → the same section already use for the delivery count. A run copy is a clone holding only the run branch locally, so `git diff <default_branch>...HEAD` and `git log <default_branch>..HEAD` fail there with "bad revision" / "unknown revision", and each reviewer has been falling back to `origin/<default_branch>` on its own, off-contract. No local default-branch ref is created in the run copy (task prompt → `## Decided (2026-11-21)`).

**Literal, not a new token.** Each site writes `origin/<default_branch>` in place. No `<diff_base_ref>` token is minted. The D.2 bullets already spell that literal, so it is the established form. `<default_branch>` stays the one token each file declares, which keeps the "never a remembered branch name" rule in the file's existing `## Resolved values` row. A new token would add a row to every file without adding any behaviour (`.claude/context/plugin.md` → `## Writing agent prose`, *"An agent's growth is paid for by behaviour"*). Each file's existing `<default_branch>` row is reworded to name the remote-tracking ref as the base.

**One fallback, worded once and copied byte for byte.** D.2 already handles an adoption with no `origin` remote by re-issuing against the local ref and saying so. Every diff and `git log` site here gets the same escape, in one sentence that is identical in every file that issues such a command:

> Where git reports `origin/<default_branch>` unknown — a repository with no `origin` remote — re-issue that command once with `<default_branch>` in its place and say which base you used.

Tasks 1–3 refer to it as **the fallback sentence**. Task 4's test holds every copy to that exact text.

**Freshness, checked and not changed.** No flow step fetches before the end-of-branch reviews, and this branch adds no fetch. In a run copy, `origin/<default_branch>` is the ref the clone was made from. In the main checkout or a linked worktree, it is as fresh as the last fetch. A three-dot diff against a stale `origin/<default_branch>` still starts at the branch's fork point. It widens only when the branch has merged a `<default_branch>` commit that the ref does not carry. `refresh-branch.sh`'s default mode cannot cause that, because it fetches `origin/<base>` before it merges (`cli/templates/scripts/refresh-branch.sh` header, *"Default mode fetches and merges `origin/<base>`"*). Only its `--local` mode can. The bare local ref has the mirror-image problem after a default-mode refresh, so the remote-tracking ref is no worse in any case and strictly better in a run copy. Task 1 states this once, in the core's `<default_branch>` row. Task 3 rewrites the one existing disclosure of a stale range (`improvement_observations_instructions.md` → `## Dispositioned units — an entry per unit closed without a fix`) against the new ref.

**Out of scope, deliberately.** `review-sweep.sh` (`cli/templates/scripts/review-sweep.sh`, and the self-adopted copy `scripts/review-sweep.sh`) resolves its own base: the local `<default_branch>` when one exists, else `origin/<default_branch>`. So it already works in a run copy and is not the failure this branch fixes. The same holds for `branch-reviewer.md`'s `git show <default_branch>:.claude/review-sweep.md`, which reads rows rather than computing a diff. It keeps the script's local-first rule, which Task 2 restates for that one command. The planning driver (`scripts/lib/planning-driver-lib.sh`) runs only plan-mode nodes, which take no diff base, so it needs no change. When implementation phases move onto graphs (#425 and after), a node prompt carrying a diff base should carry `origin/<default_branch>`; that work belongs to #425, not to this branch.

**Ship order.** Three `plugin` tasks come first, then the `cli` test, then the `general` registration. The plugin tasks are the contract and the test is its consumer. It asserts the plugin text, so landing it before Tasks 1–3 would make its own run fail. The test therefore follows the text it guards rather than the configured `layers[]` order (`.claude/context/conventions.md` → `### The order files are created, so a half-built feature is still coherent`, *"Contract before consumer, always"*). The catch-all registration is last, as always.

**Top risks:** The first risk is a site left on the bare base, which brings back the failure in exactly one reviewer. Task 4's tree guard fails on any bare `<default_branch>...HEAD`, `<default_branch>..HEAD` or `diff_base: <default_branch>` left anywhere in `plugin/**/*.md`, and Task 5 registers that guard so later plugin edits run it too. The second risk is the dispatch blocks drifting from the copies the two receiving agents quote (`plugin/agents/README.txt` → *"Port-time corrections"* requires those copies byte-identical). Task 1 owns all four blocks in one commit. The third risk is the fallback sentence drifting between files, so an adoption with no remote gets different behaviour from different agents. Task 4 asserts the exact sentence in every file that issues a diff or `git log` against the new base.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below top to bottom. **Only the committing role flips a marker:** the commit step, `commit-on-branch.sh --unit`, in every flow that runs the unit loop, and the orchestrator itself in the supervised flow, which runs none. No implementer changes a marker, or edits any other line of this section, in an index a run is iterating. `[ ]` markers anywhere else, such as sub-step bullets inside the per-task files, are informational progress markers only, and the commit step never touches them.

Each entry resolves 1:1 to `harness-runs/task_plans/fix_default_branch_diff_base/task_<K>_plan.md`.

1. [x] **Task 1** — Pass `diff_base: origin/<default_branch>` to the parity and architecture reviewers _(layer: plugin)_ _(points: 15)_
2. [x] **Task 2** — Base the branch, skeptic and review-plan reviewers' diffs on `origin/<default_branch>` _(layer: plugin)_ _(points: 15)_
3. [x] **Task 3** — Base the commit ranges, the docs-phase diff and their mentions on `origin/<default_branch>` _(layer: plugin)_ _(points: 15)_
4. [x] **Task 4** — Add the diff-base corpus test over `plugin/**/*.md` _(layer: cli)_ _(points: 15)_
5. [x] **Task 5** — Register the diff-base corpus test as a tree guard _(layer: general)_ _(points: 5)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt: *"makes every end-of-branch diff and commit range use `origin/<default_branch>` as its base, as the Done summary's delivery count already does"*.

**Derivation entry A — revision uses in the durable corpus (command).** Re-run verbatim from the checkout root:
`git grep -nE '<default_branch>\.\.\.?HEAD|diff_base: <default_branch>|git show <default_branch>:' -- plugin docs README.md ARCHITECTURE.md`

**Derivation entry B — `<default_branch>` token rows that name a base (command).** Re-run verbatim from the checkout root:
`git grep -nE '^\| .<default_branch>. \| config value \|.*(diff base|commit range|git revision)' -- plugin`

**Derivation entry C — standing-artifact rows (procedure).** **Artifact:** the two standing ledgers under `harness-runs/`, `harness-runs/lessons.md` and `harness-runs/improvement_suggestions.md`. **Traversal:** each file's `## ` topic headings in file order, then the one-line entries under each. **Per-candidate decision rule:** an entry is reached when it names a diff base, a commit range, or `<default_branch>` / `origin/<default_branch>` used as a git revision. Walked on 2026-11-21, it reached no entry, so it contributes no row.

**Closure invariant:** every site that entry A, B or C reaches appears as a row below. Entry A also matches the `origin/`-prefixed forms, so re-running it after the branch lands reaches the same sites. At that point every `change` row's command or range carries `origin/<default_branch>` as its base, and every `no-change` row reads as it does today.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `docs/analyze.md` → **(e) A shipped script, over the reviewer's own grep.** ("applies each to the added lines of `git diff <default_branch>...HEAD`") | — | entry A, `<default_branch>...HEAD` | `no-change` | Describes `review-sweep.sh`'s own diff, whose base the script resolves itself (local, else `origin/<default_branch>`). This branch changes no script (Context → *Out of scope*). |
| 2 | `docs/analyze.md` → **(f) Rows read from the default branch…** ("`git show <default_branch>:.claude/review-sweep.md` — `origin/<default_branch>` in a run copy") | — | entry A, `git show <default_branch>:` | `no-change` | Already states the run-copy base for the script's row read, and the script is unchanged. |
| 3 | `docs/work-report-research/review-plan-reviewer.md` → S7 ("Run `git diff <default_branch>...HEAD --name-only`") | — | entry A | `no-change` | Research record of the agent as it stood when measured. Editing it falsifies the record (`.claude/context/conventions.md` → `## Documents of record`). |
| 4 | `docs/work-report-research/reviews/statistics-plan-writer.md` → finding 1 ("`git diff <default_branch>...HEAD --stat`") | — | entry A | `no-change` | Research review record, same reason as row 3. |
| 5 | `docs/work-report-research/statistics-plan-writer.md` → table row "`git log <default_branch>..HEAD` messages" | — | entry A | `no-change` | Research record, same reason as row 3. |
| 6 | `docs/work-report-research/statistics-plan-writer.md` → S4 ("over `<default_branch>..HEAD`") | — | entry A | `no-change` | Research record, same reason as row 3. |
| 7 | `plugin/instructions/plan_orchestration_instructions_core.md` → `## Resolved values`, `<default_branch>` row | — | entry B, `diff base` | `change` | Task 1 |
| 8 | `plugin/instructions/plan_orchestration_instructions_core.md` → `### A1.5.1 Generate the parity review` dispatch block (`diff_base: <default_branch>`) | — | entry A | `change` | Task 1 |
| 9 | `plugin/instructions/plan_orchestration_instructions_core.md` → `### A2.1 Generate the architecture review` dispatch block (`diff_base: <default_branch>`) | — | entry A | `change` | Task 1 |
| 10 | `plugin/instructions/plan_orchestration_instructions_core.md` → `### D.2 Done summary`, delivery bullet (`git rev-list --count origin/<default_branch>..HEAD`, and its fallback `git rev-list --count <default_branch>..HEAD`) | — | entry A, `..HEAD` | `no-change` | Already the target form. Its own no-remote fallback is the precedent the fallback sentence follows. |
| 11 | `plugin/instructions/user_review_fixes_instructions_core.md` → `## Resolved values`, `<default_branch>` row | — | entry B, `commit range` | `no-change` | Already names `origin/<default_branch>` as the base of the only range that file computes. |
| 12 | `plugin/instructions/user_review_fixes_instructions_core.md` → `### D.2 Done summary`, delivery bullet | — | entry A, `..HEAD` | `no-change` | Already the target form, same as row 10. |
| 13 | `plugin/agents/architecture-reviewer.md` → `## Resolved values`, `<default_branch>` row | — | entry B, `diff base` | `change` | Task 1 |
| 14 | `plugin/agents/architecture-reviewer.md` → `### Implemented-solution mode (insertion point 2)`, quoted dispatch block (`diff_base: <default_branch>`) and its `diff_base` key row | — | entry A | `change` | Task 1 |
| 15 | `plugin/agents/business-parity-reviewer.md` → `## Resolved values`, `<default_branch>` row | — | entry B, `diff base` | `change` | Task 1 |
| 16 | `plugin/agents/business-parity-reviewer.md` → `### Implemented-solution mode (insertion point 2)`, quoted dispatch block (`diff_base: <default_branch>`) and its `diff_base` key row | — | entry A | `change` | Task 1 |
| 17 | `plugin/agents/branch-reviewer.md` → `## Resolved values`, `<default_branch>` row ("In a run copy, which carries no local `<default_branch>` … write `origin/<default_branch>`") | — | entry B, `diff base` / `git revision` | `change` | Task 2 |
| 18 | `plugin/agents/branch-reviewer.md` → `## Read first (everything — the branch reviewer needs full context)`, `git show <default_branch>:.claude/review-sweep.md` | — | entry A, `git show <default_branch>:` | `no-change` | A row read, not a diff. It keeps the script's local-first rule, which Task 2 moves into the row (row 17) without changing this line. |
| 19 | `plugin/agents/branch-reviewer.md` → `### Pass 1 — Independent review (always)`, step 3 `--stat` / `--shortstat` block and step 4 `git diff -U15 <default_branch>...HEAD` | — | entry A | `change` | Task 2 |
| 20 | `plugin/agents/branch-reviewer.md` → `### Pass 0 — the deterministic sweep`, **Exit `1`.** (`git diff -U15 <default_branch>...HEAD -- <path>`) and **(b) The new-exported-symbol caller check** (`git diff <default_branch>...HEAD -- …`) | — | entry A | `change` | Task 2 |
| 21 | `plugin/agents/skeptic-reviewer.md` → `## Resolved values`, `<default_branch>` row | — | entry B, `diff base` | `change` | Task 2 |
| 22 | `plugin/agents/skeptic-reviewer.md` → `## Process`, the `--stat` / `--shortstat` block and the `git diff -U15 <default_branch>...HEAD` hunk rule | — | entry A | `change` | Task 2 |
| 23 | `plugin/agents/review-plan-reviewer.md` → `## Resolved values`, `<default_branch>` row | — | entry B, `diff base` | `change` | Task 2 |
| 24 | `plugin/agents/review-plan-reviewer.md` → `## Process` step 3 (`--name-only` and `-U15` diffs) | — | entry A | `change` | Task 2 |
| 25 | `plugin/agents/statistics-plan-writer.md` → `## Resolved values`, `<default_branch>` row ("the base of the `<default_branch>..HEAD` commit range") | — | entry A and entry B, `commit range` | `change` | Task 3 |
| 26 | `plugin/agents/statistics-plan-writer.md` → `## Read first` ("commit messages** over `<default_branch>..HEAD`") and `## Process` step 1 (`git log --format='%h %s%n%b' <default_branch>..HEAD`) | — | entry A | `change` | Task 3 |
| 27 | `plugin/instructions/improvement_observations_instructions.md` → `## Resolved values`, `<default_branch>` row | — | entry B, `commit range` | `change` | Task 3 |
| 28 | `plugin/instructions/improvement_observations_instructions.md` → `## Optimization observations — trip-wires, not reflection` **(d)** ("over `<default_branch>..HEAD`") and `## Dispositioned units — an entry per unit closed without a fix` (the `git log … <default_branch>..HEAD` command, "`<default_branch>..HEAD` spans the whole **branch**", "where the local `<default_branch>` ref is behind") | — | entry A | `change` | Task 3 |
| 29 | `plugin/instructions/docs_phase_instructions.md` → `## Resolved values`, `<default_branch>` row, and `## Auto-skip` (the `--name-only` diff and **The content diff, computed here too.**) | — | entry A and entry B, `diff base` | `change` | Task 3 |
| 30 | `plugin/samples/sample_statistics.md` → `## Counts breakdown`, `dispositioned_points` ("no commit in `<default_branch>..HEAD`") | — | entry A | `change` | Task 3 |
| 31 | `plugin/docs/AUTONOMOUS_FLOW.md` → `## Resolved values`, `<default_branch>` row ("the diff base the branch gates compute against") | — | entry B, `diff base` | `change` | Task 3 |
