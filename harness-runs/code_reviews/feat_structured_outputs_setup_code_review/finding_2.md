### 2. Treat an empty `conventions-reviewer.findings` as none in `analyze.md` (4c)

**Severity:** Should Fix

**Site:** `plugin/commands/analyze.md` → step 4, (4c). There are two sentences:

- the reviewer-return pointer paragraph, *"`conventions-reviewer.findings` is optional, absent meaning none."*;
- the routing sentence after it, *"Take `conventions-reviewer.findings`. If it is absent, that document is done."*

**Problem.** The module these paragraphs point at, `plugin/instructions/agent_return_contract.md` → `## Reading a return` step 4, makes an optional field "absent or empty means none". The writer-return pointer paragraph in (4a) of the same file says "absent or empty meaning none". The reviewer pointer narrows that to "absent" only, and the routing sentence acts on absence only.

The routing check does not validate against the schema, so a reviewer return carrying `"findings": []` passes it. Read literally, (4c) then counts `[]` as not absent and re-dispatches `conventions-writer` as a fix with an empty `findings`. That is a dispatch the run should never send.

The schema's `minItems: 1` makes `[]` a non-conforming return, so this fires only on a misbehaving reviewer. Hence Should Fix rather than Must Fix. Still, the two pointer paragraphs in one file now state the optional-field rule two ways.

**Fix.** In `plugin/commands/analyze.md`, (4c), make these two replacements:

- `` `conventions-reviewer.findings` is optional, absent meaning none. `` becomes `` `conventions-reviewer.findings` is optional, absent or empty meaning none. ``
- `` Take `conventions-reviewer.findings`. If it is absent, that document is done. `` becomes `` Take `conventions-reviewer.findings`. If it is absent or empty, that document is done. ``

Keep the hard line wrapping of the surrounding paragraph. Change no other sentence.
