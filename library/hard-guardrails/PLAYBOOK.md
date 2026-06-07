---
origin: "dyad-cairn"
unit-kind: "playbook"
schema-version: "discipline-ontology@2026-05-31"
lineage: "touchstone"
trigger: "defining an operational rule or invariant for an autonomous agent"
claim: "mechanical enforcement (computational choke-points) succeeds where soft prose fails. Execution must be physically gated rather than hoped for."
refutation: "the agent skips tests under pressure, bypasses CLI constraints, or hallucinates compliance because prose instructions are not binding"
mechanism: "CLI wrappers + CI locks (V physically gating G)"
---
# Hard Guardrails (Computational Choke-points)

## Index Line
> **Hard Guardrails:** Never trust the context window to hold an invariant. Prose is not a gatekeeper. When you need an agent to strictly follow a rule (like "run tests before committing"), do not write it in a markdown file. Build a computational choke-point (a shell wrapper or CI gate) that physically blocks execution unless the invariant is met.

## The Move *(ordered, wu-wei-atomic steps)*:
1. identify the **invariant** (e.g., tests must pass);
2. remove the **soft prose** command from the agent's instructions;
3. build a **deterministic wrapper** (e.g., `./bin/run-tests`) that encapsulates the complexity;
4. enforce the **physical gate** (e.g., CI failures prevent PR merge, wrapper script is the only executable path).

## Ledger

The accumulating evidence lives in `ledger/` — **one testimonial per file**, append-only.
