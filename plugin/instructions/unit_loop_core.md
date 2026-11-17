# The unit loop — canonical implement → [review] → commit loop (mode-free, family-neutral)

This file is the **single owner** of the implement → \[review\] → commit loop that every phase-driven flow runs over a readiness list: pick the next unit, route it to a layer, dispatch an implementer, optionally review, commit, repeat. Callers **cite it by reference and never restate it** — a phase says which substitution row it runs and nothing more. A family that needs its own variant **appends a row to the substitution table below**; it does not declare a copy of the loop elsewhere.

It also owns `## The test-run rule`: the rule every plan a unit loop walks is written and graded against. It is homed here because the unit loop is where every such plan is executed; its citers, listed in that section's roster, reach beyond the loop's own callers to the plan writers and plan reviewers.

> **The bindings in effect here are those of the fork the citing flow was dispatched via** (`mode_contract.md` rule (5)). This file supplies no mode-specific values and names no fork.

---

## Resolved values

The tokens below resolve from the adopting repository's `devscene.config.json`, except `<test_file_cmd>`, which resolves from a conventions document. They are declared here once; after this table the body uses each one as an ordinary placeholder. Two other kinds of `<…>` name in this file resolve elsewhere and are deliberately **not** listed here: mode-contract **bindings** (`<escalate>`, `<per_unit_review>`, `<commit_call>`) resolve from the binding table of the fork the citing flow was dispatched via, and ordinary **path placeholders** (`<branch>`, `<story_path>`, `<task_file>`, …) resolve from the flow's entry core `## Setup`. `### Placeholder resolution` below states that split and the substitution table's `Placeholder owner` column applies it — this section changes neither, and its clause (ii) is about the remaining `<…>` names rather than the tokens here.

| Token | Class | How to resolve it |
|---|---|---|
| `<state_dir>` | config value | `devscene.config.json` → `stateDir` — the run-artifact tree every artifact path in this file is relative to. Default `devscene/`. It is never dot-named: no path segment of it may begin with a dot. |
| `<layer_names>` | config value | `layers[].name`. **No substitution of the names themselves** — the configured names travel through this file unchanged, because `## Layer routing table` passes the layer as a dispatch argument rather than selecting an agent filename by it. `general` is one of the `layers[]` rows a generated config emits (`{ "name": "general", "path": ".", "conventions": … }`), not an entry beside the array. |
| `<layer_path_map>` | config value | `layers[].path` together with `layers[].conventions` — the two values `## Layer routing table` passes to the implementer and the reviewer alongside the layer name. |
| `<test_cmd>` / `<typecheck_cmd>` | config value | `commands.test` / `commands.typecheck` — the full test suite and the type check. Where `commands.typecheck` holds exactly `<none>`, the repository states it has no type check. |
| `<test_file_cmd>` | conventions document | The single-file test command a conventions document states, read from the dispatched layer's `layers[].conventions` document or from the catch-all layer's — the entry whose `path` is `"."`. Used for a unit's own test files, for the tree guards `## The test-run rule` point 7 selects and, on row `G.4`, for the test file(s) its finding names (`## The test-run rule`). |
| `<tree_guards>` | config value | `treeGuards` — a list of `{ test, covers }` entries: `test` is the argument `<test_file_cmd>` takes, `covers` a repo-relative glob. Absent means none. |

---

## Mode contract — bindings this file uses

The three names below are Mode-contract **bindings**. This file states behaviour; the fork the citing flow was dispatched via carries the values inline. `mode_contract.md` owns the mechanism and the full vocabulary. **None of these has a default here — an unbound binding is a stop condition** (mechanism rule (1)): halt and report rather than guessing a value.

| Binding | Used at | Meaning (short) |
|---|---|---|
| `<escalate>` | `## The unit loop` step 3 (the implementer returns an `outcome` of `blocker`, an `outcome` of `already passing` on a row other than `G.4`, or a return that fails the routing check a third time; an `outcome` of `prohibited`, or of `already passing` on row `G.4`, takes `### The dispositioned outcome` and never reaches this binding); `### Per-unit review step` (the review loop does not converge, the reviewer returns an `outcome` of `blocker`, or its return fails the routing check a third time); `## The unit loop` step 5 (the commit call exits 1 or 2, or a landed commit is wrong) | This flow's path for halting and reporting an **agent/flow blocker**. |
| `<per_unit_review>` | `## The unit loop` step 4 (the extension point); the whole of `### Per-unit review step`, including its `iteration >= 5` convergence cap; `## Layer routing table` (its `Reviewer` column); `## The unit loop` step 5 (whether `--findings` is passed); the row `A` and `review_item` **Commit staging** bullets (whether the unit's findings folder is staged) | `on` \| `off` — whether the per-unit reviewer step runs between implementer and commit. |
| `<commit_call>` | `## The unit loop` step 5 (the commit call) | The wrapper prefix the fork binds, ahead of the call's `--unit` arguments. |

This file declares no other binding. Every remaining `<…>` name it uses is a **config value** (`## Resolved values`), a **path placeholder**, or a locally-defined name — see `### Placeholder resolution`.

**The third unit outcome adds none either.** `### The dispositioned outcome` is deliberately **not** a fourth binding: it takes no per-fork value, and a fourth row here would halt every fork that has not bound it — the mechanism rule stated above. Its second outcome, `already passing`, adds no binding either, for the same reason.

---

## Layer routing table

Read the `_(layer: …)_` tag on the readiness entry selected in step 1 — it is on the line already read off the row's index. **Do NOT open the detail file to route**; that file is the implementer's (and, when per-unit review is on, the reviewer's) ground truth, not a routing source. The tag lists one or more layer names in bottom-up order. Map each tag value to its dispatch:

| Layer tag value | Implementer | Reviewer | Dispatch arguments |
|---|---|---|---|
| any one of `<layer_names>` — **one row per `layers[]` entry** in `devscene.config.json`, and no other value routes | `layer-implementer` | `layer-reviewer` | the layer name (the tag value itself), plus that entry's `layers[].path` and `layers[].conventions` taken from `<layer_path_map>` |

**The table is generic because the layer set is adopter-configured**: `layers[]` is an arbitrary list, so an agent-per-layer scheme cannot be generated for it — the layer travels as a dispatch argument to two agents instead of selecting one of a fixed set of agent filenames.

**Catch-all.** Work that lands in none of the other layers' paths goes to **the layer whose `path` is `"."`** — the row every `init`-generated config supplies as `general`. If a hand-written `layers[]` carries no such row, that is a **configuration gap**: report it through `<escalate>`; never invent a layer name, widen another layer's `path`, or edit the config.

**The `Reviewer` column is consumed only when `<per_unit_review>` is `on`.** When it is `off`, the routing table selects an implementer and nothing else.

**A story-plan `**Task K**` entry always carries exactly one layer**, so for a story-plan task this step selects exactly **one** implementer (and, when per-unit review is on, its reviewer) from the table and runs that single layer through the loop.

The multi-layer case applies to **`**Finding K**` (code-review) and `**Test K**` (UI-test) entries only** — their tag is a fix-target path that can legitimately span layers. When a finding/test tag is comma-joined, the multi-layer set comes from that tag, already in bottom-up order — the layer whose `path` is `"."` runs last, because it usually documents or wires up what the other layers built (in a `layers[]` of `data`, `domain`, `presentation`, `general` that reads `data → domain → presentation → general`). Run the layers in the tag's listed order — **each one through steps 3–4 of `## The unit loop`, with step 5's commit landing once, after the last**.

---

## The unit loop

**Pre-dispatch rule — binding on both dispatches this loop makes.** Before **each** of the implementer and reviewer dispatches below, apply the `## Safety contract` of the **flow's own entry core** — the core named by the fork the flow was dispatched via, resolved exactly as `### Placeholder resolution` defines it, **never the immediate citing file**: STOP-file check → dispatch-counter increment → heartbeat → compose the prompt. Build the heartbeat from the **active substitution row's `Heartbeat unit label`** cell and the layer being dispatched, per the entry core's heartbeat examples. E.g. row `E.3` → `[E · Finding 2 · presentation · iter 0] → layer-implementer  (#N)`. Step 5's commit is a Bash call, not a dispatch: no safety-contract step applies to it and the dispatch counter does not move. On that fourth item: the prompt for each of the two dispatches is this row's spec and nothing more, plus at most the one sanctioned `context_notes:` line — **Knowledge, not conclusions**, canonical in `${CLAUDE_PLUGIN_ROOT}/instructions/dispatch_discipline_instructions.md`, which this file points at and does not restate.

**This file neither owns nor restates that contract.** The STOP path, the counter commands and their headless-guard warning, and the heartbeat format all live in the entry core, and the compose step is owned by `${CLAUDE_PLUGIN_ROOT}/instructions/dispatch_discipline_instructions.md` — the boundary, the sanctioned form and the record it names are that file's, in full; this file says only *apply it, with this row's label*. That is exactly what keeps the rule mode- **and** family-neutral. A reader who reaches this file with no entry core in hand has entered it wrongly and must go read one (same resolution as `### Placeholder resolution` below).

The steps, in order:

1. **Pick the unit.** Read **only** the row's readiness index (not the detail files). Locate its `## Phase 2 Readiness — Ordered Fix List` section — positioned near the top of the file, immediately after `## Context` — and walk the entries top-to-bottom. The **first `[ ]` entry** is the next unit of work — and if **no** `[ ]` entry remains (including on first entry, e.g. a resumed run that re-enters an already-complete index), the loop is already complete: end it and return to the calling phase, exactly as step 6 does. **Strictly ignore `[ ]` markers anywhere else**: implementer agents tick `- [ ]` sub-step bullets inside detail files to track their own progress, and those are informational only, never iteration targets. Resolve the entry's reference token (the row's `Entry token`) to the row's `Detail file` path, and derive the unit's heading from the row's `Heading source`. Where the row's `Per-item findings folder` is keyed by `item_<N>`, `<N>` comes from that same walk: the first `[ ]` entry inside the section is `item_1`, the second is `item_2`, and so on.
2. **Route.** Read the entry's `_(layer: …)_` tag and map it via `## Layer routing table`. **Never open the detail file to route.**
3. **Per layer in scope.** On entering a layer, `iteration = 0`. **Apply the pre-dispatch rule**, then dispatch `layer-implementer` — with `<layer>` and its `<layer_path_map>` values as dispatch arguments, per `## Layer routing table` — carrying the row's prompt:
   - First iteration: `Implement <heading> from <detail_file>.` — plus the row's `Implementer prompt extras`, if any.
   - Fix iteration: `Fix <heading> per <findings_file> from <detail_file>.` where `<findings_file>` is `` `layer-reviewer.findings_file` `` from **this layer's** reviewer's most recent `outcome` of `FAIL` — never a listing of the row's `Per-item findings folder`, which every layer of a multi-layer unit shares, so its highest-numbered file may be another layer's.

   Either prompt may carry one optional trailing `context_notes:` line, as `${CLAUDE_PLUGIN_ROOT}/instructions/dispatch_discipline_instructions.md` defines it, and **nothing else may be appended** to it. Step 5's commit call takes no `context_notes:`.

   Read the implementer's return as `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## Reading a return` states. The fields that check reads are `` `layer-implementer.cause` `` for an `outcome` of `prohibited` or `already passing`, `` `layer-implementer.blocker` `` for an `outcome` of `blocker`, and none beyond `outcome` for an `outcome` of `implemented`. `` `layer-implementer.flags` `` is **optional**.

   - An `outcome` of `implemented` → continue, keeping each `` `layer-implementer.flags` `` item for step 6.
   - An `outcome` of `prohibited` → `### The dispositioned outcome` below, keeping each `` `layer-implementer.flags` `` item for step 6.
   - An `outcome` of `already passing`, on row `G.4` only → `### The dispositioned outcome`'s route, per its `#### The already-passing close`, keeping each `` `layer-implementer.flags` `` item for step 6.
   - An `outcome` of `blocker`, an `outcome` of `already passing` on any other row, or the third consecutive return that fails the check (`${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## A return that fails the check`) → stop the whole loop and `<escalate>`, quoting `` `layer-implementer.blocker` `` for an `outcome` of `blocker`, `` `layer-implementer.cause` `` for an `outcome` of `already passing`, or naming the check that failed.

   **The fail-safe direction is escalate** — an outcome the row does not admit is the escalating kind: a wrongly-escalated unit costs one hand-off, a wrongly-closed one closes a finding nobody fixed.
4. **Per-unit review — extension point, governed by `<per_unit_review>`.** When it is `on`, run `### Per-unit review step` below before continuing. When it is `off`, skip the review: `iteration` stays `0`, the per-unit convergence cap does not apply, and the implementer's own blocker report (step 3) is the only per-unit stop. **Either way, when this layer finishes cleanly, continue with the next layer in scope (back to step 3); go to step 5 only after the last in-scope layer has finished** — the commit lands **once per unit**, never once per layer.
5. **Commit.** Issue, as **one** Bash call, with every placeholder spelled as the literal text it resolves to and no `$` anywhere:

   ```
   <commit_call> --unit <the row's commit unit> --plan <the row's readiness index> --id <K> <the row's commit extra args>
   ```

   `K` is the unit token from step 1's entry, never the walk position `N`. Issue the call once, alone. **Once, alone** means its own Bash call holding that one command and nothing else — no `cd`, `;`, `&&`, `||`, pipe, `echo "exit $?"`, `$(…)` or shell variable before or after it.

   The call reads the entry, the detail file and the tree itself; the loop passes nothing else, and nothing extra for `### The dispositioned outcome`. When `<per_unit_review>` is `on`, the row's `commit extra args` carry `--findings` set to the row's `Per-item findings folder` as resolved for this unit, passed whether or not a reviewer wrote into it. The folder holds this unit's reviewer findings, which are run artifacts of the unit rather than its work: the argument commits them with the unit and keeps them out of the work-file test, so a commit that landed no work file still prints `staged: index-only` to step 6.

   Read the call by its exit. **0** — committed: continue to step 6. **3** — `error: nothing to commit`, a unit with nothing left to commit: continue, returning to step 1. **1 or 2** — the `error:` line it prints `<escalate>`s.

   **A commit that landed is never repaired.** Exit 0 is a commit that stands — the wrapper's landed exit 1 included, which it re-syncs itself and reports as exit 0 — and it stays exactly as it landed, whatever is wrong with it: no `git commit --amend`, `git reset`, `git rebase`, `git update-ref` or second commit in its place. A line step 6 names is appended there, as step 6 says; anything else wrong with a landed commit — a subject, body line, staged path or ticked entry the unit did not mean — `<escalate>`s, naming the `commit_sha:` and what is wrong, and the loop does not continue. This is the canonical statement for every commit an orchestrator lands through the main checkout's `commit-on-branch.sh`, an artifact commit or a plain-form call included; an artifact commit point cites it rather than restating it, and reports through its own flow's escalation path.
6. **Emit one progress line** naming the unit just committed — the row's `Heartbeat unit label` followed by `committed: <sha> <subject>`, taken from the call's printed `commit_sha:` and `subject:` lines (row `A`: `Task N committed: <sha> <subject>` — the source loop's own wording, where `N` is the same task number row `A`'s `Task <K>` label calls `K`; see `### Named exceptions` → **Row A**), and when the call prints a `plan_flipped: already-[x]: <entry> — not flipped by this call` report, append that report to the same line verbatim — no halt, no park, no `<escalate>`; the run continues and the fact is on the record. **A `staged: index-only — …` line in that same output takes the same treatment** — append it to the line verbatim, no halt, no park, no `<escalate>` — it is the loop's only notice that this unit's commit staged the readiness index and no work file. **So does an `index_sync: failed — …` line**: the commit landed, and the line is the loop's only notice that the working copy's index did not take it — no halt by design, since the next unit's commit stages those paths and re-syncs it. **So does every item of `` `layer-implementer.flags` `` an implementer of this unit returned (none when the field was absent or empty, as `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## Reading a return` states) — any layer, any iteration**: append each to the same line verbatim, no halt, no park, no `<escalate>` — it is the loop's only notice of what the implementer asked the orchestrator to flag to the user, a refused instruction carried in task data among it. **When any layer of this unit took `### The dispositioned outcome` on an `outcome` of `prohibited`, the line gains one more clause** — `dispositioned: ` followed by the one-line cause — in that same shape: appended verbatim, no halt, no park, no `<escalate>`, the run continues. **When no layer was dispositioned and a layer took `#### The already-passing close`, the clause is `already passing: ` followed by its cause**, in the same shape. The cause is `` `layer-implementer.cause` ``, carried verbatim and never re-worded. **One clause, one cause:** the **first** such layer's, in the readiness entry's `_(layer: …)_` tag order. Then return to step 1. Do not pause for input. When every `[ ]` in the row's readiness index is `[x]`, the loop ends and the calling phase continues. **Where the dispositioned fact goes on:** a flow that keeps an improvement-observations intake and a Done summary reports it in both, through its own override; a flow that keeps neither leaves the record in the unit's detail file, on its commit and on this line. This file names no fork, no override and no phase — `mode_contract.md` rule (5)'s boundary, as the note at the top of this file states.

### Per-unit review step (`<per_unit_review>` = `on`)

This is the **one and only** statement of the per-unit review body. It runs between step 3 and step 5, once per layer in scope, and only while `<per_unit_review>` is `on`. Everywhere it is cited — this file's own cells and steps, and its callers — it is named by the short form `### Per-unit review step`; the gate suffix this heading carries is not part of that name.

`iteration` — the cap counter, and what the heartbeat's `iter` shows, never a file index — is reset to `0` at the start of each layer of each unit (step 3); the cap below exists to prevent one stuck layer from running forever, **not** to limit the whole session. Hitting it stops that layer's loop and reports — it does not end the whole flow.

**The pre-dispatch rule of `## The unit loop` applies here too**: apply the **flow's entry core's** `## Safety contract` before the reviewer dispatch, and again before each fix re-dispatch of the implementer, with the heartbeat label taken from the row's `Heartbeat unit label` cell and the layer under review.

Dispatch `layer-reviewer` — with the same `<layer>` and `<layer_path_map>` dispatch arguments the implementer took — with this fenced block, whose first line and whose `task_file:` / `task_heading:` / `findings_folder:` values all come from the **active substitution row**; `iteration:` carries `<review_index>`, the **next free index** in that `Per-item findings folder` — list the folder, take one past the highest `review_<n>.md`, or `0` when the folder is absent or holds none. Resolve it immediately before **each** reviewer dispatch: the previous layer or the previous iteration may just have added a file, a PASS-with-Should/Nice file included, and every layer of a multi-layer unit writes into the same folder:

```
<the row's `Review prompt first line`>
task_file: <the row's `Detail file`>
task_heading: <the row's `Heading source`>
findings_folder: <the row's `Per-item findings folder`>
iteration: <review_index>
context_notes: <omit entirely when you have no fact to pass — see ${CLAUDE_PLUGIN_ROOT}/instructions/dispatch_discipline_instructions.md>
```

Anything added to this block outside that last line is a violation the record `${CLAUDE_PLUGIN_ROOT}/instructions/dispatch_discipline_instructions.md` defines must show.

(The reviewer creates the findings folder itself only when it has findings to write — do **NOT** `mkdir -p` here.)

Read the reviewer's return as `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## Reading a return` states:

- An `outcome` of `PASS` → leave this layer and continue the loop (the next layer in scope, or step 5 if this was the last).
- An `outcome` of `FAIL` → increment `iteration`. **If `iteration >= 5`, `<escalate>`** with the `` `layer-reviewer.findings_file` `` path this return carries and a one-paragraph summary of the situation — `5 review iterations on …, layer X, did not converge`, naming the unit with the row's `Heartbeat unit label` (row `A`: `5 review iterations on Task N, layer X, did not converge`). Otherwise loop back to **step 3's implementer dispatch** with the fix prompt, its `<findings_file>` being that same `` `layer-reviewer.findings_file` `` path — step 3's `iteration = 0` reset is per layer, per unit, and is **not** re-applied on a fix iteration.
- An `outcome` of `blocker`, or the third consecutive return that fails the check (`${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## A return that fails the check`) → `<escalate>`, quoting `` `layer-reviewer.blocker` `` or naming the check that failed.

**Ownership.** A fork binds `<per_unit_review>` and **nothing more**: no fork restates this body, and no fork may cite another fork *for it*. The review step is flow-body content owned here, so it sits squarely inside `mode_contract.md` rule (5)'s scoped prohibition — see that rule for the enumerated `### Sanctioned cross-fork anchors` that fall **outside** the prohibition; this file neither repeats nor narrows that list. Per-row wording deltas belong in that row's `Exceptions` cell, never in this body.

### The dispositioned outcome

Step 3's **third** exit for a layer, reached by an `outcome` of `prohibited`, or on row `G.4` an `outcome` of `already passing` (`#### The already-passing close` below). It is neither a success nor a stop: the unit is **closed**. The `prohibited` route applies to every row of `## Substitution table` unchanged and no row owes a cell for it; the `already passing` route is row-scoped to `G.4`. (The cause either outcome carries is `` `layer-implementer.cause` ``.)

- **What it is.** This layer's work is accepted as correctly diagnosed and impossible for **any** agent in this flow. This file states the outcome; `layer-implementer`'s contract states the admissibility test that let it return that outcome. Neither restates the other, and this loop re-runs no part of that test.
- **What already exists on disk.** The implementer appended a `## Disposition` section to the unit's detail file before returning. The loop writes nothing itself and opens no detail file and no findings body to decide — the outcome is the whole decision.
- **The review step is skipped.** Step 4 is not entered for this layer: there is no code to review. `iteration` is untouched.
- **The loop continues.** This layer is finished — continue with the next layer in scope (back to step 3), or go to step 5 if it was the last.
- **It never parks and never escalates.** This exit adds no channel, no sentinel file and no clarification question, and the flow's `<escalate>` binding is not reached from it.

**The readiness marker still flips `[ ]`→`[x]`.** `[x]` means the unit is **closed**, and the disposition is its closure — recorded in the detail file and on the unit's commit, in a body line, the two artifacts a reader has. **No third readiness marker is minted**, and the reason binds anyone tempted to add one: step 1 walks for the first `[ ]`, the commit step resolves the entry and flips `[ ]`→`[x]` and nothing else, and every completion check downstream reads those two markers — a third would have to be taught to all of them at once.

**The commit's record.** The loop passes nothing extra to step 5's call for this exit. The commit step finds the detail file's `## Disposition` section — or, when none is present, its `## Already passing` section — and writes the lower-case body line `record disposition of <unit token> — <cause>` (or `mark <unit token> already passing — <cause>`), the cause taken from that section's `**Cause:** ` line; the subject stays the title subject. Only the first such section's cause goes on the commit, which lands **once per unit**, as `## Layer routing table` requires; every dispositioned or already-passing layer's diagnosis stays in the unit's detail file, each written there as its own section by its own implementer.

#### The already-passing close

A row-`G.4` layer that returns an `outcome` of `already passing` takes this outcome's route. `layer-implementer`'s contract owns the check that admits it (`## The test-run rule` point 1's row-`G.4` exception).

- **Shared with the dispositioned route:** the review step is skipped, the loop continues to the next layer or to step 5, it never parks or escalates, and the readiness entry flips `[ ]`→`[x]`.
- **What it means.** The finding's named test already passes after an earlier unit's fix — not *impossible for any agent*.
- **Its record.** The implementer appended a `## Already passing` section to the detail file, not a `## Disposition` one.
- **Its commit argument.** None: the commit step reads `## Already passing` when no `## Disposition` is present (`**The commit's record.**` above). When a layer was dispositioned, only the disposition goes on the commit, and the already-passing fact stays in the detail file.
- **Its progress clause.** Step 6's `already passing: <cause>` clause, not `dispositioned: `.

---

## The test-run rule

1. **No unit runs `<test_cmd>`, a gate script it runs, or a test file the unit did not create or edit — except a row `G.4` unit's named files and the tree guards point 7 selects, through `<test_file_cmd>` only.** The full suite and the whole-tree `<typecheck_cmd>` run once per Run gates round, through its wrapper, at `${CLAUDE_PLUGIN_ROOT}/instructions/plan_orchestration_instructions_core.md` → `## Phase G — Run gates`; the suite runs nowhere else in the flow. A targeted test the unit did not write is excluded too, unless point 7 selects it as a tree guard. The row-`G.4` exception covers **only** that row and **only** the file(s) the finding names — never `<test_cmd>`, a gate script or any other test file.
2. **A unit runs `<typecheck_cmd>`** as written, with no path argument: the whole tree. Where `commands.typecheck` is `<none>`, it runs nothing for that gate and reports it not run.
   - **Every reported failure lies outside the unit's change** — it names no file the unit created or edited and no symbol it defined or changed: an **evidence downgrade**, not a blocker. Phase G's whole-tree run verifies it.
   - **A failure the unit's change caused** is the unit's to fix; one it cannot fix is a transient blocker.
   - **A path-narrowed run**, where the configured line accepts paths, is supplementary evidence, labelled as narrowed, never reported as the whole-tree result.

   `${CLAUDE_PLUGIN_ROOT}/agents/layer-implementer.md` → **An evidence downgrade is recorded, in every mode.** owns how the downgrade is recorded.
3. **A unit that creates or edits a test file runs those files, through `<test_file_cmd>`; the only other test files it runs are point 7's tree guards.** Where no document states one, or the stated command is refused, the unit skips the run, records the skip in its return, and raises no blocker. The same skip applies to point 1's row-`G.4` run.
4. **No plan asks for a test run.** No `**Verification:**` bullet, finding fix or sub-step names `<test_cmd>`, a gate script, or a test file the unit neither creates nor edits; naming the unit's own new or edited test file is allowed, subject to (3). No plan names a tree guard the task neither creates nor edits, and no plan sentence limiting a unit's test runs (*"that is the only test file this task runs"*) cancels point 7: the guard run is the loop's, never the plan's. A guard file the task itself creates or edits stays the unit's own test file under (3), and the plan may name it as such. This binds every writer of a plan a unit loop walks — the task plan; the business-parity, architecture, code-review and skeptic findings; the user-review fix plan; the test fix plan — and every reviewer of one raises a breach as a **Must Fix**.
5. **`<typecheck_cmd>` is not a test run.**
6. **A unit's run stays in the foreground.** Run `<typecheck_cmd>` and `<test_file_cmd>` each as one foreground command whose output returns to you — never redirected to a file, piped, backgrounded or wrapped in a `cd`, a refusal included. A refusal takes its own route: point 3's skip for a test file; for `<typecheck_cmd>`, the refused-call fallback of `${CLAUDE_PLUGIN_ROOT}/agents/layer-implementer.md` → `## Resolved values`. When the tool layer moves a run to the background itself, do not collect it: no `Monitor` and no `sleep` (`${CLAUDE_PLUGIN_ROOT}/instructions/plan_orchestration_instructions_core.md` → `### G.1 Run the gates` forbids both by name), and no loop that reads its output for a completion line. Record the run in your return as moved to the background — not run, never a pass — raise no blocker, and continue.
7. **A unit runs the tree guards its change selects.**
   - **When** — after its own test run under point 3, on every row, whether or not the unit wrote a test.
   - **The changed-path set** — the union of the output of `git diff --name-only HEAD` and `git ls-files --others --exclude-standard`, each run bare from the checkout root, as repo-relative paths; the second is what lists a new, untracked file.
   - **The match** — a guard is selected when at least one changed path matches its `covers` glob. `**` matches zero or more whole path segments, `*` any run of characters inside one segment, `?` one character inside one segment; every other character is literal, and the glob matches the whole path.
   - **The run** — each selected guard once, through `<test_file_cmd>` with the entry's `test` value as its argument, verbatim. A guard whose file the unit already ran under point 3 is not run twice. Only `<tree_guards>` entries are guards: never search for or infer another.
   - **A failure** — handled as a failing own test: the unit's to fix in its own change, then the guard rerun. Never edit the guard file to make it pass unless the unit's detail file assigns that edit. A failure is an evidence downgrade, as point 2 grades one, only when it names no symbol the unit defined or changed and no path that equals a changed path or matches its trailing segments — a guard may print paths relative to its own directory rather than the repository root (`new-suite.test.mjs` for `cli/test/new-suite.test.mjs`). A failure that names no path at all is the unit's.
   - **A skip** — no command stated, the command refused, or the run moved to the background takes point 3's skip and point 6's foreground rule unchanged.

   No `<tree_guards>` entries, or no selected guard, adds no run.
8. **A tree-reading test registers itself.**
   - **The rule** — a test that reads a tree of repository files as text, rather than one module or one fixed file, has its `<tree_guards>` entry added to `devscene.config.json` in the same change, or by a later catch-all-layer task the adding task names.
   - **The boundary** — a test reading one fixed file is not a tree guard and owes no entry.
   - **The plan** — the task that adds such a test names, in its own file, the task that adds its entry.
   - **The grading** — a missing registration is a **Must Fix** for every reviewer: a plan whose adding task names no registering task, a unit whose diff adds no entry and whose task file names no registering task, a branch whose diff adds no entry.

**Who may cite this.** These documents point at this heading:

- `${CLAUDE_PLUGIN_ROOT}/agents/layer-implementer.md`
- `${CLAUDE_PLUGIN_ROOT}/agents/layer-reviewer.md`
- `${CLAUDE_PLUGIN_ROOT}/agents/test-fix-plan-writer.md`
- `${CLAUDE_PLUGIN_ROOT}/agents/architecture-reviewer.md`
- `${CLAUDE_PLUGIN_ROOT}/agents/business-parity-reviewer.md`
- `${CLAUDE_PLUGIN_ROOT}/agents/task-plan-writer.md`
- `${CLAUDE_PLUGIN_ROOT}/agents/task-plan-reviewer.md`
- `${CLAUDE_PLUGIN_ROOT}/agents/user-review-fix-plan-writer.md`
- `${CLAUDE_PLUGIN_ROOT}/agents/review-plan-reviewer.md`
- `${CLAUDE_PLUGIN_ROOT}/agents/branch-reviewer.md`
- `${CLAUDE_PLUGIN_ROOT}/agents/skeptic-reviewer.md`
- `${CLAUDE_PLUGIN_ROOT}/instructions/plan_orchestration_instructions_core.md`
- `${CLAUDE_PLUGIN_ROOT}/instructions/plan_orchestration_instructions_autonomous.md`
- `${CLAUDE_PLUGIN_ROOT}/instructions/code_review_instructions.md`
- `${CLAUDE_PLUGIN_ROOT}/instructions/code_review_fixes_instructions.md`
- `${CLAUDE_PLUGIN_ROOT}/instructions/user_review_fixes_instructions.md`
- `${CLAUDE_PLUGIN_ROOT}/docs/AUTONOMOUS_FLOW.md`
- `docs/config.md`
- `docs/cli.md`

A citer **points and never restates**, and **no document beyond this roster may point at this heading.** An edit that rewords or moves the heading updates every roster member in the same change. Pointers from this file's own sections are not roster entries.

---

## Substitution table

### Placeholder resolution

The `<…>` tokens in this file's rows, cells and named exceptions are of **two kinds**, resolved from two different places.

**(i) Mode-contract bindings** — exactly the three declared in `## Mode contract — bindings this file uses` (`<escalate>`, `<per_unit_review>`, `<commit_call>`). They resolve from the **binding table of the fork the citing flow was dispatched via** (`mode_contract.md` rule (5)). An unbound one is a stop condition.

**(ii) Path placeholders** — every other `<…>` token here (`<story_path>`, `<task_file>`, `<parity_review_path>`, `<code_review_path>`, `<qa_review_findings_dir>`, `<qa_fix_findings_root>`, and any a later family's row introduces). They are **not** bindings, are defined **nowhere in this file**, and resolve from the `## Setup` of the **flow's own entry core**: *the core named by the fork the flow was dispatched via, regardless of how many core→core citations deep the text sits.* A few are stated in a row's own cells in terms of the others (`<task_file>` = `<task_files_dir>task_<K>_plan.md`; `<finding_file>`, `<task_heading>` and `<finding_heading>` likewise) — those still bottom out in that same `## Setup`, via the row's `Placeholder owner`. The exclusions are **reasons, not banned files** — being the **immediate citing file**, being the **file that contains the text**, being the **family a cited section originated in**, or being a **fork** confers no ownership of a path placeholder; only being the entry core does. When one of those files *is* the entry core for the flow in hand, it owns them for that flow — solely on that ground.

This matters because two of these names are defined **differently** by the two cores that reach this file: one family's `## Setup` defines `<qa_review_findings_dir>` and `<qa_fix_findings_root>` with no round suffix, the other's as a next-free `<round>` slot (both definitions, with sources, are in the `Placeholder owner` footnote under the table). **Worked example, two hops:** row `E.3` is reached by both. A flow whose entry core is family 1's reaches it via that core's own `## Phase E`, so both QA folders resolve from **family 1's** `## Setup`. A **family-3 flow reaches it two hops deep** — family 3's fork → family 3's core `## Phase QA` → family 1's core `## Phase E` → this row — and its entry core is **still family 3's**, so both QA folders resolve from **family 3's** `## Setup` instead: its QA.0 next-free slot, which is the unsuffixed folder while that slot is free and the round-suffixed one once it is not. **Resolve the folder; never pre-compute its shape.** Resolving it instead from the immediate citing file (family 1's core, where `## Phase E` happens to live) or from the row's originating family (also 1) lands a family-3 flow in the exact folder its round resolution exists to avoid — the moment the task-plan flow has already produced one — and that failure is silent.

**Transitional clause** (owned by `mode_contract.md` rule (5)'s `Bindings vs. path placeholders` paragraph): a flow whose family has **no core yet** resolves its path placeholders from its **entry document's** own `## Setup` — the fork itself — and that is the **only** case in which a fork owns them; it exists solely for the transitional state and ends when that family's core lands. The steady-state formulation above stays primary and the exclusion list is unchanged: the clause fixes *when* a fork owns paths, it does not reopen the exclusions, and it never applies to a flow whose family does have a core.

**Three kinds of name are neither**, and are defined in this file at their point of use: `<layer>` (the output of `## Layer routing table`), `<iteration>` (this loop's own counter, set in step 3 and advanced in `### Per-unit review step` — **not** the QA round-index `<iteration>` that appears inside row `E.3`'s `<qa_review_path>`, which is always `0` and comes from the entry core's `## Setup`), `<review_index>` (the next free index in the row's `Per-item findings folder`, resolved before each reviewer dispatch in `### Per-unit review step` — a file index, never the cap counter `<iteration>`), and the ellipses inside quoted literals — `<heading>` / `<detail_file>` / `<findings_file>` in step 3's prompts (each named as the row cell it comes from), `<title>` inside the quoted `### Task K — <title>` heading pattern, `<sha>` / `<subject>` / `<entry>` in step 6's progress line (all three from the commit call's output), `<K>` in step 5's call (the unit token from step 1's entry), and `<unit token>` / `<cause>` in `### The dispositioned outcome`'s body-line forms (the entry's token and its section's `**Cause:** ` line). The same applies to names quoted **out of another document**, which this file reproduces but does not resolve: `<branch>` / `<round>` inside the `## Setup` values reproduced in the `Placeholder owner` footnote (each owned by the core quoted there).

**The reader's tell.** An unbound *binding* is a stop condition. An unresolved *path placeholder* means you entered this file without your entry core's `## Setup` — go read it, or, if your family has no core yet, use your entry document's own `## Setup` per the transitional clause above.

| Row | Readiness index (sole iteration source) | Entry token | Detail file | Heading source | Per-item findings folder (used only when `<per_unit_review>` is `on`) | Placeholder owner | Implementer prompt extras | Review prompt first line | commit unit | commit extra args | commit prefix | Heartbeat unit label | Exceptions |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `A` | `<story_path>` — the story index's `## Phase 2 Readiness — Ordered Fix List` (thin index: `## Context` + readiness; it has **no** `## Tasks` section) | `**Task K**`, entry form `N. [ ] **Task K** — <short title>` | `<task_file>` = `<task_files_dir>task_<K>_plan.md` | `task_heading` = the exact text of the `### Task K — <title>` heading at the top of `<task_file>` | `<per_task_findings_root>task_<K>/` | `plan_orchestration_instructions_core.md` → `## Setup` (only family 1's core reaches this row) | also pass `<story_path>`, for the shared `## Context` the implementer may need | `Review the in-progress task.` | `task` | `--findings <the row's Per-item findings folder>` when `<per_unit_review>` is `on`; nothing when `off` | computed by the wrapper from the branch name: `feat_` → `feat`, `fix_` → `fix`, `refactor_` → `refactor`, else `chore` | `Task <K>` — e.g. `[A · Task 3 · presentation · iter 0]` | `### Named exceptions` → **Row A**, and the shared bottom-up rule |
| `A1.5.3` | `<parity_review_path>` — the business-parity-review index's `## Phase 2 Readiness — Ordered Fix List` | `**Finding K**` | `<finding_file>` = `<parity_review_findings_dir>finding_<K>.md` | `<finding_heading>` = the exact text of the matching `### K. <title>` finding heading **in the parity-review index** | `<parity_fix_findings_root>item_<N>/` | `plan_orchestration_instructions_core.md` → `## Setup` (only family 1's core reaches this row) | none | `Review the in-progress review item.` | `review_item` | `--findings <the row's Per-item findings folder>` when `<per_unit_review>` is `on`; nothing when `off` | `fix`, computed by the wrapper — see `### Named exceptions` → **The fix rows** | `Item <N>` — e.g. `[A1.5 · Item 2 · domain · iter 0]` | **Skip this row unless `phases.parity` is `true` in `devscene.config.json`.** Then `### Named exceptions` → **Rows A1.5.3 / A2.3 / C2.4**, and the shared bottom-up rule |
| `A2.3` | `<arch_review_path>` — the architecture-review index's `## Phase 2 Readiness — Ordered Fix List` | `**Finding K**` | `<finding_file>` = `<arch_review_findings_dir>finding_<K>.md` | `<finding_heading>` = the exact text of the matching `### K. <title>` finding heading **in the architecture-review index** | `<arch_fix_findings_root>item_<N>/` | `plan_orchestration_instructions_core.md` → `## Setup` (only family 1's core reaches this row) | none | `Review the in-progress review item.` | `review_item` | `--findings <the row's Per-item findings folder>` when `<per_unit_review>` is `on`; nothing when `off` | `fix`, computed by the wrapper — see `### Named exceptions` → **The fix rows** | `Item <N>` — e.g. `[A2 · Item 2 · domain · iter 0]` | `### Named exceptions` → **Rows A1.5.3 / A2.3 / C2.4**, and the shared bottom-up rule |
| `C` | `<code_review_path>` — the code-review index's `## Phase 2 Readiness — Ordered Fix List` | `**Finding K**` | `<finding_file>` = `<code_review_findings_dir>finding_<K>.md` — the folder mirrors the index round suffix | `<finding_heading>` = the exact text of the matching `### K. <title>` finding heading **in the code-review index**, derived the same way row `A` derives `task_heading` from its `### Task K —` heading | `<per_review_findings_root>item_<N>/` | `plan_orchestration_instructions_core.md` → `## Setup` (only family 1's core reaches this row) | none | `Review the in-progress review item.` | `review_item` | `--findings <the row's Per-item findings folder>` when `<per_unit_review>` is `on`; nothing when `off` | `fix`, computed by the wrapper — see `### Named exceptions` → **The fix rows** | `Item <N>` — e.g. `[C · Item 5 · domain · iter 0]` | `### Named exceptions` → **Row C**, and the shared bottom-up rule |
| `C2.4` | `<skeptic_review_path>` — the skeptic-review index's `## Phase 2 Readiness — Ordered Fix List` | `**Finding K**` | `<finding_file>` = `<skeptic_review_findings_dir>finding_<K>.md` | `<finding_heading>` = the exact text of the matching `### K. <title>` heading **in the skeptic-review index** | `<skeptic_fix_findings_root>item_<N>/` | `plan_orchestration_instructions_core.md` → `## Setup` (only family 1's core reaches this row) | none | `Review the in-progress review item.` | `review_item` | `--findings <the row's Per-item findings folder>` when `<per_unit_review>` is `on`; nothing when `off` | `fix`, computed by the wrapper — see `### Named exceptions` → **The fix rows** | `Item <N>` — e.g. `[C2 · Item 2 · domain · iter 0]` | `### Named exceptions` → **Rows A1.5.3 / A2.3 / C2.4**, and the shared bottom-up rule |
| `E.3` | `<qa_review_path>` — the **merged** round-level QA index at `<qa_review_findings_dir>qa_review_<iteration>.md` assembled by the calling phase, **not** a qa-tester per-dispatch index | `**Finding K**` | `<finding_file>` = the namespaced QA finding file `<qa_review_findings_dir>finding_t<T>_<M>.md` that the merged index's entry points at | `<finding_heading>` = the exact text of the matching `### K. <title>` heading **in the merged QA-review index** | `<qa_fix_findings_root>item_<N>/` | **the flow's entry core's `## Setup`** — resolved per flow, not per family-that-owns-the-phase: a **family-1 flow**'s entry core is family 1's, reached via that core's own `## Phase E`; a **family-3 flow**'s entry core stays family 3's however many hops deep it entered (`## Phase QA` → family 1's `## Phase E` → here), so its QA folders take **family 3's next-free-slot resolution**, not family 1's — see the footnote | none | `Review the in-progress review item.` | `review_item` | `--findings <the row's Per-item findings folder>` when `<per_unit_review>` is `on`; nothing when `off` | `fix`, computed by the wrapper — see `### Named exceptions` → **The fix rows** | `Finding <N>` — e.g. `[E · Finding 2 · presentation · iter 0]` | **Skip this row unless `phases.qa` is `true` in `devscene.config.json`.** Then `### Named exceptions` → **Row E.3**, and the shared bottom-up rule |
| `UR-A` | `<fix_plan_path>` — the user-review fix-plan index's `## Phase 2 Readiness — Ordered Fix List` (index: `## Context` + readiness + per-finding pointers + `## Source observations`). The calling command passes the path in already round-resolved; this row never re-resolves the suffix | `**Finding K**`, entry form `N. [ ] **Finding K** — <short title>` | `<finding_file>` = `<fix_finding_dir>finding_<K>.md` — self-contained: the site anchor, the full problem description and the concrete fix | `<item_heading>` = the exact text of the matching `### K. <title>` pointer heading **in the fix-plan index** | `<per_item_findings_root>item_<K>/` — keyed by the `**Finding K**` number, **not** the walk position (see the named exception) | `user_review_fixes_instructions_core.md` → `## Setup` (only family 3's core reaches this row) | none | `Review the in-progress task.` — the source loop's own wording, **not** the fix rows' `Review the in-progress review item.` (see the named exception) | `review_item` | `--findings <the row's Per-item findings folder>` when `<per_unit_review>` is `on`; nothing when `off`; plus `--prefix refactor` or `--prefix chore` on a `## Should Fix` entry | three-way, computed by the wrapper from the **severity section** the finding's pointer sits under in the index, the `## Should Fix` arm taking `--prefix` — see `### Named exceptions` → **Row UR-A** | `Item <K>` — e.g. `[A · Item 3 · presentation · iter 0]` | `### Named exceptions` → **Row UR-A**, and the shared bottom-up rule |
| `G.4` | `<test_fix_plan_path>` — the test fix plan index's `## Phase 2 Readiness — Ordered Fix List` | `**Finding K**` | `<finding_file>` = `<test_fix_findings_dir>finding_<K>.md` | `<finding_heading>` = the exact text of the matching `### K. <title>` heading **in the test fix plan index** | `<test_fix_findings_root>item_<N>/` | **the flow's entry core's `## Setup`** — family 1 reaches this row through its own `## Phase G`, family 3 through its `## Phase G`, which cites family 1's | none | `Review the in-progress review item.` | `review_item` | `--findings <the row's Per-item findings folder>` when `<per_unit_review>` is `on`; nothing when `off` | `fix`, computed by the wrapper — see `### Named exceptions` → **The fix rows** | `Item <N>` — e.g. `[G · Item 2 · cli · iter 0]` | `### Named exceptions` → **Row G.4**, and the shared bottom-up rule |

> ⚠️ **Every row of this table passes `--id <K>` to the commit call — all eight of `A`, `A1.5.3`, `A2.3`, `C`, `C2.4`, `E.3`, `UR-A` and `G.4`.** The commit step resolves the readiness entry **by that unit token** and selects **no** entry by position. **Which number — this entry's `K`, never the walk position `N`.** A review index's readiness entries are `N. [ ] **Finding K** — <short title>` sorted by ship order, so the leading ordinal `N` (bound by step 1 to the walk position) and the finding's identity `K` — the number its `### K. <title>` pointer and its `finding_<K>.md` carry — are independent and legitimately differ (the canonical code-review sample at `${CLAUDE_PLUGIN_ROOT}/samples/sample_code_review.md` makes them disagree on purpose); pass this entry's `K`, or the commit step resolves that token and flips a different, unimplemented finding.

**Footnote — `Placeholder owner` for row `E.3`.** The two QA path placeholders are defined **differently** by the two cores that reach this row, which is why its cell names the *entry* core rather than a file:

- **Family 1** — `<qa_review_findings_dir>` = `<state_dir>/qa_reviews/<branch>_qa_review/`: **unsuffixed** on round 1, the folder name mirroring the round suffix on re-test rounds. Live owner: `plan_orchestration_instructions_core.md` → `## Setup`.
- **Family 3** — `<qa_review_findings_dir>` = `<state_dir>/qa_reviews/<branch>_qa_review_<round>/`: a **next-free `<round>` suffix**, resolved in that flow's QA.0 precisely so it *"MUST NOT collide"* with a QA review the task-plan flow already produced. What differs is the **resolution rule**, not always the result: with no QA review yet on the branch the next free slot is round 1, which QA.0 resolves to the **unsuffixed** folder — byte-identical to family 1's value in that one case. The divergence bites the moment the task-plan flow has produced one, which is the case QA.0 exists for, so resolve the folder and never assume either shape. Live owner: `user_review_fixes_instructions_core.md` → `## Setup`. Family 3's core landed carrying that `## Setup`, so the transitional clause above no longer applies to this family: the steady-state entry-core rule names the owner directly, exactly as row `E.3`'s `Placeholder owner` cell states it.

`<qa_fix_findings_root>` mirrors the same divergence (`<state_dir>/qa_review_point_reviews/<branch>_qa_review[_<round>]/`). This is why row `E.3` names the folder through the placeholder and never as a literal path.

**Footnote — `Heartbeat unit label`.** Rows `A`, `C` and `E.3` carry the labels their source loops used verbatim (`Task <K>`, `Item <N>`, `Finding <N>`). Rows `A1.5.3`, `A2.3` and `C2.4` had no per-item heartbeat example of their own; each ran *"the same loop as Phase C"*, so each takes Phase C's `Item <N>` label with its own phase field. The `Item` / `Finding` divergence between rows `C` and `E.3` is the pre-existing wording of the two loops: **do not harmonise it in either direction** — neither by relabelling row `E.3` to match `C`, nor `C` to match `E.3`.

**Footnote — path concatenation.** Wherever this file joins a `## Setup` path placeholder to a file name or a subfolder — the `Readiness index`, `Detail file` and `Per-item findings folder` cells, and the same paths where `### Named exceptions` repeats them — it concatenates directly, because those `## Setup` values already end in `/`. Three of the source loops wrote a redundant extra `/` at that join and one did not; the resulting path is identical either way.

**Other families append their own rows to this table** — family 3's `UR-A` row is one such appended row. The table has exactly one owner file and must never be forked into a second document. An appended row fills **every** column, `Placeholder owner` included (for a row only one family can reach — `UR-A` among them — that is *the flow's entry core's `## Setup`*, which is always that family's own core).

### Named exceptions

One subsection per row that needs more than a cell.

#### Row A

- **Commit staging.** The commit step flips the readiness checkbox **inside the story index** (`<story_path>`) and stages every changed path with it, so `<task_file>` goes when the implementer changed it — appended `**Deviations from plan:**` notes, say. With `<per_unit_review>` `on`, it also stages the unit's findings folder (`<per_task_findings_root>task_<K>/`), passed as `--findings` per step 5.
- **Progress line.** After the commit call prints `commit_sha:`, emit one progress line: `Task N committed: <sha> <subject>`. **Do not pause for input.** (This is step 6's progress line with row `A`'s `Heartbeat unit label` substituted.) The source loop writes `N` here while deriving the same number as `K` in its pick step — one number, two letters. Both spellings are carried across **verbatim** (`Task <K>` in the label cell, `Task N` in this line and in the review step's non-convergence message) rather than harmonised, because the emitted text is observable run output. Do not "fix" either one into the other.

#### Rows A1.5.3 / A2.3 / C2.4 — the index-agnostic `review_item` commit

**Row `A1.5.3` only — skip this row unless `phases.parity` is `true` in `devscene.config.json`.** Rows `A2.3` and `C2.4` are not phase-gated.

Stated once here and cited by all three rows: the commit step's `--unit review_item` is **index-agnostic** — it flips the `**Finding K**` entry its `--id <K>` names inside whatever index's `## Phase 2 Readiness — Ordered Fix List` is passed as `--plan`, so the parity / architecture / skeptic index works **unmodified**; each carries the byte-identical readiness heading. It stages the fix code + that index together. (The same property is what lets rows `C`, `E.3` and `G.4` pass their own indices.)

#### Row C — the finding folder mirrors the index round suffix

`<finding_file>` lives in the folder that mirrors the code-review index's round suffix: `<branch>_code_review_2/` for round 2. Resolve it through `<code_review_findings_dir>`, never as a round-1 literal.

#### Row E.3 — QA fixes

- **Phase gate.** Skip this row unless `phases.qa` is `true` in `devscene.config.json`.
- **Readiness source.** The **merged** round index the calling phase assembled (`<qa_review_findings_dir>qa_review_<iteration>.md`, iteration `0`, in the round-suffixed folder on re-test rounds). Read **only this merged index** — **not** a qa-tester per-dispatch index (`qa_review_<iteration>_t<T>.md`), and not the finding files. Fragmenting the readiness list across per-dispatch indices breaks step 1's single-source rule.
- **Round-suffix mirroring on both QA folders.** `<qa_review_findings_dir>` and `<qa_fix_findings_root>` both mirror the round suffix on re-test rounds. Always resolve them through the placeholders — a literal `…_qa_review/item_<N>/` silently defeats both the re-test suffix and the entry-core divergence in the `Placeholder owner` footnote.
- **Namespaced finding files.** The qa-tester namespaces per-finding files by test id (`finding_t<T>_<M>.md`); the merged index's pointer names the exact file. Take the file from the pointer; do not reconstruct the name.
- **Layer tag.** The `_(layer: …)_` tag on each merged entry was **carried through verbatim by the merge** — the calling phase copies the qa-tester's tag, it does not re-derive it. Route off that tag (step 2) and never open the finding body to determine the layer.
- **Fix target.** A real QA defect is an **app bug**, so the fix target points at one of the `layers[]` rows covering app code, or at the catch-all layer whose `path` is `"."` for workflow; the layer tag names that target.
- **Heartbeat.** Unit label `Finding <N>`, layer label = the finding's layer: `[E · Finding 2 · presentation · iter 0] → layer-implementer  (#N)`.
- **"Apply the safety contract before every implementer / reviewer dispatch."** This sentence of the source loop is **covered by `## The unit loop`'s pre-dispatch rule**, which states it for **every** row. It is not an `E.3` delta — `E.3` is simply the one loop that spelled it out. Nothing was lost in the move.

#### Row UR-A — user-review fix items

- **Severity is noted at pick time.** Step 1 additionally notes **which severity section** the finding's `### K. <title>` pointer sits under in the index — `## Must Fix` / `## Should Fix` / `## Nice to Have`. That is what the `--prefix` decision below reads at step 5; nothing else in the loop uses it.
- **`--prefix` on the Should Fix arm only.** The wrapper computes the prefix by severity: `## Must Fix` → `fix`, `## Nice to Have` → `chore`, and on neither does step 5 pass `--prefix`. On a `## Should Fix` entry step 5 passes `--prefix refactor` if the finding's nature is a code-structure / architecture change, `--prefix chore` otherwise (style / docs / workflow / small polish); **to decide structure-vs-polish read only the first paragraph of `<finding_file>` — do not re-read the whole body.** That read is the one **narrow, deliberate exception** to this row's never-open-the-detail-file discipline and is scoped to this single decision: routing still comes from the readiness entry's `_(layer: …)_` tag (step 2), never from the detail file.
- **Commit staging.** `--plan <fix_plan_path>` is the fix-plan **index** — the commit step flips the matching `[ ]`→`[x]` readiness entry **inside the index** and stages every changed path with it, so the per-finding `finding_<K>.md` goes when the implementer changed it. With `<per_unit_review>` `on`, it also stages the unit's findings folder (`<per_item_findings_root>item_<K>/`), passed as `--findings` per step 5.
- **`--id <K>`.** This row passes `--id <K>`, the `**Finding K**` number, **with** `--unit review_item`, as every row does — see the ⚠️ note under the substitution table.
- **Item numbering — `K`, not the walk position.** `<K>` in this row's `Detail file`, `Per-item findings folder` and `Heartbeat unit label` cells is the `**Finding K**` number carried on the readiness entry (the source loop's `item_number`), so step 1's `item_<N>` walk-position rule does **not** key this row's findings folder.
- **Progress line.** After the commit call prints `commit_sha:`, emit one progress line: `Item N committed: <sha> <subject>`. **Do not pause for input.** (This is step 6's progress line with this row's `Heartbeat unit label` substituted. The source loop writes `N` here while deriving the same number as `K` in its pick step — one number, two letters, both spellings carried across **verbatim** rather than harmonised, exactly as row `A`'s exception records for `Task <K>` / `Task N`.)
- **Review-step wording delta.** In `### Per-unit review step`, this row's parenthetical reads: **`<finding_file>` is the reviewer's ground truth.** The rest of that step — the fenced block, the no-`mkdir -p` note, the verdict parse and the `iteration >= 5` cap — is the shared body, unchanged.
- **Review prompt first line.** `Review the in-progress task.` is this loop's own wording at branch point, even though its unit is a review item; it is carried verbatim rather than aligned with the fix rows' `Review the in-progress review item.` Do not "fix" it — the string is the reviewer's dispatch contract.

#### Row G.4 — test-fix items

- **A new index each round.** Each Run gates round writes its own test fix plan index and finding folder, so this row resolves both, and its per-item findings folder, through `<test_fix_plan_path>`, `<test_fix_findings_dir>` and `<test_fix_findings_root>` — never as a literal path.
- **Index writer.** The index and its finding files are written by `test-fix-plan-writer`.
- **A finding an earlier unit's fix already cleared.** The unit may run its finding's named test file(s) (`## The test-run rule` point 1) and close on an `outcome` of `already passing` (`### The dispositioned outcome` → `#### The already-passing close`).

#### Shared — multi-layer fixes run bottom-up

If a fix touches multiple layers, run them in the order the tag lists them, which the tag's author writes **bottom-up** — the catch-all layer (`path: "."`) last. The tag's order is authoritative; never re-sort it against a remembered layer list. This applies to `**Finding K**` / `**Test K**` entries only — story-plan `**Task K**` entries are single-layer (`## Layer routing table`).

#### The fix rows — `fix`

The wrapper prefixes every fix row's commit `fix`; step 5 passes no `--prefix` on any of them.
