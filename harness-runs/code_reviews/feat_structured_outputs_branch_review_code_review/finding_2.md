### 2. `skeptic-reviewer`'s return-block sentence sits under the `FAIL` subsection, leaving the `PASS` path without a return instruction

**Severity:** Should Fix.

**Site:** `plugin/agents/skeptic-reviewer.md` → `## Output contract`, the subsections `### 1. No net-new findings — `PASS`` and `### 2. Findings — `FAIL``. The canonical sentence that opens `End your reply with your return object: one fenced code block whose info string is `json`` is now the second paragraph under `### 2.`

**Problem.** The old `### 1.` told the agent to return `verdict: PASS` exactly. The new `### 1.` says only:

```
If you have no net-new finding, **do not write any file**.
```

The instruction to end the reply with the return object was moved under `### 2. Findings — `FAIL``, directly after the FAIL path's write steps. Read in section order, it applies only to the FAIL path. The `blocker` outcome has no subsection either. `### Return fields` and the opening `There are three outcomes …` line do name `PASS`, so the contract is not missing the instruction outright, but it is ambiguous.

The PASS path is the one the caller most depends on. `plan_orchestration_instructions_core.md` → `### C2.1` routes an `outcome` of `PASS` straight to Phase E. A clean pass whose reply has no fenced block fails `agent_return_contract.md` → `## Reading a return` step 2. It is then re-dispatched, and after three such replies it takes `<escalate>`. In short, a clean skeptic review could halt the run.

The other four agents this branch adopts carry the sentence as the first paragraph of `## Output contract`, ahead of any per-outcome text; `plugin/agents/review-plan-reviewer.md` is an example. `cli/test/agent-return-schemas.test.mjs` only checks that the sentence appears somewhere in `## Output contract`, so it does not catch this placement.

**Fix.** In `plugin/agents/skeptic-reviewer.md` → `## Output contract`, cut this paragraph from under `### 2. Findings — `FAIL``:

```
End your reply with your return object: one fenced code block whose info string is `json`, holding one JSON object with exactly the fields `### Return fields` below lists for your outcome, with nothing after its closing fence.
```

Paste it, byte-identical, as the second paragraph of `## Output contract`. It goes right after the line that opens `There are three outcomes: `PASS`, `FAIL` and `blocker`. Pick exactly one.` and before `### 1. No net-new findings — `PASS``.

`### 2.` then holds only the `mkdir -p` / write paragraph. Change nothing else, and keep the sentence verbatim, because the static check matches it byte for byte.
