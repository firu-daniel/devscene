### Task 14 — Point the plugin contracts at `init --upgrade`

**Goal:** Correct the five plugin assets that state the profile's ownership or send a reader to the forced run for a profile refresh.

**Depends on:** Task 10, because these assets name the shipped flag.

The story index's `## Scope register` rows 57 to 60 and 101 are this task's sites. Replace words in place: `plugin/agents/layer-implementer.md` must not grow beyond what the changed behaviour needs.

### Targets

- `plugin/docs/AUTONOMOUS_FLOW.md`
- `plugin/instructions/prompt_injection_screen.md`
- `plugin/agents/layer-implementer.md`
- `plugin/scripts/README.md`
- `plugin/scripts/reserve-qa-user.sh`

**Work:**

- [ ] `AUTONOMOUS_FLOW.md`, row "Generated permission profile, selected per run": state that `init` generates the file, `init --upgrade` replaces it, and the adopter's additions live in `.claude/settings.autonomous.local.json`.
- [ ] `prompt_injection_screen.md`: in "What the person sees", change the likeliest fix for a refused call to `npx devscene init --upgrade`.
- [ ] `layer-implementer.md`, in **A sandbox refusal is the boundary working, in every mode.**: change the `init --force` that follows the `sandbox.allowedDomains` or `sandbox.optOut` edit to `init --upgrade`, keeping every other word.
- [ ] `plugin/scripts/README.md`, in **One adopter step these scripts need**: say hand-added helper entries survive `init --upgrade` as well as `--force`, through the existing plugin-root carry-forward.
- [ ] `reserve-qa-user.sh`, the header comment on the profile's `allowWrite` entry: change "changed without `init --force`" to "changed without `init --upgrade`", keeping every other word.

**Verification:**

- Re-running the story index's D1, D2, D5 and D6 entries over `plugin` reaches no site outside the register.
- `grep -c 'init --force' plugin/agents/layer-implementer.md` is lower than before this task, and the file's word count has not grown by more than the flag change requires.

**Deviations from plan:** The `plugin/scripts/README.md` edit goes past naming `--upgrade`, because the sentence would otherwise be false under it: the carry-forward now states its exception for an entry `.claude/settings.autonomous.local.json` supplies or the profile records as local (`cli/src/generators/permissionProfile.ts` → `LOCAL_ALLOW_RECORD_PREFIX`), and "the forced run" in the no-root-resolves arm became "the replacing run", because `cli/src/generators/profileUpgrade.ts` → `renderWith` takes the same carry-forward path.
