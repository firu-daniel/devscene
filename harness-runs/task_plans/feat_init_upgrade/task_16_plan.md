### Task 16 — Update the remaining adopter and contributor documents

**Goal:** Bring every other document in the scope register in line with the new route, including the update step adopters follow.

**Depends on:** Task 10 for the command. `docs/cli.md`, which these documents cite, is Task 15's.

The story index's `## Scope register` rows owned by Task 16 are this task's sites. Every command an adopter or contributor is meant to run goes in a fenced block, one command per line (`harness-runs/lessons.md`).

### Targets

- `docs/config.md`
- `docs/development.md`
- `docs/remote-execution.md`
- `docs/watcher.md`
- `docs/flow-graph-walker.md`
- `docs/github-issue-trigger.md`
- `README.md`

**Work:**

- [ ] `docs/config.md`: in `## 1.`, separate the generated profile from files the adopter owns after `init`, and name the local additions file. In the `docs.retrieval`, `sandbox.allowedDomains` and `sandbox.optOut` rows, make `init --upgrade` the route that reaches an existing profile; `docs.retrieval` also keeps the plain `init` its other files need.
- [ ] `docs/development.md`, **Regenerating this repository's adoption**: make the fenced `HARNESS_SELF_ADOPT=1 node cli/dist/cli.js init --upgrade` the route for script and profile changes, read first with `--dry-run`. Keep the forced run, its restore list and the wrapper paragraph only for other generated files.
- [ ] `docs/remote-execution.md` and `docs/github-issue-trigger.md`: make `init --upgrade` the outer-loop scripts' route at the sites the register marks `change`. The trigger and control workflows keep `init --force`. A commit step names the changed script paths. State that a job generates its own profile without the local file.
- [ ] `docs/watcher.md` and `docs/flow-graph-walker.md`: state that a released script fix reaches a checkout through `init --upgrade`, that hand-added plugin-root entries are carried by it, and that the walker's lag behind a plugin upgrade closes with that step.
- [ ] `README.md`, `### Adopting it in your own repository`: add the update step, with `npx devscene@<version> init --upgrade` in its own fenced block after the plugin update, and link `docs/cli.md`'s updating subsection.

**Verification:**

- Re-running D1, D2, D3 and D4 reaches only sites the register lists, and each `change` row's site now states the new route.
- `grep -n 'init --upgrade' README.md docs/development.md` finds each new command on a line of its own.
