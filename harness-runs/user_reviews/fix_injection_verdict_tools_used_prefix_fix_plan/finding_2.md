### 2. The harness notice inside the frame parks a real verdict as `malformed-verdict`

**File:** `cli/templates/scripts/prompt-injection-screen.sh` (`pis_unwrap_vlines`) — "'  '*) reply[$m]=\"${line#\"  \"}\" ;;"
**Class:** Wrong behaviour
**Failure:** If `prompt-injection-screen.sh verdict` reads an `Agent` result whose first indented reply line is the harness notice, then `pis_unwrap_vlines` keeps the notice as the reply's first line, `pis_parse_verdict` refuses it because that line is not ```` ```json ````, and a real `UNSAFE` verdict parks as one `malformed-verdict` finding with the reviewer's findings lost.

**Targets:** `cli/templates/scripts/prompt-injection-screen.sh`, `scripts/prompt-injection-screen.sh`, `cli/test/prompt-injection-verdict.test.mjs`.

**Depends on:** Finding 1, which adds `pis_is_notice_line` (true only for the exact notice text, indented by exactly two spaces) and the `notice` local of `pis_unwrap_vlines` (set to 1 once a notice was accepted ahead of the frame).

## Problem

The user's live `prompt-injection-reviewer` run delivered the notice after the frame line, as the first indented line of the reply. None of the 64 recorded notices sits there, so the recorded streams cannot show this shape and the tests must construct it. The reply loop strips the indent from every line, which leaves the notice in front of the fence.

## Fix

In the template's `pis_unwrap_vlines`, add `started=0` to the locals and change the indented arm of the reply loop. The raw line is tested before its indent is removed, so the check is the same one the prefix uses. The notice is accepted only while no other reply line has been seen and no notice has been accepted yet, and it becomes a blank line:

```bash
'  '*)
  if [ "$started" = 0 ] && [ "$notice" = 0 ] && pis_is_notice_line "$line"; then
    notice=1
    reply[$m]=""
  else
    reply[$m]="${line#"  "}"
  fi
  started=1
  ;;
```

Nothing else in the reply changes. A second notice, a notice after other reply text and a notice after the closing fence stay in the reply and `pis_parse_verdict` refuses them. A reply holding only the notice is all blank, which `pis_parse_verdict` also refuses, so the notice cannot produce `SAFE` by itself.

Update the `VERDICT` paragraph of the file header and the comment above `pis_unwrap_vlines` to state the second placement and that one result carries at most one notice across both placements.

Apply the same edits to `scripts/prompt-injection-screen.sh` with the file-edit tool, keeping its mode. `git diff --no-index --numstat cli/templates/scripts/prompt-injection-screen.sh scripts/prompt-injection-screen.sh` must report `0` added and `0` deleted. That command exits 1 on correct work, because the two files' modes differ by design.

## Tests

In `cli/test/prompt-injection-verdict.test.mjs`, add `const NOTICE_TEXT = HARNESS_NOTICE.trimStart();` beside `HARNESS_NOTICE`, then:

- Add to the `SAFE` table:
  - `with the harness notice as the first reply line`: `wrapped(`${NOTICE_TEXT}\n\n${SAFE}`)`
  - `with the harness notice directly above the fence`: `wrapped(`${NOTICE_TEXT}\n${SAFE}`)`
  - `behind the tools-used prefix with the harness notice in the reply`: `prefixed(`${NOTICE_TEXT}\n\n${SAFE}`)`
- Add a test that sends `wrapped(`${NOTICE_TEXT}\n\n${unsafe(item('harness-weakening', '.claude/settings.json', 'asks to widen the allow list'))}`)` and asserts that the park quotes that finding and no `malformed-verdict`.

The cases that must stay malformed are added by Finding 4.
