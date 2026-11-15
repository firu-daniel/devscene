# general review — ### 1. Replace the watcher tunable `PLANNING_DRIVER_PLUGIN_DIR` with a `devscene.config.json` key so remote jobs take script-driven planning too — iteration 1

## Should Fix
1. **"A run already past its launch is unchanged" contradicts the read-at-every-resume rule two sentences up** — `docs/watcher.md` (`### Script-driven planning (opt-in pilot)`) — "a run already past its launch is unchanged"
   The paragraph before it says the watcher reads the key "at every launch and resume", and `**When a launch takes it.**` repeats "At every launch and resume". `spawn_engine` calls `hr_script_driven_planning "$MAIN_REPO"` on every spawn, and a resume is a spawn. So a run that paused or parked before its first planning phase finished, and is resumed after the operator changed the key, does take the new value. As written, the sentence says it does not. This was confirmed by reading `cli/templates/scripts/autonomous-watcher.sh` → `spawn_engine` ("hr_script_driven_planning \"$MAIN_REPO\" || planning_key=$?") and `planning_driver_ready`'s ledger-pending test. No probe was run.
   **Fix:** Replace the clause with "a run whose launch already happened keeps its driver until its next resume, which reads the key again".

## Nice to Have
1. **The hand step still names `<scripts_dir>`, but no command in it uses it any more** — `docs/flow-graph-walker.md` (`### Not yet measured, and the hand step that measures it`) — "run from the main checkout with `<scripts_dir>` and `<state_dir>` your configured values"
   The `restart-watcher.sh` command was the only one that used `<scripts_dir>`, and it was removed. The four blocks that remain use only `<state_dir>`.
   **Fix:** Change it to "with `<state_dir>` your configured value".
2. **The `**Decision.**` sentence nests three dash pairs, so "whose planning is not finished" is hard to attach to its noun** — `docs/flow-graph-walker.md` (`### Which runs when`) — "in a watcher run of the task engine — local or a remote job — whose planning is not finished — the run's ledger is absent or its first phase is pending — with"
   **Fix:** Use parentheses for the mode: "in a watcher run of the task engine (local, or a remote job) whose planning is not finished — the run's ledger is absent or its first phase is pending — with …".
3. **"for that reason" points back at the wrong sentence** — `docs/config.md` (`## 2. Where configuration lives`) — "The last one is a boolean rather than a path for that reason:"
   The sentence before it explains why the three keys are committed rather than repository variables. The boolean-versus-path reason comes after the colon. So "that reason" reads as the committed-key argument.
   **Fix:** "The last one is a boolean rather than a path because the plugin directory its node sessions pin differs between the operator's machine and a runner, so the watcher derives it at each launch instead of reading it from this file."
