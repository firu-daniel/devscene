# Dispatch additions — refactor_graphscene_layers

## [A2 · arch-review · iter 0] → architecture-reviewer  (#5)
- **added:** `context_notes:`
- **verbatim:** context_notes: this checkout has no local `dev` branch; only the remote-tracking ref `origin/dev` exists (source: `git branch -a --list '*dev'`).
- **why the agent could not derive it:** absent from the dispatch block, which passes `diff_base: dev` (the configured `defaultBranch`) as a bare name that does not resolve as a local ref in this checkout; the fact is in the output of `git branch -a`, not in any file the reviewer reads.
