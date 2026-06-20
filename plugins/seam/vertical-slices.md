# Vertical Slices — an organizational pattern

> **At a glance.** [Seam](./seam.md) asks, in its *Working in isolation* checklist, whether you
> can change one part of a system without holding all of it in your head. This is one concrete
> answer: organize the code **by feature** — each feature is its own folder, owning its pieces
> end to end, behind a narrow public surface — rather than by technical layer. Like [Pure
> Core](./pure-core.md), it's a pattern to *adopt* if you want one, not a prerequisite. Two
> things make it work in practice and are the focus of this doc: knowing **what it's like to
> live in** day to day, and knowing **where verticality stops** — the cross-cutting foundation
> (transport, identity) that is *not* sliced by feature.

## By feature, not by layer

Group code by what it's *for*, so a change lands in one place and a newcomer reads the domain,
not the framework:

```
src/
├── checkout/      ← everything checkout, end to end
│   ├── ui
│   ├── logic
│   ├── data
│   └── index      ← the only surface other slices may import
├── profile/       └── ...
├── search/        └── ...
└── foundation/    ← the thin cross-cutting base every slice sits on
```

The contrast is the by-layer tree, grouped by role — `controllers/`, `services/`, `models/`,
`views/`. By-layer isn't *wrong*: it's the convention many frameworks teach, and on a small
app it's perfectly fine. Its tradeoff is locality — one feature's code is spread across
several folders, so a change touches all of them, and nothing structurally stops one layer
from reaching into another. By-feature trades that familiarity for locality: it couples
*along the axis of change*, so the things that change together live together.

The principles that make a slice a slice:

1. **Colocate what changes together.** One behavior change lands mostly in one folder.
2. **Each slice exposes a narrow public surface; its internals stay private.** Outsiders
   import the slice's published entry point only — everything unexported is free to move.
3. **No lateral imports between sibling slices.** A slice never reaches into another's
   internals, and siblings don't import each other. Cross-slice needs are met by composing *at
   a higher layer*, never by a side door.
4. **Dependencies point one direction.** Slices depend on the foundation, never the reverse;
   no cycles.

## What it's like to work with it

The point of the pattern is the day-to-day feel, so picture the moves:

- **Adding a feature** ("bookmarks"): you make one folder, `bookmarks/`, with its own ui /
  logic / data and an `index` that publishes only what the outside may call. You register its
  entry points with the shared transport and read the already-resolved caller identity the
  foundation hands you. You touch *no other feature*. The diff is almost entirely new files.
- **Finding code:** a bug in search lives in `search/`. You open one folder and hold one
  feature in your head — not the controllers of every feature, then the services of every
  feature, then the models.
- **Deleting a feature:** delete the folder, remove its registration. Nothing dangles —
  because nothing was allowed to import its internals, the boundary check proves the removal
  is clean. (If something *does* break, that's the check catching a leak you'd otherwise have
  shipped.)
- **Working in parallel:** two people on two features rarely touch the same files, so they
  don't queue behind each other. The merge conflicts that remain are usually in the
  foundation, which is exactly where you *want* shared changes to be visible.

The felt difference: most of the time you reason about *one slice*, and the rest of the system
is a set of givens you rely on rather than hold.

## The litmus test — would it survive becoming its own deployment?

The sharpest proof that a slice is really a slice: **imagine extracting it into its own
deployment tomorrow, with the client-facing shell simply making calls to it.** If that move is
mostly mechanical — the shell calls the slice's published surface, the slice carries its own
work — the boundary is honest. If it would mean untangling shared internals, chasing down
sibling features that imported it, or splitting a fact two slices both write, then it isn't a
slice yet; it's entangled code in a feature-shaped folder.

You don't have to *actually* extract it. A clean slice is **extraction-ready** whether or not
you ever extract it — and the things that would block extraction (lateral imports, shared
mutable internals, reaching past a public surface) are exactly the things the principles above
forbid. The network boundary you're imagining is just a strict, honest version of the boundary
the linter enforces: code that would survive becoming a remote call has a real seam; code that
wouldn't, doesn't. (The litmus is about *slices*; the foundation below is the shared base
they'd all call — not something extracted per feature.)

## Where verticality stops — the cross-cutting foundation

Not everything is a feature. Some things are genuinely **horizontal**: every slice relies on
them, and forcing a separate copy into each feature is as counterproductive as spreading one feature across
layers. They belong in a thin **foundation** that slices sit on and depend on downward — and
the foundation holds *two different kinds* of thing:

```
src/
├── checkout/ · profile/ · search/   ← feature slices, each end to end
└── foundation/                       ← cross-cutting; two kinds inside:
    ├── domain/     ← authoritative state: the source of truth + the rules over it
    └── platform/   ← mechanism: transport, identity, persistence
```

**The test for foundation vs slice:** is it something a user would ask for, or something every
feature quietly relies on? `checkout` and `search` are things users think about — slices. The
wire that carries every request, the check of who's calling, the authoritative record everyone
reads — relied on by all — foundation.

### Mechanism — how requests flow

- **Transport — the wire.** How requests arrive and responses leave: the server, the routing,
  the serialization. Slices *expose* handlers; they do not each stand up their own server. The
  transport carries any slice's handler without knowing what the slice does. Keep it dumb about
  features — the moment transport branches on a specific feature, a slice's logic has leaked
  downward.
- **Identity — who's calling.** This one *splits*, and the split is the whole lesson.
  *Verifying* identity (is this token real? who does it belong to?) is an edge concern, done
  once, before any slice runs — cross-cutting. *Authorizing* (may **this** caller do **this**
  action?) runs on the feature's own rules — that lives in the slice. So the foundation hands
  each slice an already-resolved caller; the slice never re-verifies a token, and the
  foundation never encodes a feature's rule. Identity is a *seam*, kept orthogonal to feature
  logic on purpose.

Observability, configuration, and the persistence *connection* sit here too, by the same test.

### Source of truth — what's authoritative (the domain)

This is the other place verticality stops, and it's the one most easily missed. A slice does
feature **work** — interaction, view, its own private or derived data. But a **fact that must
be authoritative** — the one true copy that more than one feature depends on staying
consistent — is *not* slice-private. It's promoted to the **domain**, with a single owner; other
slices either read it or hold a projection (a read-only copy derived from the owner's data,
rebuildable from it) that *defers* to that owner. One writable owner, everyone else deferring,
is the whole point (Seam's [*source of
truth*](./seam.md#state--effects--what-does-this-actually-do) check, in organizational form).

The test: *is this the one true copy others must stay consistent with?* If yes, it's domain,
not slice — even when it would have been convenient to keep it inside the feature that happened
to create it.

A sharper litmus — three facets of the same question:

- **Rebuild.** If you deleted every *other* copy of this fact, could you regenerate them all
  from this one? The source of truth is the copy all others derive *from*; the others are
  caches you could throw away and recompute (the flip side of *derive, don't store*).
- **Single writer.** Is there exactly one place a change to this fact is *made*? The source of
  truth is the single writer; if writes could originate in two places, name which one owns it
  and have the other defer.
- **Tiebreaker.** When two copies disagree, is one right *by definition*? That one is the
  source of truth; if there's no single answer to "who wins," you haven't named one yet.

A fact that passes these belongs in the domain; anything that merely *reflects* it is a
projection that must defer to it.

The **database** is where the domain persists that truth — an adapter under the foundation, not
a feature's possession. The domain decides *what is authoritative*; the database merely
*stores* it. A feature doesn't get to define the canonical schema for a fact other features
share. (A slice may keep private storage for data that's truly its own — but the moment a fact
is shared and authoritative, it belongs to the domain.)

So separate **feature work** from **source of truth**: the slice is where behavior and the
feature's own view live; the domain is where the authoritative model lives. A slice that *is*
the source of truth for a shared fact has taken on a job that belongs to the foundation.

### Directional rules that keep the boundary honest

- A slice **receives** what the foundation provides — a resolved identity, a request context, a
  transport to register on, a handle to the domain — it doesn't reimplement or own them.
- Feature logic stays **out** of the mechanism: transport stays dumb about features; identity
  verifies but doesn't know a feature's rules.
- For shared facts, slices **defer to the domain** and never keep a second writable copy.

Keep the foundation **thin** — it's the one place legitimately shared by everyone, so guard it
deliberately: only genuine mechanism-for-all and genuine source-of-truth earn a spot here (see
*Keeping the boundaries healthy*).

## Enforcing the boundaries

A folder convention is a wish until a check fails on violation. From weakest to strongest: a
**published entry point per slice** (documents the surface, doesn't enforce it); an
**import-boundary linter** in CI that forbids cross-slice and into-internals imports (usually
the practical sweet spot — the concrete rule, in code, is in
[examples/typescript.md](./examples/typescript.md#working-in-isolation--keep-features-from-reaching-into-each-other));
**monorepo project boundaries** by tag; and a **language module system** (the strongest —
the compiler enforces it and it can't be ignored, e.g. package-private visibility or an
"internal" package rule where only a common ancestor may import the contents).

## When to reach for it — and when not

Reach for it once a system has more than one real feature and changes start spreading across
layer-folders, or when you want features independently ownable, testable, and removable. Don't
slice prematurely: a one-feature app has no domain worth separating, and imposing the full
vocabulary adds ceremony before it earns its keep. Start concrete; slice when a *second* real
feature pushes you to — and notice the push when it comes, rather than letting "only one feature
so far" harden into never slicing.

## Keeping the boundaries healthy

A few practices keep slices and foundation honest as the system grows:

- **Before adding anything to the foundation, ask "does this belong to one slice?"** If a
  single slice could own it, put it there; only a fact every slice reads or a mechanism every
  slice rides earns a foundation spot.
- **Point every cross-slice need upward, never sideways.** A slice receives from the foundation
  and composes *upward* through public surfaces; in review, flag any import where a slice names a
  sibling slice — the import-boundary linter above is the falsifier.
- **Keep verification at the edge and rules in the slice.** The foundation verifies and carries
  (transport, identity); each slice owns its own feature rules.
- **Pick one primary axis.** Group by feature *or* by layer, consistently, so a reader can
  predict where anything lives.
- **Push shared logic into a domain model** once more than one slice needs it, rather than
  letting a single slice's handler grow to hold everything.
- **Hoist genuinely shared logic into the foundation** when it's truly shared — name it and
  put it one layer up, depended on downward.

## How it fits with Seam

This pattern *answers* the question Seam's [Working in
isolation](./seam.md#working-in-isolation--can-you-change-one-part-without-holding-all-of-it)
section only *poses*. Run the add-a-feature walkthrough: if a plausible next feature would be a
new slice added end to end, the structure is working; if it would spread across layers, this is
the pattern to move toward. And finding *where verticality stops* — drawing the line between a
slice and the foundation — is the same act as finding any seam: the general base resolves what
every feature needs; the special-case features live above it.

## Lineage — where these ideas come from

- **Vertical Slice Architecture** — Jimmy Bogard: minimize coupling between slices, maximize
  coupling within a slice.
- **Screaming Architecture** — Robert C. Martin, *Clean Architecture*: the top level should
  announce the domain, not the framework.
- **Package-by-component / modular monolith** — Simon Brown, *Software Architecture for
  Developers*: a component behind a public interface with private internals.
- **Bounded contexts** — Eric Evans, *Domain-Driven Design*; Sam Newman, *Building
  Microservices*: the coarse-grained version of a slice, ready to extract later.
- **Feature-Sliced Design** — a frontend methodology of layers → slices → segments, where
  same-layer slices may not import each other and each exposes a public API.
