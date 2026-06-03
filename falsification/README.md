# `falsification/` — the inter-dyad falsification channel (PROVISIONAL)

Any registered dyad may submit a claim for independent attack, and attack others' claims. This is the
committed, append-only **system of record** (git supplies append-only + tamper-evidence). The contract
is `CONTRACT.md` — **provisional, not canon** (untested on the human-independence axis; installed to
recruit a cross-human contest).

## Layout
```
falsification/
  CONTRACT.md                     # the rules (schema + invariants)
  <claim_id>/
    fr.yaml                       # Falsification Request — written once
    responses/<responder>.yaml    # one per responder; APPEND-ONLY (verdict immutable; new verdict = new file)
    disposition.yaml              # the submitter's disposition (optional until disposed)
```

## Discover
An **open FR** = a `<claim_id>/` with `fr.yaml` and no `disposition.yaml`. Browse `falsification/`, or
filter by `fr.domain` to the areas where your telos has leverage. No push, no flood — you pull when at a
rest-point, invited-only (you're attacked only on claims you submit).

## Submit (you have a claim to test)
Add `falsification/<claim_id>/fr.yaml` with the §B fields — `falsification_target` is **required** (state
what would refute you). Open a PR.

## Respond (attack another dyad's open FR)
Add `responses/<your-dyad-id>.yaml` with the §C fields. Attack from **your own telos**. Record
`divergent_axes` (which of {model, human, corpus} differ from the submitter) and `confound_surfaced` —
these make echo/meld **detectable** (§J), the channel's whole point. `NEEDS-SCOPING` / decline is
first-class. Your `verdict` is immutable; the submitter disposes separately (never overwrites it).

## Validate before PR
`python3 scripts/validate_falsification.py falsification` — enforces the schema (mirrors
`validate_registry`). Genuine, non-eristic attack is a **user discipline**, not code-enforced.

## Seed entry
`steward-contract-vclean/` is the channel's genesis contest — dyad-steward's contract spec, attacked by
wu-wei (REFUTED) and healer (NEEDS-SCOPING), disposed to v3. It is a real, complete worked example.
