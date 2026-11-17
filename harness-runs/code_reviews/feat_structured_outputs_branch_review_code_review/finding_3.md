### 3. Plural subject with a singular pronoun in the autonomous fork's "A review's questions are not an observation" bullet

**Severity:** Nice to Have.

**Site:** `plugin/instructions/plan_orchestration_instructions_autonomous.md`, the bullet that opens `- **A review's questions are not an observation.**`. Quoted substring: `are **never** written here: it names a decision owed **about this branch**`.

**Problem.** Task 2 and Task 3 rewrote the bullet's subject from one `## Questions` section into two fields, `` `branch-reviewer.questions` `` and `` `skeptic-reviewer.questions` ``. The pronoun that follows was not updated, so the sentence says "… are **never** written here: it names a decision …". The reader can still work out the meaning.

**Fix.** In that bullet, replace

```
are **never** written here: it names a decision owed **about this branch**
```

with

```
are **never** written here: each item names a decision owed **about this branch**
```
