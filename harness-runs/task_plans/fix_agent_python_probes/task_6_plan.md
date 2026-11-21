### Task 6 — Give `branch-reviewer`, `skeptic-reviewer` and `review-plan-reviewer` the probe route

**Goal:** Tell the three end-of-branch reviewers that a probe route exists, so they reproduce a finding by running it rather than reaching for an interpreter the profile refuses. Make every sentence that bounds what each one writes admit the probe file.

**Depends on:** Task 5, which creates `${CLAUDE_PLUGIN_ROOT}/instructions/probe_route.md` with the headings `## The route` and `## A confirmation you did not execute`, and already lists these three agents in its `## Who may cite this` roster. This task cites those two headings byte-for-byte and edits neither the module nor `layer-reviewer.md`. The pointer paragraph to copy, byte-for-byte as Task 5 writes it into `layer-reviewer.md`, is:

> `**Run the probe that would settle it**, by \`${CLAUDE_PLUGIN_ROOT}/instructions/probe_route.md\` → \`## The route\`. **A probe reads and computes; it never writes into the tree under review.** A probe the tool layer moves to the background is not waited on (\`${CLAUDE_PLUGIN_ROOT}/instructions/unit_loop_core.md\` → \`## The test-run rule\` point 6), and a finding resting on it is disclosed under the rule below.`
>
> `**Disclose a confirmation you did not execute**, by \`${CLAUDE_PLUGIN_ROOT}/instructions/probe_route.md\` → \`## A confirmation you did not execute\`. \`finding_grades.md\` and \`### Must Fix triggers\` alone set severity.`

The one word-level difference from `layer-reviewer.md` is the trigger list each agent grades by: `### Must Fix triggers` here, `## Checklist` there (`.claude/context/plugin.md` → `## Writing agent prose`, *"where copies differ only in a word, keep the difference and nothing else"*). All three agents are already on `${CLAUDE_PLUGIN_ROOT}/instructions/unit_loop_core.md` → `## The test-run rule`'s roster, so the point-6 citation needs no roster edit.

### Targets

- `plugin/agents/branch-reviewer.md`
- `plugin/agents/skeptic-reviewer.md`
- `plugin/agents/review-plan-reviewer.md`

**Work:**

- [ ] **The clause every write-bounding sentence takes**, byte-identical at each site: `, a probe file under \`<state_dir>/scratch/\` excepted`. That directory is gitignored by its contents (`scripts/scratch-run.sh` → *THE RUN MUST NEVER SEE A FILE FROM HERE IN A COMMIT*), so the clean tree a `PASS` leaves, which the orchestrator relies on, still holds.
- [ ] **`branch-reviewer.md`.** Append the clause to line 10's *"The only files you write are the review index and its per-finding files."* Insert the two pointer paragraphs at the end of `### Pass 1 — Independent review (always)`, after step 7 and before `### Pass 0 — the deterministic sweep`.
- [ ] **`skeptic-reviewer.md`.** Append the clause to line 10's *"The only files you write are your own review index and its per-finding files."*, to `## Invocation contract`'s *"The PASS branch of `## Output contract` must not touch disk."*, and to `### 1. No net-new findings — \`PASS\``'s *"do not write any file"*. Insert the two pointer paragraphs at the end of `## Process`, after step 4 and before `## Adversarial checks (your high-yield scope)`.
- [ ] **`review-plan-reviewer.md`.** Append the clause to line 10's *"The only file you write is your own findings file."*, to `## Invocation contract`'s *"The PASS branch of `## Output contract` must not touch disk."*, and to `## Output contract`'s *"Do not save a file when PASS."* Insert the two pointer paragraphs at the end of `## Process`, after step 4 and before `## What to check`.

**Verification:**

- `grep -n 'probe_route.md' plugin/agents/branch-reviewer.md plugin/agents/skeptic-reviewer.md plugin/agents/review-plan-reviewer.md` shows two citations per file, and the two pointer paragraphs are byte-identical across the three files and to `layer-reviewer.md`'s, apart from `### Must Fix triggers` in place of `## Checklist`.
- `grep -n 'touch disk\|do not write any file\|Do not save a file\|The only file' plugin/agents/skeptic-reviewer.md plugin/agents/review-plan-reviewer.md plugin/agents/branch-reviewer.md`: every hit carries the clause, so no sentence left in these files forbids the probe file the route writes.
- Each file's frontmatter, `tools:` allowlist and `## Output contract` return fields are unchanged.
