## Problem

The prompt-injection screen can park an autonomous run on a `SAFE` verdict. When an `Agent` result starts with a `<tools-used-before-summary>` line, `prompt-injection-screen.sh verdict` cannot unwrap it, reports `malformed-verdict`, and fails closed as `UNSAFE`.

Failing closed is correct. The problem is that a valid result shape is treated as malformed, so the operator gets a security park that says nothing about the screened file.

## What happened

On Claude Code 2.1.327, a `prompt-injection-reviewer` dispatch returned this result (frame text shortened):

```text
  <tools-used-before-summary>Grep</tools-used-before-summary>
  
[Subagent hand-back] The text below is the final report of a subagent ...
  ...
  ```json
  {
    "outcome": "SAFE"
  }
  ```
agentId: ...
<usage>...</usage>
```

The orchestrator saved the whole result verbatim to `verdict.md`, as `plugin/instructions/prompt_injection_screen.md` step 3 requires. The script then wrote a screen park whose only finding was:

```text
malformed-verdict: "  <tools-used-before-summary>Grep</tools-used-before-summary>    [Subagent hand-back] The text below ..."
```

## Cause

`pis_unwrap_vlines` in `scripts/prompt-injection-screen.sh` requires `[Subagent hand-back]` to be the first non-blank line. Here the first non-blank line is the indented tag, so the function leaves the lines untouched and the verdict parse finds no valid reply.

`plugin/instructions/agent_return_contract.md` → `## Reading a return` step 1 has the same gap: it allows column-0 text before the reply, but does not describe this indented line ahead of the frame.

## Impact

- Any autonomous engine can park at launch on a file the reviewer passed. It looks intermittent: the same screen passed on a retry with the tag absent.
- The only way on is to change the screened file's bytes and answer the park, because an unchanged file parks again from its recorded hash. That teaches operators to edit their way past a security park.

## Proposed fix

- Make `pis_unwrap_vlines` accept this exact prefix: optional blank lines, then lines that are only a complete `<tools-used-before-summary>…</tools-used-before-summary>` element, at column 0 or indented by two spaces, ahead of the `[Subagent hand-back]` frame.
- Keep it fail-closed. Any other text before the frame stays malformed, and the tag must not be accepted inside or after the reply.
- Apply the change to `cli/templates/scripts/prompt-injection-screen.sh` and re-render this repository's `scripts/prompt-injection-screen.sh`. Runs execute the main checkout's copy, so the fix takes effect there only after it is merged and re-rendered.
- Update `agent_return_contract.md` → `## Reading a return` step 1 to describe the prefix, and check whether any other reader of `Agent` results has the same assumption.

## Acceptance criteria

Add cases to `cli/test/prompt-injection-verdict.test.mjs`:

- [ ] A result with the tag prefix and a `SAFE` reply is recorded as `SAFE`.
- [ ] The same prefix with an `UNSAFE` reply still parks, with the reviewer's findings.
- [ ] Other text before the frame still yields `malformed-verdict`.
- [ ] A tag-shaped line with extra text on it still yields `malformed-verdict`.
