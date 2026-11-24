### 1. `RevisionFindingsStore`'s module rule says a round close writes the closed round's files into the record, but the host clears it

**File:** `devscene-flow-host/src/devscene_flow_host/host/revision_findings.py` (module docstring, `The rule:`, first bullet) — "`close_round` replaces it with the closed round's files"

The module's `The rule:` paragraph is the rule this record holds (`.claude/context/devscene-flow-host.md` → `## Shared code and constants`: *"A module states the rule it holds in its docstring"*). Its first bullet says the record has four writers and that `close_round` *"replaces it with the closed round's files"*. That is how bash's `revision_findings` key behaves (`cli/templates/scripts/flow-walker.sh` → `close_round`, `st_set revision_findings "$list"`), but it is not what this record does:

- `devscene-flow-host/src/devscene_flow_host/host/round_gates.py` → `record_outcome` calls `kept.clear()` when `_closed_a_round(result.action)` is true. It never writes the closed round's files into the store.
- `devscene-flow-host/src/devscene_flow_host/commands/render.py` → `_findings_files` falls back to the `detail` of each `GateRecord` in the action's `closed_round` when `HostStep.revision_findings` is empty. That fallback is what puts the closed round's files on a revision's `arg.findings_file:` lines and a cap's `findings_file:` lines.

After a round closes, the file this module owns is absent. A reader who takes the module rule at its word expects to find the round's files in the record. For example, #472's implementer reads `RevisionFindingsStore` to learn what the record holds at a join. The output is right only because `render` falls back to `closed_round`. The docstrings in `round_gates.py` and `devscene-flow-host/README.md` → **Kept findings files.** already describe the clear correctly, so the one inaccurate statement is in the module that owns the record.

This finding comes from reading the three modules named above. No probe was run.

**Fix:** in the module docstring of `devscene-flow-host/src/devscene_flow_host/host/revision_findings.py`, replace the first bullet under `The rule:`:

```
- The record is one key with four writers, and the last one wins, as in bash: `next`'s `dispatch`
  branch keeps `--findings` for an outcome that is not a round gate's verdict, `next`'s `answer`
  branch keeps it with `answered`, `close_round` replaces it with the closed round's files, and
  `start` clears it. A held outcome recorded in an open set (`record_in_set`) never touches it.
```

with:

```
- The record plays bash's one `revision_findings` key, whose last writer wins: `next`'s
  `dispatch` branch keeps `--findings` for an outcome that is not a round gate's verdict, and
  `next`'s `answer` branch keeps it with `answered`; a round's close and `start` clear it. Bash's
  `close_round` writes the closed round's files into the key; here the record is cleared instead,
  and those files are the closed round's `GateRecord` details, which the `commands` layer prints
  when the record is empty. A held outcome recorded in an open set (`record_in_set`) never
  touches it.
```

Change no code and no other docstring. The change is to a docstring only, so it edits no test file and runs no test.
