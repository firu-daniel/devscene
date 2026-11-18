# general review — ### 4. The documented upgrade route still pins the CLI to the plugin's version — iteration 0

## Must Fix
1. **The in-flight route's `<version>` lost its only definition** — `docs/remote-execution.md` (`### Upgrading`, **Moving a run in flight to the new version, on purpose.**) — "npx devscene@<version> init"
   This diff removes "with `<version>` the version you are moving to" from *The commands*, which was the section-wide binding for this placeholder. The in-flight passage binds only `<branch>` ("With `<branch>` the run's branch"), so both `npx devscene@<version> init` and `git commit -m "Move <branch> to the harness workflows at <version>"` are now unbound. The two definitions left in the section do not cover it: "`<version>` the version the upgrade reached" is scoped to the commit message under *The commands*, and "`<version>` that release" is scoped to the rollback.

   An operator who has just been told to use `@latest` everywhere else in the section will reasonably run `npx devscene@latest init` here. That is the wrong command whenever `latest` has moved past the pin in the workflows just checked out: the fix plan itself says this `init` "must match the workflow just checked out". The next job runs `npx --yes "devscene@$DEVSCENE_CLI_VERSION" --cwd "$GITHUB_WORKSPACE" init --plugin-root-entries` and fails on any tracked file that run changes (`cli/templates/github/workflows/devscene-run.yml`, step `Generate the job's permission profile`, "changed tracked files"), so what the operator merged and committed under another version may not be what the job's `init` expects.

   Confirmed by reading `docs/remote-execution.md` and the workflow template; no job or `init` was executed.

   **Fix:** Extend the binding sentence to "With `<branch>` the run's branch and `<version>` the `DEVSCENE_CLI_VERSION` in the `devscene-run.yml` you take from the default branch:", or add the same definition directly above the `npx devscene@<version> init` block, so it covers that block and the commit message after it.

## Should Fix
1. **The restart command's `<version>` is no longer defined** — `docs/cli.md` (`### Updating an adopted repository`) — "DEVSCENE_CLI=\"npx devscene@<version>\" bash <scriptsDir>/restart-watcher.sh"
   The section used to define `<version>` as the plugin version; this diff correctly removes that sentence, but the restart block still relies on it. The block now has no definition in the section, and the next `<version>` a reader meets, directly below it, means an earlier release to go back to. The warning prints the command filled in, so a reader who copies from the report is safe; a reader working from this page has to guess. The fix plan keeps the pin because it "must equal the CLI that just ran", and the page does not say so.

   **Fix:** Change the lead-in to say the warning prints the command filled in, with `<version>` the version of the CLI that just ran.
