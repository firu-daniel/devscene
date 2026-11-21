# Architecture review — round 0

verdict: PASS
review_mode: full

## Nice to Have

1. **`task_4_plan.md` — `FALLBACK_SENTENCE` is planned as an *exported* constant of a test file.** Case `fallback-sentence` says to "Hold the sentence as one exported constant, `FALLBACK_SENTENCE`". Nothing imports a `cli/test/*.test.mjs` module. The model suite the header copies, `cli/test/untrusted-input-corpus.test.mjs`, keeps its pinned sentences (`RULE_POINTER`, `LAUNDERING_POINTER`) as module-local `const`s. A plain module-local `const` matches that precedent, and the plan's wording would not need `export`.
