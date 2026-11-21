### Task 1 — Pass `diff_base: origin/<default_branch>` to the parity and architecture reviewers

**Goal:** The two implemented-solution reviewers receive their diff base from the orchestrator's dispatch block. Make that block pass `origin/<default_branch>`, and move the quoted copies in both receiving agents with it in the same commit, so the four blocks stay byte-identical.

**Where this task stops.** This task owns the `diff_base` wire only: the two dispatch blocks in the core, the two quoted copies, the two agents' `<default_branch>` and `diff_base` rows, and the core's `<default_branch>` row. The reviewers that compute their own `git diff <default_branch>...HEAD` without a `diff_base` argument (`branch-reviewer`, `skeptic-reviewer`, `review-plan-reviewer`) belong to **Task 2**. The commit ranges, the docs-phase diff and the flow document belong to **Task 3**. The static check over all of them belongs to **Task 4**, which reads the text this task writes. That includes the exact fallback sentence and the absence of any bare `diff_base: <default_branch>`.

### Targets

- `plugin/instructions/plan_orchestration_instructions_core.md`
- `plugin/agents/architecture-reviewer.md`
- `plugin/agents/business-parity-reviewer.md`

**Work:**

- [ ] `plan_orchestration_instructions_core.md` → `### A1.5.1 Generate the parity review` and `### A2.1 Generate the architecture review`: in each dispatch block, change the line `diff_base: <default_branch>` to `diff_base: origin/<default_branch>`. Change nothing else in either block.
- [ ] `plan_orchestration_instructions_core.md` → `## Resolved values`, `<default_branch>` row: say that the diff base the implemented-solution reviewers compute against is the **remote-tracking** ref `origin/<default_branch>`, the same ref the `### D.2 Done summary` delivery bullet counts from. Then add the freshness statement once, in this row only: no step of this flow fetches for that ref. A three-dot diff against a stale `origin/<default_branch>` still starts at the branch's fork point. It widens only when the branch merged a `<default_branch>` commit the ref does not carry, which `refresh-branch.sh`'s default mode cannot cause because it fetches `origin/<base>` before merging. Keep "Never a remembered branch name."
- [ ] `architecture-reviewer.md`:
  - `### Implemented-solution mode (insertion point 2)`: change the quoted block's first line to `diff_base: origin/<default_branch>`, byte-identical to the core's A2.1 block. Append the fallback sentence (story index `## Context`, quoted there) verbatim to the `diff_base` key row, after *"never a remembered default."*
  - `## Resolved values` → `<default_branch>` row: replace *"so the diff base of every `git diff` in this file"* with a statement that the caller passes `diff_base` as the remote-tracking ref `origin/<default_branch>`.
- [ ] `business-parity-reviewer.md`: the same three edits, the quoted block matching the core's A1.5.1 block byte for byte. Word the `<default_branch>` row and the `diff_base` row identically to `architecture-reviewer.md`'s new rows (`.claude/context/plugin.md` → `## Writing agent prose`, *"A block several agents carry is one wording, copied byte-for-byte"*).

**Verification:**

- `git grep -nE 'diff_base: ' -- plugin`: every hit reads `diff_base: origin/<default_branch>`, apart from `<diff_base>` placeholder uses and the `plugin/agents/README.txt` historical note.
- Each of the two quoted blocks is byte-identical, line for line, to the core block it names (`plugin/agents/README.txt` → *"Port-time corrections"*). Read each pair side by side.
- `git grep -nF "re-issue that command once with \`<default_branch>\` in its place and say which base you used." -- plugin/agents/architecture-reviewer.md plugin/agents/business-parity-reviewer.md` hits both files.
- `git grep -nE '(^|[^/])<default_branch>\.\.\.?HEAD' -- plugin/instructions/plan_orchestration_instructions_core.md`: the only hit is the `### D.2 Done summary` fallback `git rev-list --count <default_branch>..HEAD`, which this task does not touch.
