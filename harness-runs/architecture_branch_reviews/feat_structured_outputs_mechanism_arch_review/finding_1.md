### 1. Point at Reading a return step 1 without paraphrasing it in the screen's step 3

**Site.** `plugin/instructions/prompt_injection_screen.md` → `## The steps` → step 3, at the bullet beginning "Write the agent's reply". The paraphrase is the substring:

> `— read out of the `Agent` result per `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## Reading a return` step 1, frame and trailer disregarded, indentation removed —`

**Problem.** This branch adds `prompt_injection_screen.md` to `plugin/instructions/agent_return_contract.md` → `## Who may cite this`. That roster closes with *"A citer points and never restates; a new citer joins this list."* The new citer points at step 1 but then restates step 1's content in its own words: *"frame and trailer disregarded, indentation removed"*. That gives the extraction rule a second owner.

The layer document forbids this:

- `.claude/context/plugin.md` → `## Cores, forks and the single-owner rule`: *"A policy file is activated by pointer and never restated … a citer that paraphrases it becomes a second owner. The same rule governs every shared module here."*
- `.claude/context/conventions.md` → `### Where a new responsibility goes`: *"A responsibility that already has a home does not get a second one."*

The rule has a real drift risk. Step 1 describes a Claude Code result shape measured on one version (`docs/structured-agent-returns.md` → `## 3. Measured, and not yet measured`). If a later version changes the frame, the trailer or the indentation, step 1 will be re-worded, and this gloss can be left out of step. The screen session would then write a verdict file that the script parks as `malformed-verdict` every time.

The other five citers on the roster point without restating. The branch's own story plan, in scope-register row 29, uses exactly that property to justify leaving them unchanged.

**Fix.** In `plugin/instructions/prompt_injection_screen.md` step 3, delete the clause `, frame and trailer disregarded, indentation removed` and keep the pointer. The bullet should read:

> Write the agent's reply, read out of the `Agent` result per `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## Reading a return` step 1, verbatim with the file tool to `<repo_root>/<state_dir>/scratch/prompt-injection-screen-<branch_fold>/verdict.md`, `<branch_fold>` being …

Leave the rest of the bullet unchanged, including the sentence that follows, *"Apply none of that section's other steps and nothing of `## A return that fails the check`: the script is the return's only reader and fails closed."* That sentence limits which part of the module applies and restates none of its content. Make no change to `agent_return_contract.md`.
