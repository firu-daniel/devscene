# Architecture review — round 4

verdict: PASS
review_mode: converging

## Incidental findings (not gating)
- **On `init --upgrade`, the carry-forward note will tell the adopter that `--force` kept their entries, although `--upgrade` refuses `--force`.** In `cli/src/generators/permissionProfile.ts` → `appendCarriedPluginRootEntries`, the resolved-roots note ends "so --force ${dryRun ? 'would leave' : 'left'} them in place rather than revoking a permission set that was pasted in by hand". Task 5's `renderCurrentProfile` sets `renderProfile`'s `force` from `carryForward`, which defaults to `true`, so an upgrade reaches this note. `planProfileUpgrade` returns `notes`, and Task 10 prints "the profile plan's `notes` with `info`". Task 4's revised sentence covers "every statement in `permissionProfile.ts` that the carry-forward exclusion, the local-file read or `init --upgrade` makes untrue", but its list names only the module header and doc comments, and no task rewords this message. This is message accuracy rather than layer placement, so it is outside this review's lens. Lead for the end-of-branch review: check the note's wording on an `--upgrade` run, real and `--dry-run`.
