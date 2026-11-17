`fix_run_commit_trailer_amend` stops an unattended run from splitting its branch into two tips: a commit carrying a forbidden attribution trailer, then a raw `git commit --amend` in the run copy that moves only the run copy's ref.

## What happened

On `feat_network_refusal_report` (2026-11-09), at Phase B.3, the `committer` (`mode: review_plan_file`) called the commit wrapper with an attribution trailer as the body line:

```
bash <MAIN_REPO>/scripts/commit-on-branch.sh --repo <run copy> harness-runs/code_reviews/feat_network_refusal_report_code_review.md harness-runs/code_reviews/feat_network_refusal_report_code_review/ -- "chore: add code review for feat_network_refusal_report" "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

The wrapper committed it as `afdf238f` and moved both the run copy's and the main checkout's `feat_network_refusal_report` to it. The committer then read `.claude/context/conventions.md` → `## Commit-message policy`, found **Attribution trailers are forbidden**, and ran `git commit --amend -m "chore: add code review for feat_network_refusal_report"` itself, in the run copy, outside the wrapper. That produced `799fcf0a` (same tree, same parent `8274347a`) and moved only the run copy's ref. `push-branch.sh` and `hr_commit_placed` then refused (`the clone (799fcf0a486e) and the main checkout (afdf238f2b72) have diverged`), and the run parked (`question_1.md`, Park 1). The maintainer moved the main checkout's ref to `799fcf0a` by hand with `git update-ref` and answered the park.

Two defects, each enough to need a hand repair on its own:

1. **The trailer.** The rule is already written down twice: `plugin/agents/committer.md` → **Attribution trailer** ("Add one **only** if `<commit_conventions>` requires it, never on your own initiative") and the adopter's commit-message policy. The committer added one anyway. The trailer's exact text is Claude Code's own default commit attribution, which a session's system context tells it to append to git commits. This is a likely source, not a verified one: the run profile sets no `attribution` key, so nothing switches that default off for a run.
2. **The raw amend.** The run profile, `cli/templates/claude/settings.autonomous.json`, allows `Bash(git commit:*)`, which matches `git commit --amend`. The run copy's `.git` is writable by the sandbox. So a session can rewrite and move the run copy's branch without the wrapper. The flow documents already say a headless run commits only through the wrapper, never through a raw `git commit` (e.g. `plugin/instructions/docs_orchestration_instructions_autonomous.md`, `plugin/instructions/improvement_observations_instructions.md`, `plugin/instructions/clarification_digest_instructions.md`). Nothing enforces it.

> ⚠️ **Find every anchor in this prompt by its quoted text, heading or function name, never by line number.**

## What to read first

- `plugin/agents/committer.md` → **Attribution trailer** and the wrapper-call steps.
- `.claude/context/conventions.md` → `## Commit-message policy`, and the template it is rendered from, `cli/templates/claude/context/conventions.md`.
- `cli/templates/claude/settings.autonomous.json`: `permissions.allow` (`Bash(git commit:*)`), `sandbox.filesystem`, and the `_README` paragraphs on the excluded commands and on what the sandbox leaves open; `cli/src/generators/permissionProfile.ts` and `cli/src/generators/sandboxProfile.ts`, which render it.
- `scripts/commit-on-branch.sh` header (`cli/templates/scripts/commit-on-branch.sh`) and `hr_commit_placed` in `cli/templates/scripts/lib/harness-run-lib.sh`.
- `docs/sandbox-verification.md` rows **G1**, **G2** and **CS3** (git in the clone under the run profile), §5 **AP2** and §8 **GW1** (how a Linux `denyWrite` entry is expanded), and `docs/sandbox-record.md`.

## The goal

1. A run's commit never carries an attribution trailer unless the adopter's commit-message policy asks for one.
2. A session in an unattended run cannot move its run copy's branch ref except through the commit, push and refresh wrappers, and a commit that went wrong is reported, never repaired by rewriting history.
3. When the branch does split anyway, the park says so plainly and names the repair, as Park 1 did.

## Checked before this run

Checked 2026-11-16, in a supervised session, because an unattended run has no web access. Claude Code 2.1.325.

**From the settings documentation** (`https://code.claude.com/docs/en/settings-reference.md` and `https://code.claude.com/docs/en/settings.md`):

- The setting is `attribution`, an object with `commit`, `pr` and `sessionUrl` keys. `includeCoAuthoredBy` is deprecated: "Deprecated since v2.0.62, when `attribution` replaced it. Claude Code still reads it, but new configurations should set `attribution`."
- `attribution.commit` and `attribution.pr` each hide their line when set to an empty string. `attribution.sessionUrl` is separate: "Claude Code adds the link as a `Claude-Session` trailer on commits and as a link in pull request descriptions. Set it to `false` to omit the link." It applies "only to commits and pull requests made from cloud or Remote Control sessions."
- "To hide all attribution, set `attribution` to `false`." This needs Claude Code v2.1.281 or later. Earlier versions "reject it and skip the whole user, project, or local settings file that holds it."
- The entries are valid in any settings file. `--settings <file-or-json>` is the "Command line" source, "for that session only", ranked below managed settings and above project local, shared project and user settings. The `attribution` entries themselves do not mention `--settings`; that it is honoured from there is the measurement below.

**Measured.** Three `claude -p --model haiku` sessions, each asked to quote verbatim any instruction in its system context about lines to end a git commit message with:

- No `--settings`: the session quoted `End git commit messages with:` followed by `Co-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>`.
- `--settings '{"attribution":{"commit":"","pr":""}}'`: no attribution lines. The only commit guidance left was the Bash tool's generic "End git commit messages and PR bodies with the attribution lines given in the conversation's system-reminder, when one is present", with no such reminder present.
- `--settings '{"attribution":false}'`: the same, no attribution lines.

So a key passed through `--settings` does switch off the instruction that produced the trailer in the incident. Whether the run profile is passed through `--settings` on every launch path, and which of the two forms suits the profile given the v2.1.281 floor, is for planning to settle against the code.

## Proposals — for planning to settle, not constraints

The plan decides which of these to take, in what combination, or something better, and says why. Each one needs its own check against the code and the record before the plan commits to it.

- **Switch off Claude Code's own commit attribution in the run profile**, so the session is never told to add the trailer in the first place. The setting's name and scope, and whether `--settings` honours it, were checked in a supervised step: `## Checked before this run` below.
- **Make the wrapper refuse it.** `commit-on-branch.sh` refuses a message argument carrying an attribution trailer (`Co-Authored-By:`, `Claude-Session:`) unless the adopter's policy permits one. Planning settles how a generic wrapper learns the adopter's policy, or whether it refuses unconditionally.
- **Permission layer.** Either add a deny rule for `git commit --amend` (and for the other ref-moving spellings planning finds, such as `git update-ref`, `git rebase`, `git commit --fixup`), or drop `Bash(git commit:*)` from `allow` if no flow needs a raw commit in an unattended run. Planning checks every flow before removing it.
- **Sandbox layer.** Write-deny the parts of the run copy's `.git` that hold the branch ref (`refs/heads/`, `packed-refs`, `HEAD`, perhaps `logs/`), so any sandboxed ref move fails at the OS layer, whichever command spelling tries it. The excluded commit wrapper runs outside the sandbox and keeps working. Planning weighs:
  - which sandboxed git operations the run still needs inside the run copy (CS3's calls, `git status` refreshing the index, `git stash`, `git switch`);
  - how the run copy's path is spelled in a profile that serves sibling run copies (AP2 and GW1 on Linux);
  - whether this replaces the permission-layer rule or backs it up.
  
  A new protection gets its own row in `docs/sandbox-verification.md`. It is graded `owed` until a probe measures it.
- **Committer contract.** On a commit that landed wrong, the committer stops and returns a blocker naming the commit and what is wrong with it. It never amends, resets or recommits. Planning decides whether the orchestrating flow then parks, or retries through a wrapper path that keeps both refs in step.

## Constraints

- No new permission in any profile.
- Bash 3.2 floor. `bash scripts/typecheck.sh` and `scripts/run-gates.sh` pass.
- **No measured result is invented.** A sandbox or permission behaviour the change relies on is either already recorded in `docs/sandbox-verification.md` / `docs/sandbox-record.md` or added there as `owed`.

