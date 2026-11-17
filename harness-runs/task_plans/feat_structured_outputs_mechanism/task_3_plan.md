### Task 3 — Read the screen agent's return object in the screen script's verdict verb

**Goal:** Rewrite `cli/templates/scripts/prompt-injection-screen.sh` → the `verdict` verb so it reads `prompt-injection-reviewer`'s return **object**, not `verdict:` / `finding:` lines. It must stay fail-closed: only an exact `SAFE` object passes, and a well-formed `UNSAFE` parks its own findings. Anything else parks one `malformed-verdict` finding. The parser accepts nothing it refused before; a parser that accepts more is a regression.

**Depends on:** Task 2. It makes the return-schema check hold a citation of the form `` `<agent>.<field>.<property>` `` and scan `cli/templates/scripts/**` for citations. This task's header cites the fields it reads in that form, so they are held to the schema once Task 5 adds it.

**Where this layer stops.** The agent's own contract and its schema file are **Task 5's**: `plugin/agents/prompt-injection-reviewer.md` and `plugin/schemas/prompt-injection-reviewer.return.json`. What the orchestrating session writes to the verdict file is **Task 4's**: `plugin/instructions/prompt_injection_screen.md`, read per `agent_return_contract.md` → `## Reading a return`.

This task moves the script first on purpose. Until Task 5 lands, the agent still returns `verdict:` lines, and the script parks them as `malformed-verdict`, which fails closed. The reverse order would leave the script reading lines the agent no longer returns.

**The return this task reads (restated from the story index `## Context`; Task 5 produces it):**

- **The verdict file holds the agent's reply.** That reply is exactly one fenced `json` block:
  - an opener line that is exactly ```` ```json ````;
  - the object's JSON text;
  - a closer line that is exactly ```` ``` ````;
  - optionally whitespace-only lines before the opener and after the closer.
- **`SAFE`** — the object is exactly `{"outcome":"SAFE"}`: the key set is `["outcome"]` and the value is `"SAFE"`.
- **`UNSAFE`** — the object's key set is exactly `["findings","outcome"]`, `outcome` is `"UNSAFE"`, and `findings` is an array of at least one item. Each item is an object whose key set is exactly `["check_id","excerpt","reason"]`, and each of the three is a non-empty string carrying no CR or LF. `check_id` is one of `PI_CHECK_IDS`.
- **`blocker`** — `{"outcome":"blocker","blocker":"<one line>"}`. It is schema-valid, and the script parks it as `malformed-verdict`, exactly as it parks a `blocker:` line today.

### Targets

- `cli/templates/scripts/prompt-injection-screen.sh` — `pis_verdict`, `pis_parse_verdict` (replaced), and the header's `VERDICT` section.
- `cli/test/prompt-injection-verdict.test.mjs` — every verdict case moved to the object, the malformed matrix widened, and the header rule.

**Work:**

- [x] `pis_verdict`: replace the line reader and its one-fence strip (`PIS_VLINES`, the ```` '```'* ```` case) with block extraction and a JSON parse.
  - **Extraction.** Drop leading and trailing whitespace-only lines. The first remaining line must be exactly ```` ```json ```` and the last exactly ```` ``` ````, and no line between them may begin with ```` ``` ````.
  - **Parse.** Hand the lines between to one `jq` program (jq is already required by `pis_run_args`). It must parse as exactly one JSON value, and that value must be an object. A `jq` parse failure is `MALFORMED`, never exit 2.
  - **What never passes.** Anything at all outside the block is `MALFORMED`: prose, a second block, a column-0 `agentId:` trailer, or a two-space-indented fence.
  - **Floors.** Keep the bash 3.2 / jq 1.5 floors the header's `FLOORS` paragraph states: no regex builtin in jq, every `if` with an `else`, no associative array.
- [x] **The check.** One jq program, with `PI_CHECK_IDS` passed in by `--arg`, decides `SAFE`, `UNSAFE` (emitting one `check_id<TAB>excerpt<TAB>reason` line per finding, a tab inside `excerpt` or `reason` turned into a space as today) or `MALFORMED`, by the rules above.
  - Then feed `pis_park_write` the same six-field records it takes today: path, sha, id, empty line, excerpt, reason.
  - The `MALFORMED` path is unchanged: the first 1024 bytes through `pis_excerpt`, id `malformed-verdict`, reason `PIS_MALFORMED_REASON`.
  - These do not change: `pis_park_write`, `PI_CHECK_IDS` with its `MIRROR OF` comment, `PIS_RAISED`, every exit code, the scratch-directory and `--path` refusals, the verdict-file removal rules, and the script's own stdout lines (`verdict: SAFE <path> sha256 <hex>`, `verdict: UNSAFE`, then `parked:` or `discarded:`). Those stdout lines are the script's wire, read by `plugin/instructions/prompt_injection_screen.md` → step 0, not the agent's return.
- [x] **The header's `VERDICT` section.**
  - Restate the accepted shapes above in the section's own style, as the closed list it has today.
  - Name the fields it reads as `` `prompt-injection-reviewer.outcome` ``, `` `prompt-injection-reviewer.findings` ``, `` `prompt-injection-reviewer.findings.check_id` ``, `` `prompt-injection-reviewer.findings.excerpt` `` and `` `prompt-injection-reviewer.findings.reason` ``, and name the schema file `plugin/schemas/prompt-injection-reviewer.return.json` as the shape they mirror.
  - Say that the script carries its own check rather than loading that file: the copied script is never told the plugin's location, and its check is narrower than the schema (an exact `SAFE` object, a closed id set).
  - Keep the fail-closed sentence: *"only the exact SAFE block passes"* becomes *"only the exact SAFE object passes"*.
- [x] **`cli/test/prompt-injection-verdict.test.mjs`.**
  - **The header rule** reads that only the exact `SAFE` object, in one fenced `json` block, passes.
  - **SAFE cases** — the object compact, pretty-printed over several lines, and surrounded by blank lines — each exit 0 with the hash line.
  - **UNSAFE cases.** The two-findings case is re-expressed as an object, keeping its neutralisation assertions (`@`, backtick, `<!--`). The `" | "` case becomes an excerpt containing `" | "` that is kept verbatim. The answer re-ask and screen-park-answer cases are re-expressed as objects.
  - **The malformed matrix** keeps every existing row re-expressed where it still applies, and adds each of these as a row that must park `malformed-verdict` with exit 1:
    - the retired forms `verdict: SAFE` (bare and in a plain ```` ``` ```` fence);
    - a bare object with no fence;
    - ```` ```JSON ```` and a plain ```` ``` ```` opener;
    - prose before or after the block;
    - a column-0 `agentId: …` / `<usage>…</usage>` trailer after the closer;
    - the whole block indented by two spaces;
    - two fenced blocks;
    - JSON that does not parse, a JSON array, and two objects in one block;
    - `{"outcome":"safe"}`;
    - `SAFE` with an extra key, and `SAFE` with `"findings":[]`;
    - `UNSAFE` with no `findings`, with `[]`, and with an item missing `reason`;
    - an item with an extra key;
    - an unknown `check_id`;
    - an empty `excerpt`;
    - a non-string `reason`;
    - an `excerpt` containing a newline;
    - `{"outcome":"blocker","blocker":"cannot read the file"}`.
  - Keep both `PI_CHECK_IDS` mirror tests unchanged.

**Verification:**

- `cli/test/prompt-injection-verdict.test.mjs` passes, every malformed row included.
- Fail-closed holds at the boundary:
  - **Passes.** Only the exact `SAFE` object, in one fenced `json` block, exits 0.
  - **Parks, retired form.** The retired `verdict: SAFE` text parks.
  - **Parks, wrapping left in.** A block left with the measured two-space indentation or the Claude Code trailer parks.
- `grep -n "verdict: SAFE'\|'finding: '" cli/templates/scripts/prompt-injection-screen.sh` finds no case arm or parser line matching the agent's retired lines. The script's own `printf 'verdict: SAFE %s sha256 %s\n'` output line stays.
- **Not done here.** No file under `plugin/` changes in this task.

**Deviations from plan:**

- The header's `FLOORS` paragraph did not state the jq 1.5 floor this task's Work bullet cites. One line was added to it so the header names the floor `PIS_JQ_VERDICT` is held to: no regex builtin, and every `if` has an `else`.
- `pis_is_check_id` was removed. The jq program now owns the id-set membership check, and nothing else called the function.
- The malformed matrix also has rows the plan did not list: the retired `verdict: SAFE` inside a `json` fence, the retired `blocker:` line, a trailing space on the opener, an opener with no closer, an error line after the block, `UNSAFE` with an extra key, an item that is not an object, an empty reason, a reason containing a CR, and one good item next to one bad item. One new test was also added: a tab in an excerpt or a reason becomes a space.
