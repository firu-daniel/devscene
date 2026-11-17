### Task 6 — Teach `conventions-reviewer` the `sweep` target and the regex-grounding check

**Goal:** Let the single `pass: document` review of the sweep document run every row's regex against the code it covers. A regex that matches nothing there, matches nearly every line, or does not compile is a finding. So is a row the script cannot parse.

**Depends on:** Task 5, which defines what `conventions-writer` emits on `target: sweep` (`plugin/agents/conventions-writer.md` → `## The sweep document`). The rows sit in the one table under the exact heading `## Sweep rows`, whose header row is exactly `| Escape class | Regex | Covers | Exempts | A hit is a candidate for |`. `Regex` is one backtick code span holding a `grep -E` pattern, in which `\|` stands for `|`. `Covers` is code-spanned repo-relative paths separated by `, `, and `Exempts` is the same or `—`. This reviewer reads that section of the writer's contract, as it already reads `## Scope`, `## The document`, `## The fix dispatch` and `## House rules`, so the strings come from the writer rather than from memory.

**Where this task stops.** When the dispatch is sent is **Task 7's**. This task changes no return field: findings on `target: sweep` are ordinary `document_reviewed` findings (`claim`, `evidence`, `correction`), so `plugin/schemas/conventions-reviewer.return.json` is unchanged. The sweep document is never a `pass: corpus` member, so the corpus checks `C1`–`C6` never see it.

### Targets

- `plugin/agents/conventions-reviewer.md`

**Work:**

- [ ] `## Resolved values` → the `<layer_names>` row: on `pass: document`, `target` may also be `sweep`. In the opening paragraph's "Read `${CLAUDE_PLUGIN_ROOT}/agents/conventions-writer.md` before you grade" sentence, add `## The sweep document` to the sections read.
- [ ] `## Invocation contract` → the `pass: document` table's `target` row: add `sweep` for `.claude/review-sweep.md`. Add one sentence that `sweep` is never a `corpus_documents` member's `target`, so the corpus `target` paragraph's three values stand unchanged.
- [ ] `## What to verify`: add check **16. Every sweep row is grounded** — `target: sweep` only. For each row of the table under `## Sweep rows`:
  - **Format.** It must parse in the writer's stated format: five cells, `Regex` exactly one code span, a non-empty `Covers`, and `Exempts` paths or `—`. A row that does not is the finding.
  - **Run.** From `<repo_root>`, run `git grep -c -E -e '<regex with each \| turned into |>' -- <each Covers path> <each excluded_paths entry as ':(exclude)<path>'>`. `Exempts` stays **inside** the count, because the owner sites are where the construct legitimately lives.
  - **Findings:** grep exits 2, so the regex does not compile; zero matching lines across the covered paths, so the regex matches nothing there; or matching lines above one half of the non-blank lines in the same paths (`git grep -c -E -e '[^[:space:]]'` over the same pathspec), so it matches nearly every line and cannot be a lead.
  - **Corrections, concrete:** re-derive the regex from a real occurrence the evidence names; or drop the row and record the class in `## Not determined` with what would settle it.
- [ ] State, beside check (16), which of checks (1)–(15) run on `target: sweep` and which do not. This restates the exceptions the writer's `## The sweep document` defines (Task 5), so the two files agree:
  - **Run:** (1), (2), (3), (7), (8), (10), (11), (14) and (15), with these readings:
    - **(1) runs without its example clause.** The writer's `## The sweep document` states that this target carries no example, because the skeleton has no generic example and its worked examples are removed with the `**What belongs here**` guidance. Every other clause of (1) holds: banner, no `<!-- devscene:unfilled -->`, provenance line, `## Not determined`. Its `prior_prompts` clause is answered by the rows under `## Sweep rows`, plus a `## Not determined` line for each class looked for and not settled.
    - **(2)** grades the rule block as the writer's section bounds it: between the `**What belongs here**` guidance and `## Sweep rows`.
    - **(3)**: the provenance is the conventions document and heading the class came from.
  - **Do not run:** (4), because the sweep document carries no harvested rule; (5), because the sweep document has **no `demand_set` scope of its own**, the reason Task 5's section states (the caller still sends `demand_set`, and this target ignores it); (6), because it names no concept of its own; (9), because a row is a pattern rather than prose about the present code; (12) and (13), because it binds no actor and states no process.

  One line per check, giving each its reason once.
- [ ] Frontmatter `description:`: name that a document-pass dispatch may review the review-sweep document. No other edit there.

**Verification:**

- `git grep -n -E '^16\. ' -- plugin/agents/conventions-reviewer.md` resolves to the new check.
- `git grep -n -F '## The sweep document' -- plugin/agents/conventions-reviewer.md plugin/agents/conventions-writer.md` resolves in both files. The reviewer cites the heading Task 5 created.
- `plugin/schemas/conventions-reviewer.return.json` is unchanged from `dev`.
