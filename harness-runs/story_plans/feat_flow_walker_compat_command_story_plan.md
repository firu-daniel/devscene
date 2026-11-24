# Story: `flow-walker.sh`'s compatibility command over `devscene-flow-host`

## Context

This branch gives `devscene-flow-host` its first command line: `devscene-flow-walker`, a compatibility command that speaks `flow-walker.sh`'s grammar — the verbs `start` / `next` / `current` / `check-round-file`, their flags, the `key: value` output and the exit codes 0–3 with one `flow-walker: <cause>` line on stderr. It is built over the host from #418 and the round-file rules from #464, so that #419 can hand `flow-walker.sh` off to it for every caller with no bash fallback. The command records an outcome only through `host/round_gates.py` → `record_outcome`, starts only through `host/re_entry.py` → `start_walk` and re-reads only through `current_step` — never through GraphScene's `Walker` directly, which would skip the round-file check, the refusal count and the `refused:` lines.

The bar is the task prompt's **Decided (2026-11-24)**, not byte-for-byte parity. Every line a caller parses keeps bash's form — the keys, their order, the exit codes and the actions — as `cli/templates/scripts/flow-walker.sh`'s header (`OUTPUT`, `EXIT CODES`) states them. Where the host routes better, the host's way wins, and each such difference, plus every one still open, is listed in `devscene-flow-host/README.md` so #419 updates the `cli/test/flow-walker*.test.mjs` suites instead of rediscovering them. A refusal's stderr text may be the host's own wherever no caller parses it; a `git grep` over `plugin/`, `cli/templates/`, `cli/test/` and `scripts/` for `no walk in progress` and `no run-mode record` finds no reader outside the walker itself.

The branch also closes #464's non-round findings-file gap. Bash keeps the findings file given at a non-gate call — a non-round reviewer's `FAIL` (`ui_review`), or `answered` — as `revision_findings`, overwrites it when a round closes, and clears it on `start` (`flow-walker.sh` → `next`'s `dispatch` and `answer` branches, `close_round`, `start`). The host gets the same record, beside the walk as #464's refusal record is: `RevisionFindingsStore` at `<stateDir>/.flow_walker_state/revision_findings/<quote(branch, safe="")>.json`, written only under `RefusalStore`'s lock, carried on `HostStep.revision_findings`, and taking precedence over a closed round's files exactly as bash's single `revision_findings` key does. The `TODO: @claude` marker in `record_outcome`'s non-gate branch goes; the other one, at `_redispatch` (the held-gate escalation), is #472's and stays.

The work is eight single-layer tasks, bottom-up: two `host` tasks (the kept findings file, the predicate host's last refusal reason), four `commands` tasks (rendering, argument parsing, the entry point, its concurrency suite), the package README, and last the catch-all `general` task for `ROADMAP.md`. Decisions this plan makes where the prompt left them to planning: the graph is located by a launcher-supplied `--flows <dir>` flag (the one flag `flow-walker.sh` lacks, since bash finds its graph beside itself), as `<dir>/<flow>.v4.graph.json`; the two locks keep their own 120 s bounds, because every `start` and `next` takes `RefusalStore`'s lock first and `current` takes neither, so the walk store's lock is never contended among the command's own callers and the effective wait stays bash's 120 s; and the run-mode refusal keeps the host's text, `… and no skipped ids given`, listed as a difference.

**Top risks:** a rendered line that drifts from bash's form breaks every caller that parses it at #419's switch-over, so Task 3 asserts each block against literals written from `flow-walker.sh`'s `OUTPUT` grammar and `REPRO` block, and Task 5 walks the `REPRO` sequence end to end through the command. An exit status read wrongly is the second risk: the orchestrator reads `current`'s exit 1 as *"no saved walk"* and exit 2 as a blocker, so Task 5 maps an absent saved walk to bash's exit-1 refusal and every fault, an unexpected exception included, to exit 2, never to Python's own exit 1. The third is the kept findings file going stale or missing: Task 1 pins that a round closing clears it, `start` clears it, a held outcome in an open set never writes it, and `ui_review`'s `FAIL` reaches `ui_writer`'s revision with it.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below top-to-bottom; the commit step flips each one to `[x]` as that task's commit lands. **Only the committing role flips a marker** — the commit step — `commit-on-branch.sh --unit` — in every flow that runs the unit loop, the orchestrator itself in the supervised flow, which runs none: no implementer changes a marker here, or edits any other line of this section, in an index a run is iterating. `[ ]` markers anywhere else (sub-step bullets inside the per-task files) are informational progress markers for the implementer — they are never the iteration source and the commit step never touches them.

Each entry resolves 1:1 to a self-contained `harness-runs/task_plans/feat_flow_walker_compat_command/task_<K>_plan.md`. Ordered bottom-up by ship sequence, with the catch-all layer last.

1. [x] **Task 1** — Keep a non-round findings file for the writer's revision in `host/revision_findings.py` _(layer: devscene-flow-host)_ _(points: 20)_
2. [x] **Task 2** — Expose the predicate host's last refusal reason as `HarnessPredicateHost.last_refusal` _(layer: devscene-flow-host)_ _(points: 8)_
3. [x] **Task 3** — Render a `HostStep` as `flow-walker.sh`'s `key: value` output in `commands/render.py` _(layer: devscene-flow-host)_ _(points: 20)_
4. [x] **Task 4** — Parse `flow-walker.sh`'s verbs and flags in `commands/arguments.py` _(layer: devscene-flow-host)_ _(points: 10)_
5. [x] **Task 5** — Add the `devscene-flow-walker` command in `commands/flow_walker.py` with its exit codes _(layer: devscene-flow-host)_ _(points: 20)_
6. [x] **Task 6** — Pin the command's concurrency in `tests/test_flow_walker_concurrency.py` _(layer: devscene-flow-host)_ _(points: 10)_
7. [x] **Task 7** — Document the command and its differences from `flow-walker.sh` in the package README _(layer: devscene-flow-host)_ _(points: 15)_
8. [x] **Task 8** — Record the compatibility command in `ROADMAP.md`'s GraphScene row _(layer: general)_ _(points: 5)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt: *"Each such difference is listed on the branch (in the package README), so that #419 updates the `flow-walker*` suites that pin bash's behaviour instead of rediscovering it."* — together with the gap it closes, *"`devscene-flow-host/README.md` → **Recording a gate.**"*

**Derivation entry — corpus files (command).** Re-run verbatim from the checkout root: `git grep -n -i -e 'no command line' -e 'holds no module' -e 'non-round findings' -e 'compatibility command' -- '*.md' ':!harness-runs/**' ':!examples/**'`

**Derivation entry — the package README's sections (procedure).** **Artifact:** `devscene-flow-host/README.md`. **Traversal:** its `##` headings in file order, and inside `## What it reads, answers and keeps` its bold paragraph leads in order. **Decision rule:** a section is reached when it states that the package has no command line, names what the `commands` or `host` layer holds, describes the non-round findings-file departure, or leaves an exit status to *"the caller"*; the section the predicate requires — the list of differences — is reached as the place it lands.

**Closure invariant:** every site either entry reaches appears as a row below.

| # | Site | Copy | Evidence (what the derivation matched) | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `devscene-flow-host/README.md` → `## What it is` ("it has no command line yet") | — | command entry, `no command line`; procedure entry | `change` | Task 7 |
| 2 | `devscene-flow-host/README.md` → `## The layers`, the `commands` and `host` rows | — | procedure entry, names what a layer holds | `change` | Task 7 — the `commands` row gains its three modules, the `host` row `RevisionFindingsStore` |
| 3 | `devscene-flow-host/README.md` → **Recording a gate.**, the bullet **The non-round findings file.** | — | command entry, `non-round findings`; procedure entry | `change` | Task 7 — replaced by the kept record Task 1 adds; the held-gate bullet stays (#472) |
| 4 | `devscene-flow-host/README.md` → `## Errors` ("Which exit status each of these becomes is the caller's; the package has no command line yet") | — | command entry, `no command line`; procedure entry | `change` | Task 7 |
| 5 | `devscene-flow-host/README.md` → the new `## The command line` and `## Differences from flow-walker.sh` sections | — | procedure entry, the place the predicate's list lands | `change` | Task 7 |
| 6 | `ROADMAP.md` → the `GraphScene` row ("with no command line yet") | — | command entry, `no command line` | `change` | Task 8 |
| 7 | `.claude/context/devscene-flow-host.md` → `## Not determined`, first bullet ("the `commands` layer, which holds no module yet") | — | command entry, `holds no module` | `no-change` | a conventions document is never a plannable target; Tasks 3–5 falsify it, recorded as a `stale-rule` entry in `corpus_staleness` |
| 8 | `.claude/context/conventions.md` → `## Not determined` (how `devscene-flow-host` reaches an adopter; "runs its compatibility command") | — | command entry, `compatibility command` | `no-change` | a conventions document; and the launch route it leaves open is #419's, which this branch does not settle |
| 9 | `docs/cli.md` → the `command-wrappers` paragraph ("holds no command line at all") | — | command entry, `no command line` | `no-change` | about `commands.typecheck` answered `<none>`, not this package |
