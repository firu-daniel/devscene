### Task 6 — Read the `<MAIN_REPO>` corpus guard's expected carriers from the resolution module's roster

**Goal:** Make `cli/test/main-repo-resolution-corpus.test.mjs` take its expected set of `<MAIN_REPO>` clause carriers from the roster it already parses, `plugin/instructions/main_repo_resolution.md` → `## Who may cite this`, instead of from a literal map in the test. A plugin task can then move a carrier and its roster entry in one plugin-layer unit and keep the guard green. Task 20 does exactly that when it deletes `plugin/agents/committer.md` and makes the two semi-autonomous forks carriers.

**Why this ships first.** The suite is a tree guard over `plugin/**/*.md`. Today a carrier change in a plugin task fails that task's own guard run, and only a `cli` edit could fix it. This task changes no plugin file and keeps every check the suite makes against the corpus as it stands, so it passes now. It still fails on everything it fails on today, except a simultaneous, deliberate removal of a file from both the roster and the corpus.

### Targets

- `cli/test/main-repo-resolution-corpus.test.mjs` — this task's own test file, and the only file it changes.

**Work:**

- [ ] **Derive the clause case.** The `main-repo-resolution-clause` row's `expected` becomes `Object.fromEntries(roster.map((f) => [f, CLAUSE_COUNT_OVERRIDES[f] ?? 1]))`.
  - `roster` is the module's `## Who may cite this` list, parsed by the code the roster check already uses, hoisted so `CASES` can read it.
  - `CLAUSE_COUNT_OVERRIDES` is a new exported constant holding today's one non-1 count, `'plugin/commands/branch-start-user-review-fix-autonomous.md': 2`, with a comment saying why it is two.
- [ ] **Derive the binders.** `ROW_BINDERS` becomes the roster minus `Object.keys(EXEMPT)`, so the `main-repo-resolved-values-row` and `main-repo-literal-spelling` cases follow the roster too. The literal-spelling case keeps its explicit extra member, `plugin/instructions/prompt_injection_screen.md`.
- [ ] **Keep the checks.**
  - The forbidden patterns, `EXEMPT` and the module path stay as they are.
  - The roster check (`roster` deep-equals the clause carriers found in the tree) stays. It now compares the tree's actual carriers against the roster, and that comparison is what still catches a carrier missing from the roster and a roster entry without the clause.
  - Add one assertion that every roster entry names an existing file, so a roster left pointing at a deleted file fails by name.
- [ ] **Header.** Update the header's rule paragraph to say the expected carrier set is the roster. Add a dated **RED ONCE** note: in the working tree only, delete one roster line from `plugin/instructions/main_repo_resolution.md`, run the suite, record the failing assertion and its message, then restore the file byte-identical.

**Verification:**

- `npm test --workspace cli -- test/main-repo-resolution-corpus.test.mjs`, from the repository root as one plain foreground command, exits zero with `fail 0`.
- After the red-once restore, `git status --short -- plugin` prints nothing.
- `git grep -n "'plugin/agents/committer.md'" -- cli/test/main-repo-resolution-corpus.test.mjs` prints nothing: the file is no longer named in the suite, and it reaches the expected set only through the roster.
