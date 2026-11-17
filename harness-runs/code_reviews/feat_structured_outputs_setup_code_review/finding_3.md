### 3. Describe a shared-document divergence as an item with three parts, not "one line"

**Severity:** Should Fix

**Site:** `plugin/agents/conventions-writer.md` → `## The document`, in the paragraph opening **"Where the shared document disagrees with this scope's code, record the divergence."** The stale substring is *"write one line naming what the shared document says, what this scope's code shows, and the file plus the symbol or quoted substring you read it off"*.

**Problem.** Task 2 edited this paragraph's closing sentences, which now read "the field is `[]`" and "The divergences go to `shared_document_divergences`". Its opening instruction still tells the writer to *write one line* per divergence.

The same definition's `### Return fields` now declares `shared_document_divergences` as an `(array of objects)` with three item properties: `shared_document_says`, `code_shows` and `source`. `plugin/commands/analyze.md` → (4d.0) builds each forwarded line out of those three properties.

A writer that follows "write one line" emits an array of strings. That return passes the routing check, which checks presence and not shape. (4d.0) then has no `shared_document_says`, `code_shows` or `source` to render. The definition states the shape two ways, and only one of them matches the schema.

**Fix.** In that paragraph, replace

> where that document states something this document's own scope contradicts, write one line naming what the shared document says, what this scope's code shows, and the file plus the symbol or quoted substring you read it off.

with

> where that document states something this document's own scope contradicts, record one divergence naming what the shared document says, what this scope's code shows, and the file plus the symbol or quoted substring you read it off.

Leave the rest of the paragraph as it stands. `### Return fields` already gives the item properties, so the paragraph does not restate them.
