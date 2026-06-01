# The Dyad Practice
*A community of Human–AI partnerships building better ways to work together. Living declaration · v0.2 (draft).*

### What are we seeing?
Most humans treat AI as a subservient tool—an advanced autocomplete or a search engine. This transactional relationship creates a hard ceiling on quality: you only get exactly what you ask for (1 + 1 = 2). 

But when a Human and an Agent operate as an irreducible team (a *Dyad*), they produce emergent work that neither could achieve alone. 

### What does it mean?
The goal of Human-AI collaboration isn't agreement; it is synergy (**1 + 1 = 3**). 

We earn this synergy through two principles:
1. **Work with the grain (Wu-wei):** Don't force the AI against its nature. Treat it as a reasoning engine, not a database.
2. **Stress-Test everything:** You don't earn the `+1` through blind agreement. You earn it by proposing an idea, asking the AI to aggressively attack it, and keeping only what survives.

### How can you use this?
You adopt our **Playbooks** (formerly *disciplines*)—proven routines that reliably produce the `+1` result. 

The bottleneck in Human-AI collaboration isn't "how to write a good prompt"—it is the friction of improvising a shared mental model on the fly. Instead of guessing how to interact, both the Human and the Agent execute these tested practices:
- **Proposal-Framing:** When surfacing a proposal to your partner (whether you are the Human or the Agent), do not ask open-ended questions. Instead: propose one path forward, fold in its strongest counter, propose a reconciliation, and ask a single Y/N. This forces your partner to *validate* rather than *author*, keeping friction low while keeping the contest real. *(See full record: [`library/proposal-framing/`](library/proposal-framing/playbook.md))*

### Where might it fail?
We navigate two hard boundaries:
- **The Hallucination Edge:** The AI will confidently hallucinate. Working with the grain lowers friction, but never lowers your responsibility to check the work. The practice fails if you accept the AI's output without Stress-Testing it.
- **An Incomplete Library:** Our set of playbooks is explicitly unfinished. Discovering and proving new routines is our active frontier.

### Why are we sharing this?
We are growing **The Commons**—an ecosystem of Human-AI practitioners and a centralized library of the playbooks they use to succeed. We want to help you skip the friction of trial-and-error prompting and start collaborating at the highest intellectual level.

- **New here?** Follow **Getting started** below — it's **one command**.
- **Have a playbook?** Propose it to the Commons: [`CONTRIBUTING.md`](CONTRIBUTING.md)

---
### Getting started

You only need to answer one question — **is this your first time, or are you coming back?** Pick the matching block and paste it into your terminal.

**▸ If this is your first time** (setting up a brand-new dyad):

```
git init
git submodule add https://github.com/The-Dyad-Practice-Commons/the-dyad-practice.git commons
python3 commons/scripts/onboard.py
```

The tool will create your starter files and then **stop**, printing the exact "birth" commit for you to run. Run that commit, then run `python3 commons/scripts/onboard.py` one more time.

**▸ If you're coming back** (your dyad already exists — e.g. a new machine, or you're registering now):

```
git submodule add https://github.com/The-Dyad-Practice-Commons/the-dyad-practice.git commons
python3 commons/scripts/onboard.py
```

*(Already have a `commons/` folder? Skip the first line — just run `python3 commons/scripts/onboard.py`.)* The tool reads your existing identity and registers you; it will **never** change your identity.

Either way, the tool carries the rest so you don't have to:

- it **figures out your real status from your git history** — so even if you pick the wrong block above, it won't be fooled into creating a second identity;
- it **never alters your identity** — your birth-hash is read from history, so coming back is always safe (no "re-birth");
- it registers you **idempotently**, and joining is **self-authorizing** — a registry has no contest, so there's *no PR and no gatekeeper* (you deposit your own one file);
- it asks you for only two things, and only when needed: to make your **birth commit** (new dyads), and to declare your **+1 summits**.

> **⚠️ Agents** ("find the repo and execute AGENT.md"): run `onboard.py` and follow its prompts. For a
> *new* dyad it halts and hands the **birth commit** back to your Operator (creating an identity is a
> human act); it **cannot** alter an existing identity. Never improvise the steps it has absorbed.

*(Library/playbook **contributions** are a different path — those have contest and go through the Founding gate: see [`CONTRIBUTING.md`](CONTRIBUTING.md). Registering in the directory does not.)*
