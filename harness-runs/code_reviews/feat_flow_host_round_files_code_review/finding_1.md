### 1. The `ROADMAP.md` GraphScene row links the host's README twice in one clause, and its list of what the host does now reads "and loads … reads … and resumes"

**File:** `ROADMAP.md` (the `| GraphScene |` row) — "in its own suite, reads the round and reviewer files"

Task 10 inserted the host's new capabilities into the middle of an existing clause of the `GraphScene` row. The clause now reads:

> … keeps each branch's walk in its own file, and loads and walks the harness's format-4 graph through GraphScene's `Walker` in its own suite, reads the round and reviewer files, applies the reviewer-file rules — … — and resumes a round from the files on disk through `Walker.start`'s `RoundResume` ([`devscene-flow-host/README.md`](devscene-flow-host/README.md)), with no command line yet, depending on GraphScene's public surface only, enforced by its own test, and gated by gate 13's legs 13h–13j ([`devscene-flow-host/README.md`](devscene-flow-host/README.md));

There are two problems:

- The same link, `[devscene-flow-host/README.md](devscene-flow-host/README.md)`, appears twice in one clause, a few words apart. Every other item in this row carries one link at the end of its clause.
- The list now has two `and`s. "and loads and walks" was the last item before this change, and the inserted items follow it, so the sentence reads "keeps …, and loads and walks …, reads …, applies …, and resumes …".

This is wording only, and no reader acts on it wrongly.

**Fix:** in that row, make exactly these two edits and nothing else:

1. Replace `keeps each branch's walk in its own file, and loads and walks the harness's format-4 graph` with `keeps each branch's walk in its own file, loads and walks the harness's format-4 graph`.
2. Replace `` through `Walker.start`'s `RoundResume` ([`devscene-flow-host/README.md`](devscene-flow-host/README.md)), with no command line yet `` with `` through `Walker.start`'s `RoundResume`, with no command line yet ``.

The single link left at the end of the clause, after `gated by gate 13's legs 13h–13j`, stays as it is. The fix touches a document only, so it runs no test.
