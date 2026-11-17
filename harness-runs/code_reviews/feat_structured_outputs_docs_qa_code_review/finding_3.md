### 3. The report-don't-substitute sentence in `plugin/agents/README.txt` nests two em-dash asides

**File:** `plugin/agents/README.txt`. The site is the paragraph after `Sample fixture pointers`, starting "One convention rides along with those pointers": "REPORTS it — through its return"

**Problem.** Task 2 rewrote the sentence as:

> an agent that cannot read a cited contract, sample or instruction file REPORTS it — through its return object — a `blocker` outcome, or the outcome its schema names for that case — naming the path and the refusal — and produces no artifact.

It now has four em dashes, and they do not pair up clearly. On a first read, "through its return object" looks like the whole aside and "a `blocker` outcome …" reads like a second, unattached clause. The rule is unchanged, but it is harder to read than the version it replaced.

**Fix.** Replace the clause from "REPORTS it" through "and produces no artifact." with:

```
REPORTS it in its return object — a `blocker` outcome, or the outcome its
schema names for that case, naming the path and the refusal — and produces no
artifact.
```

Keep the rest of the paragraph, from "A substitution is a finding, not a fallback" onward, unchanged. Keep this file's hard wrap of about 80 columns.
