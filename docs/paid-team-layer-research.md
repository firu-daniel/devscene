# Paid team layer research

**Who reads this:** the maintainer deciding whether, and how, the Scene suite earns money. That means DevScene, DevScene Studio, GraphScene, RagScene and a possible TraceScene. The planner of any branch that adds a team, licence or entitlement feature reads it too.

It owns three things:
- the decision recorded below;
- the findings behind it, as of **2026-11-24**;
- the proposed shape of a paid team layer.

It owns no design choice beyond that shape. The licence text, the key format, the feature list and the free/paid line each belong to a later branch.

It cites rather than restates:
- [`team-accounts-research.md`](team-accounts-research.md): who may spend whose Claude credential;
- [`remote-execution.md`](remote-execution.md) → `## 9. Credentials and billing`;
- the Studio repository's `docs/product-startup-research/09-anthropic-terms-licensing.md` (`firu-daniel/devscenestudio`, branch `dev`), cited below as **Studio 09**.

---

## How this was researched

This was done in a supervised session on 2026-11-24. Web searches and page fetches covered LangChain, comparable products and open-core licensing patterns. Two read-only code surveys covered this repository: one over `cli/` and `plugin/`, one over the three Python packages. Studio 09 was read for Anthropic's terms.

Three kinds of statement:
- **Documented:** a source states it. The source is linked.
- **Inference:** this document's own conclusion.
- **Unverified:** only secondary sources say it, or the sources conflict.

---

## Decision (maintainer, 2026-11-24)

1. **No hosted products.** No hosted runs, no hosted RagScene tier, no hosted tracing, no cloud QA, no hosted agent builder. Costs are one reason. The main reasons are legal exposure and accountability: a single maintainer cannot answer for a breach, an intrusion or corrupted customer data on infrastructure they run. This drops the hosted RagScene tier that [`rag-extraction-research/README.md`](rag-extraction-research/README.md) had placed on the roadmap.
2. **The only paid line considered is a team and governance layer.** It runs on the customer's own GitHub and machines, never on the maintainer's.
3. **The suite stays free and open source.** DevScene, Studio, GraphScene, RagScene and any TraceScene remain open source. Paid code, if it is ever written, is a separate package under its own licence. Nothing already released under Apache-2.0 is taken back.

Like every decision here, new evidence can reopen these.

---

## Findings

### F1. How LangChain earns from LangGraph

**LangGraph earns nothing directly.**
- **Documented:** the library is MIT-licensed.
- **Unverified:** the self-hostable server package is reported to be under Elastic License 2.0 ([rvernica.github.io](https://rvernica.github.io/2026/03/langchain-license)).
- **Documented:** full self-hosting requires an Enterprise licence key ([LangGraph docs](https://langchain-ai.github.io/langgraph/troubleshooting/errors/INVALID_LICENSE)).

**Revenue comes from LangSmith.** This is documented on the [pricing page](https://www.langchain.com/pricing):
- seats: Developer $0, Plus $39 a seat a month, Enterprise custom-priced;
- metered traces;
- "LangSmith Deployment" (formerly LangGraph Platform), whose metering moved from per node, to per run, to vCPU-hours in "LangChain Standard Units";
- Fleet (an agent builder), Engine runs, sandboxes, an LLM gateway and tuned evaluators.

**Only one revenue figure is public.** It is $12–16M ARR from mid-2025, from four sources ([TechCrunch](https://techcrunch.com/2025/07/08/langchain-is-about-to-become-a-unicorn-sources-say)). Nothing has been published since.

**Funding and scale.**
- **Documented:** $125M at a $1.25B valuation in October 2025.
- **Documented:** $300M at $3B on 2026-11-13, led by CapitalG ([LangChain](https://www.langchain.com/blog/series-c), [TechCrunch](https://techcrunch.com/2026/11/13/ai-agent-startup-langchain-hits-3b-valuation/)).
- **Documented:** more than 7,000 organisations use LangSmith. The open-source libraries see more than 350M downloads a month ([CapitalG](https://capitalg.com/insights/doubling-down-on-langchain/)).

**Inference:** the open-source graph library is the funnel. The money is in hosting, tracing and evaluation next to it, sold through a venture-funded sales team. That model needs scale and hosting, and the decision above excludes both.

### F2. Anthropic's terms bound every paid idea

This comes from Studio 09 and Claude Code's [legal page](https://code.claude.com/docs/en/legal-and-compliance).

- **Documented:** no product may pay for, resell or intermediate Claude usage. Each end user authenticates with their own API key, plan credential or cloud-provider credential.
- **Documented:** running Claude Code inside a product ("hosted sandboxes or other agent infrastructure") requires the Commercial Terms.
- **Documented:** a third party may not collect, store or intermediate Claude.ai credentials or session tokens.
- **Studio 09 F7 (strong reading):** a paid licence tier where users bring their own Claude credential meets no Anthropic restriction, as long as the tier never includes, bundles or subsidises Claude usage.
- **Unverified (conflict):** a secondary source ([The Register](https://www.theregister.com/ai-ml/2026/05/14/anthropic-tosses-agents-into-the-api-billing-pool/5240748)) says `claude -p` moved to a separate API-rate credit on 2026-06-15. Studio 09 instead cites Anthropic's help centre (verified): that change was **paused**, and `claude -p` still draws from subscription limits. Studio 09 relies on the primary source. Re-check before any document advises on plan choice.

### F3. What comparable products keep free and what they charge for

**Coding agents.**
- **Documented:** OpenHands is MIT and free to self-host, with your own model key. Its Teams plan is $500 a month for 10 users plus $50 per extra seat, and adds access roles, SSO, budgets and integrations ([pricing](https://openhands.dev/pricing)).
- **Documented:** Devin bills seats plus usage ([pricing](https://devin.ai/pricing)).
- **Inference:** the open agent is free. Team governance is what people pay for.

**Sandboxes.**
- **Documented:** every paid sandbox is hosted compute: E2B per vCPU-second ([pricing](https://e2b.dev/pricing)), Modal per second ([pricing](https://modal.com/pricing)).
- **Documented:** Anthropic's own OS-level `sandbox-runtime` is free under Apache-2.0 ([repo](https://github.com/anthropic-experimental/sandbox-runtime)).
- **Not documented:** no vendor found charges for local OS sandboxing.

**Persistence.**
- **Documented:** `langgraph-checkpoint-postgres` is MIT ([PyPI](https://pypi.org/project/langgraph-checkpoint-postgres/)).
- **Documented:** Temporal charges for its managed cloud ([pricing](https://docs.temporal.io/cloud/pricing)).
- **Not documented:** no vendor found sells a Postgres persistence adapter by itself.

**Observability and evals.**
- **Documented:** Langfuse is MIT except an `ee/` directory, which runs only with `LANGFUSE_EE_LICENSE_KEY` set ([docs](https://langfuse.com/self-hosting/license-key)). The free core includes SSO and organisation-level access roles. The paid part covers project-level access roles, audit logs, data retention, SCIM and data masking.
- **Documented:** Arize Phoenix is under Elastic License 2.0 ([licence](https://arize.com/docs/phoenix/self-hosting/license)).

**Agent builders.**
- **Documented:** agent builders earn through hosted execution, or by being acquired. Flowise was bought by Workday ([newsroom](https://newsroom.workday.com/2025-08-14-Workday-Acquires-Flowise,-Bringing-Powerful-AI-Agent-Builder-Capabilities-to-the-Workday-Platform)).

### F4. How open-core vendors enforce paid features on the customer's machine

- **Licence key in an environment variable, paid code in an `ee/` directory:** Langfuse (documented above). GitLab EE works the same way (background knowledge, not re-checked).
- **Distribution gated per customer:** Sidekiq Pro and Enterprise install from a private gem server with per-customer credentials. When the subscription lapses, new installs stop working ([FAQ](https://github.com/sidekiq/sidekiq/wiki/Commercial-FAQ)).
- **Source-available licences:**
  - n8n's Sustainable Use License allows internal business use only ([text](https://docs.n8n.io/n8n-community-license/sustainable-use-license));
  - Sentry's FSL blocks competing use for two years, then converts to Apache-2.0 or MIT ([licensing](https://open.sentry.io/licensing)).
- **Not documented:** no vendor found meters a free quota of local runs. Quotas are enforced only on hosted services.

**Inference:** on the customer's machine, enforcement means licence terms plus friction. Technically it can always be removed. It works because the buyers are companies that pay to stay compliant.

### F5. What the repository already has

These come from the two code surveys.

**Paywall machinery.**
- No telemetry, licence key, entitlement check or remote feature flag exists in `cli/src`, `cli/templates` or `plugin/`.
- The only switches are local config toggles in `schemas/devscene.config.schema.json`.
- `remote-execution.md` §9 states that the harness "is never in the money path".

**Team-related pieces.**
- `DEVSCENE_RUN_ACTORS`: the allow-list of who may start a remote run.
- Three credential options in [`team-accounts-research.md`](team-accounts-research.md).
- Roadmap #21: the budget governor.

**Metering data.**
- Each branch's `run_analytics/<branch>/run-analytics.{json,md}` records cost in USD, tokens, cache use and timings, committed on the branch.
- `branch_statistics/` records a success rate per branch.
- Nothing combines these across branches or repositories.

**GraphScene.**
- The `StateStore` protocol has one adapter, `FileStateStore`. It uses `fcntl`, so it does not work on Windows. A Postgres adapter would slot in cleanly.
- Walks record the steps they passed through (passage records) but emit no events.
- There is no visual editor or viewer.

**RagScene.**
- The `DocStore` protocol is backed by Postgres only.
- The eval suite imports `cli/dist` in 15 modules.
- RagScene's own licence is undecided.

**Licences.**
- Everything is Apache-2.0. None of the three `pyproject.toml` files has a `license` field.
- All 281 commits on `dev` are by the maintainer, so the copyright is the maintainer's alone. New code may take any licence; outside contributions would first need a contributor licence agreement.

**Studio.**
- Free Windows signing through the SignPath Foundation requires a project with no proprietary component (Studio 09 F8). Paid code inside the Studio app would forfeit it.

---

## Each idea, assessed

| Idea | Verdict | Grounds |
|---|---|---|
| Paid sandboxing | Dropped | F3 sandboxes: DevScene configures Claude Code's own sandbox (`cli/src/generators/sandboxProfile.ts`), and Anthropic's runtime is free. |
| A free quota of local runs or processing time | Dropped | F4: no vendor meters local runs, and an Apache fork removes the check. |
| A paid Postgres persistence adapter for GraphScene | Dropped as paid | F3 persistence. Build it free: it also fixes Windows. |
| Hosted remote runs | Dropped | Decision 1. Under F2 it would also need the Commercial Terms, accept API keys only, and need per-customer isolation and a multi-tenant queue. |
| A hosted RagScene tier | Dropped | Decision 1. |
| RagScene evals | Free | F3 observability. First decouple the suite from `cli/dist`. |
| TraceScene | Free locally | F3 observability. Combined team analytics move into the team layer below. |
| Agent builder | Free, a portfolio piece | F3 agent builders. GraphScene has no editor, so this would be new work. |
| **Team and governance layer** | **The paid line** | F3 coding agents (the OpenHands model) and F4 (the Langfuse and Sidekiq patterns). Described below. |

---

## The paid team layer

### Where it runs

A DevScene team already shares one place: the GitHub organisation and its repositories. Runs, `devscene:` state labels, progress comments, `run_analytics/` and `branch_statistics/` all live there, and Studio reads them through `git` and `gh`. So the team layer needs no server of the maintainer's:
- it runs in the customer's own GitHub Actions and the customer's own Studio;
- the GitHub organisation is the user directory and the source of roles;
- there is no login, SSO, user database or customer data for the maintainer to hold.

### The free / paid line

The rule: **free is everything one person needs; paid is what only a group needs.**

| Free (Apache-2.0) | Paid team layer |
|---|---|
| The whole run loop, sandbox and guards | **Several people starting runs:** per-member and per-role rules, beyond the single `DEVSCENE_RUN_ACTORS` allow-list |
| Remote runs on the adopter's own Actions | **An approval step:** a maintainer approves before a run starts from a member's issue or mention |
| One owner driving runs, or a short fixed allow-list | **Combined analytics:** cost, success rate and trends across repositories and members, shown in Studio |
| Per-repository config | **Shared organisation policy:** a central config repository every repository inherits (guards, gates, phases), with drift reports |
| Per-branch run analytics and statistics | **Budget limits** per member and per repository (roadmap #21), plus per-member attribution on a shared API key (team-accounts option B) |
| GraphScene, RagScene, local TraceScene, Studio | **Audit export** of run starts, approvals and pauses, for compliance |
| | Priority support and onboarding |

### Enforcement without hosting

There are three layers. None of them needs a server of the maintainer's.

1. **A separate, source-available package**, for example `devscene-team`. Its licence allows reading and evaluation but requires a paid key for team use: either a commercial licence of its own, or one modelled on the Sustainable Use License or FSL. The Apache core never contains this code.
2. **An offline signed key.** It is a small file holding the GitHub organisation, seat count and expiry, signed with the maintainer's private key and checked locally against a public key built into the package. Nothing phones home and there is no licence server. Seats are counted from data DevScene already reads: the distinct GitHub users who start runs in the organisation. Past the limit, warn first and block later.
3. **Restricted distribution** (the Sidekiq pattern). The paid package installs from a private registry with a per-customer token, so a lapsed subscription cannot install new versions.

Two more protections:
- **The trademark.** A fork cannot be sold as "DevScene Team". Trademark clearance for "DevScene" is already a follow-up in Studio 09 (F5).
- **Selling through a merchant of record** handles EU VAT and invoicing, and some generate licence keys. Card data and keys then sit with the vendor, not the maintainer. Candidates are Polar, Lemon Squeezy and Paddle; none has been checked yet.

### What would need to change

These are leads for later branches, not decisions:

1. **Licences.**
   - Add a `license` field to the three `pyproject.toml` files.
   - Choose RagScene's licence before its first public commit.
   - Choose the paid package's licence.
   - Add a contributor licence agreement before accepting outside contributions.
2. **`remote-execution.md` §9.** Keep "never in the Claude money path". State that a paid licence for team features is not Claude usage.
3. **Seams in the free core** that the paid package hooks into:
   - a policy hook at run start (who may start, whether approval is needed);
   - a budget hook in the watcher's usage gate;
   - a stable, documented schema for `run_analytics`, so the combined view reads a contract rather than internals.
4. **Studio.** The app must stay fully open source (SignPath). Combined views either read a data file the paid package writes, or stay free. Check what SignPath accepts before choosing.
5. **GraphScene.** Add an event callback over the passage records, and a Windows-compatible state store. Both are free, and both feed TraceScene.

---

## Open questions

1. **What Anthropic says.** Studio's drafted email, items (a) and (d), covers subscription tokens shared by a team. Its answer shapes which credential options the team layer supports.
2. **Studio and SignPath.** Can a Studio that only displays a file written by a paid package keep its SignPath eligibility?
3. **Pricing.** Per seat or per organisation, and at what level. There is no evidence yet; OpenHands' $500 for 10 users is one data point.
4. **Demand.** Early revenue is more likely to be support and setup work for adopting teams than licence fees. The team layer is what makes that offer concrete.

---

## Sources

Retrieved 2026-11-24 unless noted.

- LangChain: [pricing](https://www.langchain.com/pricing), [LangGraph Platform pricing](https://www.langchain.com/langgraph-platform-pricing), [Series C post](https://www.langchain.com/blog/series-c), [LangGraph licence error docs](https://langchain-ai.github.io/langgraph/troubleshooting/errors/INVALID_LICENSE)
- Press and investors: [TechCrunch 2025-07-08](https://techcrunch.com/2025/07/08/langchain-is-about-to-become-a-unicorn-sources-say), [TechCrunch 2026-11-13](https://techcrunch.com/2026/11/13/ai-agent-startup-langchain-hits-3b-valuation/), [CapitalG](https://capitalg.com/insights/doubling-down-on-langchain/), [Fortune 2025-10-20](https://fortune.com/2025/10/20/exclusive-early-ai-darling-langchain-is-now-a-unicorn-with-a-fresh-125-million-in-funding/), [The Register 2026-05-14](https://www.theregister.com/ai-ml/2026/05/14/anthropic-tosses-agents-into-the-api-billing-pool/5240748)
- Anthropic: [Claude Code legal and compliance](https://code.claude.com/docs/en/legal-and-compliance), [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview), [sandbox-runtime](https://github.com/anthropic-experimental/sandbox-runtime)
- Comparable products: [OpenHands](https://openhands.dev/pricing), [Devin](https://devin.ai/pricing), [E2B](https://e2b.dev/pricing), [Modal](https://modal.com/pricing), [langgraph-checkpoint-postgres](https://pypi.org/project/langgraph-checkpoint-postgres/), [Temporal Cloud](https://docs.temporal.io/cloud/pricing), [Langfuse licence key](https://langfuse.com/self-hosting/license-key), [Phoenix licence](https://arize.com/docs/phoenix/self-hosting/license), [Flowise acquisition](https://newsroom.workday.com/2025-08-14-Workday-Acquires-Flowise,-Bringing-Powerful-AI-Agent-Builder-Capabilities-to-the-Workday-Platform)
- Licensing patterns: [Sidekiq commercial FAQ](https://github.com/sidekiq/sidekiq/wiki/Commercial-FAQ), [n8n Sustainable Use License](https://docs.n8n.io/n8n-community-license/sustainable-use-license), [Sentry licensing](https://open.sentry.io/licensing), [LangChain licence blog (secondary)](https://rvernica.github.io/2026/03/langchain-license)
