# Pure Core — a suggested architecture

> **At a glance.** [Seam](./seam.md) is a way of thinking through *any* system, whatever its
> architecture. This is the opposite kind of doc: one concrete architecture you can *adopt*
> when you're building something fresh and want a strong default. It is a suggestion, not a
> prerequisite — Seam works whatever you choose. The shape: a **pure, I/O-free core** wrapped
> in a **thin shell**, with state modeled as an **immutable fold over events**. Read it as one
> good set of answers to the questions Seam's checklist asks about state and effects — not as
> the only right answers.

## When to reach for it

- Greenfield, or a piece you own end to end and could rebuild.
- The logic is worth testing in isolation and replaying — a rules engine, a state machine, a
  domain model with real invariants.
- **Don't bolt it onto a system that already has its own shape.** If you're working inside
  existing code, use Seam to think through *that* system as it is; don't reach for this as a
  rewrite you didn't need.

## The shape

### A pure center, dependencies pointing inward

- The center is a **pure function of its inputs**: zero I/O, zero framework — no clock,
  network, filesystem, UI surface, or globals. Rendering, persistence, CLI, and any future UI depend
  on the center; the center depends on none of them.
- The center **never branches on input kind.** Different inputs flow through one engine via
  pluggable *adapters*; kind-specific behavior (a special renderer, a diff-aware step) is an
  additive layer *outside* the center. If the center needs to know what a special case *is*,
  the seam drifted.
- I/O lives behind thin **ports & adapters** — the center talks to an abstract port; the
  shell supplies the concrete adapter (a real database, a fake one for tests).
- *Guard:* make the purity boundary a **build failure**, not a convention — an
  import/dependency linter, or a module boundary the type checker enforces, that forbids the
  center from importing anything in the shell.

### Immutable state, changed only through events

- State is immutable — build and return new state, never mutate in place. Avoid in-place
  collection mutation; use the forms that return a copy.
- A **pure fold** is the whole engine: `reducer(state, event) → state` (current state + one
  event → the next state), or `phase(state, choices) → events` (current state + the choices
  available → the events to apply, which then fold back into state).
- *Guard:* a static check that fails on shared mutable state — immutability annotations on
  every state type, or a test/lint that rejects mutable fields. (Function-local accumulators
  are fine; it's *shared, persistent* mutable state that's banned.)

### The event log is the source of truth

- All state changes go through **events**; the ordered, serializable log *is* the state —
  fold the reducer over the ordered events from an initial state to get the current one. You
  get replay, an audit trail, and undo for free, because every intermediate state is a real,
  inspectable value.
- **Deletes are tombstones, not erasure** — append a "deleted" event; never rewrite history.

### Derive, don't store

Anything computable — a total, a projection (a view derived from the data), a "current
position" — is computed at the point
of use, never cached as a field that can drift from the log. The recompute cost is usually
negligible; the staleness bug it prevents is not.

### Determinism

No hidden inputs. Pass time and randomness **in** (seeded), so a run replays identically; keep
wall clocks, globals, and env vars out of the core, so its output depends only on what it was
handed.

### Extend by adding (open/closed)

A new capability is a new event/variant plus a **registry entry** — a lookup that maps each
variant to its handler, so the variant registers itself instead of forcing an edit to the
central fold. Existing code stays untouched. Orchestration stays a **thin fold**, so the
interesting logic lives in the small units it folds over.

## How it answers Seam's questions

This architecture is attractive because it gives a single, clean answer to each question in
Seam's [State & effects](./seam.md#state--effects--what-does-this-actually-do) checklist:

- **Source of truth?** The event log — singular by construction; nothing else is writable.
- **Reconstruct why?** Replay the log to any point; the history *is* the explanation.
- **Side-effect safety?** Effects live in the shell, past the pure center; re-running the
  center is always safe because it's pure.
- **Multi-step work?** Each step is an event; a half-finished sequence is just a prefix of the
  log, always a valid state.
- **Consistency?** One in-process fold is strongly consistent by default; distribution is a
  shell concern you add deliberately, not an accident in the center.

That tidiness is exactly why it's only a *suggestion*: it buys its guarantees by owning all
its state and keeping side effects out of the center. When a system can't do that, Seam's
neutral questions still apply — this set of answers just won't.

## Vocabulary

- **Pure function / pure fold.** *Pure* means the output depends only on the inputs — no
  hidden state, no side effects, same inputs always give the same result. A *fold* is a
  `reduce`-style pure function `(state, event) → state` that walks a list of events into a
  final state, never mutating anything in place.
- **Event sourcing / the event log.** Instead of storing current state and overwriting it,
  you store the ordered list of *events* that happened; current state is the result of
  folding them. The log is the single source of truth — and it buys replay, an audit trail,
  and undo for free.
- **Reducer / phase.** Two shapes of the fold. A *reducer* applies one event to the state:
  `(state, event) → state`. A *phase* looks at the state and the choices available and
  decides what happens next: `(state, choices) → events`, whose events then fold back in.
- **Tombstone.** A "deleted" marker (here, a deletion event) left in place of erasing a
  record, so the history stays intact.
- **Derive, don't store.** Compute a value at the moment you need it rather than caching a
  copy, so the copy can't drift out of sync with what it was derived from.
- **Seeded determinism.** Passing time and randomness in as explicit, fixed ("seeded") inputs
  so a run produces the same result every time and can be replayed exactly.

For *ports & adapters*, *open/closed*, *tagged unions*, and the type-checking terms, see the
[Vocabulary in Seam](./seam.md#vocabulary).
