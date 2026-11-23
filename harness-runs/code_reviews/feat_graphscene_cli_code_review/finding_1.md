### 1. `## The command line` gives the `provision` step as an inline command instead of a fenced block

**File:** `graphscene/README.md` (`## The command line`) — "`bash scripts/python-service.sh provision` installs the console script into the package environment. Once it has, run the command from the repository root:"
**Class:** Broken contract
**Failure:** If a host author follows `graphscene/README.md` → `## The command line` by running its fenced blocks in order, then the first one, `uv run --frozen --no-sync --project graphscene graphscene check …`, fails because no `graphscene` executable is installed: the step that installs it is the only command in the section that is not fenced.

The new section tells the reader to run a command — `bash scripts/python-service.sh provision` — as inline code at the start of a prose sentence, and then fences only the `uv run …` commands that depend on it. The lessons ledger (`harness-runs/lessons.md` → `## Adopter-facing documentation`, *"Every command an adopter is meant to run sits in a fenced block, one command per line; never inline it, join two with prose, or cut its block when compacting a document."*) forbids exactly this. `## The command line` exists for hosts outside this repository, so this is adopter-facing documentation. The inline sentence also leaves out the condition that `## Running the toolchain` states for the same command, *"outside any sandbox"*. Without that condition, a reader who runs it inside a sandbox has it refused, because `provision` reaches the network.

**Fix:** in `graphscene/README.md` → `## The command line`, replace the sentence

```
`bash scripts/python-service.sh provision` installs the console script into the package environment. Once it has, run the command from the repository root:
```

with

````
Install the console script into the package environment first, outside any sandbox (this provisions every package's environment):

```
bash scripts/python-service.sh provision
```

Then run the command from the repository root:
````

Leave the `uv run …` blocks that follow unchanged. This is a prose-only edit to a README, so no test file is created or edited, and the fix runs no test.
