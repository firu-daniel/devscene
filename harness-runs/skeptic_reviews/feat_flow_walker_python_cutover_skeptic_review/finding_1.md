### 1. `cli/templates/scripts/README.md` still says `init` builds the walker's environment only "when asked (`--provision-python`, or yes at its prompt)"

**File:** `cli/templates/scripts/README.md` (the paragraph opening "**The other family in this directory is not generated.**", its sentence on `flow-host-provision.sh`) — "`init` runs it when asked (`--provision-python`, or yes at its prompt)"

**The problem.** This branch changed `init` to build the walker's environment by default and never ask:
- `cli/src/commands/init.ts` → `resolveProvisionPython` returns `!provisioned || flowHostChanged > 0` unless an opt-out is set. Its doc comment says it "Asks nothing, on a terminal or off one."
- `provisionPythonOptOut` reads only `--no-provision-python` or the test-only probe variable.
- The old `askYesNo` prompt was removed.
- `docs/cli.md` §2 item 6 now says this is "the one decision on the list that is **never asked**", and that `--no-provision-python` is "the only way to skip it".

Task 9 edited this same paragraph in this branch. The `flow-host-provision.sh` sentence gained "and fails the bootstrap when `uv` is not on PATH or the flow host's project is missing". The clause just before it, "`init` runs it when asked (`--provision-python`, or yes at its prompt)", was not changed and is now false.

This README is the template tree's own description of the outer-loop scripts and who runs each one. `cli/templates/README.md` says each subdirectory's README "names its own content owner and its writer". It is not one of the files `init` writes.

**Who reads it wrong.** The reader is a maintainer, or an implementing agent working in the `cli` layer, who reads this README to learn when `init` reaches the network to build `<scriptsDir>/python/.venv`. That reader comes away with two wrong conclusions:
- That a plain non-interactive `init` (a fixture, a script) builds nothing unless `--provision-python` is passed. In fact it builds by default, which is why the suite needed `FLOW_HOST_PROVISION_PROBE_ENV`.
- That a prompt offers a way to decline. The paragraph never names `--no-provision-python`, which is now the only opt-out.

No documented command fails because of this. It is a Should Fix (`finding_grades.md` → *A sentence that only describes the project and has become false*).

**Not raised by the committed review.** The committed code review's Finding 4 covers `docs/cli.md`'s gate-library mention, and its Finding 3 covers `remote-run.sh`'s REPRO. Neither touches this sentence.

**How it was confirmed.** This was confirmed by reading only. No probe was run. The evidence read:
- `git diff origin/dev...HEAD -- cli/templates/scripts/README.md`: the paragraph was edited on this branch and the stale clause was kept.
- `cli/src/commands/init.ts` → `provisionPythonOptOut`, `resolveProvisionPython`, and the post-plan block that calls them.
- `docs/cli.md` lines 66–67, 127 and 173.
- A `git grep` for "yes at its prompt" outside `harness-runs/` and `examples/`: it finds only this live occurrence.
- `git grep` over `cli/test`: no test reads this sentence.

**Fix.** In `cli/templates/scripts/README.md`, in that one sentence, replace exactly

```
`init` runs it when asked (`--provision-python`, or yes at its prompt), a person runs it,
```

with

```
`init` runs it by default after wiring, without asking, unless `--no-provision-python` is given, a person runs it,
```

Keep the rest of the sentence ("`doctor` names it as its remedy, and `setup-worktree.sh`'s step 6 runs the same sync … missing.") and the rest of the file unchanged. No test reads this text, so the fix runs no test. The full suite runs in the Run gates phase.
