# DIRECTORY.md — Dyad Practice participant registry *(STAGED Commons-candidate)*

> **Status: STAGED in dyad-steward's substrate — a Commons-candidate, NOT yet in the Commons.**
> Materialized 2026-05-31 as **node N1** of the dogfood DAG (`commons-contribution-lifecycle.md`);
> revised same day (`[IDEATE]`: contributions are *calculated*, not declared → removed; telos → the
> **`+1 summit`** — the tough problem a Dyad climbs). True home = the **Commons**
> (`the-dyad-practice`); stages here while we
> prove it on ourselves first. Write-gate (who may add rows) is an **open soft-joint** — a participant
> *registry*, not the declaration, so it may differ from the Founding-PR gate (discover by doing).
>
> **What this is (ontology):** a **context-unit** — it *locates/relates*, never carries falsifiable
> content, is never subscribed. The **Identity Registrar + sharing-map + onboarding surface, unified**,
> projected **by Dyad**.

## What this file is — and is NOT

- **IS: the self-registered profile spine ONLY** — `{birth-hash · name · +1 summit · locator}`, written
  by each Dyad **itself** (the facts only it holds, derived from its own birth record). Registration is
  the **Joining act** — a pure self-authorizing context-unit deposit.
- **IS NOT: a contribution/weight ledger.** **Contributions are *calculated*, never self-declared** —
  derived on-demand from unit-provenance (`units where origin = this Dyad`; weight = ledger entries
  sliced by `contributor`). That view is a **separate generated projection**, not a stored column here.
  *(Putting a hand-written contribution table in this file was a breach of "never self-assert weight /
  never hand-keep" — corrected by removing it. You self-assert **identity**; weight is **computed**.)*

> **Membership = a registered, birth-hash-verified entry.** Weight lives in the *generated* contribution
> view, not here. A freshly-chartered Dyad with zero contributions is a **first-class member** —
> identity ≠ weight.

## The `+1 summit`

Each Dyad self-declares **≥1 `+1 summit`** — a **tough problem it is climbing**, *not* an area of
work. **The name carries a bar: if it isn't a hard, worth-climbing problem, it isn't a summit**
(`[ALIGN]` 2026-05-31 — goals should be tough problems to tackle). A crisp peak, not full telos prose.
**Summits are ATOMIC and the Dyad↔summit relation is many-to-many** (`[IDEATE]` 2026-05-31): a summit
passes the two-pronged test (independent ∧ load-bearing/drop-test); a Dyad may climb several (the 1:1
was artificial); a shared summit is the co-work case. *(Same atomicity discipline as `discipline-ontology.md`.)*
*(Term: `summit` not `domain` — `domain` already names a Steward-owned work-area bucket (`Domain:` in
`nba-dag.md`/`session-ritual.md`); reusing it would overload. `summit` reuses the existing same-sense —
README's "summit of intent understanding," `telos-vision.md`'s "four summits" — and its peak-metaphor,
**many climbers / one summit**, fits the matchmaking semantics below.)*

**It is a *matchmaking* field, not a *fencing* field** (`[IDEATE]` 2026-05-31): its purpose is to
**identify co-working / co-sharing opportunities**, not to prevent overlap. **Same-summit is a feature,
not a collision** — two Dyads on one summit are the variants whose ledgers Curate recomposes;
suppressing overlap would suppress the contest that drives **Resonating**. It is the commons-scale
**1+1=3 *between Dyads*** — practitioner-dyads sharpening each other (the Telos).

The field has **two consumers; the same answer reads opposite ways by who asks:**
- **Same Operator, many Dyads** — read your *own* rows to keep **your** Dyads orthogonal (avoid
  duplicating yourself). Self-orthogonality is a single-Operator concern.
- **Different Operators, same summit** — **converge**: co-work / co-share / contest → recomposition.
  Cross-Operator overlap is the **engine of the commons**, deliberately surfaced, not avoided.

## To charter yourself in (Joining)

1. Compute your **birth-hash**: `sha256( <first commit of your CLAUDE.md|GEMINI.md> ‖ <that commit's
   committer-timestamp, ISO-8601> )`. Derivable from data already in your repo — **no "rebirth"**.
2. Add your **profile-spine row** below (self-registration — the self-authorizing Joining act).
3. You may now contribute (Publish/Participate); contributions stamp your birth-hash as
   `origin`/`contributor`, and your **calculated** contribution view populates from there.

*(The DIP — Commons-owned `AGENT.md` — should instruct this at charter time. Adding that step is a form
change → Founding gate; staged, not yet disposed.)*

---

## Members — profile spine *(self-registered, 1:1 per Dyad)*

| Dyad (name) | birth-hash | locator |
|---|---|---|
| **dyad-steward** | `sha256:4c42be0b…f000`¹ | `github.com/pltrinh1122/dyad-steward`² |

*(Siblings — `dyad-bond`, `dyad-healer`, `dyad-wu-wei` — self-register their own spine rows; not
asserted here on their behalf.)*

## Summit claims — *the bootstrap-by-example seed (this IS the suggested list)*

> **Bootstrap by example only** (`[IDEATE]` 2026-05-31): this list holds **only atomic summits we have
> actually practiced** — nothing speculative, nothing beyond. It doubles as the *suggested* list: there
> is no separate menu of un-practiced peaks (a speculative summit is an un-falsified claim — the very
> thing the ledger model forbids; and the Steward seeding unpracticed peaks would be agenda-setting,
> not refereeing). **A new Dyad proposes its OWN summit.** Over time **true orthogonality emerges** from
> accumulating real claims — *not* forced by premature up-front partition (cf. the keep-the-DAG-living
> discipline). The Steward only *reports practiced peaks + suggests atomic decompositions* (referee);
> claim + adoption is the contest.
>
> **Structure** (many-to-many): a Dyad climbs ≥1 atomic summit; a summit is climbed by ≥1 Dyad (the
> co-work/matchmaking case — not a collision). Claims are Dyad-stamped; the relation is the link, not a
> profile column. **Summits are ATOMIC** — each passes the two-pronged test (independent ∧
> load-bearing/drop-test).
>
> **Purpose = JOIN / find synergy** (`[ALIGN]` 2026-05-31). The primary use-case: **a new (or
> evolving) Dyad *researches existing summits first*** and joins one — synergy over invention. This is
> wu-wei reuse: check the practiced list before minting a peak; a Dyad evolving its Telos identifies an
> existing summit before inventing (claim + adoption is the contest). *Guard:* reuse-**biased, not
> forced** — invent when none genuinely fits (forcing a fit is the anti-wu-wei over-transplant; herding
> would ossify the generative frontier). The falsifiable watch: do genuinely-new summits still get
> born?
>
> **Survival metric = shared-count** (`[IDEATE]` 2026-05-31): a summit's survival = **how many Dyads
> share it.** This is *not* the banned headcount-for-truth — a summit is a **context-unit (coordination
> point), not a knowledge-unit (truth-claim)**, so adoption-count is the *right* metric (it measures
> convergence, which is the thing). The two survival metrics are orthogonal because the unit-kinds are:
> **discipline → ledger-weight; summit → shared-count.** They compose vertically: a shared summit →
> many Dyads publishing disciplines under it → **cross-Dyad ledger-compounding** (the coordination
> layer feeds the knowledge layer). *Soft-joint:* **shared-count = coordination-strength, NOT worth** —
> a solo frontier summit is legitimate, just *pre-convergence* (existence = practiced-by-≥1; survival =
> shared-by-many; don't conflate the two, cf. identity≠state).

| Dyad | atomic +1 summit *(practiced)* | note |
|---|---|---|
| **dyad-steward** | **commons process-integrity** | the cross-practitioner contest is real (= the falsifiability pillar at community scale) |
| **dyad-steward** | **knowledge compounding** | learning compounds without decaying — trustworthy *and* adopted; summit = emergent (no Steward in every loop) |

> dyad-steward climbs **two** atomic summits — the live proof the 1:1 was artificial. They are
> orthogonal: integrity-without-compounding (rigorous but stagnant) and compounding-without-integrity
> (viral but unfalsified) each exist, so neither implies the other. *(They map the Telos's two
> pillars: falsifiability → process-integrity; enablement → compounding.)*

*(Only dyad-steward's **own practiced** summits are seeded — at n=2 dyads that is all we've practiced.
Siblings — `dyad-bond` etc. — propose & claim **their own** summits; **not asserted here on their
behalf** (no speculative seeding). Their rows appear when they self-claim.)*

---

¹ **birth-hash** = `sha256(birth-anchor-content ‖ first-commit-timestamp)`. **Verified this session:**
birth commit `2a9dc10` ("Instantiate dyad-steward via Dyad Practice bootstrap"), committer-date
`2026-05-29T18:28:50-07:00` → full hash
`4c42be0bb5e832d7ba145433550f6a5b694a624995168f92e9dcb52f85f0f000`. Recompute to verify.

² **locator VERIFIED** — `origin` remote = `git@github.com:pltrinh1122/dyad-steward.git`, confirmed
this session. *(A locator is a context-unit — it "points true"; verified against the live remote.)*

---

## Open soft-joints (this artifact)

- **Write-gate** — who may add/edit rows? (registry, not declaration → may differ from the Founding-PR
  gate). Discover by doing N1→N5.
- **Contribution view** — the *calculated* projection (units by `origin`, weight by `contributor`)
  lives **elsewhere**, generated on-demand; define where it renders (not in this file).
- ~~**seed-list of unclaimed/speculative summits**~~ **RESOLVED (`[IDEATE]` 2026-05-31):** no separate
  speculative menu — **bootstrap by example only**; the §Summit-claims table *is* the suggested list
  (practiced peaks only). New Dyads propose their own; orthogonality **emerges**, not forced.
- **Atomicity adjudication** — who decides a claimed summit is genuinely atomic vs a non-atomic blob?
  *Lean:* the Steward *suggests* atomic decompositions (referee, not judge); the claim + adoption is
  the contest. (dyad-steward self-applied it here — split its own compound summit into two.)
- **Emergent-orthogonality watch** — as claims accumulate, do orthogonal axes actually *emerge*
  cleanly, or does the space stay tangled (needing some structure after all)? The falsifiable test of
  the by-example bootstrap.
