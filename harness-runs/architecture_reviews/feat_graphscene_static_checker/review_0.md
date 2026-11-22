# Architecture review — round 0

verdict: PASS
review_mode: full

## Nice to Have

1. **`task_6_plan.md` — the static fixture family is wired by analogy to a conventions row that does not name it.** `.claude/context/conventions.md` → `## What accompanies a new unit of each kind`, row *"A fixture a check rejects rather than a schema"*, names only the `vocabulary_negative_<name>.json` family (`validate:graphscene-schema`, `_NEGATIVES` in `graphscene/tests/engine/test_vocabulary.py`, `_VOCABULARY_NEGATIVES` in `graphscene/tests/facade/test_loading.py`). The plan applies the same three-part set to `static_negative_<check_id>.json` (Task 6 → `validate:graphscene-schema`; Tasks 1–2 → `_NEGATIVES` in `test_references.py` / `test_static_check.py`; Task 4 → `_STATIC_NEGATIVES` in `test_loading.py`), which is the right mirror, and the story index's scope register row 1 already routes the row's silence to `corpus_staleness`. Nothing to change in the plan; noted so the supervised conventions re-run adds the family to that row.
