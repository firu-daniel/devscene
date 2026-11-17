### 1. The verdict verb passes a return whose text carries an `UNSAFE` outcome, through a duplicate `outcome` key

**File:** `cli/templates/scripts/prompt-injection-screen.sh` (`pis_parse_verdict`) — "SAFE) PIS_VERDICT=SAFE; return 0 ;;", with the decision in `PIS_JQ_VERDICT` — "elif keys == [\"outcome\"] and .outcome == \"SAFE\" then \"SAFE\""

The `verdict` verb is a tripwire, and the task prompt makes its one passing path a hard constraint: *"The rewrite must stay fail-closed and must not loosen the SAFE test … a parser that accepts more than it did is a regression."* The script's own header says *"Fails closed: only the exact SAFE object passes."*

`PIS_JQ_VERDICT` decides SAFE on the object jq has already **parsed**, not on the text the agent wrote. jq does not reject a duplicate key; it keeps the last value. So a block whose text is

```
{"outcome":"UNSAFE","outcome":"SAFE"}
```

parses to `{"outcome":"SAFE"}`. `keys == ["outcome"]` and `.outcome == "SAFE"` both hold, and the file is held `SAFE`: the script prints `verdict: SAFE <path> sha256 <hex>` and the run goes on. That text is not "exactly `{"outcome":"SAFE"}`", and it carries an `UNSAFE` outcome. The retired parser could not be passed this way, because it compared the line text itself (`'verdict: SAFE'` and no other line). So this is a loosening of the SAFE test. A garbled or manipulated reply would reach `SAFE`, the one outcome that lets an unattended engine act on the screened file.

The `UNSAFE` path is not affected. A duplicate key there either still parses as a well-formed `UNSAFE` and parks, or fails the shape check and parks as `malformed-verdict`. Both are fail-closed.

**Fix:** make the SAFE decision also require that the block's **text** is that object, whitespace aside. Pretty-printed SAFE stays accepted, as the existing tests require. In `pis_parse_verdict`, replace the SAFE arm of the `case "$out" in` statement:

```bash
    SAFE) PIS_VERDICT=SAFE; return 0 ;;
```

with:

```bash
    SAFE)
      # jq keeps the last of a duplicate key: the text itself must be the object.
      [ "${body//[[:space:]]/}" = '{"outcome":"SAFE"}' ] && PIS_VERDICT=SAFE
      return 0
      ;;
```

`PIS_VERDICT` is already `MALFORMED` on entry, so a SAFE object whose text differs falls through to the malformed park.

In the header's `VERDICT` table, extend the SAFE row so the comment states the rule the code now enforces:

```
#   {"outcome":"SAFE"}                     key set exactly `outcome`, and the
#                                          block's text exactly that object,
#                                          whitespace aside
```

In `cli/test/prompt-injection-verdict.test.mjs`, add two rows to the `malformed — … — parks as malformed-verdict with exit 1` table:

```js
  ['a duplicate outcome key, UNSAFE then SAFE', '```json\n{"outcome":"UNSAFE","outcome":"SAFE"}\n```\n'],
  ['SAFE spelled with a unicode escape', '```json\n{"outcome":"\\u0053AFE"}\n```\n'],
```

The second row pins that the text comparison, not jq's decoding, decides SAFE. Run that one file, `npm test --workspace cli -- test/prompt-injection-verdict.test.mjs`, from the repository root. The existing `SAFE, pretty-printed over several lines` and `SAFE, surrounded by blank lines` cases must still pass.
