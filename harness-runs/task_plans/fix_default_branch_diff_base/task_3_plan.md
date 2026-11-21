### Task 3 — Base the commit ranges, the docs-phase diff and their mentions on `origin/<default_branch>`

**Goal:** Move the two Phase-D commit ranges (`git log … <default_branch>..HEAD`), the docs phase's scoped branch diff, and the prose that names them onto `origin/<default_branch>`. Each command site gets the fallback sentence for an adoption with no `origin` remote.

**Where this task stops.** The reviewer diffs are **Task 1's** (`diff_base`) and **Task 2's** (self-computed). The D.2 delivery count already uses `origin/<default_branch>` and is not touched. **Task 4**'s test holds this task's text to three rules: no bare `<default_branch>..HEAD` or `<default_branch>...HEAD` (the D.2 fallback `git rev-list --count <default_branch>..HEAD` is the one permitted bare form), and the fallback sentence present verbatim in `statistics-plan-writer.md`, `improvement_observations_instructions.md` and `docs_phase_instructions.md`, the three files here that run `git log` or `git diff` against the new base. The sample and the flow document issue no command and owe no fallback sentence.

### Targets

- `plugin/agents/statistics-plan-writer.md`
- `plugin/instructions/improvement_observations_instructions.md`
- `plugin/instructions/docs_phase_instructions.md`
- `plugin/samples/sample_statistics.md`
- `plugin/docs/AUTONOMOUS_FLOW.md`

**Work:**

- [ ] `statistics-plan-writer.md`:
  - `## Resolved values` → `<default_branch>` row: the base of step 1's commit range is now `origin/<default_branch>..HEAD`. Keep the resolve-before-issuing sentence, and append the fallback sentence (story index `## Context`) verbatim.
  - `## Read first` ("commit messages** over …") and `## Process` step 1's `git log --format='%h %s%n%b' <default_branch>..HEAD`: change both to `origin/<default_branch>..HEAD`.
- [ ] `improvement_observations_instructions.md`:
  - `## Resolved values` → `<default_branch>` row: the range's base is the remote-tracking ref `origin/<default_branch>`. Append the fallback sentence verbatim.
  - **(d)** under `## Optimization observations — trip-wires, not reflection` and the `git log … --name-only <default_branch>..HEAD` command under `## Dispositioned units — an entry per unit closed without a fix`: change both to `origin/<default_branch>..HEAD`.
  - The **Bound the set to this run** paragraph: change *"`<default_branch>..HEAD` spans the whole **branch**"* to the new range. Rewrite *"where the local `<default_branch>` ref is behind"* as *"where `origin/<default_branch>` is behind a `<default_branch>` commit the branch merged"*. Keep the rest of that disclosure.
- [ ] `docs_phase_instructions.md`:
  - `## Resolved values` → `<default_branch>` row: the auto-skip rule's diff base is `origin/<default_branch>`. Append the fallback sentence verbatim.
  - `## Auto-skip`: change the `--name-only` diff and the **The content diff, computed here too.** diff to `origin/<default_branch>...HEAD`, keeping both exclusion pathspecs.
- [ ] `sample_statistics.md` → `## Counts breakdown`, `dispositioned_points`: change "no commit in `<default_branch>..HEAD`" to `origin/<default_branch>..HEAD`. Change no figure, task number or title (`plugin/samples/README.md`: the fixtures are one coherent worked branch).
- [ ] `AUTONOMOUS_FLOW.md` → `## Resolved values`, `<default_branch>` row: *"and therefore the diff base the branch gates compute against"* becomes *"and therefore the branch whose remote-tracking ref `origin/<default_branch>` is the diff base the branch gates compute against"*.

**Verification:**

- `git grep -nE '(^|[^/])<default_branch>\.\.\.?HEAD' -- plugin/agents/statistics-plan-writer.md plugin/instructions/improvement_observations_instructions.md plugin/instructions/docs_phase_instructions.md plugin/samples/sample_statistics.md plugin/docs/AUTONOMOUS_FLOW.md` prints nothing.
- `git grep -nF "re-issue that command once with \`<default_branch>\` in its place and say which base you used." -- plugin/agents/statistics-plan-writer.md plugin/instructions/improvement_observations_instructions.md plugin/instructions/docs_phase_instructions.md` hits each of the three files.
- Each `git log` command still reaches the tool layer free of `$(`, a backtick, `|`, `>` and `<` once `<default_branch>` is resolved. The new `origin/` prefix adds none of them.
