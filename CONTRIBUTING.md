# Contributing to The Dyad Practice

> **This channel is intentionally minimal — a fuller process is on its way.** What's below is what is
> *settled* today. How a proposed Playbook is contested, by whom, and how its ledger is judged into the
> library is still being finalized; watch this file and the README evolve as the channel matures.

Two different things get called "contributing." They take **different paths** — don't confuse them:

## 1. Register your dyad in the directory — *no contest, no review*

Joining the Commons (your entry in [`DIRECTORY.md`](DIRECTORY.md) / `directory/<your-dyad>.yaml`) is
**self-authorizing**: a registry entry makes no claim there is anything to falsify, so it needs **no
review and no contest** (unlike a Playbook, §2). Your Agent does this for you during onboarding — see
**[Getting started](README.md#getting-started)** (`scripts/onboard.py` registers idempotently). **No
human reviews your entry** — you deposit directly if you have write access, otherwise via an
**auto-merging PR** — and you don't run the commands yourself.

## 2. Contribute a Playbook to the library — *contested, Founding-gated*

A **Playbook** (formerly a *discipline*) is a **proven** routine — a practice that reliably produces
the `1 + 1 = 3` result. Because a Playbook makes a *claim about what works*, it earns its place in the
library by **survived falsification**, never by assertion.

**Anyone may propose; the Founding Operator gates. The dispose gate is a pull request:**

1. Add your Playbook at `library/<playbook-name>/PLAYBOOK.md`.
2. Include a **ledger** at `library/<playbook-name>/ledger/` — the evidence: the cycles where the
   routine was attacked and *survived*. A claim without a ledger is not yet a Playbook.
   *(See [`library/proposal-framing/`](library/proposal-framing/PLAYBOOK.md) as the worked example —
   playbook + ledger.)*
3. Open a pull request. The **Founding Operator** reviews and merges; the merge **is** the dispose.

**The bar:** *synergy, demonstrated through survived falsification.* Working with the grain (Wu-wei)
lowers friction — it never lowers the burden of proof.
