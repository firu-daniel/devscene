### Task 6 — Record the five agents' outcomes in the decision record, state the every-agent rule, and close the roadmap row

**Goal:** `docs/structured-agent-returns.md` records the outcome decisions this branch took for `qa-tester`, its two mobile stubs, `docs-writer` and `docs-reviewer`, and states the rule Task 5 put in force — every agent definition has a return schema — in place of every "adopt one at a time" sentence. `ROADMAP.md` marks **Structured agent outputs** done, pointing at the decision record, and drops it from the index of outstanding work.

**Depends on:** Task 5, which made `cli/test/agent-return-schemas.test.mjs` fail an agent definition with no `plugin/schemas/<agent>.return.json`, and through it Tasks 1–4, which defined the outcomes recorded here:

- `qa-tester`: `PASS`; `FAIL` with `findings_file` and `must_fix_count` (at least 0); `blocked` with `blocked_tests`, object items `test_id` (integer, at least 1) and `cause`; `blocker` with `blocker`.
- `qa-tester-mobile-maestro`, `qa-tester-mobile-mcp`: `blocker` with `blocker`, alone.
- `docs-writer`: `written` with `doc_path` and the optional `unverified`, `parity_gaps`, `notes`; `targets` with `targets`, object items `action` (`enum` `new` / `update`), `slug`, `output_path`, `reason`, `entry_hints`; `targets_none` with `reason`; `phase_disabled` with `reason`; `blocker` with `blocker`.
- `docs-reviewer`: `PASS` and `FAIL`, each with `findings_file`, `summary` and the optional `missed_docs`; `phase_disabled` with `reason`; `blocker` with `blocker`.

This is the **catch-all** task, so it reads every configured layer's conventions document: it records what the `plugin` tasks decided and what the `cli` task enforces. It changes nothing in either layer, and adds nothing to `## 3. Measured, and not yet measured`: the change relies on no fact about the `Agent` result or a `result` event that section does not already record.

### Targets

- `docs/structured-agent-returns.md` — the `**Who reads this:**` paragraph; `### The schema lives in its own file inside the plugin`'s **Cost.** sentence listing what the suite fails; one paragraph appended to each of `### A list of structured items is an array of objects, one level deep`, `### One discriminator, `outcome`, held to the graph` and `### An agent's own `error:` return becomes an outcome, never `error``, plus that last section's **Cost.** sentence; and `### Adopting it for another agent`'s closing paragraph.
- `ROADMAP.md` — the `Structured agent outputs` row under `## Quality and testing`, and the `## Index` table.

**Work:**

- [ ] **The decision record's audience and the rule in force.**
  - `**Who reads this:**` — *"a maintainer changing an agent's return, and the author of `feat_structured_outputs_remaining_agents` (#380; `ROADMAP.md` → the `Structured agent outputs` row), who adopts the mechanism for the agents that do not carry it yet."* becomes *"a maintainer changing an agent's return or adding an agent."* Keep the next paragraph.
  - `### The schema lives in its own file inside the plugin` → **Cost.** — *"it also fails a definition that re-inlines a schema and a schema file with no agent"* gains *"and an agent with no schema file"*.
  - `### Adopting it for another agent`, the closing paragraph — *"An agent with no `plugin/schemas/<agent>.return.json` is outside every check until it gains one, so agents adopt one at a time."* becomes *"Every agent definition under `plugin/agents/` has a `plugin/schemas/<agent>.return.json`: `cli/test/agent-return-schemas.test.mjs` fails one that does not, so a new agent lands with its schema file and the steps above."* Keep the paragraph's list of what the suite holds an agent to. Drop *"That work is #380's (`ROADMAP.md` → the `Structured agent outputs` row)."*
- [ ] **The two object-item lists, under `### A list of structured items is an array of objects, one level deep`.** Append a paragraph **The docs and QA agents, `feat_structured_outputs_docs_qa`.**: `docs-writer.targets` — `action` (`enum` `new` / `update`), `slug`, `output_path`, `reason` and `entry_hints`, replacing the survey's `action(new|update) · slug · output_path · reason · entry-hints` line, a delimited string per item this decision rejects; and `qa-tester.blocked_tests` — `test_id` (integer) and `cause`, one item in per-single-test mode and one per blocked test in the full-run mode, replacing `error: blocked — test <T>: <cause>` and `tests <ids>: <causes>`.
- [ ] **The outcomes, under `### One discriminator, `outcome`, held to the graph`.** Append a paragraph **The docs and QA agents, `feat_structured_outputs_docs_qa`.**:
  - None of the five is dispatched by the planning graph, so the section's cost applies to all five.
  - `docs-writer`'s outcomes name what it produced — `written`, `targets`, `targets_none` (the former `targets: none`, its words kept and its spacing dropped);
  - both docs agents take `phase_disabled` for a dispatch with `phases.docs` off. For `docs-reviewer` that replaces *"`verdict: PASS` plus one line … and no `findings_file:`"*: the consts are distinct across variants and `PASS` carries a required `findings_file`, so a disabled `PASS` could not be a second variant. The alternative weighed was `findings_file` optional on `PASS`, declined because a real `PASS` with no findings file would then pass the check.
  - **Deviations from plan:** The plan quotes the retired `docs-reviewer` line as *"… and no `findings_file:`"*; the source (`git grep -n 'verdict: PASS. plus one line' 0ddc2e45~1 -- plugin` → `plugin/agents/docs-reviewer.md`) reads *"…, and omit `findings_file:` entirely"*. The record quotes it as *"`verdict: PASS` plus one line … and omit `findings_file:`"*.
- [ ] **The renamed `error:` returns, under `### An agent's own `error:` return becomes an outcome, never `error``.**
  - Append a paragraph **`feat_structured_outputs_docs_qa` decided it for `qa-tester`.**: its `error: blocked — test <T>: <cause>` return, which every caller treats as non-halting, became the outcome `blocked` — the old literal's word, as the rule's carry-over states — with its causes in `blocked_tests`. Its unmarked `error: <reason>` return, on which every caller halts, became `blocker` with its cause in `blocker`. The two mobile stubs, which return only the latter, carry the `blocker` variant alone, with the same field name, so their schemas are a subset of `qa-tester`'s. Every `qa-tester` dispatch site names its halt arm as its own `error` route, so a third failing return halts as a `blocker` does and never reads as a blocked test. The docs pair's `blocker:` lines became `blocker`.
  - The section's **Cost.** — *"A caller that today matches a prefix such as `error: blocked — ` must route on a new outcome instead, in the same change as that agent's schema."* becomes *"A caller that matched a prefix such as `error: blocked — ` routes on a new outcome instead, changed in the same change as that agent's schema."*
- [ ] **`ROADMAP.md`.**
  - The `Structured agent outputs` row's status cell becomes `Done`, and its description becomes a statement of what shipped, ending with a pointer: every agent under `plugin/agents/` declares its return in `plugin/schemas/<agent>.return.json` and its callers read fields rather than lines; a new agent without one fails `cli/test/agent-return-schemas.test.mjs`; the mechanism and its decisions are recorded in `docs/structured-agent-returns.md`.
  - Remove the `## Index` row `| 18 | [Structured agent outputs](#quality-and-testing) |` — the index lists outstanding work only — and renumber every row below it down by one, so the priorities stay contiguous from 1, as the closing of `Committer as a script` did.
  - Change no other row.

**Verification:**

- `git grep -nE 'one at a time|outside every check until|#380|remaining_agents' -- docs/structured-agent-returns.md` has no hit.
- `git grep -n 'Structured agent outputs' -- ROADMAP.md` hits only the `## Quality and testing` row, which ends in `| Done |` and names `docs/structured-agent-returns.md`.
- The `## Index` table's first column runs 1, 2, 3, … with no gap and no repeat, and every other row's feature link is unchanged (`git diff -- ROADMAP.md`).
- Every outcome and field the record names for the five agents matches the five schema files (`jq '.oneOf[] | .properties.outcome.const' plugin/schemas/qa-tester.return.json` and its siblings).
- `### The return block`'s fenced canonical sentence and every heading of the decision record are byte-identical to before (`git diff -- docs/structured-agent-returns.md`), since other files cite them.
