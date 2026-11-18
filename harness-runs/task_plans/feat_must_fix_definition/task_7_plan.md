### Task 7 — Move `branch-reviewer` and `skeptic-reviewer` onto the definition

**Goal:** Both end-of-branch reviewers grade by `finding_grades.md`, map their triggers to classes, and write the two fields on every Must Fix finding.

**Depends on:** Task 4, which creates `${CLAUDE_PLUGIN_ROOT}/instructions/finding_grades.md`. Task 6's `review-plan-reviewer` reads `**Class:**` and `**Failure:**` from each Must Fix `finding_<N>.md`, directly after the site anchor.

### Targets

- `plugin/agents/branch-reviewer.md`
- `plugin/agents/skeptic-reviewer.md`

**Work:**

- [ ] In both files add the `## Read first` bullet: `` `${CLAUDE_PLUGIN_ROOT}/instructions/finding_grades.md` — what each grade means. Grade every finding by it; never restate it. `` Delete the "Grade every finding by consequence" block with its three bullets.
- [ ] In both files replace the "not downgradable" paragraph with one that says every trigger in `### Must Fix triggers` keeps its grade under `finding_grades.md` → `### Checklist triggers`. Remove its sentences about "the rubric". `branch-reviewer` keeps its band rule for the size ladder, its rule that an ungraded listed item and a `<state_dir>/lessons.md` entry are Must Fix triggers, and Pass 2's do-not-promote rule.
- [ ] Add `### Must Fix triggers` to `branch-reviewer`. **Broken contract:** every parity item while the parity phase is on, each conventions-document violation, a missing accompanying test or required-set item, an unregistered tree-reading test, a file over the second size threshold, every architecture leak, and a `<state_dir>/lessons.md` entry. **Wrong behaviour:** a new exported symbol with zero callers, and a missing or fabricated-authorization `<reference_impl>` behaviour when the parity phase is on.
- [ ] Add `### Must Fix triggers` to `skeptic-reviewer`. **Wrong behaviour:** check 1 (unwired code), check 2 (a runtime failure copied from the spec or an invalid runtime address), check 3 (an authorization that does not hold), and check 5 (runtime faults and client-only gates). **Broken contract:** check 4 (a divergence failing either leg) and check 5's shared-constant and reuse smells.
- [ ] In both files state, in the per-finding format, that a file listed under `## Must Fix` carries `**Class:**` and `**Failure:**` directly after the site anchor. In each "Prose volume" paragraph replace "the ladder above gives it" with "`finding_grades.md` gives it", keeping the two copies identical to each other.

**Verification:**

- `grep -nE 'Grade every finding by consequence|would do the wrong thing|[Tt]he rubric|ladder above' plugin/agents/branch-reviewer.md plugin/agents/skeptic-reviewer.md` prints nothing.
- Both files name `finding_grades.md`, and each trigger list above appears in the matching table.
