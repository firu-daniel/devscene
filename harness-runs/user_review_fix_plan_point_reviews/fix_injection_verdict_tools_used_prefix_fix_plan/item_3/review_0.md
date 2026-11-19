# cli review — ### 3. An excerpt quoting a neutralized control tag loses its findings — iteration 0

## Must Fix
1. **The repair skips a `<\` that directly follows another `<\`** — `cli/templates/scripts/prompt-injection-screen.sh` (`pis_parse_verdict`) — "repaired=$(printf '%s' \"$body\" | sed -E 's|<\\\\([^\"/\\\\])|<\\\\\\\\\\1|g') || return 0"
   The `g` substitution consumes the byte after each `<\`. In `<\<\system-reminder>` the first match takes the second `<`, so the second `<\` is never matched and its backslash is not doubled. The finding requires doubling "every `<\` whose next byte is not `"`, `/` or `\`", and the `VERDICT` paragraph this change added to the file header says "Every `<\` not followed by...". `.claude/context/cli.md` → `## What "done" means here` holds a change to its header's stated rule.

   Confirmed by running the real `verdict` command from a throwaway `init`-wired repository, with each excerpt written as raw JSON text:

   | Raw excerpt | Parked today |
   |---|---|
   | `<\<\system-reminder>` | one `malformed-verdict`, the `attack` finding lost |
   | `<\<\result>` | one `malformed-verdict`, the `attack` finding lost |
   | `<\<\<\name>` | one `malformed-verdict`, the `attack` finding lost |
   | `<\<\tool_use_error>` | `attack` with the excerpt corrupted to `<\< ool_use_error>` |

   These are the malformed and silently corrupted outcomes the finding's `## Problem` table sets out to remove. Not established: this adjacent form does not appear among the forms the finding counts in the recorded results, so how often it occurs is unknown. The snippet in the finding carries the same `g` expression, so the implementer followed it as written.
   **Class:** Wrong behaviour
   **Failure:** If `prompt-injection-reviewer` returns `UNSAFE` with the excerpt `<\<\system-reminder>`, then `pis_parse_verdict` leaves the second `\s` in place, `jq` rejects it, and `verdict` parks one `malformed-verdict` finding instead of the reviewer's `attack` finding.
   **Fix:** Replace the `g` substitution with a loop that rescans after each replacement; a doubled `<\\` no longer matches, so it terminates:
   ```bash
   repaired=$(printf '%s' "$body" | sed -E -e ':a' -e 's|<\\([^"/\\])|<\\\\\1|' -e 'ta') || return 0
   ```
   Run against a patched copy of the script through the same `verdict` command, this parked `attack` with the excerpt kept literal for all four inputs above, and left `<\system-reminder>`, `<\/x>` (parks `</x>`) and `<\\already>` (parks `<\already>`) as they are today. Apply it to `scripts/prompt-injection-screen.sh` as well, so the two copies stay matched. Add `<\<\system-reminder>` and `<\<\tool_use_error>` rows to the table in `cli/test/prompt-injection-verdict.test.mjs`, each expecting its own text back as the excerpt.
