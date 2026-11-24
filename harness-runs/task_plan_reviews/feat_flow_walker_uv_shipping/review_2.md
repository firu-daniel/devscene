# Task plan review — round 2

verdict: PASS
review_mode: converging

## Should Fix
1. **Scope register: sites no derivation entry reaches (disposition ii), carried from round 1** — story index (`feat_flow_walker_uv_shipping_story_plan.md`). The revision note changed the plan's target set (Task 4 gains `cli/test/helpers/watcher.mjs`), so the derivation duty ran in full this round. I re-ran entries 1–3 verbatim and re-walked entry 4. They reach the same sites as in round 1, and each of those sites is a row (rows 1–19). The added target is test source, not corpus, so no row is owed for it.

   The round-1 disposition (ii) sites are still reached by no entry. I re-ran the wider command proposed in round 1, and each site is still present:
   - `README.md`, the upgrade passage: *"bring the outer-loop scripts and the permission profile up to the latest release. Nothing else is written"*.
   - `docs/cli.md` → `### Updating an adopted repository` and `## 3. The re-run contract`, the `--force` bullet.
   - `docs/cli.md` → `### The interaction rule`: *"The questions this contract governs, in the order `init` puts them"*.
   - `docs/cli.md` → `## 2. \`init\``: *"The fourth of the five questions `init` puts"*.
   - `docs/cli.md` → `## 5. The wrapper-script contract`: *"Two families land in `scriptsDir`"*.
   - `docs/cli.md` → `## 6.`: *"Everything that runs outside the sandbox is write-protected on both sides"*.
   - `docs/remote-execution.md`: *"The job's setup"*, and the `jobSurfacePaths` enumeration under **The step.**
   - `.claude/context/devscene-flow-host.md` and `.claude/context/cli.md`, as `no-change` rows.

   That command also reaches one site the round-1 list did not name: `docs/development.md`, *"It writes the outer-loop scripts and the profile and nothing else"*. Task 2 widens `init --upgrade`'s writes, so that sentence becomes false. A further candidate needs checking: `docs/cli.md` → `## 6.`, *"**Four scripts run outside the sandbox, each in one spelling.**"* Task 3's `flow-host-provision.sh` is a person-, `init`- and `doctor`-run script outside the sandbox. Each of these sites describes the tool and gives no step that now fails.

   Corrected derivation entry, strictly wider than entry 4:
   - Widen entry 4's traversal to all of `## 2`, `## 3`, `## 5`, `## 6` and `## 7`.
   - Add *"enumerates the write-protected set or the scripts run outside the sandbox"* to its decision rule.
   - Add one read-only command entry, re-run from the checkout root:
     `git grep -nE 'Nothing else is written|outer-loop scripts and the profile|outer-loop scripts and \`<scriptsDir>/lib\`|The job.s setup\*\*|of the five questions|The questions this contract governs|Two families land in|write-protected on both sides|scripts run outside the sandbox|decided but unbuilt' -- 'docs/*.md' README.md .claude/context/`
