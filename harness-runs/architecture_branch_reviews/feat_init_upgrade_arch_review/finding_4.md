### 4. Print the upgrade report's commands with the npx prefix

**Severity:** Should Fix (a presentation issue seen in passing, not a layering violation)

**Site:** `cli/src/upgrade/report.ts` → `UPGRADE_COMMAND`, quoted: `const UPGRADE_COMMAND = 'devscene init --upgrade';`, and `upgradeReport`, quoted: `a plain devscene init merges the ignore rule`

**Problem.** The report tells the adopter to run `devscene init --upgrade` and `devscene init`. The bare form resolves only where a global binary was installed, and no documented adoption path installs one. `doctor` names the same remedy as `npx devscene init --upgrade` (`cli/src/doctor/checks.ts` → `INIT_UPGRADE_COMMAND`), so the two surfaces disagree about one command.

**Rule source.** `cli/src/commands/init.ts` → the doc comment on `CLI`, stated "for the whole command surface": "an occurrence an adopter is told to *run* carries the `npx` prefix". The conventions documents do not state this rule, which is why this finding is not graded Must Fix.

**Fix.**

1. In `cli/src/upgrade/report.ts`, add `const CLI = 'npx devscene';`, the module-local form `commands/daemon.ts`, `commands/config.ts`, `commands/docs.ts` and `doctor/checks.ts` already use.
2. Define `UPGRADE_COMMAND` as `` `${CLI} init --upgrade` ``.
3. Write the ignore-rule warning with `` `${CLI} init` ``.
4. In `cli/test/upgrade-report.test.mjs`, update the three expected strings: `followed by another devscene init --upgrade.`, `a plain devscene init merges the ignore rule.` and `run devscene init --upgrade from the CLI matching the plugin.`
