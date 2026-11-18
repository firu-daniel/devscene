### Task 14 — Mark `Review severity markers` done in the roadmap

**Goal:** The roadmap shows this work as done and removes it from the outstanding-work index.

### Targets

- `ROADMAP.md`

**Work:**

- [ ] Set the `Review severity markers` row's status in `## Quality and testing` to `Done`. Keep its description unchanged.
- [ ] Delete the `Review severity markers` row from `## Index` and renumber every later priority down by one, keeping their order and links.

**Verification:**

- `grep -n 'Review severity markers' ROADMAP.md` prints only the `## Quality and testing` row, ending in `Done`.
- The `Priority` values in `## Index` run consecutively from 1 with no gap or repeat.
