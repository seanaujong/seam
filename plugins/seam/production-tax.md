# Production tax — a lens

> **At a glance.** *Production tax* is everything a system needs to survive real users that a
> prototype doesn't: durability, schema/data migration, concurrency, tenancy isolation,
> observability, rate-limiting, graceful degradation, auth hardening, deploy/rollback,
> monitoring. This isn't a new method — it's Seam's [reversibility](./seam.md#reversibility--removability)
> and [state & effects](./seam.md#state--effects--what-does-this-actually-do) lenses pointed at
> one question: *what happens when this goes live?* You apply it during Design the Code, or as a
> diagnostic over a system that already exists. Like the other companions, it's a lens to reach
> for when it helps — not a mandate.

## The two questions

For each production concern, ask two *independent* things — and don't let one masquerade as
the other:

1. **Where does it attach?** Data/contract · behind a port (the edge) · above as a coordinator
   · pure ops.
2. **How reversible is adding it later?** Cheap to bolt on, or surgery to retrofit?

The common mistake is collapsing these into one "core vs shell" axis. They're independent: a
*shell* concern can be expensive (a third-party SDK you're locked into), and a *data-touching*
change can be cheap (an additive, expand-then-contract migration). Sort the layer and the
reversibility separately.

## The neutral test

One question keeps this from turning into "you should've used a pure core" — which is exactly
the trap to avoid on someone else's codebase:

> **Would a clean core change the *fix*, or just *where you attach it*?**

- **Changes the fix** → the concern is *data/contract-shaped*. Anticipate it now; architecture
  won't save you.
- **Only changes where you attach it** → it's *edge-shaped*. Cheap later — **if** there's a
  seam to attach it to.
- **Neither** → *true shell*. Defer freely.

This test works the same on a pristine core and a tangled monolith, which is what makes the
lens fair rather than preachy.

## Where concerns land

- **Data & contract — anticipate now (hard to reverse).** Schema/event migration and
  *versioning*, source-of-truth ownership, the consistency model, tenancy isolation, the id
  model, the published contract. These touch what's *stored* and what's *promised*; retrofitting
  them is surgery. Name them as invariants during Design the Code — even just leaving the
  migration path open counts.
- **Behind a seam — defer (cheap later).** Observability, rate-limiting/backpressure, auth
  *verification*, caching, the real persistence/transport adapter. If the seam exists, these
  land at the edge without touching the center.
- **Seam-blocked / ripple — the trap.** Edge concerns that *look* deferrable but have **no
  insertion point yet** (input validation, a pagination cap, per-request context — fused into
  the logic), or a shell choice that *ripples a core signature* (going multi-process forces the
  whole call path async). Here the missing seam is the unlock. Flag these explicitly; don't
  file them under "free later."
- **Above, as a coordinator — cross-cutting.** Erase/GDPR, account merge, cross-context
  reporting. They live *above* the core/shell split; route them to a thin coordinator, not down
  into the core.
- **Ops — hand off (an overlay, not a peer).** Deploy/rollback, monitoring, alerting, on-call,
  *running* the migration. The same concern often splits: a migration's *shape* is data
  (anticipate), its *tool* is edge, *running it in prod* is ops. Keep the halves separate.

## Two guards

- **Anticipate the few.** The hard-to-reverse concerns cluster in *data & contract*. Bake those
  in, or at least leave the door open. Missing here is the surgery you'll regret.
- **Don't pay tax you don't owe.** Most concerns are reversible — do **not** build them
  speculatively for a prototype that may never ship. Earn each against a real forcing function.
  Over-built production infrastructure is the inverse failure, and it's just as costly.

## On an existing system

Run as a diagnostic, the lens's value isn't green-field foresight — it's catching *data-shaped
debt that's already wrong*: an over-fetch fused to the response contract, a missing index on the
column every hot query filters, a source of truth that has quietly forked. Walk the neutral test
per concern; where the answer is "the fix doesn't change, only the insertion point," the missing
seam is the unlock — introduce it incrementally, don't reach for a rewrite.

## What the lens surfaces, by archetype

| If the system is… | Going live is mostly… | Anticipate (data-shaped) |
|---|---|---|
| a pure, event-sourced core | shell additions — the seam pre-pays it | event/snapshot **versioning**, the persistence-port async ripple, tenant/member revocation |
| a clean kernel behind ports | swapping in real adapters | migrations, the id/tenancy model, the concurrent-create race |
| logic fused with I/O (conventional) | first carving a seam to attach to | the over-fetch tied to the contract, the missing index — *plus* seam-blocked edges (validation, pagination caps) |

The pattern holds across all three: a clean seam makes most of production tax a deferral, and
concentrates the unavoidable part in *data and contract*. The messier the seam, the more the
"defer later" concerns turn into "carve the seam first."

## How it fits with Seam

Find the seam, name the hard-to-reverse invariants, guard the few, defer the rest — that's just
Seam, asked of production. The lens adds nothing to the method; it only points it at the moment
a system meets real users.
