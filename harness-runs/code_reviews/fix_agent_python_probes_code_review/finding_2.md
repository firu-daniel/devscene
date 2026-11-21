### 2. The not-run `<typecheck_cmd>` clause in `layer-implementer`'s evidence-downgrade list attaches its note requirement mid-list

**File:** `plugin/agents/layer-implementer.md` → **An evidence downgrade is recorded, in every mode.** — "a `<typecheck_cmd>` step its own output reports as not run (`BLOCKED`, `SKIPPED`), whose note names the step and quotes its line,"

The paragraph's dash-delimited list names the kinds of verification claim that could not be executed, separated by commas. The new item puts a requirement on the *note* ("whose note names the step and quotes its line") inside the list itself. Grammatically, "whose" attaches to "step", and the next comma leads straight into the following item ("a whole-tree `<typecheck_cmd>` whose every failure …"). So the requirement reads as part of the enumeration rather than as a rule about what the note says. The paragraph already has a sentence for case-specific note contents ("The whole-tree case is **not** a blocker; its note names …"). This requirement belongs in a sentence of that kind.

This is a wording and ordering finding: the requirement is present, and an implementer reading closely can recover it.

**Fix:** In that paragraph, shorten the list item to `a \`<typecheck_cmd>\` step its own output reports as not run (\`BLOCKED\`, \`SKIPPED\`),` by deleting ` whose note names the step and quotes its line,`. Keep the comma that separates it from the next item. Then, immediately after the sentence that ends "…and that the Run gates phase's whole-tree `<typecheck_cmd>` run verifies it.", add this sentence:

```markdown
A not-run step's note names the step and quotes the line that reported it.
```

No test file covers this prose, so this fix runs no test.
