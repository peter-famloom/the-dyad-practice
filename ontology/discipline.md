# Discipline Ontology — the field-schema for a `discipline` knowledge-unit

> **version: 2026-05-31** *(this is the handle `schema-version` references; bump on any field-set
> change — a declaration-level change → Founding gate.)* A Commons knowledge-unit in its own right
> (claim + refutation + ledger), homed **separately from any instance** so the *schema* falsifies
> independently of the disciplines that conform to it. **Provisional — n=1** (seeking a second
> discipline to map). Origin: `dyad-steward`. Record shape: `ontology/discipline.md` (body, this gate)
> + `ontology/ledger/<contributor-hash>-<n>.md` (append-only; the ontology dogfoods its own structure).

## Claim (the schema's own falsifiable +1)

**`{trigger, move, claim, refutation, ledger}`** (+ `name` as identifier, `mechanism` as a derived
tag) is the **orthogonal, two-pronged-atomic** field-set for a `discipline` knowledge-unit —
*complete* (every real discipline maps with no leftover and no empty field) and *orthogonal* (each
field answers a question no other does, and **diffs independently**), so that **Curate is a diff, not
a judgment**: structure-divergence (different fields → maybe a fork) is mechanically distinguished from
content-divergence (same field, different atoms → a refinement to merge).

## Two-pronged atomicity (the criterion)

An atom (a field, and within a list-valued field each item) must be **both**:
1. **independent** — diffs cleanly (varies without forcing other atoms) — *orthogonality recursed to
   atom-level*; serves content-vs-structure discrimination.
2. **load-bearing (wu-wei)** — drop-tested: removing it loses the +1; serves subset-interpretability
   (B's `move` ⊂ A's `move` is a *refinement* iff the dropped atoms were non-load-bearing — else a
   *fork* asserting a different claim).

"wu-wei move" is the criterion *instantiated per list-valued field* (move → drop loses the +1;
refutation → each condition alone can kill; ledger → one survived dyadic-cycle), and it **stops the
atomization regress**.

## The fields

| field | role | atomicity |
|---|---|---|
| `trigger` | when it applies | survives both prongs |
| `move` | the ordered steps | each step wu-wei-atomic (drop-tested) |
| `claim` | the falsifiable +1 | **pinned separate from `refutation`**, collapse-flag armed (independence unproven at n=1 — a variant that tightens refutation while keeping claim proves it; else merge) |
| `refutation` | the kill-conditions | each condition independently sufficient |
| `ledger` | accumulated survived dyadic-cycles | each entry Dyad-stamped `{contributor, timestamp, testimonial}` |
| `name` | identifier *(context-unit, not a knowledge-field)* | drop-fatal but unfalsifiable |
| `mechanism` | form-catalog tag *(derived, not authored)* | computable from `move` |

## Refutation conditions (how this schema dies)

- **Leftover content** — a real discipline carries load-bearing content with no field to hold → incomplete; add a field (itself a schema-variant to contest).
- **A field never diffs independently** across real variants → not orthogonal → collapse it (the `claim`/`refutation` flag is this test, pre-loaded).
- **Atomicity fails to discriminate** — a subset-divergence stays uninterpretable even with the two-pronged test → the criterion doesn't earn its keep.
- **Sub-kind misfit** — `term`/`ritual` units can't use this set and no clean per-sub-kind schema emerges → it was over-generalized (then the claim's scope narrows to disciplines only).

## Ledger

Survived tests of *this schema* (distinct from any instance's ledger) live in `ledger/`. See
`ontology/ledger/`. **n=1** — seeking a second discipline to map.

## Open joints

- `mechanism`: drop entirely vs keep as derived tag · `claim`/`refutation` merge-or-keep (awaiting a
  2nd variant) · per-step drop-test as an admissibility gate · sub-kind generalization (term/ritual).
