### 4. "returns its return object" in the two Override D trigger sentences

**Severity:** Nice to Have.

**Sites:** each is the Override D paragraph that opens with the bold `Trigger / ordering.` label, and each contains the same quoted substring, `dispatch returns its return object and`.

- `plugin/instructions/plan_orchestration_instructions_autonomous.md`
- `plugin/instructions/user_review_fixes_instructions_autonomous.md`

**Problem.** Task 5 replaced the old text, which said the dispatch "returns its contract" and listed the old `key:` lines, with "returns its return object". The new wording repeats "return". The sentence only needs to say that the commit runs after D.1's dispatch has returned.

**Fix.** In both files, replace

```
dispatch returns its return object and
```

with

```
dispatch returns and
```

Change nothing else in either sentence.
