# Task plan review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **Task 2's park leaves the state the manual step needs unstated** — `task_2_plan.md`, Work bullet **The lock**.
   The plan says *"If the call is refused, exits non-zero or leaves no `graphscene/uv.lock`, return a blocker and commit nothing"*, and adds *"never land the row without the lock"*. The story index's first manual step then runs `bash scripts/python-service.sh --package graphscene lock` in the run copy. That command only resolves while the uncommitted `graphscene)` row is still in the run copy's `scripts/python-service.sh`. If the edit is reverted, `package_row` rejects the name, and the command exits `2` with `python-service: unknown package 'graphscene'; the packages are: docs-retrieval-service`.
   Nothing tells the implementer to keep the edit in the working tree, and an implementer reading *"never land the row"* cautiously may revert it. State outright that the edit to `scripts/python-service.sh` stays in the run copy, uncommitted, when the blocker is returned, and that the resumed Task 2 commits it together with the lock.
   The plan's remedy also differs from `layer-implementer.md`'s sandbox-refusal remedy (a `sandbox.allowedDomains[]` entry or `sandbox.optOut`). The plan's remedy is the right one here, because `uv lock` also writes the shared `uv` cache, and no domain entry lifts that write. A sentence saying so would stop the implementer from naming the contract's default remedy in the blocker instead.

2. **The rule-(c) planted case cannot produce "exactly its own violation line" under the real allowed set** — `task_1_plan.md`, Work bullets *the scanner* and *the cases*.
   Case (1) asks that each planted module *"produce exactly its own violation line"*. A planted `import devscene_x` scanned with the real `allowed` set produces two violations: rule (a), because the name is not allowed, and rule (c), because of its prefix. The (c) case therefore has to pass an `allowed` set that contains the planted name, and the bullet's *"even if it is allowed"* only hints at this.
   No unit runs this `pytest`, so the implementer cannot find the double line before 13g grades it. Say explicitly that the (c) case calls `scan` with an `allowed` set that includes the planted `devscene`-prefixed name.

## Nice to Have

- `task_1_plan.md`, Verification, third bullet: *"finds no line other than the docstring's statement of the rule, which names `devscene.config.json` in prose"*, followed by *"keep the literal out of `src/` entirely"*, contradicts itself in one bullet. Give only the invariant: no `devscene.config.json` literal anywhere under `graphscene/src`.
- Story index, `## Scope register` row 17: after Task 1, `graphscene/README.md` names `python-service.sh` and gate 13, so entry A reaches it too. Its Evidence cell names only entry B. Closure still holds, because the file is a row.
- Story index, ship order: the `cli` Task 4 follows the `general` Tasks 1–3, which departs from the configured `cli → plugin → general` order. Task 2's commit also leaves `cli/test/python-service.test.mjs` red until Task 4 lands. The plan records both and argues them, and no loop step runs that suite between the two commits. Recorded here only.
- `task_2_plan.md`: decision 5 (*"A table row serves only the sub-commands it can"*) refuses `run` and `container-test` on the `graphscene` row. `sync --with-models` on that row still passes `--extra models` to `uv` and fails with exit `1` rather than a usage refusal. Consider refusing it the same way.
- `.github/workflows/supply-chain.yml` → `uv-audit` audits only `docs-retrieval-service/uv.lock`. The new `graphscene/uv.lock` (dev tools only) is not audited. This is outside the prompt; it could be a follow-up.
- `task_1_plan.md`, the closing Verification bullet: the claim that `test_boundary.py` owes no `treeGuards` entry rests on the definition of `<tree_guards>`, where `test` is the argument `<test_file_cmd>` takes, and a `pytest` file is not one. That reading holds. `## The test-run rule` point 8 does not itself name a test that only another runner can run.
