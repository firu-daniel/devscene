### 2. A writer that fails during the docs phase's fix loop is told to "skip this target", which leaves an already-written doc uncommitted

**File (plugin layer):** `plugin/instructions/docs_phase_instructions.md` → `## Loop`, step 2, the **Write.** bullet, the sentences this branch added: "an `outcome` of `phase_disabled` or `blocker`, or a third failing return — this bullet's `error` route → log it, skip this target, and continue with the next. A re-dispatch in the fix loop routes the same way."

**Problem.** The `error` route "log it, skip this target" fits the first write of a target, because nothing is on disk yet. Task 3's plan gives exactly that reason: "skip this target (nothing to review or commit)". The bullet then applies the same route to "a re-dispatch in the fix loop". There the premise is false: by then the first write has already put the document at `` `docs-writer.doc_path` ``, and the reviewer has graded it `FAIL`. Here is how the run reaches that point:

1. The **Write** dispatch returns `written`, and the document is on disk.
2. The **Review** dispatch returns an `outcome` of `FAIL`.
3. The **Fix loop (cap 3)** re-dispatches `docs-writer` with `` `docs-reviewer.findings_file` ``. It returns an `outcome` of `blocker` (for example, the findings file cannot be read, which `docs-writer.md` → `## Invocation contract` → *"A cited path you cannot read is a finding, not a fallback"* turns into a `blocker`), or fails the routing check three times.
4. The bullet says: log it, skip this target, continue.

Nothing then commits that document, and nothing records it in `<state_dir>/docs_catalog/needs_review.md`. The **Commit + push** bullet is never reached for this target. Every later commit in the phase and in Phase D stages explicit paths only, so the new or modified document stays in the run copy's working tree as an uncommitted change. It never reaches the branch, and no human is told about it. This contradicts the bullet just below it. The **Fix loop (cap 3)** bullet handles a loop that ends without a clean `PASS` by saying "commit as-is and append `<slug>` + the open findings to `<state_dir>/docs_catalog/needs_review.md`". The **Review** bullet's own `error` route also commits the doc as-is and flags it.

**Precedent (two-leg test, leg 2).** Both established sibling routes for a docs-review cycle that cannot finish say to commit and flag:

- the docs phase's own fix cap, quoted above;
- the catalog's reviewer `error` route (`plugin/instructions/docs_orchestration_instructions_autonomous.md` → `## Per-entry loop`, step 2): "treat it as step 3's exhausted cap: record `<slug>` and … in `<state_dir>/docs_catalog/needs_review.md` and proceed to commit the doc as-is".

The new fix-loop route matches neither, and the story index's routing summary ("a write's logs and skips that target") only covers the first write.

**Fix.** In `plugin/instructions/docs_phase_instructions.md`, step 2's **Write.** bullet, replace

```
A re-dispatch in the fix loop routes the same way.
```

with

```
A re-dispatch in the fix loop routes an `outcome` of `written` the same way; on its `error` route the document is already on disk, so treat it as the fix loop's exhausted cap — commit the doc as-is and append `<slug>` + the open findings to `<state_dir>/docs_catalog/needs_review.md`.
```

Change no other sentence. The text cites no new return field, so `cli/test/agent-return-schemas.test.mjs` needs nothing.
