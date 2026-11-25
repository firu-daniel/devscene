`feat_graphscene_executor_interface` defines how GraphScene runs a node: an executor interface, plus a stub executor for tests. Part of #376.

## Why

The engine shouldn't know what runs a node: the harness uses headless `claude` sessions, tests use a stub, other hosts something else. Retries, joins and the safety contract must behave the same with any executor.

## Decided (2026-11-25)

- **This branch ships only the interface and the stub.** The engine-driven run loop is #484, and the retry, join, breaker and park rules are #422, so this branch does not run a walk. The order is #420 → #421 → #422 → #484.
- **The interface is `asyncio`-based**: an executor runs a node as a coroutine. A round fans its gates out, the implementation unit loop will dispatch in parallel too, and GraphScene puts no limit on how many gates a round declares. Concurrent work on one event loop serves that without a thread per dispatch. `docs-retrieval-service` already uses `asyncio`; `graphscene` and `devscene-flow-host` use neither `asyncio` nor threads today. Step mode (#416) and the CLI (#452) stay synchronous.
- **The public surface and the stub's tests are this branch's callers.** No production code calls the interface until #421 and #484. That is expected for a library milestone and is not un-wired code.

## Leads

_The leads below are starting points from #376 and the discussion that split it, not requirements. The planning session decides what holds when this branch is planned._

- The executor classifies its own failures (`infra` retryable, `agent` reported, *undelivered*) so the engine never parses reasons.
- Validating a return against a schema the executor names, with a standard validator.
- A scriptable stub (outcomes, delays, failures, stalls) for the engine's tests from here on.
- **Who owns the stall timeout is open.** #421's leads give the stall timeout to the `claude` executor, and the stub here simulates stalls. The maintainer leans towards the engine at least reporting a timeout, as an HTTP client library does, whatever the executor detects on its own. With `asyncio`, a deadline around a node's coroutine is the engine's to set, and an executor may still classify a stall it detects itself. Planning settles the split, and #484's loop acts on it.
- **An adopter's synchronous executor.** An adopter with blocking code can wrap it, for example with `asyncio.to_thread`. Whether GraphScene offers a helper for that is for planning.
- **Two ways a host uses GraphScene, and the interface must serve both.** Step mode: the walker (#416) returns the next action and the host runs it however it likes, recording the outcome; GraphScene launches nothing. Run mode, built in #484: the host hands the engine an executor, and the engine drives the loop, applying #422's rules the same for any executor. LangGraph has only the second (`graph.invoke` runs the loop in the caller's process, and a node is the caller's own function); GraphScene needs an executor because its nodes are declared data, where `agent` is only a string something has to interpret.
- **Any provider plugs in here.** The interface names no provider: a Claude executor (#421), an OpenAI or local-model executor an adopter writes, a script or a human. #421 ships a generic `claude` one as an optional adapter; the stub here is the other built-in one.
- **An executor chooses no sandbox or permission setting.** Sandboxing, permission modes and allowed tools belong to the host, which passes them to its executor. LangGraph's core sandboxes nothing either; sandboxing there is a separate layer (Deep Agents' sandbox backends).
- **Resume re-runs a node.** LangGraph re-runs an interrupted node from its start on `Command(resume=…)`, so side effects must be repeatable; a re-dispatched GraphScene node is the same case, which matters for #423's hooks.

## Depends on

#419
