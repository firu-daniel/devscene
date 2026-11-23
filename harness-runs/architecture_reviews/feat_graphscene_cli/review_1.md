# Architecture review — round 1

verdict: PASS
review_mode: full

## Should Fix
1. **`task_4_plan.md` — the README rule "Callers import from `graphscene` only and never name `graphscene.facade`" still gets no stated exception for the console-script target.** Round 0 raised this; it is non-blocking and so was not acted on. Task 3 declares `graphscene = "graphscene.facade.cli:main"` in `graphscene/pyproject.toml`, and `graphscene/tests/facade/test_cli.py` names `graphscene.facade.cli`. Both are defensible: `main` is deliberately not public, and the command's real caller is a process, which Task 3's test header says. But `graphscene/README.md` → `## The layers` and `.claude/context/graphscene.md` → `## The internal layers` state the rule with no carve-out, so the README Task 4 writes will read as contradicted by its own package manifest. Task 4's new `## The command line` section, or its `facade/` row entry, should add one clause: the console-script entry and its own suite name the module directly because the command line is reached as a process, not imported. Then a later reviewer will not raise it as a boundary breach.
