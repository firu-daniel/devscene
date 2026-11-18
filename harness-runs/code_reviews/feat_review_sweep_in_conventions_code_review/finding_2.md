### 2. `conventions-writer`'s `scope` row reads as if `sweep` were a scope value

**File:** `plugin/agents/conventions-writer.md` → `## Invocation contract`, the `scope` row — "which governs every layer, or `sweep`."

**The problem.** The row now reads:

> The absolute path(s) this document's evidence is gathered from — this layer's `layers[].path`, or the **repository root** when the target is the shared document, which governs every layer, or `sweep`.

`scope` is a list of absolute paths, so "or `sweep`" sits in the list of values `scope` may take, and a reader can take the literal `sweep` as a scope. The intent comes from the story `## Context` and from `plugin/commands/analyze.md` → (4e) "`scope` the repository root": on `target: sweep` the scope is the repository root. That is only recoverable from the caller, so the writer's own contract is unclear on the value it receives.

**Fix.** Replace the row's cell text with:

> The absolute path(s) this document's evidence is gathered from — this layer's `layers[].path`, or the **repository root** when the target is the shared document, which governs every layer, or the review-sweep document (`target: sweep`). Every `layers[].path` is repo-relative and resolves against `<repo_root>`, never against `<app_dir>`.

This is a prose-only edit to an agent definition, so it runs no test. The manifest gate runs in the Run gates phase.
