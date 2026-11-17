### 1. The core's `<escalate>` row and both autonomous Override D `not_written` gates restate the cases the core's `### D.1` routes

**Severity:** Must Fix. This is a `harness-runs/lessons.md` named check: *"State a new behaviour once, in the section that decides it, and cite it from everywhere else; never re-walk in prose the cases that other arms or sections already route."* It is codified in `.claude/context/plugin.md` → `## Writing agent prose` as "Each rule is stated once".

**Sites:** three, all added by this branch.

- `plugin/instructions/plan_orchestration_instructions_core.md`, the `<escalate>` row of the bindings table. The quoted substring:

  ```
  D.1's `statistics-plan-writer` route — an `outcome` of `not_written`, or a third failing return — is **not** a site
  ```

  The base had ``D.1's `statistics-plan-writer` `error:` is **not** a site``; Task 5 rewrote it into the case list above.

- `plugin/instructions/plan_orchestration_instructions_autonomous.md`, the Override D paragraph that opens with the bold `not_written` gate heading, `(skip on failed write).` The quoted substring:

  ```
  If D.1 took its `not_written` route (an `outcome` of `not_written`, or a third failing return — the core's `### D.1`) (e.g., the story index is missing)
  ```

- `plugin/instructions/user_review_fixes_instructions_autonomous.md`, the same Override D paragraph. The quoted substring:

  ```
  If D.1 took its `not_written` route (an `outcome` of `not_written`, or a third failing return — the core's `### D.1`) (e.g. the story index is missing
  ```

**Problem.** The core's `### D.1` decides which returns take the non-halting route: *"An `outcome` of `not_written`, or the third consecutive return that fails the check … This is this dispatch's `error` route"*. That core is `plugin/instructions/plan_orchestration_instructions_core.md` for the first two sites and `plugin/instructions/user_review_fixes_instructions_core.md` for the third.

Each site only needs to name the route and cite the section that decides it. Each also lists the route's two cases, which gives that list three more owners. Suppose the core's D.1 arm changes, for example by adding a case. These copies then drift silently: the `<escalate>` row stops matching the set of returns that are not a halt site, and the forks' commit gate stops matching the route that the Done-summary bullet omits.

The core's own D.2 **Branch statistics** bullet names the route without the list, and so do both forks' Override I bullet and `plugin/instructions/improvement_observations_instructions.md`. Each fork gate also has two parentheticals back to back.

**Fix.** Replace each case list with a citation of the section that decides it. Leave the rest of each sentence as it is.

In `plugin/instructions/plan_orchestration_instructions_core.md`, in the `<escalate>` row, replace

```
D.1's `statistics-plan-writer` route — an `outcome` of `not_written`, or a third failing return — is **not** a site
```

with

```
D.1's `statistics-plan-writer` `not_written` route (`### D.1`) is **not** a site
```

In `plugin/instructions/plan_orchestration_instructions_autonomous.md`, replace

```
If D.1 took its `not_written` route (an `outcome` of `not_written`, or a third failing return — the core's `### D.1`) (e.g., the story index is missing)
```

with

```
If D.1 took its `not_written` route (the core's `### D.1`; e.g., the story index is missing)
```

In `plugin/instructions/user_review_fixes_instructions_autonomous.md`, replace

```
If D.1 took its `not_written` route (an `outcome` of `not_written`, or a third failing return — the core's `### D.1`) (e.g. the story index is missing
```

with

```
If D.1 took its `not_written` route (the core's `### D.1`; e.g. the story index is missing
```

This sentence's closing parenthesis comes later, after ` — the path the existing Phase D already handles …`. Leave it there.

**Check:** `git grep -n 'or a third failing return' -- plugin` prints nothing.
