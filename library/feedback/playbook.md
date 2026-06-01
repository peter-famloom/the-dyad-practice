---
origin: "sha256:4c42be0b…f000"
unit-kind: "playbook"
schema-version: "discipline-ontology@2026-05-31"
lineage: "none"
trigger: "the Agent produces an error or violates a constraint"
claim: "writing the exact rule to a permanent file prevents recurrence across sessions"
refutation: "the rule file bloats until the context window chokes · the rule is too specific to generalize"
mechanism: "falsification + codification"
---
# Feedback

## Index Line
> **Feedback:** When the AI errs, write down the exact rule it broke and save it to its core instructions to prevent recurrence.

## The Move *(ordered, wu-wei-atomic steps)*:
1. identify the **error**;
2. write the **invariant rule** that prevents it;
3. commit the rule to a **permanent instruction file** (e.g., AGENT.md).
