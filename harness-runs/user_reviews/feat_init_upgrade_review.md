Context: the task prompt's `## Versions` section asked `init --upgrade` and `doctor` only to name a plugin and CLI version mismatch, and to document `npx devscene@<version> init --upgrade`. While reviewing the finished branch I realized that this leaves a real gap: the upgrade writes the scripts and the permission profile first and warns afterwards, so a repository can end up with a plugin and CLI from different versions. I am changing that decision in this review. The plugin and the CLI are released together at one version and should always match on a machine.

1. `init --upgrade` should refuse before writing anything when the installed plugin version can be read and differs from the running CLI version. The refusal moves the adopter forward: when the plugin is older, it says to run `claude plugin update devscene@devscene`, restart any open session, and upgrade again; when the CLI is older, it says to run `npx devscene@latest init --upgrade`. It should no longer recommend pinning the CLI to the plugin's older version.

2. `init --upgrade --dry-run` should report the mismatch as a note and still show what would change, as it does for the run-registry refusals. When the plugin version cannot be read, the upgrade proceeds, because there is nothing to compare.

3. In this harness repository, under `HARNESS_SELF_ADOPT=1`, a mismatch stays a warning rather than a refusal. `dev` changes between releases while the version number stays the same, and the installed plugin copy here can lag the checkout.

4. The documented adopter route becomes, in order, `claude plugin update devscene@devscene` and then `npx devscene@latest init --upgrade`, with no version in the normal command. Update `README.md`, `docs/cli.md` and any other document or template that gives the pinned form as the normal route. A pinned `npx devscene@<version>` may be mentioned only as a rollback route. The docs should also say that `init --upgrade` leaves the GitHub workflows alone, so repositories using remote runs still need `init --upgrade-workflows`.

5. `doctor`'s `plugin-cli-version` check stays a warning, and its remedy and the upgrade report's wording should follow item 1: update whichever half is older, never pin the CLI back to an older plugin.

6. The removed-entries warning from `init --upgrade` still sends two kinds of entry to `.claude/settings.autonomous.local.json`, which refuses them: a `permissions.allow` entry naming only an MCP server with no tool, such as `mcp__foo`, and a `permissions.deny` entry naming a browser tool. Treat them like the refused MCP entries already handled: name them separately and do not advise moving them there. Keep the local file's refusals as they are.

