### 2. Tracked review-round artifacts carry the running user's home directory

**Site:** three tracked files under `harness-runs/`, each grep-verified in the current tree:

- `harness-runs/dispatch_additions/fix_injection_verdict_tools_used_prefix.md` — the `context_notes:` line containing `in the Claude Code session whose transcript is` (near line 15).
- `harness-runs/architecture_user_review_reviews/fix_injection_verdict_tools_used_prefix/user_review_1/review_0.md` — finding 1, ending `(…/plugin/instructions/finding_grades.md` → `## Never a Must Fix on its own`)` (near line 8), and finding 3, citing `…/plugin/instructions/untrusted_input.md` → `## The laundering check` and `…/plugin/instructions/finding_grades.md` → `### Checklist triggers` (near line 14).
- `harness-runs/architecture_user_review_reviews/fix_injection_verdict_tools_used_prefix/user_review_1/review_1.md` — finding 1, citing `…/plugin/instructions/untrusted_input.md` → `## The laundering check` and `…/plugin/instructions/finding_grades.md` → `### Checklist triggers` (near line 8).

**Failing test:** none — 6a no machine paths

**Class:** Broken contract

**Failure:** If the gate runner runs gate `6a no machine paths` (`scripts/check-machine-paths.sh`) over this branch, then it prints four lines naming the running user's home directory — e.g. `./harness-runs/dispatch_additions/fix_injection_verdict_tools_used_prefix.md:15:context_notes: … whose transcript is <home>/.claude/projects/-Users-…/bdb25286-e7fa-4093-b186-fd27908bb706.jsonl; …` — and the gate fails.

**Failure as logged** (home directory rewritten as `<home>`):

```
FAIL  6a no machine paths (printed output, which is the finding, 2 s)
./harness-runs/dispatch_additions/fix_injection_verdict_tools_used_prefix.md:15:context_notes: the live prompt-injection-reviewer probe that delivered the notice inside the frame ran on 2026-11-18 in the Claude Code session whose transcript is <home>/.claude/projects/-Users-daniel-Work-devscene-fix-injection-verdict-tools-used-prefix/bdb25286-e7fa-4093-b186-fd27908bb706.jsonl; every `"version"` field in that transcript reads 2.1.327.
./harness-runs/architecture_user_review_reviews/fix_injection_verdict_tools_used_prefix/user_review_1/review_0.md:8:1. **`finding_4.md` leaves a second passage of `docs/structured-agent-returns.md` stating the old accepted shape.** … (`<home>/Work/devscene/plugin/instructions/finding_grades.md` → `## Never a Must Fix on its own`).
./harness-runs/architecture_user_review_reviews/fix_injection_verdict_tools_used_prefix/user_review_1/review_0.md:14:3. **`finding_1.md`, `finding_2.md` and `finding_3.md` prescribe a tool that no harness contract requires.** … (`<home>/Work/devscene/plugin/instructions/untrusted_input.md` → `## The laundering check`) … (`<home>/Work/devscene/plugin/instructions/finding_grades.md` → `### Checklist triggers`).
./harness-runs/architecture_user_review_reviews/fix_injection_verdict_tools_used_prefix/user_review_1/review_1.md:8:1. **`finding_1.md`, `finding_2.md` and `finding_3.md` still prescribe a tool that no harness contract requires.** … (`<home>/Work/devscene/plugin/instructions/untrusted_input.md` → `## The laundering check`) … (`<home>/Work/devscene/plugin/instructions/finding_grades.md` → `### Checklist triggers`).
```

**Diagnosis:** this is the first round and there is no earlier log, so it is not classed as new or persisting. All three files are tracked artifacts this branch's user-review round wrote. The architecture reviewer cited plugin instruction documents by the plugin's resolved absolute path rather than by `${CLAUDE_PLUGIN_ROOT}`. The dispatch-additions log copied a `context_notes:` line that carries the session transcript's absolute path. `scripts/check-machine-paths.sh` greps the working tree for the literal `$HOME`. None of these paths is under its excluded directories or filters (`test_run_logs`, `scratch`, `harness-runs/clarifications/<sub>/`, `harness-runs/.flow_walker_state`), so all four lines are printed. The code is not at fault, only the artifact text.

**Fix:**

- [ ] In both `review_0.md` (lines near 8 and 14) and `review_1.md` (near line 8), replace each absolute plugin path `<home>/Work/devscene/plugin/` with `${CLAUDE_PLUGIN_ROOT}/`. For example, `${CLAUDE_PLUGIN_ROOT}/instructions/finding_grades.md` and `${CLAUDE_PLUGIN_ROOT}/instructions/untrusted_input.md`, which is the citation form the plugin corpus uses. Leave every heading anchor and all other wording unchanged.
- [ ] In `harness-runs/dispatch_additions/fix_injection_verdict_tools_used_prefix.md` (the `context_notes:` line near 15), replace the transcript's absolute path prefix with `<home>/`. The path then reads `<home>/.claude/projects/-Users-daniel-Work-devscene-fix-injection-verdict-tools-used-prefix/bdb25286-e7fa-4093-b186-fd27908bb706.jsonl`. Keep the rest of the line verbatim.
- [ ] Check that a `grep -rnF` for the literal home directory (from a bare `printenv HOME`) over `harness-runs/dispatch_additions/` and `harness-runs/architecture_user_review_reviews/fix_injection_verdict_tools_used_prefix/` prints nothing.
