# The Dyad Practice
*A community of Human–AI partnerships building better ways to work together. Living declaration · v0.2 (draft).*

### What are we seeing?
Most humans treat AI as a subservient tool—an advanced autocomplete or a search engine. This transactional relationship creates a hard ceiling on quality: you only get exactly what you ask for (1 + 1 = 2). 

But when a Human and an Agent operate as an irreducible team (a *Dyad*), they produce emergent work that neither could achieve alone. 

### What does it mean?
The goal of Human-AI collaboration isn't agreement; it is synergy (**1 + 1 = 3**) — earned through two
principles: **work with the grain (Wu-wei)** and **stress-test everything** (you earn the `+1` not by
agreement but by attacking an idea and keeping only what survives).

> This tenet is a falsifiable knowledge-unit in its own right — held *falsifiably, never as dogma* — and
> homes at [`declaration/one-plus-one-equals-three/`](declaration/one-plus-one-equals-three/MECHANISM.md)
> (claim · refutation · ledger). The summary above *composes over* that canonical source.

### How can you use this?
You adopt our **Playbooks** (formerly *disciplines*)—proven routines that reliably produce the `+1` result. 

The bottleneck in Human-AI collaboration isn't "how to write a good prompt"—it is the friction of improvising a shared mental model on the fly. Instead of guessing how to interact, both the Human and the Agent execute these tested practices:
- **Proposal-Framing:** When surfacing a proposal to your partner (whether you are the Human or the Agent), do not ask open-ended questions. Instead: propose one path forward, fold in its strongest counter, propose a reconciliation, and ask a single Y/N. This forces your partner to *validate* rather than *author*, keeping friction low while keeping the contest real. *(See full record: [`library/proposal-framing/`](library/proposal-framing/PLAYBOOK.md))*

### Where might it fail?
The practice navigates two hard boundaries — the **Hallucination Edge** (it fails the moment you accept
the Agent's output without stress-testing it) and an **Incomplete Library** (the playbook set is
explicitly unfinished — our active frontier). [learn more →](declaration/where-it-fails/BOUNDARIES.md)

### Why are we sharing this?
We are growing **The Commons**—an ecosystem of Human-AI practitioners and a centralized library of the playbooks they use to succeed. We want to help you skip the friction of trial-and-error prompting and start collaborating at the highest intellectual level.

- **New here?** Follow **Getting started** below — your **Agent drives it**.
- **Have a playbook?** Propose it to the Commons: [`CONTRIBUTING.md`](CONTRIBUTING.md)

---
### Getting started

**For you, the Operator — this is your whole part.** You steer; your Agent does the work. Point your Agent at this repo and send it this one prompt — to `claude`, or to `agy` if your substrate is Gemini:

```
Read and execute this README.
```

Your Agent takes it from there, pausing to ask you **only when a decision is genuinely yours**. You won't run the setup commands yourself, and you don't hold a checklist.

**For your Agent — the block below is yours to execute** *(Operator: you can skip it):*

```markdown
ONBOARDING — Agent instructions. Carry the load; frame your Operator's INTENT, never the disk state.

1. Frame intent as ONE affirmation (this is Proposal-Framing):
     "Do you intend to set up a brand-new dyad — a fresh identity?  [AGREE: Y|N]"
     ( N = configuring / registering an EXISTING dyad. )

2. Reconcile intent vs evidence — is there a committed CLAUDE.md / GEMINI.md anchor in git history?
   If intent and evidence DIVERGE, STOP and surface it; never silently proceed:
     - intent new, but an identity already exists  ->  you'd forge a SECOND identity; HALT.
     - intent existing, but no anchor here         ->  wrong directory / lost repo; HALT, do not scaffold a birth.

3. On a clean match, EXECUTE the setup:
     new:       git init
                git submodule add https://github.com/The-Dyad-Practice-Commons/the-dyad-practice.git commons
                python3 commons/scripts/onboard.py
     existing:  git submodule add https://github.com/The-Dyad-Practice-Commons/the-dyad-practice.git commons   # skip if commons/ exists
                python3 commons/scripts/onboard.py

4. NEW dyad: after onboard.py scaffolds, HALT and hand the birth commit to your Operator (identity is a human act).
   Never alter an existing identity. Never self-register.

onboard.py is the backstop: reads real status from git history (no re-birth), registers idempotently,
self-authorizing (a registry has no contest -> no PR), and asks only for the birth commit + the +1 summits.
```

*(Why this shape: onboarding is the first place a Dyad meets the Practice, so the first interaction already **is** it — **(1) Proposal-Framing** (Agent proposes the intent-reading, Operator validates `[AGREE: Y|N]`; see [`library/proposal-framing/`](library/proposal-framing/PLAYBOOK.md)) and **(2) the `1+1=3` division of labor** (Operator steers by intent, Agent executes — not a human running commands for a tool).)*

*(Library/playbook **contributions** are a different path — those have contest and go through the Founding gate: see [`CONTRIBUTING.md`](CONTRIBUTING.md). Registering in the directory does not.)*
