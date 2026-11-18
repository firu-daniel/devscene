### 1. `branch-reviewer` grades a failed two-leg divergence Must Fix with no table row

**File:** `plugin/agents/branch-reviewer.md` (`### Must Fix triggers`) — "| A `<state_dir>/lessons.md` entry | Broken contract |"

`## Output contract`, in the index's call-out-section bullet, opens "**A divergence earns a call-out rather than a Must Fix only after the skeptical two-leg test:**" and grades both failures Must Fix: "dropping the intended part is a **Must Fix**, not a call-out" and "code matching **neither** `<reference_impl>` nor the precedent is a **Must Fix**".

No row of the agent's `### Must Fix triggers` table covers this. The nearest rows cover a parity item from `## Common findings to look for`, and a reference behaviour missing from the diff or waived by a bad authorization. `finding_grades.md` → `### Checklist triggers` requires each trigger an agent grades Must Fix to name its class in that table. The same trigger already has a row in both sibling agents: `skeptic-reviewer` ("Check 4: a divergence failing either leg") and `business-parity-reviewer` ("A failed leg of the **Obvious-reference-bug exception**"), each graded **Broken contract**.

This is a Should Fix: the reviewer can still work out a class from `finding_grades.md`, so the gap is an unmapped trigger and not a certain failure. It is listed first because the test in Finding 2 fails until this row exists.

**Fix:** in `plugin/agents/branch-reviewer.md` → `### Must Fix triggers`, add this row directly after the `` A `<state_dir>/lessons.md` entry `` row, the last **Broken contract** row:

```markdown
| A `<reference_impl>` divergence failing either leg of the call-out two-leg test, while `phases.parity` is `true` | Broken contract |
```

Keep the cell byte-exact: Finding 2's test names it literally.
