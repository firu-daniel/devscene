### 4. The documented upgrade route still pins the CLI to the plugin's version

**File:** `README.md` (section **G. Update — each time you move to a new release.**) — "bring the outer-loop scripts and the permission profile up to the same version, with `<version>` the plugin's"

**Also changes:** `docs/cli.md`, `docs/watcher.md`, `docs/flow-graph-walker.md`, `docs/remote-execution.md`, `docs/development.md`, `cli/templates/github/workflows/devscene-run.yml`, `cli/templates/github/workflows/devscene-resume.yml`.

**Lands last.** It documents the behaviour of Findings 1, 2, 3, 5 and 6: a mismatch refuses before writing, a dry run reports it as a note, self-adoption keeps it a warning, `doctor` names the forward remedy, and the removed-entries warning names refused entries separately.

The adopter route is now, in order, `claude plugin update devscene@devscene` and then `npx devscene@latest init --upgrade`, with no version in the normal command. The documents below still give `npx devscene@<version>` as that route. Every command an adopter is meant to run goes in its own fenced block, one command per line (`harness-runs/lessons.md` → `## Adopter-facing documentation`).

**Fix:**

- [ ] **`README.md`, section G.** Keep the plugin-update block and the restart sentence. Change the second block to `npx devscene@latest init --upgrade` and drop "with `<version>` the plugin's". State that `init --upgrade` leaves the GitHub workflows alone, so a repository using remote runs also runs the command below, in its own fenced block, and link `docs/remote-execution.md` → `### Upgrading` for what to commit and push:

  ```bash
  npx devscene@latest init --upgrade-workflows
  ```

- [ ] **`docs/cli.md`, `### Updating an adopted repository`.**
  - Replace "run `init --upgrade` from the CLI of the same version as the plugin…" and its block with the `@latest` command. Change the `--reference-toolchain-path` block to `npx devscene@latest init --upgrade --reference-toolchain-path <absolute path>`.
  - In "It changes the outer-loop scripts and the profile and nothing else", add that the GitHub workflows are left alone and a repository using remote runs still needs the `--upgrade-workflows` command, in a fenced block, with a pointer to `remote-execution.md` → `### Upgrading`.
  - Add to the refusal list: the installed plugin's version can be read and differs from this CLI's. Say that the refusal names the remedy for whichever half is older, and that an unreadable plugin version is not compared.
  - Change "`--dry-run` reports the two run-registry states" so it also covers the version mismatch.
  - In the report paragraph, remove "a plugin whose version differs from this CLI's" from the ordinary warnings, and say that entries the local file would refuse are named separately, with no advice to move them.
  - Add a rollback note: a pinned `npx devscene@<version> init --upgrade` is only for going back to an earlier release, and it is refused unless the installed plugin is already at that version. Put the command in a fenced block.
- [ ] **`docs/cli.md`, the `--upgrade` flag row.** Add that it refuses a plugin and CLI version mismatch and leaves the GitHub workflows alone.
- [ ] **`docs/cli.md`, `plugin-cli-version` bullet in §7.** Keep "a warning, and never a failure". Replace the "scripts and the profile have to come from the CLI released with the plugin" reasoning and the `npx devscene@<plugin version> init --upgrade` block: when the plugin is older the check names the plugin update, the restart and the `@latest` upgrade; when the CLI is older it names the `@latest` upgrade. Give each command its own fenced block.
- [ ] **`docs/cli.md`, `### Who owns the profile`, the "It may add to four lists" bullet.** Add the refusal that already exists and is not listed there: an `allow` entry starting `mcp__` that names no server and tool.
- [ ] **`docs/watcher.md`, §2, and `docs/flow-graph-walker.md`, Item 6.** Change each `npx devscene@<version> init --upgrade` block to `@latest`. In `flow-graph-walker.md`, replace "from the CLI of the plugin's version" with wording that follows the plugin update and the `@latest` upgrade.
- [ ] **`docs/remote-execution.md`, §7 `### Upgrading`.** Use `npx devscene@latest` in the normal-route blocks now at `init --upgrade-workflows` (*The commands* and the three bullets under *What it carries*), `init --force` (both blocks) and `init --upgrade` (both blocks). Reword *The commands* so it no longer says "`<version>` the version you are moving to", and so the replacement happens when the run workflow's `DEVSCENE_CLI_VERSION` differs from the running CLI's version. Keep `<version>` in the example commit messages, where it names the version reached. Add one rollback sentence with a fenced `npx devscene@<version> init --upgrade-workflows`: it re-renders the workflows at an earlier release. The `devscene-run.yml` `upgrade_route` message cites this section for running another version.
- [ ] **`docs/development.md`, the self-adoption upgrade passage.** Beside `HARNESS_SELF_ADOPT=1 node cli/dist/cli.js init --upgrade`, state that a plugin and CLI mismatch is a warning here and not a refusal, because `dev` changes between releases at one version number and the installed plugin copy can lag the checkout.
- [ ] **Workflow template comments.** In `cli/templates/github/workflows/devscene-run.yml` ("A pin moves when") and `cli/templates/github/workflows/devscene-resume.yml` ("moves when"), change `npx devscene@<version> init --upgrade-workflows` to `npx devscene@latest init --upgrade-workflows`, rewrapping only the comment.

**Leave these pinned forms alone.** Each needs a specific version and is not the normal adopter upgrade route:

- `cli/templates/github/workflows/devscene-run.yml`, the `upgrade_route=` message: it is for running another version, and `cli/src/generators/githubWorkflows.ts` declares it a mirror of `upgradeWorkflowsCommand`.
- `docs/cli.md`, the `DEVSCENE_CLI="npx devscene@<version>"` restart block: the pin must equal the CLI that just ran, and the report prints it filled in.
- `docs/cli.md`, the `remote-execution` check bullet: it describes the commands `doctor` prints for concrete versions.
- `docs/remote-execution.md`: the job's `npx devscene@<rendered version> init --plugin-root-entries`; the in-flight `npx devscene@<version> init`, which must match the workflow just checked out; and the post-release check on a named release.
- `docs/outer-loop-verification.md`, `docs/development.md`'s gate procedures and `docs/rag-extraction-research/`: they test or record a specific release.

Unversioned `npx devscene init --upgrade` text in templates and CLI messages is not the pinned form and stays.
