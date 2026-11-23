# Story: The flow host reads the round and reviewer files

## Context

This branch gives `devscene-flow-host` the harness's round and reviewer files. That covers four things: reading a reviewer's verdict, the rules a reviewer file must meet, the refusal and re-dispatch of a reviewer file the check rejects, and resuming a round from the files on disk. It is part of #376. Today those rules live only in the bash walker: `cli/templates/scripts/lib/flow-walker-gates.sh` and the `ROUNDS`, `A REFUSED ROUND FILE` and `STATE` paragraphs of `cli/templates/scripts/flow-walker.sh`. GraphScene reads no harness file (`graphscene/src/graphscene/engine/walker.py` → *"Deliberately not covered"*), so the rules have to sit in the host before the compatibility command (#465) can answer `next` and `check-round-file` the way `flow-walker.sh` does. This branch adds no command line. Rendering a step, a `refused:` line or an exit status stays with the `commands` layer, and `devscene-flow-host/src/devscene_flow_host/commands/` stays empty.

**Where the code lands** follows #418's three layers (`.claude/context/devscene-flow-host.md` → `## The internal layers`). `records` reads files into plain values and imports only the standard library. `host` applies the rules and composes GraphScene's `Walker`. The work is cut bottom-up:

- Tasks 1–3 are `records` readers, each reading its file as one named bash function reads it:
  - Task 1: the reviewer file (`fw_review_verdict`, `fw_round_file_check`, `fw_next_review_index`, `fw_fail_count`).
  - Task 2: a round's evidence (`fw_round_evidence`), the only reader that asks `git`.
  - Task 3: the story index's escalation evidence (`fw_index_evidence`). It feeds the cap payload that `rounds:` / `evidence` lines carry, so #465 only has to render it.
- Tasks 4–8 are `host` modules:
  - Task 4: path templates and the round lookups.
  - Task 5: the refusal record.
  - Task 6: the resume rules.
  - Task 7: recording an outcome under the reviewer-file rules.
  - Task 8: the two re-entry calls, `start` and `current`.
- Task 9 updates the package README.
- Task 10 is the catch-all task. It updates the two root documents that list what the host ships.

**Decided here — where the refusal count lives.** GraphScene's `WalkState` has no field for it, and its codec refuses an extra key. So the count lives in a host-owned file in the walk's own directory: `<stateDir>/.flow_walker_state/round_refusals/<quote(branch, safe="")>.json` (Task 5). It holds each gate's refusal count, last reason and re-dispatch mark for one round and round number, plus the `refused:` lines the last printed step carried. A count recorded for another round or number reads as empty, so a closed round needs no clean-up for its counts to stop applying. It is guarded by its own lock, which is taken *outside* the walk store's lock. #418 rejected a companion file for the walk's branch. That risk does not carry over here: a lost or stale count costs at most two extra re-dispatches, and a lost file is never a wrong route (task prompt, *"A lost state file is the case this branch makes work"*).

**How a refused file fits GraphScene's round.** A refused reviewer file records nothing in the walk, so in GraphScene's view that gate is still *out*. The host gives the bash behaviour back on top of this (Tasks 7–8):

- The refused gate is left out of a `wait`'s pending list and out of `current`.
- When no other gate is out, the refused gates are re-dispatched as one set, in the same round, with their `refused:` lines.
- The third refusal records the held outcome `error`.

**Two departures, each deferred with a marker.** First, in one case the bash walker escalates a held gate at once: no gate is out except refused ones (`flow-walker.sh` → `record_in_set`, *"With none out: a held gate escalates"*). GraphScene has no way for a host to set a due gate aside, so in that case the host re-dispatches the refused gates first and escalates at the join that follows. Task 7 writes the entry-point marker `# TODO: @claude add a follow up task for this: …`, naming the GraphScene change that would revert this (`harness-runs/lessons.md` → *Ports and parallel implementations*, first rule). Task 7's test pins the behaviour as it stands.

Second, bash keeps a findings file given outside a round gate (a non-round reviewer's `FAIL`, such as `ui_review`'s, or `answered`) as `revision_findings`, and the writer's revision prints it as `arg.findings_file:` (`flow-walker.sh` → `next`). GraphScene refuses a `detail` outside a round, so the host requires that file but does not keep it. Task 7 writes a second entry-point marker at `record_outcome`'s non-gate branch, naming what reverts it: a host-side record of `revision_findings` for a non-round reviewer and for `answered`. Task 7's test pins this behaviour as it stands too.

**Not this branch's.** Each of these is stated as "Deliberately not covered" in the module concerned:

- The `check-round-file` command and its exit 3.
- Every rendered line.
- Carrying a non-round reviewer's findings file (`ui_review`'s FAIL), or one given with `answered`, to its writer's revision. This is deferred with Task 7's second `TODO: @claude` marker, not excluded.
- The prompt variants and the loop counter that a lost state file loses, as in bash (`docs/flow-graph-walker.md` → *What `start` reads, and what it never carries*).

**Top risks:** The likeliest failure is the refusal record and the GraphScene walk drifting apart when a round's gates are recorded by simultaneous calls. Task 5's lock, taken outside the walk's lock by every recording call, guards it, and Task 7 pins it with a two-thread join. Second is a refused gate leaking back into a `wait` or `current` as if it were still out, or being dispatched twice. Task 7 owns the re-dispatch translation and Task 8 the `current` filter, and each asserts the exact pending list. Third is a resume mapping that differs from `start_round`: it either re-reviews a recorded gate or skips a missing one. Task 6 pins each of the `STATE` paragraph's rules with hand-written evidence, and Task 8 replays them end to end on the harness's own format-4 graph.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below top-to-bottom; the commit step flips each one to `[x]` as that task's commit lands. **Only the committing role flips a marker** — the commit step — `commit-on-branch.sh --unit` — in every flow that runs the unit loop, the orchestrator itself in the supervised flow, which runs none: an implementer never changes a marker here, and never edits any other line of this section, in an index a run is iterating. `[ ]` markers anywhere else (sub-step bullets inside the per-task files) are informational progress markers for the implementer — they are never the iteration source and the commit step does not touch them.

Each entry resolves 1:1 to `harness-runs/task_plans/feat_flow_host_round_files/task_<K>_plan.md`. Ordered bottom-up by ship sequence, with the catch-all layer last.

1. [x] **Task 1** — Read a reviewer file: its verdict, the round-file check, the next free index and the FAIL count _(layer: devscene-flow-host)_ _(points: 20)_
2. [x] **Task 2** — Read a round's evidence from its reviewer files, revision note and plan commits _(layer: devscene-flow-host)_ _(points: 20)_
3. [ ] **Task 3** — Read a story index's escalation evidence _(layer: devscene-flow-host)_ _(points: 8)_
4. [ ] **Task 4** — Render a graph path template and find a reviewer's round and next index _(layer: devscene-flow-host)_ _(points: 10)_
5. [ ] **Task 5** — Keep a round's reviewer-file refusals in the host's own file beside the walk _(layer: devscene-flow-host)_ _(points: 15)_
6. [ ] **Task 6** — Build a round's `RoundResume` from the files on disk _(layer: devscene-flow-host)_ _(points: 20)_
7. [ ] **Task 7** — Record a gate's outcome under the reviewer-file rules _(layer: devscene-flow-host)_ _(points: 20)_
8. [ ] **Task 8** — Start a walk from the round files and re-read it without its refused gates _(layer: devscene-flow-host)_ _(points: 15)_
9. [ ] **Task 9** — Describe the round and reviewer files in the package README _(layer: devscene-flow-host)_ _(points: 8)_
10. [ ] **Task 10** — List the host's new suites under gate 13 and its round files in the roadmap _(layer: general)_ _(points: 8)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt: *"`feat_flow_host_round_files` gives `devscene-flow-host` the harness's round and reviewer files: reading a reviewer's verdict, the rules a reviewer file must meet, and resuming a round from the files on disk."*

**Derivation entry — corpus files that describe the host (command).** Re-run verbatim from the checkout root: `git grep -l -E 'devscene-flow-host|devscene_flow_host' -- '*.md' ':!harness-runs/**'`

**Derivation entry — corpus files that describe the bash rules being ported (command).** Re-run verbatim from the checkout root: `git grep -l -E 'fw_round_evidence|fw_round_file_check|fw_next_review_index|fw_review_verdict|fw_fail_count|fw_index_evidence' -- '*.md' ':!harness-runs/**'`

No standing matrix under `harness-runs/` covers a file this plan targets, so no row-class entry is owed. The register covers the corpus targets only (Tasks 9 and 10); the source and test files of Tasks 1–8 are outside it.

**Closure invariant:** every site either derivation entry reaches appears as a row below.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `devscene-flow-host/README.md` → `## What it is`, `## The layers`, `## What it reads, answers and keeps`, `## Errors` | — | first entry | `change` | Task 9 |
| 2 | `docs/development.md` → **Gate 13** (*"the suites of its records, … and of its walk of the harness's format-4 planning graph"*) | — | first entry | `change` | Task 10 |
| 3 | `ROADMAP.md` → the `GraphScene` row (*"the harness's GraphScene host at `devscene-flow-host/` … keeps each branch's walk in its own file"*) | — | first entry | `change` | Task 10 |
| 4 | `.claude/CLAUDE.md` → the opening paragraphs and the `devscene-flow-host` context row | — | first entry | `no-change` | names the package, its boundary and its conventions document; none of it changes |
| 5 | `.claude/context/conventions.md` → `## The layers`, `### Where a new responsibility goes` | — | first entry | `no-change` | a conventions document; what it states about the host (its place, its boundary, its lock) is unchanged |
| 6 | `.claude/context/devscene-flow-host.md` → `## Records, and which one is the truth`, `## Errors` | — | first entry | `no-change` | a conventions document. Nothing it states is falsified: the refusal record stays inside `.flow_walker_state/`, and a missing round file is read as a value, as `read_run_mode` already reads a missing ledger |
| 7 | `.claude/review-sweep.md` → the two `devscene-flow-host` rows | — | first entry | `no-change` | its regexes match forms this branch does not write: a `graphscene.` submodule import, and a retyped requirement-name normalisation |
| 8 | `docs/flow-graph-walker.md` → *What `start` reads, and what it never carries*, `### Item 9` | — | second entry | `no-change` | describes the bash walker, which this branch leaves unchanged |
| 9 | `docs/work-report-research/review-plan-reviewer.md` | — | second entry | `no-change` | a research record of its date, not a statement of the host |
| 10 | `docs/work-report-research/reviews/review-plan-reviewer.md` | — | second entry | `no-change` | a research record of its date |
| 11 | `docs/work-report-research/reviews/ui-tests-plan-reviewer.md` | — | second entry | `no-change` | a research record of its date |
| 12 | `docs/work-report-research/task-plan-reviewer.md` | — | second entry | `no-change` | a research record of its date |
| 13 | `docs/work-report-research/ui-tests-plan-reviewer.md` | — | second entry | `no-change` | a research record of its date |
