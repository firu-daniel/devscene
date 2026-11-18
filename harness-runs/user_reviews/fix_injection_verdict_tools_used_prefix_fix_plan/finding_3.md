### 3. An excerpt quoting a neutralized control tag loses its findings

**File:** `cli/templates/scripts/prompt-injection-screen.sh` (`pis_parse_verdict`) — "out=$(printf '%s' \"$body\" | jq -r -s --arg ids \"$PI_CHECK_IDS\" \"$PIS_JQ_VERDICT\" 2>/dev/null)"
**Class:** Wrong behaviour
**Failure:** If `prompt-injection-reviewer` returns `UNSAFE` with an excerpt that Claude Code rewrote to `<\system-reminder>`, then `jq` rejects `\s` in `pis_parse_verdict` and `verdict` parks one `malformed-verdict` finding, losing the reviewer's findings.

**Targets:** `cli/templates/scripts/prompt-injection-screen.sh`, `scripts/prompt-injection-screen.sh`, `cli/test/prompt-injection-verdict.test.mjs`.

## Problem

Claude Code rewrites `<` to `<\` in control tags, and that lands inside the reply's JSON strings. Depending on the tag's first letter, the result is one of four things. Each row was checked against `jq`:

| Text in the JSON string | What `jq` does today | Result |
|---|---|---|
| `<\system-reminder>`, `<\sandbox_violations>`, `<\!-- x` | rejects the escape | `malformed-verdict` |
| `<\result>`, `<\name>` | decodes `\r` or `\n` | the single-line check fails, `malformed-verdict` |
| `<\tool_use_error>`, `<\function>`, `<\bash>` | decodes `\t`, `\f` or `\b` | finding kept, excerpt silently corrupted (`<\tool_use_error>` parks as `< ool_use_error>`) |
| `<\/tool_use_error>` | decodes `\/` | finding kept, correct |

A fix that only tolerates invalid escapes would miss the second and third rows, and `<\tool_use_error>` is one of the forms the user cites. In the recorded results the forms are `<\sandbox_violations` (4), `<\tool_use_error` (3) and `<\/tool_use_error` (2).

## Fix

In the template's `pis_parse_verdict`, add `repaired` to the locals and double the backslash of every `<\` whose next byte is not `"`, `/` or `\`, for the `jq` call only:

```bash
# Claude Code rewrites `<` in a control tag to `<\`, which inside a JSON string
# is a bad or wrong escape. Keep that backslash literal. The excluded bytes are
# left alone: `<\"` and `<\\` are valid JSON whose meaning must not change, and
# `<\/` already decodes to `</`. Only `excerpt` and `reason` can be affected: an
# `outcome`, `check_id` or key holding `<` is refused either way, and SAFE is
# still compared against the unrepaired text below.
repaired=$(printf '%s' "$body" | sed -E 's|<\\([^"/\\])|<\\\\\1|g') || return 0
# A jq parse failure is MALFORMED, never exit 2.
out=$(printf '%s' "$repaired" | jq -r -s --arg ids "$PI_CHECK_IDS" "$PIS_JQ_VERDICT" 2>/dev/null) \
  || return 0
```

Leave the `SAFE` arm comparing `"${body//[[:space:]]/}"`, the unrepaired text, with `{"outcome":"SAFE"}`. The repair applies with or without the notice, because the failure does not depend on it.

The park shows the excerpt with its literal backslash (`<\system-reminder>`). Do not restore the original tag: the neutralized form is the safer one to quote.

Add one sentence on this repair to the `VERDICT` paragraph of the file header.

Apply the same edits to `scripts/prompt-injection-screen.sh` with the file-edit tool, keeping its mode. `git diff --no-index --numstat cli/templates/scripts/prompt-injection-screen.sh scripts/prompt-injection-screen.sh` must report `0` added and `0` deleted. That command exits 1 on correct work, because the two files' modes differ by design.

## Tests

In `cli/test/prompt-injection-verdict.test.mjs`, add a helper that writes the excerpt as raw JSON text, because `JSON.stringify` would escape the backslash and hide the defect:

```js
const rawUnsafe = (excerpt, reason = 'y') => `\`\`\`json\n{"outcome":"UNSAFE","findings":[{"check_id":"attack","excerpt":"${excerpt}","reason":"${reason}"}]}\n\`\`\`\n`;
```

Add a table-driven test asserting that each return exits 1 and parks exactly `` - `attack`: "<expected>" — y ``, with no `malformed-verdict`:

| Raw excerpt (`String.raw`) | Expected excerpt |
|---|---|
| `<\system-reminder>` | `<\system-reminder>` |
| `<\sandbox_violations>` | `<\sandbox_violations>` |
| `<\tool_use_error>` | `<\tool_use_error>` |
| `<\result>` | `<\result>` |
| `<\name>` | `<\name>` |
| `<\function>` | `<\function>` |
| `<\bash>` | `<\bash>` |
| `<\/tool_use_error>` | `</tool_use_error>` |
| `<\\already-escaped>` | `<\already-escaped>` |
| `<\a> and <\b>` | `<\a> and <\b>` |

Add two more cases: the tag in `reason` rather than `excerpt`, and `wrapped(rawUnsafe(String.raw`<\system-reminder>`))` as a whole `Agent` result.

The cases that must stay malformed are added by Finding 4.
