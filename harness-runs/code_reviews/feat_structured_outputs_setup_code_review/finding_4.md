### 4. Re-spell Gate 8's corpus-review `findings:` references as `conventions-reviewer.findings`

**Severity:** Should Fix

**Site:** `docs/development.md` → `## 5. Verifying a change`, Gate 8's corpus-pass legs. There are two sentences:

- the **Leg — sensitivity** invariant, *"The invariant: each planted shape appears in the corpus review's `findings:` under the check named beside it"*;
- the **Leg — false positive** criterion, *"The criterion is the **corpus review's** `findings:`, read off the closing report's corpus block"*.

**Problem.** This branch removes the reviewer's `findings:` line form. The field is now the array `conventions-reviewer.findings`, and an empty result is an omitted field rather than `findings: none`. Each finding's check is now its own property, `conventions-reviewer.findings.check_id`.

These two Gate 8 sentences still spell the field in the old prose form. Scope-register row 13 marked `docs/development.md` `no-change`, and its C2 derivation grep matched `findings: none` but not a bare `` `findings:` ``, so these two sites were missed.

A hand-runner can still work out the meaning: both criteria are read off the closing report. That is why this is Should Fix and not Must Fix. But the decision record → `### Citing a field` makes `<agent>.<field>` the only spelling for naming a field of a return, and these sentences break that rule.

**Fix.** In `docs/development.md`, make these two replacements:

- `` appears in the corpus review's `findings:` under the check named beside it `` becomes `` appears in the corpus review's `conventions-reviewer.findings` under the check named beside it — its `check_id` `` (keep the text that follows, starting with ", with a concrete correction naming which document changes").
- `` The criterion is the **corpus review's** `findings:`, read off `` becomes `` The criterion is the **corpus review's** `conventions-reviewer.findings`, read off ``

Change nothing else in Gate 8.
