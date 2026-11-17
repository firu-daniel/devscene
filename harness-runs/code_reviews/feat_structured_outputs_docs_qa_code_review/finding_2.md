### 2. `qa-tester.md` keeps two phrases written for the old line-form return

**File:** `plugin/agents/qa-tester.md`. There are two sites:

- `## Output contract` → `### 2. Some tests fail`: "Then return an `outcome` of `FAIL`:"
- `## Resolved values`, the opening paragraph: "in the templates and the return blocks."

**Problem.** Task 1 replaced the fenced `verdict:` / `error:` return blocks with the return object, but two phrases still assume those blocks:

- **The colon in `### 2.`.** "Then return an `outcome` of `FAIL`:" used to introduce the fenced three-line block. That block is gone, so the colon now introduces the `findings_file` paragraph, which describes a field rather than a return to copy.
- **"the return blocks" in `## Resolved values`.** This paragraph says `<base_url>` / `<findings_folder>` / `<title>` are resolved "in the templates and the return blocks". The definition no longer has return blocks. `<base_url>` now appears in the `## Invocation contract` dispatch block (`base_url: <base_url>`), in step 1's blocker reason (`application not reachable at <base_url>`) and in the example `blocker` text in `### 4. The run cannot proceed`. The last two are return examples, not return blocks.

Neither phrase changes what the agent returns. They are wording leftovers.

**Fix.** Two edits in `plugin/agents/qa-tester.md`:

1. In `### 2. Some tests fail`, replace

   ```
   Then return an `outcome` of `FAIL`:
   ```

   with

   ```
   Then return an `outcome` of `FAIL`.
   ```

2. In the opening paragraph of `## Resolved values`, replace

   ```
   in the templates and the return blocks.
   ```

   with

   ```
   in the templates and the return examples.
   ```

These edits add no words and change no field, outcome or heading, so no other file changes.
