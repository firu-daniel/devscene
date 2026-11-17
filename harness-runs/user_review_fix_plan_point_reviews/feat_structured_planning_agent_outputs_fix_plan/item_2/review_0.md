# cli review — 2. The return-contract module and this branch's agent prose spend tokens on authoring rules and restatement their runtime readers never act on — iteration 0

## Nice to Have
1. **Section banner still says only "the module" over a reader that now reads the authoring document** — `cli/test/agent-return-schemas.test.mjs` (banner above `canonicalSentence`) — "// Reading the module."
   The banner covers both `canonicalSentence` and `roster`. After this edit, `canonicalSentence` reads `AUTHORING_DOC` (`docs/structured-agent-returns.md`), not `MODULE`. The top-level test was renamed to match ("the authoring document yields a canonical sentence and the module a roster"), but the banner was not. Nobody acts on the wrong thing because of it, since the doc comment directly under it names the document. It is a wording drift only.
   **Fix:** Rename the banner to `// Reading the authoring document and the module.`, or put a separate banner above `canonicalSentence`.
