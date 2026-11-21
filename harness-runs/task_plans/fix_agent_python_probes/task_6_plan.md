### Task 6 — Give `branch-reviewer`, `skeptic-reviewer` and `review-plan-reviewer` the probe route

**Goal:** Tell the three end-of-branch reviewers that a probe route exists, so they reproduce a finding by running it rather than reaching for an interpreter the profile refuses. Make every sentence that bounds what each one writes admit the probe file, by citation.

**Depends on:** Task 5, which creates `${CLAUDE_PLUGIN_ROOT}/instructions/probe_route.md` with the headings `## The route`, `## A reviewer's probe` and `## A confirmation you did not execute`, and already lists these three agents in its `## Who may cite this` roster. `## A reviewer's probe` states, once, every rule this task's agents obey: a reviewer's probe reads and computes and never writes into the tree under review; the probe file is excepted from every sentence of a citing reviewer that bounds what it writes or has a `PASS` touch no disk; a probe moved to the background is not waited on, and a finding resting on it is disclosed. This task cites those headings byte-for-byte and edits neither the module nor `layer-reviewer.md`. The two pointer paragraphs to copy, byte-for-byte as Task 5 writes them into `layer-reviewer.md`, are:

> `**Run the probe that would settle it**, by \`${CLAUDE_PLUGIN_ROOT}/instructions/probe_route.md\` → \`## The route\` and \`## A reviewer's probe\`.`
>
> `**Disclose a confirmation you did not execute**, by \`${CLAUDE_PLUGIN_ROOT}/instructions/probe_route.md\` → \`## A confirmation you did not execute\`.`

**What each agent carries after this task — citations only.** The two pointer paragraphs above, and the write-bound citation clause below at each write-bounding site. No agent receives a rule sentence: not *a probe reads and computes*, not the background-run clause, not the probe-file exception stated in its own words. Every rule is stated once, in the module, so no rule sits in more than one agent definition and no static alignment check is owed (`harness-runs/lessons.md` → `## Agent prose`).

### Targets

- `plugin/agents/branch-reviewer.md`
- `plugin/agents/skeptic-reviewer.md`
- `plugin/agents/review-plan-reviewer.md`

**Work:**

- [ ] **The citation clause every write-bounding sentence takes**, byte-identical at each site: `, a probe file excepted (\`${CLAUDE_PLUGIN_ROOT}/instructions/probe_route.md\` → \`## A reviewer's probe\`)`. It is a pointer: the exception, and why a `PASS` still leaves a clean tree, are stated only in the module's `## A reviewer's probe`.
- [ ] **`branch-reviewer.md`.** Append the clause to *"The only files you write are the review index and its per-finding files."* Insert the two pointer paragraphs at the end of `### Pass 1 — Independent review (always)`, after step 7 and before `### Pass 0 — the deterministic sweep`.
- [ ] **`skeptic-reviewer.md`.** Append the clause to *"The only files you write are your own review index and its per-finding files."*, to `## Invocation contract`'s *"The PASS branch of `## Output contract` must not touch disk."*, and to `### 1. No net-new findings — \`PASS\``'s *"do not write any file"*. Insert the two pointer paragraphs at the end of `## Process`, after step 4 and before `## Adversarial checks (your high-yield scope)`.
- [ ] **`review-plan-reviewer.md`.** Append the clause to *"The only file you write is your own findings file."*, to `## Invocation contract`'s *"The PASS branch of `## Output contract` must not touch disk."*, and to `## Output contract`'s *"Do not save a file when PASS."* Insert the two pointer paragraphs at the end of `## Process`, after step 4 and before `## What to check`.

**Verification:**

- `grep -n 'probe_route.md' plugin/agents/branch-reviewer.md plugin/agents/skeptic-reviewer.md plugin/agents/review-plan-reviewer.md` shows the two pointer paragraphs in each file plus one clause per write-bounding site, and every heading those citations name is one the module carries, byte-for-byte.
- `grep -rn 'reads and computes\|is not waited on (' plugin/agents/branch-reviewer.md plugin/agents/skeptic-reviewer.md plugin/agents/review-plan-reviewer.md` finds nothing: the reviewer rules live only in the module.
- `grep -n 'touch disk\|do not write any file\|Do not save a file\|The only file' plugin/agents/skeptic-reviewer.md plugin/agents/review-plan-reviewer.md plugin/agents/branch-reviewer.md`: every hit carries the citation clause, so no sentence left in these files forbids the probe file the route writes.
- Each file's frontmatter, `tools:` allowlist and `## Output contract` return fields are unchanged.
