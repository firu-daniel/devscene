`feat_graphscene_walker_engine` builds GraphScene's walker: the state machine that walks a declared graph and says what runs next, without launching anything. Part of #376.

## Why

`flow-walker.sh` is generic at its core but written in bash 3.2 + jq 1.5 and carries harness rules. The aim is a generic core written in Python from the start, not a line-by-line port. The `flow-walker*.test.mjs` suites show what behaviour is expected.

## Leads

_The leads below are starting points from #376 and the discussion that split it, not requirements. The planning session decides what holds when this branch is planned._

- The state store behind an interface (file store with locking first, the committed ledger later). Where such an interface lives is settled: a `typing.Protocol` an adapter implements and the engine drives is declared in `model`, and walk state, as plain types, goes there too (`.claude/context/graphscene.md` → `## The layers`).
- Walk, record, advance, counters and caps, resume through `current`.
- Fan-out/join rounds: a held `error`/`blocker` waits for its siblings, never cancelling them.
- Skips answered by the host, never read from config by the engine.
- The review loop's rules are left to #417.
- The engine routes on #413's declared primitives, never on names: an outcome's `verdict` and `held`, a binding's `interrupt` / `stop` / `end`, a predicate's `records` and `inRoundCounts`.
- A binding's `resumeOutcome` (`"answered"` in the harness graph) is not itself declared under `vocabulary.outcomes`, and `vocabulary_violations` does not check it. Whether it has to be a declared outcome is open.
- **What a loaded graph now guarantees** _From #415 as merged (#444, 2026-11-22)._ `load_graph` runs schema → build → vocabulary → static, the last as `Stage` `"static"`. A graph it returns has every node, counter, path, report-slot and prompt name resolved, `start` listed in `entries`, every node reachable from `start` and reaching a terminal or a `stop` binding, every fail-verdict cycle capped, and every round's gates and writer routed as checks 8 and 9 require. The walker can rely on that instead of checking it again.
- **The cost for the walker's tests:** every test graph loaded through `load_graph` has to pass all of those checks, `start-in-entries` included. A deliberately partial graph (an unreachable corner, a missing terminal) is rejected at load. The suites either build complete graphs from `valid_generic.json` or get an unchecked one from `graphscene.adapters.builder.build_flow_graph`, which is not exported from the package root but which the engine suites already import directly (`graphscene/tests/engine/test_vocabulary.py` → `_graph`).
- `graphscene.static_violations(graph: FlowGraph)` is public, so the walker can re-check a graph it holds.

## Depends on

#414, #415 (a graph `load_graph` returns has passed the static checks)
