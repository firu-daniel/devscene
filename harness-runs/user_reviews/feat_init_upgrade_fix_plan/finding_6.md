### 6. The removed-entries warning advises moving entries the local file refuses

**File:** `cli/src/upgrade/report.ts` (`removedEntriesWarning`, `refusedEntriesNotice`) — "list === ALLOW_LIST_PATH && namesUnstartedMcpServer(entry, startedMcpServers);"

**Also changes:** `cli/src/generators/permissionProfile.ts` (`namesBrowserTool`, `mcpEntryServer`) — "export function namesBrowserTool(entry: string): boolean {"; `cli/src/generators/profileUpgrade.ts` (`ProfileUpgradePlan`, `planProfileUpgrade`) — "startedMcpServers: enabledServers(rendered),"; `cli/src/upgrade/initUpgrade.ts` (`runInitUpgrade`) — "startedMcpServers: profile.startedMcpServers,"; `cli/test/upgrade-report.test.mjs`; `cli/test/init-upgrade.test.mjs`.

`removedEntriesWarning` treats only a `permissions.allow` entry for an unstarted MCP server as refused. `assertLocalAdditionsUsable` in `permissionProfile.ts` refuses two more shapes:

- a `permissions.allow` entry that starts `mcp__` and names no server and tool, such as `mcp__foo`, because `MCP_SERVER_PATTERN` does not match it;
- a `permissions.deny` entry for which `namesBrowserTool` is true.

The warning currently calls both movable. An adopter who follows it adds an entry that `readLocalAdditions` accepts and `assertLocalAdditionsUsable` then refuses, and every later render of the profile fails with that refusal, including the `init --upgrade` the advice says to run next.

`assertLocalAdditionsUsable` itself is correct and its conditions and messages do not change.

`upgradeReport` must stay pure (its module header), and `namesBrowserTool` reads the QA template through `browserServerNames()`. So the browser server names have to arrive as an input.

**Fix:**

- [ ] In `permissionProfile.ts`, give `namesBrowserTool` a second parameter, `servers: readonly string[] = browserServerNames()`, so existing callers are unchanged. Export a pure `namesMcpServerWithoutTool(entry)`: true when `entry` starts with `MCP_ENTRY_PREFIX` and `mcpEntryServer(entry)` is `undefined`. It may be used inside `assertLocalAdditionsUsable`'s existing branch only if that function's behaviour and messages stay identical.
- [ ] In `profileUpgrade.ts`, add `browserMcpServers: readonly string[]` to `ProfileUpgradePlan`, set from `browserServerNames()`. In `runInitUpgrade`, pass it to `upgradeReport`, and add the same field to `UpgradeReportInput`.
- [ ] In `report.ts`, classify each removed entry by its list:
  - `permissions.allow` and `namesUnstartedMcpServer`: the existing group, with its wording unchanged.
  - `permissions.allow` and `namesMcpServerWithoutTool`: a new group.
  - `permissions.deny` and `namesBrowserTool(entry, browserMcpServers)`: a new group.
  - Everything else stays movable, including a `permissions.ask` entry and a `permissions.deny` entry for a non-browser server.
- [ ] Generalize `refusedEntriesNotice` so each group gets its own sentence. Every entry is spelled out, and the movable advice never lists a refused entry. Use `was removed` / `were removed`, or `would be removed` under `--dry-run`:
  - `1 permissions.allow entry was removed and cannot be moved to .claude/settings.autonomous.local.json, because it names an MCP server and no tool: mcp__foo.`
  - `2 permissions.allow entries were removed and cannot be moved to .claude/settings.autonomous.local.json, because they name an MCP server and no tool: mcp__foo, mcp__bar.`
  - `1 permissions.deny entry was removed and cannot be moved to .claude/settings.autonomous.local.json, because a deny naming a browser tool would revoke the interactive-test agent's own grant: mcp__playwright__browser_click.`
  - The plural deny sentence follows the same pattern, starting `2 permissions.deny entries were removed`.
  - Build the path from `PROFILE_LOCAL_PATH`. Add a `permissions.deny` constant next to the use, or export one beside `ALLOW_LIST_PATH`.
- [ ] Keep `Any of these` in the movable advice whenever any group is non-empty, and `Anything` otherwise.
- [ ] In `cli/test/upgrade-report.test.mjs`, add `browserMcpServers: ['playwright']` to the `report` defaults. Add exact-wording cases for both new groups, singular and plural, real and dry-run; a mix of all three refused groups with a movable entry; a bare `mcp__playwright` in `permissions.allow`, which is refused even though the server is started; a non-browser deny, which stays movable; and a browser-named entry in `permissions.ask`, which stays movable. The existing wording cases stay as they are.
- [ ] In `cli/test/init-upgrade.test.mjs`, beside "a retired entry for a server the profile does not start is not sent to the local file", add a case that puts `mcp__retired-server` in `permissions.allow` and `mcp__playwright__browser_click` in `permissions.deny` of the on-disk profile. Assert both new sentences on a dry run and a real run, and no `still wanted` text.
