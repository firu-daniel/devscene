# The flow-graph walker — the planning pilot's decisions and measurements

**Who reads this:** a maintainer deciding whether a second orchestrated flow adopts the walker, or debugging a planning run's routing.

**What it owns.** The decisions of record for the pilot that moved the task-plan-writing loop's **routing** out of `plugin/instructions/task_plan_writing_instructions_core.md` and into a declared graph, `cli/templates/scripts/flows/task_plan_writing.graph.json`, walked by `cli/templates/scripts/flow-walker.sh`; the core's measured size before and after; and the walker's second driver, the watcher's opt-in planning driver (`cli/templates/scripts/lib/planning-driver-lib.sh` and its two sibling libraries), which walks the same graph with one headless session per node and no orchestrator — which driver runs when, how each runs a round, what a resume after an escalation park re-runs, and what of the second is not yet measured (`## 5. The two drivers`). It does not restate how to call the walker (its own header, and the core's `## The walker — routing is its, judgement is yours`), the graph's shape (the generic format-4 schema the graph is authored in, `graphscene/src/graphscene/schemas/flow-graph.schema.json`), the static checks (`graphscene.static_violations`, and `devscene-flow-host/tests/core_agreement.py` → `core_agreement_violations`) or the outer-loop file table (`docs/watcher.md` → `## 2. The scripts`).

---

## 1. The core's size, measured

Measured on the real file, never on a fixture. The baseline is commit `1fd5ce9`, the branch's merge base with `main` (`git merge-base main HEAD`); the core last changed on this branch in `1c38ba3` (`git log --format='%h %s' 1fd5ce9..HEAD -- plugin/instructions/task_plan_writing_instructions_core.md`).

| When | Command | Exact output |
|---|---|---|
| Before | `git cat-file -s 1fd5ce9:plugin/instructions/task_plan_writing_instructions_core.md` | `38036` |
| After | `wc -c plugin/instructions/task_plan_writing_instructions_core.md` | `   35066 plugin/instructions/task_plan_writing_instructions_core.md` |

The core is 2970 bytes smaller. That is the net of two movements, and the gross split matters more than the net. Bytes per heading, each line counted up to the next line that starts with `#`, from this command on the working file (for the baseline, pipe `git show 1fd5ce9:plugin/instructions/task_plan_writing_instructions_core.md` into the same `awk`):

```
LC_ALL=C awk '/^#/{h=$0} {if(!(h in b))k[++n]=h; b[h]+=length($0)+1} END{for(i=1;i<=n;i++)printf "%6d  %s\n",b[k[i]],k[i]}' plugin/instructions/task_plan_writing_instructions_core.md
```

| Heading | Before | After |
|---|---|---|
| `# Task-plan writing loop — core (mode-free)` | 688 | 688 |
| `## Resolved values` | 1724 | 1887 |
| `## Mode contract — bindings this file uses` | 2480 | 2686 |
| `## Setup (once per session)` | 5301 | 5657 |
| `## The walker — routing is its, judgement is yours` | — | 3411 |
| `## Safety contract — applies before EVERY Agent dispatch` | 3011 | 3308 |
| `## Loop` | 1260 | 437 |
| `` ### 1. Spawn `task-plan-writer` `` | 1384 | 1473 |
| `### 2. Business-parity review (plan-review mode)` | 3239 | 940 |
| `### 3. Architecture review (plan-review mode)` | 2805 | 797 |
| `` ### 4. Spawn `task-plan-reviewer` `` | 542 | 395 |
| `### 5. Parse the reviewer's return` | 736 | 511 |
| `## UI-test-plan write loop` | 950 | 348 |
| `` ### 1. Spawn `ui-tests-plan-writer` `` | 2645 | 2052 |
| `` ### 2. Spawn `ui-tests-plan-reviewer` `` | 1665 | 1368 |
| `### 3. Parse the reviewer's return` | 455 | 156 |
| `## Convergence` | 5364 | 5390 |
| `## Stop conditions` | 1432 | 967 |
| `## What you must NOT do` | 2355 | 2595 |

**Where prose left.** The routing sections: `## Loop` and its five steps, the UI-test-plan loop and its three steps, and `## Stop conditions`. What went is the gate order, the fall-through and loop-back sentences, the counter and its cap, both skip semantics and the per-folder `iteration:` derivation.

**Where prose stayed or grew.** Every non-routing rule stayed beside the node it governs: the dispatch blocks, path-only discipline, the `## Questions` verbatim rule, the writer's `## Parity exclusions / deferrals` return, the dispatch discipline, the disclosure lines, `## Convergence` and `## What you must NOT do`. The new `## The walker` section, `## Setup` step 7 and the `<scripts_dir>` row are new text the walker costs.

**What these figures do not count.** The orchestrator now also reads each walker call's printed output, once per call; that read is not in the figures above and was not measured on a real run. The graph is read by the walker through `jq`, never by the orchestrator: `wc -c cli/templates/scripts/flows/task_plan_writing.graph.json` prints `    7075 cli/templates/scripts/flows/task_plan_writing.graph.json`, and none of it enters the orchestrator's context.

---

## 2. The decisions

Each one restates an outcome the tasks that built it settled, with its reason and its cost.

### Item 2 — each node's dispatch block stays in the core

**Decision.** The agent name and argument lines of every dispatch stay in the core's `## Loop` and `## UI-test-plan write loop` steps. The walker supplies values, never lines: `arg.iteration` (on a round gate and on every `plan_writer` dispatch, the round number), `arg.review_mode` (`full` or `converging`, keyed on the loop counter), `arg.findings_file` and the prompt variant (`prompt: initial` or `revision`), per the core's `## The walker` → **`action: dispatch`**. A `plan_writer` revision receives every findings file of the round it follows, as one `arg.findings_file:` line per file in the round node's `gates` order — a **repeated key**, chosen over a list value on one line and over a sibling argument such as `arg.findings_files:`.

**Reason.** The block's key names are wire strings the six planning agents' `## Invocation contract` sections quote (`plugin/agents/task-plan-writer.md`, `task-plan-reviewer.md`, `business-parity-reviewer.md`, `architecture-reviewer.md`, `ui-tests-plan-writer.md`, `ui-tests-plan-reviewer.md`). Moving them into the graph would move a contract those agents cite into a file they cannot cite. The repeated key keeps that string byte-stable for every reader of the walker's output; a list value would need a separator, and a path may contain any separator a list could use; and a one-file revision — `ui_writer`'s — prints exactly the line it printed before.

**Cost.** Each gate's findings folder is written twice: in the graph's `findingsFolder` and in the core's `## Setup` step 2 table. That duplication is held by `devscene-flow-host/tests/core_agreement.py` → `core_agreement_violations` → `findings-folder-in-core`. The core joins the repeated values itself, in printed order with `, `, to fill the writer's `<findings_files>`.

### Item 3a — walker state is machine-local, and a re-entry continues it

**Decision.** The walker's state is the directory `<state_dir>/.flow_walker_state/`, ignored beside `.dispatch_counter` (`cli/src/generators/repoRoot.ts` lists both; this checkout's `.gitignore` carries both). Each branch's walk is its own file, `<state_dir>/.flow_walker_state/<percent-encoded branch>.json`, and the host's records for that branch sit in subdirectories under the same name — `round_refusals/`, `revision_findings/` and `printed_reads/` (`devscene-flow-host/README.md` → `## What it reads, answers and keeps` → **The walk.**, **Recording a gate.**, **Kept findings files.**, **Printed reads.**). A different branch is never refused: it has its own walk, and another branch's walk is never read. A planning (re-)entry issues `current` first and continues a pending walk (`plugin/instructions/task_plan_writing_instructions_core.md` → `## The walker — routing is its, judgement is yours` → **Continuing a saved walk.**). Only `start` overwrites the branch's walk and resets every counter to 0, and **proceed fresh**, **extend**, **review** and **skip** all issue it (`devscene-flow-host/README.md` → `## What it reads, answers and keeps` → **Resuming a round.**). The pilot reset the state on every re-entry; this reverses that.

**Changed 2026-11-25 (#419).** Until this branch the state was one flat file, `<state_dir>/.flow_walker_state`, holding whichever branch was walking, and a `next` or `current` naming another branch was refused with exit 1. A flat file the bash walker left is now deleted by `flow-walker.sh` before it hands `start`, `next` or `current` to the command (`flow-walker.sh` → `HAND-OFF` step 2), and its walk is not carried over: `current` answers "no saved walk" with exit 1, and the core's `current` → `start` recovery starts the walk fresh (task prompt, decided 2026-11-24). One state directory cannot hold the flat file and the per-branch directory at the same path, so the file goes (`devscene-flow-host/README.md` → `## Differences from flow-walker.sh` → **The walk's state.**).

**Reason.** The pilot's reset reproduced the pre-walker loop, which opened with *"`iteration = 0`. Loop:"* and held the counter only in context (`git show 1fd5ce9:plugin/instructions/task_plan_writing_instructions_core.md` → `## Loop`). With the step on disk, discarding it did harm. The autonomous fork's former case (b), *"Story index exists with a complete Phase 2 Readiness list"* (`git show 1fd5ce9:plugin/instructions/task_plan_writing_instructions_autonomous.md` → `## Override 2 — resumability`), skipped a draft no reviewer had passed, because a first draft already carries a complete readiness list. And `start` rewrote a finished UI-test plan with the `initial` prompt. So the counter now survives a pause, and the loop cap counts every revision of one walk, across every session it took.

**Which record wins.** The flow-progress ledger stays the only durable record, and it wins in both directions. A walk still in the task-plan loop is not used when `P1` is `[x]`. A walk past that loop is not used when `P1` is `[ ]`, unless its printed action carries `ledger: P1`; that flip is re-applied, idempotently through the commit wrapper's exit 3 (`task_plan_writing_instructions_autonomous.md` → `## Override 2 — resumability` → **Saved walk first.**, and `## Override 5 — pause/resume + flow-progress ledger (planning half)`). The fork checks a saved walk, never the walker: the walker reads no plan artifact, and reads nothing from the ledger but its run-mode block. A walk is unusable when the artifact its pending action works on is absent, which is what a draft deleted by hand leaves. A finished walk, `<escalate>` or `<terminal_handoff>`, is never acted on again; with `P3` `[ ]`, the ledger's own fallback reaches `--entry convergence`. A saved walk of another flow is refused by `current` with exit 1; another branch's walk is never read. A committed plan is no evidence of convergence: `P1` is.

**What `start` reads, and what it never carries.** The loop counter is carried only by a continued saved walk; every `start` sets it to 0, so an answered cap park — which **extend** answers through `start` — opens a fresh five-round budget while the round numbering carries on. The round number, and a mid-round position, come from the round files on disk (`flow-walker.sh` → `ROUNDS`; `devscene-flow-host/README.md` → `## What it reads, answers and keeps` → **Resuming a round.**, through `read_round_evidence`): `start` dispatches only the round's missing gates when every round file present holds exactly one verdict line and no plan file postdates the round's earliest file, recording the present gates' verdicts; otherwise it dispatches the round's whole set, and each gate replaces its file. It never infers convergence from files: a round whose files all read `PASS` is reviewed again.

**Evidence.** `cli/test/flow-walker-resume.test.mjs` pins continuation and resume: cases `(1) a set in flight is re-printed with only its unrecorded gates, and the counter and the round's recorded findings carry on`, `(2) a revision a FAIL round queued is re-printed with every file of the round`, `(3) a ledger line printed again flips nothing twice`, `(4) a UI reviewer in flight is re-dispatched, and the UI plan is not rewritten`, `(5) a parked <ask> resumes at the writer that parked, on its stored revision`, `(6) a finished walk is recognised as finished and replaced by the ledger fallback` and `(7) with no saved walk, a draft on disk — committed or not — is reviewed, never skipped or rewritten`, the three round-routing cases `(8) with the saved walk deleted and two of three round files committed, start dispatches only the third gate at counter 0`, `(9) inconsistent round evidence dispatches the whole set, and each gate replaces its file` and `(10) convergence is never read from round files: a complete round is reviewed or moved past`, and the two set cases `(11) a partial return: one gate's error escalates after the set, and a start dispatches only the missing gate` and `(12) a pause honoured at the join resumes at the writer revision on a FAIL round and at the UI-test writer on a PASS round`. The set itself is pinned by `cli/test/flow-walker-fan-out.test.mjs`, and its recording under simultaneous calls by `cli/test/flow-walker-concurrency.test.mjs`. What `start` still resets is the counter, as before, pinned by `cli/test/flow-walker-ui-and-reentry.test.mjs` → case `(6) re-entry mid-loop restarts the counter and continues the findings folder`: after `start` again, the heartbeat's counter is 0 while the writer's and the architecture gate's `arg.iteration` is 1, because the round numbering continues from the round files — round 0's are written — and is read off no counter. Case `(13) an answered cap park starts a fresh cap budget, and the round series carries on` pins the fresh budget: after a cap park at round 4, the restarted walk's counter runs from 0 while its rounds run from 5.

**Cost.** A `P2` flip lost between the walker's print and the fork's flip, on a finished walk, is re-earned with one UI-review round rather than trusted from the saved walk. The semi-autonomous fork does not continue saved walks, because it keeps no ledger to check them against (`task_plan_writing_instructions_semi_autonomous.md` → its `<existing_artifact_decision>` row). The core's `## Setup` step 7 mapping of **extend** to `ui_writer`, added for the pilot's skeptic Finding 2 (`harness-runs/skeptic_reviews/feat_orchestrator_flow_graph_planning_pilot_skeptic_review/finding_2.md`), stays as the fallback, for a park at a loop's cap and for a lost state file.

### Item 4 — STOP, the counter and PAUSE stay orchestrator steps

**Decision.** The STOP check, the `.dispatch_counter` increment and, in the autonomous fork, the PAUSE check stay in the core's `## Safety contract — applies before EVERY Agent dispatch`. The walker's heartbeat carries the literal slot `(#<total_dispatches>)` for the orchestrator to fill (`flow-walker.sh` → `THE SAFETY CONTRACT IS DELIBERATELY NOT THE WALKER'S`). For a set, STOP and the increment run once per block, while the PAUSE check runs once before the set, and a PAUSE placed while the set is out is honoured at the join (`plugin/instructions/task_plan_writing_instructions_autonomous.md` → `## Override 5 — pause/resume + flow-progress ledger (planning half)`).

**Reason.** The autonomous fork's PAUSE check sits **between** STOP and the increment (`task_plan_writing_instructions_autonomous.md` → `## Override 5 — pause/resume + flow-progress ledger (planning half)`, *"immediately after it"*), and it carries a judgement: pausing at the next clean tracked-tree boundary. Moving its two neighbours into the walker would either reorder STOP and PAUSE, which is a behaviour change, or need a new mode binding for PAUSE, which the task prompt's item 5 rules out by freezing the forks' binding tables. The halt messages also name `<reentry_command>`, a binding the walker must not resolve.

**Cost.** The "two separate, plain commands exactly as written" rule for the increment stays prose an agent follows, not code.

**On the script-driven path.** There the three are the driver's, per set, exactly as **A set.** words them: before anything of the set goes out, the STOP check runs per block, the PAUSE check once, and the cap against the whole set; the counter is then incremented and the heartbeat logged per block (`cli/templates/scripts/lib/planning-driver-lib.sh` → `pd_run_set`). The halt messages are the core's, with `<reentry_command>` resolved to the autonomous fork's value, `/devscene:branch-start-plan-autonomous` (`planning-driver-lib.sh` → `PD_REENTRY_COMMAND`; `task_plan_writing_instructions_autonomous.md` → its `<reentry_command>` row).

### Item 6 — the walker and graph ship into `scriptsDir`, and the graph is found beside the walker

**Decision.** `flow-walker.sh` and `flows/task_plan_writing.v4.graph.json` ship from `cli/templates/scripts/` into the adopter's `scriptsDir`, with the flow host's packages under `<scriptsDir>/python/` (`cli/src/flowHost/layout.ts`). The walker's row in `cli/src/generators/outerLoopScripts.ts` → `OUTER_LOOP_SCRIPTS` is `agentInvocable: true`, so the autonomous profile grants it. The graph is found **beside the walker** by flow id: the hand-off passes its own `flows/` directory as `--flows` on `start`, `next` and `current`, and the command reads `<flows>/<flow>.v4.graph.json` (`flow-walker.sh` → `HAND-OFF` step 4); the caller passes no path. The format-3 graph `flows/task_plan_writing.graph.json` still ships, because `lib/planning-node-lib.sh` and `lib/planning-driver-lib.sh` read its node list; no walker reads it, and its retirement is #459's (`OUTER_LOOP_SCRIPTS` → that row's comment; `ROADMAP.md` → the GraphScene row, *"the format-3 readers moving to format 4"*).

**Changed 2026-11-25 (#419).** `lib/flow-walker-gates.sh` no longer ships: its checks are the flow host's (`### Item 9`). Until this branch the bash walker read the format-3 graph beside itself, at `<this script's dir>/flows/<flow>.graph.json`, and `init` never wrote the format-4 source.

**Changed 2026-11-25 (#459).** The format-4 graph now ships as `flows/task_plan_writing.graph.json`, the one graph under `flows/`, which `lib/planning-node-lib.sh` and `lib/planning-driver-lib.sh` read for its node list as well. The command reads `<flows>/<flow>.graph.json` (`devscene-flow-host/src/devscene_flow_host/commands/flow_walker.py` → `GRAPH_SUFFIX`).

**Reason.** Every invocation stays one plain literal command, which the permission profile can grant and the script-allowlist guard does not withhold. And the orchestrator never has to resolve the plugin root, which `docs/development.md` → `## 2. The one authoring rule that follows` records a real orchestrator doing by hand, with `find`, after its own `${CLAUDE_PLUGIN_ROOT}` citations were refused.

**Cost.** An adopter's copies are written `create-if-absent` (`outerLoopScripts.ts` → the re-run contract), so they lag a plugin upgrade until `init --upgrade`, run from the latest CLI after the plugin update, replaces them (`docs/cli.md` → `### Updating an adopted repository`). A missing walker is a loud non-zero exit, which the core's `## The walker` routes to `<escalate>` with `bash`'s own line. A `lib/harness-run-lib.sh` kept from an `init` that predates the walker is kept by that same `create-if-absent` contract. The walker refuses it at `start` with a line naming the file and the remedy: delete it and re-run `init`. The step that closes the lag:

```bash
npx devscene@latest init --upgrade
```

### Item 7 — every gate every round, closed by a round node

**Decision.** The task-plan loop's three gates — `business_parity_review`, `architecture_review`, `plan_review` — route `PASS` and `FAIL` alike forward to the next gate, so every gate runs every round. A new node, `plan_round`, of the new kind `round`, closes the round: it dispatches nothing, routes `FAIL` when any of its `gates` recorded `FAIL` this round and `PASS` otherwise, prints `round: <n> <PASS|FAIL>`, and on `FAIL` hands every file of the round to the writer's revision. The graph's `formatVersion` is 2 (`schemas/flow-graph.schema.json` → `formatVersion`, `kind`). `scripts/check-flow-graph.sh` → `THE CONTRACT` item 8, `gate-in-round`, holds every failing gate inside exactly one round node, and item 3, `fail-cycle-capped`, treats a round node's computed `FAIL` edge as an outcome edge.

**Reason.** Format 1 had no node that routes without an agent outcome, and no state that remembers verdicts within a round; a gate's `FAIL` could only route straight back to the writer. The walker reads a round node's `gates` from the graph rather than naming them in code, so a gate added to or dropped from a round is an edge change in the graph. The fan-out itself turned out to need a format change and walker changes as well — `### Item 8 — a round's gates fan out, and the round node joins`.

**Cost.** A format bump: every fixture graph under `schemas/flow-graph-check/` and `schemas/negative/` moved to format 2, and the walker reads format 2 only — any other `formatVersion` is refused with exit 1. An adopter's walker and graph are therefore replaced together by re-running `init` — with `--force`, since the `create-if-absent` contract `### Item 6` already records keeps an existing copy (`cli/src/generators/outerLoopScripts.ts` → `writeOuterLoopScripts`); a new walker beside an old graph refuses it rather than misrouting.

### Item 8 — a round's gates fan out, and the round node joins

**Decision.** The graph is format 3, and a round node carries `"parallel": true` (`schemas/flow-graph.schema.json` → the round node's `parallel`). Each gate's `PASS`, `FAIL` and skip edges, and the writer's `returned` edge, route into the round node, and `entries` names `plan_round` (`scripts/check-flow-graph.sh` → `THE CONTRACT` item 9, `round-fan-out`; items 1 and 2 walk the fan-out edge from a round node to each of its gates). Arriving at the round node opens it and prints every due gate at once, as a set of dispatch blocks; a set of one gate is a single dispatch block, byte-identical to a single dispatch. Each gate's outcome is recorded by its own `next --node <gate>`, which refuses three things while a set is pending: no `--node`, a `--node` that is not a pending gate of the round, and a second outcome for one gate. Every outcome but the last prints `action: wait`; the last is the join, which prints the first held gate's binding when any gate returned `error` or `blocker`, and otherwise closes the round. `start` and `next` take two `flock`s, in this order: `RefusalStore`'s, `<state_dir>/.flow_walker_state/round_refusals/<percent-encoded branch>.json.lock`, then the walk's own, `<state_dir>/.flow_walker_state/<percent-encoded branch>.json.lock`, never the first inside the second; so exactly one of several simultaneous calls prints the round's result. Each lock dies with the process that took it, so none is left behind to break (`devscene-flow-host/README.md` → `## What it reads, answers and keeps` → **Recording a gate.**; `## Differences from flow-walker.sh` → **The locks.**). `start` at a round reads the round files: when every present file holds one verdict line and no plan file postdates the round's earliest file, it records those gates and dispatches only the missing ones; otherwise it dispatches the whole set. `current` re-prints a pending set keyed on recorded outcomes: only the gates with none. The mechanics are `flow-walker.sh` → `ROUNDS`, `A REFUSED ROUND FILE`, `OUTPUT` and `EXIT CODES`, with the state, locks and records `devscene-flow-host/README.md` → `## What it reads, answers and keeps`; the one-message dispatch form with its per-block safety contract is the core's `## Safety contract — applies before EVERY Agent dispatch` → **A set.**

**Changed 2026-11-25 (#419).** The bash walker held one `mkdir` lock, `<state_dir>/.flow_walker_state.lock`, broke one older than a minute and gave up after 120 s with an `rmdir` remedy; its mechanics were the header's `STATE` and `CONCURRENCY` paragraphs, which this branch removed with the bash walker's body.

**Reason.** No gate reads another's file of the same round (`plugin/instructions/plan_review_rounds.md` → `## The round file`, `## Converging mode` item 4), so the serial order cost only wall time. `--node` lets the walker refuse a gate by name, and lets a per-gate session record its own outcome without knowing the others'. `current` is keyed on recorded outcomes — a deliberate departure from the task prompt's wording, which had `start` and `current` print only the gates without a valid round file — because `current` is read-only: a gate it skipped by its file would never have its outcome recorded, and the round could never close. The two rules differ in one case only, a gate whose reviewer wrote its file but whose `next` never ran: `current` dispatches it again, while `start`, which reads the files, records it.

**Cost.** A format bump: an adopter's walker and graph are replaced together by `init --force`, as `### Item 7` records for format 2. A gate whose reviewer wrote its file but whose `next` never ran is dispatched again by `current`, at the cost of one review. The dispatch form is stated ahead of probe BG11 (`docs/sandbox-verification.md` → `## 5. Failures and their follow-ups`, row BG11): if the calls do not overlap, a round runs serially with the same result.

**What a second driver must do.** The input for #159 (`ROADMAP.md` → `Script-driven planning pilot`), a script that runs each node as its own headless session. Read a set as the blocks between `action:` lines. Run its own STOP check, counter increment and heartbeat per block, and its PAUSE check once per set. Start one session per block. Record each session's outcome with `next --node <node>` as that session ends, in any order and concurrently. Treat `action: wait` as nothing to do. Act on the one call that prints the round's result or the held binding. A `refused:` line needs no action of its own: the refused gates arrive as an ordinary dispatch set. Recover a lost session with `current`, which prints only the unrecorded gates. Nothing in this needs the orchestrator's prose: every value it acts on is in the walker's output, and `cli/test/flow-walker-fan-out.test.mjs` drives a round this way, through the walker's CLI alone. That driver is built, and `## 5. The two drivers` records it.

### Item 9 — a round file is checked before its verdict is recorded

**Decision.** A round gate's `PASS` or `FAIL` is recorded only when `round_file_problem` (`devscene-flow-host/src/devscene_flow_host/records/round_files.py`) accepts the file `--findings` names; it reads as the retired `fw_round_file_check` did (`devscene-flow-host/README.md` → `## What it reads, answers and keeps` → **Round and reviewer files.**). The file must carry exactly one verdict line. A `verdict: FAIL` needs at least one numbered entry at column 0 under `## Must Fix` and a `verdict: PASS` needs none, and every entry needs a non-empty `**Class:**` and `**Failure:**`. A refused file records no verdict: the walker prints a `refused:` line, waits for the gates still out, and at the join dispatches every refused gate again as one set, in the same round, with the round number and the loop counter unchanged. Each reviewer replaces its own file, and a refusal never reaches the writer. `ROUND_FILE_ATTEMPTS` (`devscene-flow-host/src/devscene_flow_host/host/refusals.py`) is 3: a gate's third refusal in a round is held as `error`, which the join escalates like any held outcome (`flow-walker.sh` → `A REFUSED ROUND FILE`). On resume, `read_round_evidence` reads a present file the check refuses as `unreadable`, so `start` at the round node opens that round's whole set. The prose-routed user-review fix-plan rounds run the same check through `flow-walker.sh check-round-file --findings <path>`, whose exit 3 alone means the file is invalid.

**Reason.** No agent meta-reviews a plan round, so without a scripted check a Must Fix missing its fields would reach the writer unchallenged. The check proves presence only: it does not compare the class name with the list `finding_grades.md` owns, and it cannot tell whether the failure sentence is true. The defect is in the reviewer's file, so the reviewer is the one sent back, and leaving both numbers alone means a malformed file spends no revision of the five-round cap.

**Cost.** Each re-dispatch draws on `MAX_TOTAL_DISPATCHES`, up to two per gate per round. `## Setup (once per session)` step 4 sizes `MAX_TOTAL_DISPATCHES = 40` with a margin of 10 that these share with writer clarification re-dispatches, so a run of repeated refusals can halt there before any loop cap. `ui_review` and the test-fix plan's architecture review are not round gates, so they are not checked and their entries carry the fields by contract alone. An adopter must update the walker scripts together with the plugin, by `init --force` under the `create-if-absent` contract `### Item 6` records: a new walker beside reviewers that omit the fields refuses every `FAIL` file, and each such gate escalates on its third attempt. In the other direction, a walker too old to have `check-round-file` exits 1, which the user-review fix-plan rounds take as a held binding with no reviewer re-dispatch. A round file written before the fields existed reads `unreadable` on resume, at the cost of re-running that round's gates.

### The iteration cap — the graph owns it, the core keeps two descriptions held by a check

**Decision.** `counters.iteration.cap` in `cli/templates/scripts/flows/task_plan_writing.graph.json` owns the cap, and the cap counts **rounds**: the counter advances once per `FAIL` round, on `plan_round`'s `FAIL` edge. The core keeps two descriptions of it: `## Setup (once per session)` step 4's sizing sentence (*"`iteration >= 5` caps"* … *"caps at 5 revisions"*, from which `MAX_TOTAL_DISPATCHES = 40` is sized), now restated to read that `## Loop` dispatches **exactly** four agents per round because every gate runs every round, and `## Safety contract` step 2's halt message (*"5-revision caps"*). The three checked phrases are unchanged. The cap escalation's `rounds: <node> <n>` lines count each gate folder's `verdict: FAIL` files, not its files, because a `PASS` now writes one too; `{open_gates}` in its summary names the gates that failed the closing round.

**Reason.** Step 4 is cited from `plugin/instructions/user_review_fix_plan_writing_instructions_autonomous.md`, and the task prompt freezes the halt messages (`harness-runs/task_plans/feat_orchestrator_flow_graph_planning_pilot/task_9_plan.md`, the bullet keeping step 4's sizing sentence as a retained **description**).

**Cost, and how it is guarded.** That is a duplication, so it is checked rather than accepted: `scripts/check-flow-graph.sh` → `THE CONTRACT` item 7, `cap-matches-core`, fails when the graph's cap and any of the three phrases disagree, or when a phrase no longer yields a number. Changing the cap is still a three-place edit: the `counters.iteration.cap` of the format-4 source `cli/templates/scripts/flows/task_plan_writing.v4.graph.json`, regenerated into both format-3 copies with `node scripts/generate-flow-graph-v3.mjs --write`, and both core sentences. It also needs a re-sizing of `MAX_TOTAL_DISPATCHES`, which no check derives.

**Changed 2026-11-25 (#459).** `cap-matches-core` is now a check of `devscene-flow-host/tests/core_agreement.py` → `core_agreement_violations`, run in gate 13's leg `13j`. Changing the cap is a two-place edit with no regeneration step: the `counters.iteration.cap` of `cli/templates/scripts/flows/task_plan_writing.graph.json`, and both core sentences.

### Format 4 — the graph declares its vocabulary, and format 3 is generated from it

**Decision.** The planning graph is authored in format 4 (`"formatVersion": 4`), in `cli/templates/scripts/flows/task_plan_writing.v4.graph.json`, against the generic schema `graphscene/src/graphscene/schemas/flow-graph.schema.json`, which lives in `graphscene/` and travels with the library. A format-4 graph declares its own outcomes, bindings and skip predicates, and each declared name maps to an engine primitive: an outcome may carry `verdict` or `held`; a binding is an `interrupt`, a `stop` or an `end`; a skip predicate states what its node `records` and whether it is `inRoundCounts`. Node kinds stay the engine's and are not declared. `graphscene.engine.vocabulary.vocabulary_violations` (`graphscene/src/graphscene/engine/vocabulary.py`) is the generic check that every name a format-4 graph uses is one it declares. For this graph, `scripts/generate-flow-graph-v3.mjs` makes the same refusal before it generates the format-3 copies. `init` does not write the format-4 source. Both format-3 copies — `cli/templates/scripts/flows/task_plan_writing.graph.json` and the self-adoption copy `scripts/flows/task_plan_writing.graph.json` — are generated from it by `scripts/generate-flow-graph-v3.mjs` (its header block `THE RULE`), and gate 3's leg `3i` fails when either differs from what it generates (`docs/development.md` → `## 5. Verifying a change`, **Gate 3**). The walker, `scripts/check-flow-graph.sh`, `cli/test/agent-return-schemas.test.mjs` and the `validate:flow-graph*` scripts stay on format 3.

**Reason.** A generic engine cannot ship a closed list of one host's names, so the graph declares them. Declaring the names alone would only move the coupling the walker's fixed behaviour has, from the engine's code to an unstated agreement about what each name does; mapping each name to a primitive states that behaviour in the graph itself.

**Cost.** The planning graph exists twice until the cutover — the walker and the format-3 readers moving to format 4, and the generated copy and its generator retired — which `ROADMAP.md` → the GraphScene row (`## Scene products`) owns. The generator holds the mapping from format-4 names back to the format-3 names the walker knows, and that mapping is harness knowledge kept out of `graphscene/` (`scripts/generate-flow-graph-v3.mjs` → `WHY THE MAPPING LIVES HERE`). The format-4 source sits inside the npm tarball, because `cli/package.json` → `files` carries `templates`, but `init` never writes it.

**Changed 2026-11-25 (#419).** The walker moved to format 4 and `init` now writes the format-4 source into `scriptsDir` (`### Item 6`). The generated format-3 copies, their generator and the other format-3 readers stay, until #459.

**Changed 2026-11-25 (#459).** The generated format-3 copies, their generator, the format-3 schema and its fixtures, `scripts/check-flow-graph.sh` and gate 3's legs `3c`–`3f` and `3i` are retired. The format-4 graph ships under the shipped name, `cli/templates/scripts/flows/task_plan_writing.graph.json` (`### Item 6`). Checks 4–7 moved to the flow host's test checker, `devscene-flow-host/tests/core_agreement.py` → `core_agreement_violations`, while checks 1–3, 8 and 9 run as `graphscene.static_violations`. `init` removes no file it stopped shipping.

### The runtime — bash 3.2 and `jq` 1.5

**Decision.** The walker and its gate library are bash with a 3.2 floor and `jq` 1.5 (`flow-walker.sh` → `BASH 3.2 AND JQ 1.5 ARE THE FLOORS`).

**Reason.** That is what an adopter's unattended run already has: `doctor`'s `jq` check fails a `jq` older than 1.5 (`cli/src/doctor/checks.ts` → `JQ_CHECK`), and the shared library every outer-loop script sources already holds the same bash floor (`cli/templates/scripts/lib/harness-run-lib.sh` → `BASH 3.2 IS THE FLOOR`). So the walker needs no new `doctor` check.

**Superseded 2026-11-25 (#419).** The walker is Python — `devscene-flow-host`'s `devscene-flow-walker`, run through `uv` from `<scriptsDir>/python/` (`### Item 6`) — and the bash and `jq` floors above no longer bound it. The hand-off, `flow-walker.sh`, stays bash-3.2-safe and needs `jq` only through `lib/harness-run-lib.sh`'s `stateDir` read, `hr_state_dir`, which it runs to find a leftover flat state file (`flow-walker.sh` → `HAND-OFF` steps 1 and 2). A host without `uv` is refused by the hand-off with exit 2 (`HAND-OFF` step 3), failed by `doctor`'s `uv` check (`cli/src/doctor/checks.ts` → `UV_CHECK`), and fails a run copy's bootstrap at `setup-worktree.sh` step 6. A run's planning driver runs the main checkout's walker, not the run copy's, because the driver runs outside the sandbox and anything that does must not be writable from inside it (`cli/templates/scripts/lib/planning-driver-lib.sh` → `THE WALKER IS THE MAIN CHECKOUT'S`).

### Per-call startup cost

**What is measured.** The wall-clock time of one walker call whose work is negligible: `check-round-file` on a path that does not exist, which exits 3 on the absent file. The figure is therefore the hand-off, `uv run` and Python's start-up. No threshold is set: the cutover was decided whatever the figure (task prompt).

**The commands.** From this repository's root, after the self-adopted `scripts/` have been re-rendered so `scripts/flow-walker.sh` is the hand-off, run this ten times, reading the `real` line each prints (the walker's own exit 3 and `flow-walker:` line are expected):

```
time bash scripts/flow-walker.sh check-round-file --findings harness-runs/no-such-review.md
```

Then record the `uv` version:

```
uv --version
```

**How to read it.** Record the median of the ten `real` figures, the `uv` version, the host and the date.

**The figure.** A median of **0.126 s** over ten calls, with every call between 0.126 s and 0.127 s. Taken on 2026-11-25 with `uv` 0.12.23 (Homebrew) on an Apple M4 running macOS 15.7.4. The run was by hand from an interactive session, with no autonomous run active and a load average of about 1.8. It was taken after #481 re-rendered this repository's `scripts/`, so `scripts/flow-walker.sh` was the hand-off, and the main checkout's `scripts/python/.venv` had just been provisioned. The `uv` cache was warm.

---

## 3. Four findings established rather than assumed

- **The supervised `/devscene:branch-start-plan` does not reach the core.** `plugin/commands/branch-start-plan.md` names no instruction file (`grep -n "instructions/" plugin/commands/branch-start-plan.md` prints nothing), so it was left untouched.
- **No planning agent quotes the core's routing as its own rule.** Each of the six cites a heading the rewrite preserved (`harness-runs/story_plans/feat_orchestrator_flow_graph_planning_pilot_story_plan.md` → `## Scope register`, rows 12–17), and every wire string they return — `verdict: PASS`, `no_ui: true`, `## Questions` and the rest — is unchanged.
- **The run-mode precedence at the parity gate is the core's textual order: run mode before config.** The pre-change `### 2. Business-parity review (plan-review mode)` opens on *"Before anything else in this step, re-read the run mode"* and only then states *"Skip this gate unless `phases.parity` is `true`"*. `cli/test/flow-walker.test.mjs` → case `(6) with both parity switches off, passed-by-exclusion wins` pins it.
- **The graph format and `scripts/check-flow-graph.sh` needed no change for the two new entries.** `business_parity_review` and `ui_review` are nodes `start` already reaches, so `reachable-from-start` and `reaches-terminal` hold, and no check reads `entries`. An entry that is not a node makes the walker fault at `start` with exit 2, which the core routes to `<escalate>`. `formatVersion` stays `1`, because the key set did not change; only the schema's `entries` description is restated, since a continued walk resumes without naming an entry. That held for the pilot; the round routing did change the format, to 2, recorded at `### Item 7 — every gate every round, closed by a round node`, and the round's fan-out changed it again, to 3, recorded at `### Item 8 — a round's gates fan out, and the round node joins`.

---

## 4. What a second flow would need before it adopts the walker

A proposal to the maintainer, not scheduled work. Every other orchestrated loop was out of the pilot's scope, and none is a candidate until the pilot is judged (`harness-runs/task_prompts/feat_orchestrator_flow_graph_planning_pilot_task_prompt.md` → `## Out of scope`). A flow that adopts the walker would need:

- **its own graph**, and a flow-id row in `devscene-flow-host/tests/core_agreement.py` → `CORE_FOR_FLOW`;
- **any outcome or construct the format lacks today** — for example the per-unit loop's iteration over a readiness list;
- **its own ledger template's ids for `ledger-id-known`**, which reads only the task-engine template today;
- **its own safety-contract decision**, since item 4's reasoning rests on this flow's STOP / PAUSE / increment order;
- **scenario tests derived from its pre-change prose**, as `cli/test/flow-walker.test.mjs` and `cli/test/flow-walker-ui-and-reentry.test.mjs` were, never from the graph.

---

## 5. The two drivers

The walker has two drivers: the orchestrating session, which reads the core, and the watcher's planning driver, which is the second driver `### Item 8` → **What a second driver must do.** describes. Each subsection below is a decision, its reason and its cost, as in §2. The watcher's side — the switch, the launch sequence and the exit mapping — is `docs/watcher.md` → `### Script-driven planning (opt-in pilot)`.

### Which runs when

**Decision.** The orchestrator is the default, and the driver in every mode: supervised, semi-autonomous, a local autonomous run and a remote job. The script driver runs only when the configuration key `execution.scriptDrivenPlanning` is `true`, in a watcher run of the task engine — local or a remote job — whose planning is not finished — the run's ledger is absent or its first phase is pending — with the three libraries readable, the plugin's runtime root resolved from the agent runner's records, and that root's manifest and planning core readable (`cli/templates/scripts/autonomous-watcher.sh` → `planning_driver_ready`; the header's `SCRIPT-DRIVEN PLANNING IS AN OPT-IN PILOT.`). The pinned plugin directory is that runtime root, re-derived at every launch and never configured (`lib/harness-run-lib.sh` → `hr_plugin_runtime_root_var`, the shell mirror of `cli/src/machine/plugins.ts` → `pluginRuntimeRoot`).

**Reason.** The driver's savings are not yet measured (`### What the follow-up measures`, below), so an adopter who does not opt in gains no new surface: the key is `false` by default. It is a committed key rather than a watcher tunable because a remote run pays the orchestrator's cache-read tokens as a local one does, and a job reads its branch's `devscene.config.json` but no `watcher.env`. It is a boolean rather than a path because a committed path cannot be right both on the operator's machine and on a runner, so the directory is derived where the run executes: the installed copy locally, the copy `Install the pinned plugin` installs in a job.

**Cost.** A launch that is not ready logs one `planning driver off for '<branch>': <reason>` line and takes the orchestrated path, so a key that is not a boolean, or a runtime root that does not resolve, costs the pilot's data, not the run.

### How each runs a parallel round

**Decision.** The orchestrator runs a printed set as one message of foreground `Agent` calls (`plugin/instructions/task_plan_writing_instructions_core.md` → `## Safety contract — applies before EVERY Agent dispatch` → **A set.**). The driver runs one headless session per block, all launched at once once the set's safety contract has passed (`### Item 4` → **On the script-driven path.**), and records each with `flow-walker.sh next --node <node>` as its session ends, in finish order (`planning-driver-lib.sh` → `pd_run_set`, `pd_reap_one`). An `action: wait` is nothing to do. A held `error` or `blocker` comes back as one binding after the last outcome, printed by the walker's join. A sibling is never cancelled: an `error`, a `blocker` or a stall kill ends that one session. The driver splits `error` by class, which `pnl_reap` prints as `class=infra` or `class=agent` on every `kind=error` so the driver never parses a reason (`planning-node-lib.sh` → `pnl_reap`, `PNL_REAP_JQ`). **An infrastructure failure** — a session the driver killed as stalled, a missing `init` event, a session that ended not `success` or with `is_error`, a return that carries no return block or fails its agent's schema file, `schemas/<agent>.return.json`, a `FAIL` or a round gate's `PASS` whose `findings_file` is blank — is held unrecorded, and after `PD_BACKOFF_SECS` its node alone is dispatched again from the blocks `flow-walker.sh current` re-prints, its siblings keeping their recorded outcomes; only attempt `PD_MAX_ATTEMPTS` (3) is recorded as `error`, and a node's count restarts at 1 once it records an outcome. **Every other `error`** — an `init` event carrying a tool the agent does not declare, or a schema-valid outcome the node does not declare — is recorded at once, as is an agent's `blocker` outcome (`planning-driver-lib.sh` → `pd_reap_one`, `pd_run_set`'s `retry` result).

**Reason.** That is the contract `### Item 8` → **What a second driver must do.** wrote, followed as written, so the walker needed no change for a second driver: the join, the held binding and the refusal of a second outcome are the walker's (`flow-walker.sh` → `ROUNDS`; `devscene-flow-host/README.md` → `## What it reads, answers and keeps` → **Recording a gate.**).

**Cost.** The driver polls the set once a second with `kill -0`, because bash 3.2 has no `wait -n` (`planning-driver-lib.sh` → `BASH 3.2 AND JQ 1.5 ARE THE FLOORS`). A session that delivered nothing — no `result` event, or an API overload error — is not recorded but dispatched again, and a third consecutive undelivered set pauses planning, resumed by hand (`pd_undelivered`); that re-dispatch consumes no infrastructure attempt, and in a set holding both, the undelivered path takes the set and the held node goes out with its re-dispatch. An infrastructure retry is a dispatch like any other: it passes the set's safety contract again and counts against `MAX_TOTAL_DISPATCHES`, but neither against the undelivered strikes nor as a recovery through `current`. While attempts remain it raises no park, pause or notification — one `[plan-drive]` line and one observation per retry. When they run out the run parks once, after the siblings have finished, and the question's detail for that node carries `- agent:` and an `- attempts:` list of how each attempt ended (`pd_session_detail`). The observations file's session table is `seq node agent attempt result duration cost`, one row per launched session, retries included, `attempt` written `k/3`.

### A resume after an escalation park

**Decision.** A gate that passed in the round that escalated is re-dispatched on resume only where a writer revision has run since its verdict, or where the walker cannot tell its verdict apart from the files. At an `<escalate>` carrying `held:` lines, the driver commits the round's planning artifacts as `chore: Plan round <n> partial for <branch>` before it parks, the commit the PAUSE and undelivered self-pause paths already make, so the resume's `flow-walker.sh start` reads the round's evidence as committed (`planning-driver-lib.sh` → `pd_escalate_park`, `pd_partial`). `flow-walker.sh` is unchanged. Each path below is one case in `cli/test/planning-driver-control.test.mjs` (`escalation resume (a)`, `(b)`, `(c)` and `(d)`), driven to the park with an agent-reported `blocker` on `architecture-reviewer` in round 0, so no infrastructure retry intervenes, then driven again:

- **(a) The park answered.** Entry `plan_writer` with the answered pair: the writer runs, then all three gates at round 1. The passed gates re-run, after a writer revision.
- **(b) No answered pair, and the escalated gate left no findings file.** Entry `plan_round`: only `architecture-reviewer` runs, at round 0. The passed gates are not re-dispatched.
- **(c) No answered pair, and the escalated gate left a PASS findings file before it ended.** Entry `plan_round`: the round is complete and all-PASS, so all three gates re-run at round 0 with no writer revision.
- **(d) The park answered, and the escalated gate left a PASS findings file.** Behaves as (a): entry `plan_writer` with the answered pair, the writer runs, then all three gates at round 1.

**Reason.** The rule is that a passed gate does not run again unless the plan changed since its verdict. A held round prints no `round:` line, so nothing had committed its files at the park; the resume's `start --entry plan_round` then read `plan: unknown`, and path (b) re-dispatched all three gates in round 0. The walker could not tell only because the evidence was uncommitted, so the fix is the driver's commit rather than a different entry. On path (c) the walker cannot tell: a PASS file written by a session that then failed reads the same as a clean PASS, and convergence is never inferred from files (`devscene-flow-host/README.md` → `## What it reads, answers and keeps` → **Resuming a round.**, *"a complete round that is unreadable or has no `FAIL` is reviewed again"*). That is why the passed gates re-run there.

**Cost.** The commit is the driver's, not the autonomous fork's. `plugin/instructions/task_plan_writing_instructions_autonomous.md` makes a `Plan round <n> partial` commit only for `## Override 5 — pause/resume + flow-progress ledger (planning half)`'s PAUSE and the API-overload self-pause, and `## Override 6 — commit each plan-review round` commits a round only on a `round:` line; the library's module header records the divergence. The orchestrated path makes no such commit, so its held round stays uncommitted and, by the same `plan: unknown` reading, its resume re-runs every gate. That is inferred from the walker's rule, not driven. A UI-loop escalation resuming at `ui_writer` is not covered: the suite's fixture runs `phases.qa` `false` and hands off without entering the UI loop.

### Why the driver is three watcher-sourced libraries

**Decision.** The driver is `lib/planning-node-lib.sh` (one node session), `lib/planning-record-lib.sh` (every durable write) and `lib/planning-driver-lib.sh` (the walk), each sourced by the watcher inside the run's launch subshell (`autonomous-watcher.sh` → `planning_driver_run`), never executed, shipped without an executable bit and with `agentInvocable: false` (`cli/src/generators/outerLoopScripts.ts` → `OUTER_LOOP_SCRIPTS`). It is not a script of its own.

**Reason.** Three properties follow from running inside the watcher. **One producer of the launch vector:** every node session is launched through the watcher's `session_exec`, the same function the engine session goes through, so a node gets the run's per-run settings, permission mode, model, effort, added directories, environment scrub and main-checkout anchor, with only the per-node flags appended (`autonomous-watcher.sh` → `session_exec`; `planning-node-lib.sh` → `pnl_agent_flags`). **No new agent reach:** nothing an agent can invoke starts the driver — a library run rather than sourced only defines functions, and none carries a profile entry (`docs/watcher.md` → `## 2. The scripts`). **The full environment for the wrappers:** the driver's `commit-on-branch.sh` and `push-branch.sh` calls run in the launch subshell, which keeps the watcher's environment; only a session's own launch pipe head is scrubbed (`docs/watcher.md` → `### The session's environment`).

**Cost.** The driver cannot be run on its own; a reproduction by hand sources the libraries into a shell against a throwaway fixture (each library's `REPRO` block). A checkout `init` wrote before the libraries shipped lacks them until `init --force` rewrites the family, and until then every launch with the key on logs the driver off.

### Why the prompts come from the pinned plugin's core

**Decision.** At every drive, `pnl_init` reads `<root>/instructions/task_plan_writing_instructions_core.md`, where `<root>` is the plugin's runtime root (`### Which runs when`, above), takes each node's prompt from the fenced blocks under the headings `PNL_CORE_BLOCKS` names and the dispatch cap from `## Setup (once per session)` step 4's `MAX_TOTAL_DISPATCHES` line, and fills them with the walker's values, appending nothing but a resumed writer's answered pairs (`planning-node-lib.sh` → `THE CORE IS WIRE TEXT.`, `pnl_prompt`).

**Reason.** The core stays the one owner of every dispatch block, as `### Item 2` decided for the orchestrator: a copy in the script would be a second owner that drifts. The core's opening note names those headings, their fence counts and that line as wire text the library keys on.

**Cost.** Renaming one of those headings, or changing a fence count under one, faults the driver at `pnl_init` with exit 2, and the run ends `failed`. `cli/test/planning-node-lib.test.mjs` builds its fixture plugin's core from this repository's, so a change of that kind fails the suite.

### The return schema, the graph's outcomes, and the `init` check

**Decision.** A node session is launched with no `--json-schema`; its outcome is read from the return block that ends its `result` text, validated against its agent's schema file, which `pnl_init` loads from the pinned plugin's `schemas/<agent>.return.json` for every dispatch node (`planning-node-lib.sh` → `pnl_load_schemas`). The mechanism — the block, the schema, and why the flag was dropped — is `docs/structured-agent-returns.md`'s. `pnl_reap` decides a node's result from its stream alone, in one fixed order (`PNL_REAP_JQ`): no `system`/`init` event is an infrastructure `error`, retried (`### How each runs a parallel round`, above), and an `init` whose tools carry one the agent file's `tools:` line does not name is an agent `error`, recorded at once; then a missing `result` event or an overload is undelivered; then a session that ended not `success` or with `is_error` is an infrastructure `error`; then a `result` text with no return block, a block that is not one JSON object, or an object that fails the schema is an infrastructure `error`; then a schema-valid outcome the graph does not declare for the node is an agent `error`; then a `FAIL`, or a round gate's `PASS`, whose `findings_file` is blank is an infrastructure `error`. The validated object is the only source of a field the driver reads afterwards (`planning-driver-lib.sh` → `pd_ret_field`, `pd_ask_park`). A declared tool the `init` lacks is not refused: `pnl_reap` prints it on `withheld=`, and the driver logs one `[plan-drive] #<seq> <node> (<agent>): the init event lacks declared tools [<tools>] (a lacking tool is never refused)` line for the session (`planning-driver-lib.sh` → `pd_reap_one`).

**Reason.** The graph stays the one owner of a node's outcomes, and a session cannot route the walk with an outcome its node does not have; the schema is checked first because its `outcome` values are the graph's outcome keys less `error`, so the graph rule refuses only a schema that has drifted from the graph. A malformed return is infrastructure because a re-dispatch of the same prompt is its remedy, bounded at the three attempts `plugin/instructions/agent_return_contract.md` → `## A return that fails the check` sets for both drivers. The `init` check refuses in one direction only because a missing tool cannot widen what a session does, and an agent that needs a withheld tool fails visibly in its own work. Claude Code 2.1.325 withholds `Glob` and `Grep` from every session that has `Bash` (`### Not yet measured, and the hand step that measures it`, below), so a two-way check refused every node whose agent declares `Bash` beside `Glob` or `Grep`. The `init` check and the launch flags answer the three gaps `docs/orchestrator-cost-measurement.md` → `## 4. Does a session's main agent keep its \`tools:\` allowlist?` → **Three things a launcher must handle:** names. **MCP tools not shown to be excluded:** an agent whose `tools:` line names no `mcp__` tool is launched with `--disallowedTools mcp__*`; one that names some, with `--strict-mcp-config` and an MCP configuration cut to those servers (`pnl_agent_flags`). **An unknown agent fails silently with exit 0:** an unknown agent produces no `init` event (`docs/orchestrator-cost-measurement.md` → `## 4.`, the `Unknown agent` row), so the no-`init` rule catches it: the session is `error` once its third attempt has none either. **The agent set comes from the environment:** every session pins the plugin with `--plugin-dir <root>`, the plugin's runtime root, and names its agent by the scoped name `<plugin name>:<agent>`, the plugin name read from `<root>/.claude-plugin/plugin.json`.

**Cost.** A return that fails its schema every time costs three sessions before the node records `error`. A dispatch node whose agent has no readable `schemas/<agent>.return.json` — or one that is not one JSON object, or has no top-level `oneOf` — faults the driver at `pnl_init`, before any session is launched. A shadowing agent definition is now caught only when its `tools:` line names a tool the pinned one does not; a narrower one passes. The driver ties its refusal to nothing a Claude Code version withholds, so a change in what is withheld shows in `<branch>.log`, not as a park: the log line is the deliberate surface, and no observation is written for it.

### The cost

- **A setup session per launch.** A launch the driver takes runs a setup session first — the engine command through its steps 1–4 and its step 4a, then nothing else — and, on the driver's hand-off, a second engine session for the rest of the run (`plugin/commands/branch-start-plan-autonomous.md` → step 4a). The orchestrated path is one engine session.
- **Node streams reach the run stream one node late.** Each node's stream is written to its own file and appended to the run's `<branch>.stream.jsonl` only when that node is reaped (`planning-node-lib.sh` → `pnl_reap`), so the usage gate and run analytics, which read the run stream, see a node's events only after it has ended.
- **No `context_notes:` on this path.** A node's prompt is its dispatch block filled with the walker's values, plus a resumed writer's answered pairs and nothing else, so the orchestrator's one sanctioned addition has no equivalent here.

### What the follow-up measures

`ROADMAP.md` → the `Script-driven planning pilot` row ([#159](https://github.com/firu-daniel/devscene/issues/159)) owns the follow-up: the pilot ends with a cost comparison against the orchestrated path, which decides whether the unit loop follows. The suites that drive the driver (`cli/test/planning-driver-walk.test.mjs`, `cli/test/planning-driver-control.test.mjs`, `cli/test/watcher-planning-driver.test.mjs`) run a stub agent CLI; they are evidence of the driver's behaviour, and no figure taken under them is evidence of a saving.

### Not yet measured, and the hand step that measures it

One fact the driver once depended on was measured on a plain session, outside the driver. It is kept as the dated record it is; the driver no longer reads `structured_output` or passes `--json-schema` (`### The return schema, the graph's outcomes, and the \`init\` check`, above):

- **A `stream-json` session's closing `result` event carries `structured_output` under `--json-schema`.** Measured 2026-11-15 on Claude Code 2.1.325, a plain session with no `--agent` and no `--plugin-dir`:

  ```
  claude -p --output-format stream-json --verbose --model haiku --json-schema '{"type":"object","properties":{"outcome":{"type":"string","enum":["PASS","FAIL"]},"return":{"type":"string"}},"required":["outcome"]}' 'Reply with outcome PASS and return "probe ok".'
  ```

  whose `result` event, read with `jq -c 'select(.type=="result") | {subtype, is_error, structured_output, result}'`, was:

  ```
  {"subtype":"success","is_error":false,"structured_output":{"outcome":"PASS","return":"probe ok"},"result":"{\"outcome\":\"PASS\",\"return\":\"probe ok\"}"}
  ```

  Both of the sources `pnl_reap` then read carried the decision: `structured_output` as an object, and `result` as the same object in JSON text.

  **Corrected 2026-11-16, Claude Code 2.1.325:** under `--agent`, `--json-schema` is not applied and the `result` event carries no `structured_output`. A session launched `--plugin-dir <main checkout>/plugin --agent devscene:prompt-injection-reviewer` and asked to reply with outcome `PASS` carried no `structured_output` key, and its `result` was prose: `probe ok` followed by the agent declining to return `PASS` because its own contract emits only `verdict: SAFE` or `verdict: UNSAFE`. The first real script-driven node, `--agent devscene:task-plan-writer` with the driver's schema (run `fix_run_commit_trailer_amend`), carried no `structured_output` key either, and its `result` was the writer's prose return ending in its fenced `story_file:` / `task_files_dir:` / `tasks_count:` / `story_points_total:` block. Both rows are `harness-runs/task_prompts/feat_structured_planning_agent_outputs_task_prompt.md` → `## Measured, 2026-11-16, Claude Code 2.1.325`'s, with the same `--json-schema` as the command above, and `docs/structured-agent-returns.md` → `## 3. Measured, and not yet measured` carries that table whole. So the plain-session entry is not a fact a node session can rely on.

Two facts the driver depends on are measured on a real node session, on Claude Code 2.1.325, 2026-11-16:

- **The `init` tools under `--json-schema` are the agent's allowlist less what Claude Code withholds, and nothing more.** Node 1 (`plan_writer`) of the run `fix_run_commit_trailer_amend`, launched by the driver with `--json-schema`, had an `init` `tools` list of:

  ```
  ["Read","Write","Edit","Bash"]
  ```

  against the `tools:` line `Read, Write, Edit, Bash, Glob, Grep, mcp__devscene-docs__search_docs`. `--json-schema` added no tool. The only difference from the `tools:` line is the `Glob`/`Grep` omission the sessions below show. Three more sessions were launched by hand as the driver launches them, one per agent:

  ```
  claude -p --output-format stream-json --verbose --plugin-dir <main checkout>/plugin --agent devscene:<agent>
  ```

  reading the `system`/`init` event's `tools`:

  | Agent | `tools:` line | `init` tools |
  |---|---|---|
  | `task-plan-writer` (the run's node 1) | `Read, Write, Edit, Bash, Glob, Grep, mcp__devscene-docs__search_docs` | `Read, Write, Edit, Bash` |
  | `architecture-reviewer` | `Read, Glob, Grep, Bash, Write, mcp__devscene-docs__search_docs` | `Read, Bash, Write` |
  | `committer` | `Bash, Read, Edit` | `Bash, Read, Edit` |
  | `prompt-injection-reviewer` | `Read, Grep, Glob` | `Read, Grep, Glob` |

  The run's orchestrator session, launched with no `--agent`, has no `Glob` or `Grep` in its `init` tools either, beside `Bash`. So in this Claude Code version a session that has `Bash` is given neither `Glob` nor `Grep`, whatever the agent declares. A session without `Bash` keeps them. No session was given a tool its agent does not declare. The two-way check the one-way rule replaced (`### The return schema, the graph's outcomes, and the \`init\` check`, above) refused node 1 for that omission, and the run parked after its first node:

  ```
  [plan-drive] #1 plan_writer: error (the agent tools do not match its init event: missing [Glob, Grep], extra [])
  ```

- **No installed plugin copy is loaded beside `--plugin-dir`.** The same node-1 `init` event loaded `devscene` once:

  ```
  {"name":"devscene","path":"<main checkout>/plugin","source":"devscene@inline","version":"0.7.1"}
  ```

  beside Claude Code's built-in plugins. No installed copy was loaded beside the `--plugin-dir` one.

The driver's read of a node's return rests on the corrected entry's second session: a node's `result` text is the agent's own reply, ending in its fenced block. The fact the orchestrated path's routing check depends on is now measured: an `Agent` result does not carry the sub-agent's reply verbatim, but wraps it between a frame line and an `agentId:` / `<usage>` trailer and indents every line of it, and the routing check's reading takes the reply out and disregards the rest. Its record is `docs/structured-agent-returns.md` → `## 3. Measured, and not yet measured`.

The hand step that reads a node's return, and re-measures the facts above, is one real planning run with the key on, from a terminal outside any agent session, run from the main checkout with `<scripts_dir>` and `<state_dir>` your configured values. Turn the key on — the watcher reads it at the next launch, with no restart:

```
npx devscene config set execution.scriptDrivenPlanning true
```

Then drop a task prompt for a throwaway branch `<branch>` as usual. Once its first node has ended, read its `result` text from that node's stream:

```
jq -r 'select(.type == "result") | .result' <state_dir>/autonomous_logs/<branch>.planning/1-plan_writer.stream.jsonl
```

The node's return block is that text's last ```` ```json ```` fence, and nothing but whitespace may follow its closing fence. To re-measure the two facts above on a later Claude Code version, read the same stream's `init` tools and plugins, one command at a time, and compare the first with the `tools:` line of `plugin/agents/task-plan-writer.md` in the pinned plugin:

```
jq -c 'select(.type == "system" and .subtype == "init") | .tools' <state_dir>/autonomous_logs/<branch>.planning/1-plan_writer.stream.jsonl
jq -c 'select(.type == "system" and .subtype == "init") | .plugins' <state_dir>/autonomous_logs/<branch>.planning/1-plan_writer.stream.jsonl
```

These two reads are the re-measurement route; the 2.1.325 values above were read from the sessions' `system`/`init` events, not recorded as these commands' output.

Each fact is recorded with its command, its exact output, the Claude Code version and the date, as this tree's documents of record require (`.claude/context/conventions.md` → `## Documents of record`).
