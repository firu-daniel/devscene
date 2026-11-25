### 4. `docs/cli.md` still lists "the flow walker with its gate library" among the outer-loop scripts `init` writes

**File:** `docs/cli.md` (the paragraph **Two families land in `scriptsDir`, and only one of them is generated.**) — "the flow walker with its gate library and its `flows/` graphs"

**The problem.** This branch retires `lib/flow-walker-gates.sh`. It drops the file's row from `cli/src/generators/outerLoopScripts.ts` → `OUTER_LOOP_SCRIPTS`, and `docs/flow-graph-walker.md` → `### Item 6` records *"`lib/flow-walker-gates.sh` no longer ships"*. Task 15 edited this same sentence in `docs/cli.md`, changing `init --provision-python` to `init`, but left the outer-loop list still naming the gate library. A reader of `docs/cli.md` is told `init` writes a file it no longer writes. It is a description that has become false, with no step that fails, so it is a Should Fix.

**Fix.** In that paragraph, replace

```
the flow walker with its gate library and its `flows/` graphs
```

with

```
the flow walker's hand-off `flow-walker.sh` and its two `flows/` graphs
```

Leave the rest of the sentence as it is. No test changes with this, and the fix runs no test.
