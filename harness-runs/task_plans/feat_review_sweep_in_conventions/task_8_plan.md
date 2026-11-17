### Task 8 — Make `branch-reviewer` take its Pass 0 grep sweep from `review-sweep.sh`

**Goal:** Replace the in-agent sweep table with one call to the main checkout's `review-sweep.sh`, whose rows come from the adopter's own `.claude/review-sweep.md`. The reviewer keeps the method: added lines only, every covered layer path, the `<state_dir>` exclusion, and every hit verified in context before it becomes a finding. A missing or unfilled sweep document becomes a reported configuration gap, never a blocker. Half (b) and the rest of the review are unchanged.

**Depends on:**
- **Tasks 2 and 3.** The script lands as `<scripts_dir>/review-sweep.sh` in every adopter's checkout, and the profile allow-lists it. The contract this task calls, restated so no reader needs Task 2's file:
  - **Invocation:** `bash <MAIN_REPO>/<scripts_dir>/review-sweep.sh --repo <repo_root>`, one plain command with no `$`, pipe or redirect.
  - **The rows:** read from `.claude/review-sweep.md` as `<default_branch>` commits it, applied to the added lines of `git diff <default_branch>...HEAD`, with each row's `Covers` minus its `Exempts`, and the whole `<state_dir>` tree excluded.
  - **Exit `0`:** no hits, nothing printed.
  - **Exit `1`:** one `<path>:<line>: <escape class>` per hit on stdout, `<line>` being the line in the branch's file.
  - **Exit `2`:** a configuration error, one stderr line naming the cause, such as the document absent from `<default_branch>`, still an untouched skeleton, a malformed row or an invalid regex.
- **Task 1.** The document's path is `.claude/review-sweep.md`. Its rows sit in the table under `## Sweep rows`, whose last column, `A hit is a candidate for`, is what a hit is checked against.

**Where this task stops.** This agent's return object is unchanged: the sweep's outcome goes in the index's Context paragraph. So `plugin/schemas/branch-reviewer.return.json` is unchanged. `skeptic-reviewer` and `review-plan-reviewer` neither run nor cite Pass 0's half (a), so neither is edited.

### Targets

- `plugin/agents/branch-reviewer.md`
- `plugin/instructions/main_repo_resolution.md` — the `## Who may cite this` roster.

**Work:**

- [ ] `## Resolved values`:
  - **Add the `<MAIN_REPO>` row**, copied byte for byte from the row `plugin/docs/AUTONOMOUS_FLOW.md` carries: `` | `<MAIN_REPO>` | derived at runtime | The main checkout — the path a bare `printenv DEVSCENE_MAIN_REPO` prints, else the path `${CLAUDE_PLUGIN_ROOT}/instructions/main_repo_resolution.md` → `## The fallback` resolves, and a stop with its sentence when it resolves none. Spell it as a literal absolute path in the command, never through a substitution or a variable. | ``
  - **Add a `<scripts_dir>` row:** config value, `scriptsDir`, the directory the outer-loop scripts live in.
  - **The `<repo_root>` / `<app_dir>` row:** drop "the Pass 0 sweep" from the list of things that scope to `layers[].path`. The caller check and the Leg 2 grep keep it.
  - **The `<impl_stack>` row:** drop the clause "You need them to write a Pass 0 regex and".
  - **The table's lead paragraph:** remove `<regex>` from the ordinary placeholders list.
- [ ] `## Read first`: add a bullet for the sweep document, `.claude/review-sweep.md` as `<default_branch>` holds it (`git show <default_branch>:.claude/review-sweep.md`, run bare from `<repo_root>`). It is where each hit's escape class and its "A hit is a candidate for" text are read. State in the same bullet that the document absent, unfilled or unreadable is **a configuration gap reported in the index's Context paragraph, never a `blocker`**. Leave the closing "A cited path you cannot read is a finding, not a fallback." paragraph's list of blocker inputs unchanged.
- [ ] Rewrite `### Pass 0 — the deterministic sweep` → **(a)**. Delete the "stub, to be edited" paragraph, the whole escape-class table, the *"add a row when `<state_dir>/lessons.md` records a new one"* sentence and the "An empty sweep list disables this half only." paragraph. Write instead:
  - **Run.** Run `bash <MAIN_REPO>/<scripts_dir>/review-sweep.sh --repo <repo_root>` once, as written. The script applies the method: added lines only, each row's covered layer paths, its exemptions, and the `<state_dir>` exclusion.
  - **Exit `1`.** Each printed `<path>:<line>: <escape class>` is a candidate. Read it in context with `git diff -U15 <default_branch>...HEAD -- <path>`, check it against that class's "A hit is a candidate for" text and the owning layer's conventions document, and file it as a finding only when it is one. Keep the existing examples of legitimate hits: the styling-token owner, test-attribute locator values, a test fixture's inline constant.
  - **Exit `0`.** Nothing to verify.
  - **Configuration gap.** Exit `2`, the script missing, the call refused, or `<MAIN_REPO>` unresolved — where the `<MAIN_REPO>` row's stop ends this half only — is a configuration gap. Quote the script's stderr line, or the refusal or stop sentence, in the index's Context paragraph. Half (b) and `## Common findings to look for` still run.
  - **No other grep.** Never build the sweep grep yourself.
  - Keep **(b)** byte-identical.
- [ ] `## Output contract` → **Files you write** → the Context paragraph bullet: add, to its headline conclusions, the Pass 0 sweep's outcome. That is the hit count and how many became findings, or the configuration gap with its quoted line.
- [ ] `plugin/instructions/main_repo_resolution.md` → `## Who may cite this`:
  - add `${CLAUDE_PLUGIN_ROOT}/agents/branch-reviewer.md` in its sorted place among the `${CLAUDE_PLUGIN_ROOT}/agents/` entries;
  - change "no document beyond these 27" to the number of entries the list then holds. Count the `- ` lines between `## Who may cite this` and the closing "A citer **points and never restates**" paragraph after the edit, since the file carries bullets in other sections too.

**Verification:**

- `git grep -n -E 'stub, to be edited|records a new one|Regex — \*replace' -- plugin` prints nothing.
- `git grep -n -F 'review-sweep.sh --repo <repo_root>' -- plugin/agents/branch-reviewer.md` resolves, and that line carries no `$`.
- `git grep -n -F '| `<MAIN_REPO>` | derived at runtime |' -- plugin/agents/branch-reviewer.md plugin/docs/AUTONOMOUS_FLOW.md` prints the two rows, byte-identical after the path prefix.
- The roster's stated count equals the number of `- ` entries under `## Who may cite this`.
- `plugin/schemas/branch-reviewer.return.json` is unchanged from `dev`, and `### Return fields` lists the same fields as before.
