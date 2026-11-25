### Task 9 — Record the retirement in the flow-graph decision record, the watcher's script table and the roadmap

**Goal:** Bring three documents in line with this branch's outcome:
- the flow-graph decision record states the retirement;
- the watcher's shipped-scripts table lists the one graph `init` ships;
- the roadmap's GraphScene row moves the format-4 cutover from **Left** to shipped.

The decision record keeps its earlier decisions, and records what this branch changed as dated **Changed** paragraphs.

**Depends on:** Tasks 1, 5, 6 and 7.
- **Task 1** ships one planning graph, `<scriptsDir>/flows/task_plan_writing.graph.json`, in format 4. `devscene-flow-walker` walks it, and `lib/planning-node-lib.sh` and `lib/planning-driver-lib.sh` read it for its node list.
- **Task 5** makes `devscene-flow-walker` find it as `<flows>/<flow>.graph.json` (`devscene_flow_host.commands.flow_walker.GRAPH_SUFFIX`).
- **Task 6** holds the cap, findings-folder, run-mode and ledger agreement in `devscene-flow-host/tests/core_agreement.py` → `core_agreement_violations`, with its flow-to-core table `CORE_FOR_FLOW`, run by gate 13's leg `13j`.
- **Task 7** deletes `scripts/check-flow-graph.sh`, `scripts/generate-flow-graph-v3.mjs`, `schemas/flow-graph.schema.json` and its fixtures.

This task changes none of their files.

**Decision-record rule.** `docs/flow-graph-walker.md` states decisions of record. A decision whose mechanism this branch moved gets a **Changed** paragraph below the existing ones in its item, in the form the file already uses: `**Changed <date> (#459).**`, dated the day this task lands. #459 is the issue that `cli/src/generators/outerLoopScripts.ts`'s retired row and the existing *Format 4* **Changed** paragraph already give this retirement. Its **Decision**, **Reason** and **Cost** text stays as decided. Headings are cited anchors (`ROADMAP.md` and `docs/development.md` cite *Format 4*), so no heading changes. Items 7 and 8, and `## 3. Four findings established rather than assumed`, are records of what was true then, and stay untouched (story index → `## Scope register`, rows 14 and 17). The roadmap edit records only what shipped. It does not change the row's status cell, or decide that the GraphScene item is done (`harness-runs/lessons.md` → *"A decision rule's outcome is a proposal to the maintainer"*).

### Targets

- `docs/flow-graph-walker.md` — the opening **What it owns.** paragraph; `### Item 2` → **Cost.**; `### Item 6`; `### The iteration cap` → **Cost, and how it is guarded.**; `### Format 4`; and `## 4. What a second flow would need before it adopts the walker`, the *"its own graph"* bullet.
- `docs/watcher.md` — the shipped-scripts table's two `flows/…` rows.
- `ROADMAP.md` — `## Scene products`, the GraphScene row.

**Work:**

- [ ] **`docs/flow-graph-walker.md`, the live text.** These three passages describe the present, so edit them in place:
  - **What it owns.** names the graph's shape as `graphscene/src/graphscene/schemas/flow-graph.schema.json` alone. It names the static checks as `graphscene.static_violations` plus `devscene-flow-host/tests/core_agreement.py` → `core_agreement_violations`, in place of `scripts/check-flow-graph.sh` → `THE CONTRACT`.
  - Item 2's **Cost.** says the findings-folder duplication is held by `core_agreement_violations` → `findings-folder-in-core`.
  - In `## 4`, the *"its own graph"* bullet asks for a flow-id row in `devscene-flow-host/tests/core_agreement.py` → `CORE_FOR_FLOW`.
- [ ] **`docs/flow-graph-walker.md`, the dated records.** Add a `**Changed <date> (#459).**` paragraph after the last existing one in three places:
  - **Item 6:** the graph now ships as `flows/task_plan_writing.graph.json`, the one graph under `flows/`, and the walker finds `<flows>/<flow>.graph.json`.
  - **The iteration cap:** `cap-matches-core` is now `core_agreement_violations`, run in gate 13's leg `13j`, and changing the cap is the graph's `counters.iteration.cap` plus both core sentences, with no regeneration step.
  - **Format 4:** the generated format-3 copies, their generator, the format-3 schema and its fixtures, `scripts/check-flow-graph.sh` and gate legs `3c`–`3f` and `3i` are retired. The format-4 graph ships under the shipped name. Checks 4–7 moved to the flow host's test checker, while 1–3, 8 and 9 run as `graphscene.static_violations`. `init` removes no file it stopped shipping.
- [ ] **`docs/watcher.md`.** Replace the two rows `flows/task_plan_writing.graph.json` (*"format-3 flow graph, which no walker reads"*) and `flows/task_plan_writing.v4.graph.json` with one row, `flows/task_plan_writing.graph.json`. It carries the planning loop's flow graph — its nodes, their outcomes, the `iteration` counter and its cap, the escalation payloads. Two readers use it: `flow-walker.sh`'s hand-off, which passes its directory to `devscene-flow-walker` as `--flows`, and `lib/planning-node-lib.sh` and `lib/planning-driver-lib.sh`, which read its node list. It is never executed, and its agent-invocable cell is `no`, as both old rows had.
- [ ] **`ROADMAP.md`, the GraphScene row.**
  - The shipped clause *"the harness's planning graph authored in it and its format-3 copy generated from it"* becomes the harness's planning graph authored in it and shipped as the one planning graph `init` writes, with checks 4–7 held by the host's test checker.
  - The **Left:** clause drops *"and the format-4 cutover — the walker and the format-3 readers moving to format 4, and the generated copy and its generator retired"*.
  - Leave *"the walker's port onto the engine"* and the status cell unchanged.

**Verification:**

- Run the story index's `## Scope register` derivation entry A pattern in its line form, `git grep -n -E 'v4\.graph\.json|check-flow-graph|generate-flow-graph-v3|schemas/flow-graph\.schema\.json|flow-graph-check|validate:flow-graph|flow-graph-schema-|format-3|format 3|no walker reads' -- docs/flow-graph-walker.md docs/watcher.md ROADMAP.md`. It prints no line of `docs/watcher.md` or `ROADMAP.md`. In `docs/flow-graph-walker.md`, every line it prints falls inside one of the sites this task's own Work and Decision-record rule leave in place, and nowhere else:
  - **What it owns.** — only for the format-4 schema path `graphscene/src/graphscene/schemas/flow-graph.schema.json`, which the new text names and which matches `schemas/flow-graph\.schema\.json` as a substring;
  - `### Item 6` — the kept **Decision.** (`flows/task_plan_writing.v4.graph.json`), the kept `**Changed 2026-11-25 (#419).**` (*"format-3 graph"*) and the new `**Changed <date> (#459).**`;
  - `### Item 7` and `### Item 8` — register row 14, untouched;
  - `### The iteration cap` — the kept **Cost, and how it is guarded.** (`scripts/check-flow-graph.sh`) and the new **Changed** paragraph;
  - `### Format 4` — the kept heading (*"format 3 is generated from it"*), the kept **Decision.** (`task_plan_writing.v4.graph.json`), the kept **Cost.** (*"format-3 readers"*), the kept `**Changed 2026-11-25 (#419).**` and the new **Changed** paragraph;
  - `## 3. Four findings established rather than assumed` — register row 17, untouched.

  In particular, it prints no line of Item 2's **Cost.** or of `## 4`'s *"its own graph"* bullet, and no `scripts/check-flow-graph.sh` in **What it owns.**. Those are the three passages the Work edits in place.
- `git grep -n -e 'v4\.graph\.json' -e 'format-3' -- docs/watcher.md ROADMAP.md` prints nothing.
- `git diff -- docs/flow-graph-walker.md` changes no `### ` or `## ` heading line, and removes no **Decision.**, **Reason.** or earlier **Changed** paragraph.
- Each path and symbol the new text cites exists: `devscene-flow-host/tests/core_agreement.py` (`core_agreement_violations`, `CORE_FOR_FLOW`), `cli/templates/scripts/flows/task_plan_writing.graph.json` and `devscene-flow-host/src/devscene_flow_host/commands/flow_walker.py` (`GRAPH_SUFFIX`).
