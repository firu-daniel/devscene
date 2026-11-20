### 1. Gate 3i's printed remedy silently discards a hand edit of a format-3 copy

**File:** `scripts/generate-flow-graph-v3.mjs` (`main`): "run node scripts/generate-flow-graph-v3.mjs --write" (line 354, navigation hint only)
**Class:** Wrong action from operative text
**Failure:** Suppose a maintainer, or a fix-loop agent reading a Run gates log, edits `cli/templates/scripts/flows/task_plan_writing.graph.json` by hand. Gate 3e's `check-flow-graph: cli/templates/scripts/flows/task_plan_writing.graph.json — <check-id>: …` lines name that file, so this is a likely step. If that person then follows gate 3i's printed remedy `run node scripts/generate-flow-graph-v3.mjs --write`, both format-3 copies are regenerated from the unedited format-4 source and the edit is lost. The command exits 0 and prints nothing.

This branch makes both format-3 copies generated files. Gate 3i (`node scripts/generate-flow-graph-v3.mjs`) fails whenever a copy differs from what the generator produces. A copy can differ for two reasons:

1. The format-4 source `cli/templates/scripts/flows/task_plan_writing.v4.graph.json` was edited and not regenerated. Here `--write` is the right remedy.
2. A format-3 copy was edited by hand. Here `--write` is harmful: in `main`, `mode === 'write'` calls `writeFileSync(join(repoRoot, target), result.text)` for each of `TARGETS` and then `report()` with no findings. The hand edit is overwritten, the exit status is 0, and nothing is printed.

The message treats both cases alike:

```js
finding(target, `differs from the graph generated from ${sourceLabel}; run node scripts/generate-flow-graph-v3.mjs --write`);
```

Case 2 is reachable through an existing path. `scripts/check-flow-graph.sh` (gate 3e) still checks only the format-3 file. Its default `graph="cli/templates/scripts/flows/task_plan_writing.graph.json"` is unchanged, and its header documents each finding as `check-flow-graph: <graph> — <check-id>: <detail>`. A 3e finding therefore points the reader at the generated file. The format-3 file's own `description` (`V3_DESCRIPTION`) does not say that the file is generated. Gate 3i's message is the first and only text that reaches the reader at the moment it matters, and it tells them to run the command that throws their change away.

The committed code review's Finding 3 described this revert, but only fixed the `docs/flow-graph-walker.md` sentence that leads to it. The program output that gives the harmful step is unchanged. This finding is about that output.

**Fix:** in `scripts/generate-flow-graph-v3.mjs` → `main`, replace the comparison finding with a message that says the file is generated, names the real source and warns that `--write` overwrites:

```js
    if (bytes !== result.text) {
      finding(
        target,
        `differs from the graph generated from ${sourceLabel}; this file is generated and never edited by hand — make the change in ${SOURCE}, then run node scripts/generate-flow-graph-v3.mjs --write, which overwrites both format-3 copies`,
      );
    }
```

`SOURCE` is used for the "make the change in" path rather than `sourceLabel`. Under `--check --source <path>` the label is a planted copy, and `--write` never reads that copy. No other file quotes this message: a `git grep "differs from the graph generated"` outside `harness-runs` finds only this line. No test or document needs a matching edit. This fix edits no test file and runs none. Gate 3i confirms the clean path in the Run gates round.
