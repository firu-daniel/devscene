### Task 7 — Describe the review-loop pattern in `graphscene/README.md`

**Goal:** The package README states that a round is a plain fan-out and join unless it declares `writer`, which makes it a review loop. It names where the pattern lives, and which of checks 8 and 9's clauses apply to every round and which only to a review loop.

**Depends on:**
- Task 1, which adds `graphscene/src/graphscene/engine/review_loop.py`. The module is not public: `ReviewLoop`, `review_loop`, `review_loops` and `is_converging`, the one place that decides whether a round is a review loop.
- Task 3, which splits checks 8 and 9:
  - round rules on every round: a gate is a dispatch node; a gate's verdict outcomes and skips go to the round;
  - review-loop rules on a round declaring `writer`: the writer is a dispatch node; each gate declares both verdicts; the writer routes to the round; nothing else targets it;
  - check 8's *uncapped fail verdict is a gate of exactly one round*, only when the graph declares a review loop.
- Task 4, which makes `writer`, `counter` and `convergingFrom` an optional group in the format-4 schema, with `plan` and `revisionNote` allowed only with `writer`, and `formatVersion` still `4`.

**Where this task stops.** This task is the package README only. Root documents of record (`ROADMAP.md`, `docs/development.md`) are Task 8's. The conventions document `.claude/context/graphscene.md` is never a target: what it states stays true, because the check ids, their order and the loading order do not change.

### Targets

- `graphscene/README.md`

**Work:**

- [ ] `## What it is`, the opening paragraph: add one sentence. A round node dispatches its gates as one set and joins them. A round that declares `writer` is a review loop — write, parallel gates, round, revision with the closed round's records, capped by its counter — and its rules are checked and walked only where a graph declares one.
- [ ] `## What it is`, the `src/graphscene/engine/` row:
  - Add `review_loop.py`: whether a round is a review loop, and its writer's round number and its gates' convergence; not public.
  - Restate the `static_check.py` entry so that `gate-in-round` and `round-fan-out` read as round rules on every round plus review-loop rules on a review loop.
- [ ] `## The layers`, the `engine` row's *Holds* cell: *"Checks and walks over the built model: the vocabulary check, the static checker, the walk with its rounds, and the review-loop pattern."*

**Verification:**

- Every module and name the README now cites exists at the path it gives. `review_loop.py` is not listed as public, and `graphscene/src/graphscene/__init__.py` → `__all__` names none of its names.
- The README still states `formatVersion` 4 nowhere differently from the schema: `git grep -n "format 5" -- graphscene/README.md` prints nothing.
