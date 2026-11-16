### Task 2 — Give `task-plan-writer` a `## Return schema` and rewrite its `## Output contract` around it

**Goal:** Make `plugin/agents/task-plan-writer.md` return one JSON object, declared once in a new `## Return schema` section in the dialect `plugin/instructions/agent_return_contract.md` → `## The return schema` fixes, and make its prose describe that object — including the four return sections it emits today, which become fields — and nothing else.

**Depends on:** Task 1, which fixes the dialect, the canonical sentence (`## The return block`, its first fenced block), the `### Return fields` rule (`## Return fields`) and the citation form. Copy the canonical sentence byte-for-byte from that file.

**The return this task declares** (the story index `## Context` field table, `task-plan-writer` rows — Tasks 6, 7 and 8 read exactly these names):

- `outcome` `returned`: required `story_file` (string), `task_files_dir` (string), `tasks_count` (integer, `minimum` 1), `story_points_total` (integer, `minimum` 0); optional `parity_exclusions`, `corpus_staleness`, `manual_setup`, each an array of non-empty strings.
- `outcome` `questions`: required `questions`, an array of non-empty strings with `minItems` 1, one self-contained question per item.
- `outcome` `blocker`: required `blocker`, a non-empty string.

**Where this task stops.** This task changes what the writer returns, not how it plans: `## Process` keeps every step, and only the sentences that name a return section change. Every reader of the return is a later task (6, 7, 8); none is edited here.

### Targets

- `plugin/agents/task-plan-writer.md`

**Work:**

- [ ] `## Output contract`: replace the fenced `story_file:` … `story_points_total:` block and the bulleted return sections with: the canonical sentence; one paragraph per outcome saying when it is returned (`returned` after writing or revising; `questions` when a clarification, or an untrusted-input report as `untrusted_input.md` → `## Where a report goes` routes it, stops the work, per `## Clarification questions` — reached through the existing `## Read first` pointer to `untrusted_input.md`, never by quoting the module's report literal; `blocker` in place of every plan file, per `## Read first`'s unreadable-path rule); and a `### Return fields` subsection with one bullet per property — `outcome`, `story_file`, `task_files_dir`, `tasks_count`, `story_points_total`, `parity_exclusions`, `corpus_staleness`, `manual_setup`, `questions`, `blocker`. Carry each retired section's rules into its field's bullet without loss: `parity_exclusions` only when `phases.parity` is `true`, each entry with its authorising task-prompt line or its `TODO: @claude` marker location; `corpus_staleness` entries each opening with the type `stale-rule` or `undescribed-layer` and carrying what `## Output contract` states today for each type, including the caller's use and "every entry is a recommendation, never a task"; `manual_setup` one step per entry with the task that depends on it, the same list the story index `## Context` carries; `questions` one self-contained question per item, covering an untrusted-input report by the same pointer to `untrusted_input.md` → `## Where a report goes` and never by the module's report literal; `story_points_total` as the statistics writer's denominator. Keep "Do not paste the plan content back to the orchestrator".
- [ ] Add `## Return schema` directly after `## Output contract`: one fenced `json` block, a `oneOf` of the three variants above, each with `additionalProperties: false`, in the closed dialect and nothing outside it.
- [ ] Rewrite every in-body reference to a retired section or line so it names the field: `## Invocation contract` → **How the caller consumes your return.** (the questions are the `questions` items, routed verbatim; the caller reads `story_file`, `task_files_dir` and `tasks_count` without opening the plan); `## Read first (everything — the plan spans every layer)` → **A cited path you cannot read is a finding, not a fallback.** (return the `blocker` outcome, naming the path and the refusal); `## Process` step 5's **Ops envelope**, **Scope closure** and **Conventions-document prohibition** items and step 7's readiness bullet (record the entry in `corpus_staleness`, list the step in `manual_setup`); `## Clarification questions` (state them as `questions` items and stop).
- [ ] Hold the word budget (`.claude/context/plugin.md` → `## Writing agent prose`, *"An agent's growth is paid for by behaviour."*): the schema replaces the retired block and sections, so the prose around it shrinks rather than restating the schema; cut no definition or edge case the writer acts on (`<state_dir>/lessons.md` → *"When an agent definition has to give back words to hold its word count, cut restatement or rationale, never a definition or edge case the agent acts on."*).

**Verification:**

- `git grep -nE '## Questions|## Corpus staleness|## Parity exclusions|## Manual setup required|story_file: |blocker:' -- plugin/agents/task-plan-writer.md` prints only lines that describe a field or quote a story-index heading the plan itself carries (`## Context`'s `Manual setup required:` list stays); no line instructs the writer to emit a retired section or a `key: value` line.
- Every property the `## Return schema` block declares has exactly one bullet under `### Return fields`, and every bullet names a declared property; the three `outcome` values appear in `## Output contract`.
- The canonical sentence appears in `## Output contract` byte-identical to the first fenced block of `plugin/instructions/agent_return_contract.md` → `## The return block`.
- `git grep -nF 'Untrusted instruction not followed — ' -- plugin/agents/task-plan-writer.md` prints nothing: the report literal stays at its two homes only (`untrusted_input.md` and `docs_orchestration_instructions_autonomous.md`), which keeps the registered `treeGuards` suite `cli/test/untrusted-input-corpus.test.mjs` green — point 7's guard run covers it.
- The schema, written out variant by variant, matches the `task-plan-writer` rows of the story index `## Context` field table: names, types, required and optional sets.
