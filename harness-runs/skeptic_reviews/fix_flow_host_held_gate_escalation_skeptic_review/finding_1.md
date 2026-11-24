### 1. The Chosen entry says bash's resume reopens only the missing gates, but a refused file makes it reopen the whole set

**File:** `devscene-flow-host/README.md` (`## Differences from flow-walker.sh` → **Chosen** → **The held-gate escalation.**) — "because `start` reopens a round's missing gates when the evidence is consistent"

**Problem.** The new **Chosen** entry gives the mechanism by which bash reviews the refused gate again after it escalates the held gate. It says that `start` reopens the round's *missing* gates when the evidence is consistent, and it cites `flow-walker.sh` → `STATE` and `flow-walker-resume.test.mjs` → *"(8) with the saved walk deleted and two of three round files committed, start dispatches only the third gate at counter 0"*. That path cannot apply in this case. The refused gate's round file is on disk: it is the file the walker refused. So the evidence is never consistent, and bash's `start` reopens the **whole set** at that round. Test (8) covers a round where every present file is valid, which is not this one.

The entry's conclusion is still true: *"Both orders review the refused gate again; they differ in when."* The whole set includes the refused gate. What is false is the mechanism and the test the entry cites for it. Bash also reviews again every gate that had already passed, here `business_parity_review`, which the entry's wording rules out. #419 reads this list to switch `flow-walker.sh`'s callers. A reader who trusts this entry takes the wrong resume path and the wrong pinning suite case for bash.

**Proof.**
- `cli/templates/scripts/lib/flow-walker-gates.sh` → `fw_round_evidence`, for each present file: `v=$(fw_review_verdict "$file") || v=unreadable` and then `fw_round_file_check "$file" >/dev/null || v=unreadable`. A refused file is one `fw_round_file_check` rejects, so it reads `unreadable`.
- `cli/templates/scripts/flow-walker.sh` → `start_round`: `if [ "$unread" -eq 0 ] && [ "$plan" = not-newer ]; then … START_MODE=subset`. Any `unreadable` gate skips the subset, so the round opens whole. `STATE` says the same: *"a round with files missing whose evidence is consistent — no present gate reads `unreadable` … any other incomplete round opens the whole set at that round"*.
- `docs/flow-graph-walker.md`, the round-file-check **Decision.** paragraph, already records this: *"On resume, `fw_round_evidence` reads a present file the check refuses as `unreadable`, so `start` at the round node opens that round's whole set."*
- The suite case that pins it is `flow-walker-resume.test.mjs` → *"(9) inconsistent round evidence dispatches the whole set, and each gate replaces its file"*, not (8).
- The host agrees with bash: `devscene-flow-host/src/devscene_flow_host/host/resume.py` → `round_resume` takes the subset only when `"unreadable" not in statuses`.

The task prompt's **Decided** bullet uses the same wrong mechanism. Its conclusion, that the refused gate is reviewed again in either order, survives, so the decision itself stands. The prompt is a run artifact, and this finding does not change it.

**Grade.** Should Fix, not Must Fix. The divergence itself is authorized by the task prompt's decision, and that authorization holds. What is wrong is a sentence that describes bash, plus the test it cites (`finding_grades.md` → `## Never a Must Fix on its own`).

**Fix.** In that README bullet, replace this text:

> the refused gate is reviewed again only on resume, because `start` reopens a round's missing gates when the evidence is consistent (`flow-walker.sh` → `STATE`; `flow-walker-resume.test.mjs` → *"(8) with the saved walk deleted and two of three round files committed, start dispatches only the third gate at counter 0"*)

with:

> the refused gate is reviewed again only on resume: `fw_round_evidence` reads the refused file on disk as `unreadable`, so `start` at the round node reopens the round's whole set (`flow-walker.sh` → `STATE`, *"any other incomplete round opens the whole set at that round"*; `flow-walker-resume.test.mjs` → *"(9) inconsistent round evidence dispatches the whole set, and each gate replaces its file"*)

Change nothing else in the bullet. *"Both orders review the refused gate again; they differ in when."* stays true. No code or test changes. This edits a README only, so it runs no test.
