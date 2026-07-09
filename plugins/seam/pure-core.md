# Pure Core — a suggested architecture

> **At a glance.** [Seam](./seam.md) is a way of thinking through *any* system, whatever its
> architecture. This is the opposite kind of doc: one concrete architecture you can *adopt*
> when you're building something fresh and want a strong default. It comes in two commitments
> of different weight. The **foundation** — a pure, I/O-free core behind a thin shell,
> talking through narrow ports, with immutable state and trivial orchestration — is the
> recommendation, and it stands entirely on its own. The **event-sourced log** — representing
> every state change as an event and folding the log into state — is an optional further step
> that buys audit, replay, and undo at a real ergonomic cost; take it only when those pay
> rent — when one of them is a real requirement, not a nice-to-have. Read both as one good
> set of answers to the questions Seam's checklist asks about state and effects — not as the
> only right answers. Unfamiliar terms — *fold*, *reducer*, *tombstone* — are defined in the
> [Vocabulary](#vocabulary) at the end.

## When to reach for it

- Greenfield, or a piece you own end to end and could rebuild.
- The logic is worth testing in isolation — a rules engine, a state machine, a domain model
  with real invariants.
- **Don't bolt it onto a system that already has its own shape.** The test: could you rebuild
  this piece end to end? If no, you don't own it — use Seam to think through *that* system as it
  is; don't reach for this as a rewrite you didn't need.

These gates admit you to the foundation. The event-sourced log has its own, stricter gate —
see [Whether the log pays rent](#whether-the-log-pays-rent).

## The foundation — a pure core behind narrow ports

Everything in this section stands without event sourcing. A plain function core with a
repository port (a storage interface — save this, load that) is a complete, honest version of
this architecture — not a stepping stone to a fancier one.

Three words recur, borrowed from [Why "Seam"](./seam.md#why-seam): the **core** is the pure
engine in the middle; the **shell** is everything wrapped around it — I/O, framework, UI; the
**seam** is the line where they meet.

### A pure core, dependencies pointing inward

- The core is a **pure function of its inputs**: zero I/O, zero framework — no clock,
  network, filesystem, UI surface, or globals. Rendering, persistence, CLI, and any future UI depend
  on the core; the core depends on none of them.
- The core **never branches on input kind.** Different inputs flow through one engine via
  pluggable *adapters* (swappable implementations — see *Narrow ports* below); kind-specific
  behavior (a special renderer, a diff-aware step) is an
  additive layer *outside* the core. If the core needs to know what a special case *is*,
  the seam drifted. Keeping the core general isn't only a containment rule — it's what gives
  the outer layer a *home* to be freely bespoke in, since nothing it does can leak back into the
  core. (Story: [Boundaries buy freedom](./stories/boundaries-buy-freedom.md).)
- *Guard:* make the purity boundary a **build failure**, not a convention — an
  import/dependency linter, or a module boundary the type checker enforces, that forbids the
  core from importing anything in the shell.

### Narrow ports, one per concern

- I/O lives behind thin **ports & adapters**, one per concern (one storage port, one API
  port); the core talks to the abstract port, the shell supplies the concrete adapter — a
  real database in production, a fake one in tests.
- Prefer the **narrowest port that serves the concern — single-method where possible.** A
  one-method port is the limiting case of a small interface over hidden behavior: cheap to
  substitute, hard to misuse, and trivially faked.
- *Guard:* the test fake for a port is a lambda (or a one-line stub). If faking it takes
  more, the port is too wide — split it by concern rather than growing the fake.

### Immutable state

- State is immutable — build and return new state, never mutate in place. Avoid in-place
  collection mutation; use the forms that return a copy.
- The engine is a pure step: `(state, input) → state`. How a *change* is represented — a
  plain function call, or an explicit event — is the further step below; immutability itself
  doesn't require events.
- *Guard:* a static check that fails on shared mutable state — immutability annotations on
  every state type, or a test/lint that rejects mutable fields. (Function-local accumulators
  are fine; it's *shared, persistent* mutable state that's banned.)

### Thin orchestration

- The top-level flow — the game loop, the request pipeline, the turn sequencer — is a **thin
  pass over small units that hold all the interesting logic.** It should read like a table of
  contents: what happens, in what order, and nothing else.
- If the orchestrator is accumulating branches and special cases, logic is in the wrong
  place — push it down into the unit that owns it.
- *Guard:* a size/complexity lint on the orchestrator module, so growth there fails the build
  instead of accreting silently.

### Derive, don't store

Anything computable — a total, a projection (a view derived from the data), a "current
position" — is computed at the point
of use, never cached as a field that can drift from what it was derived from. The recompute
cost is usually negligible; the staleness bug it prevents is not.

### Determinism

No hidden inputs. Pass time and randomness **in** (seeded), so a run replays identically; keep
wall clocks, globals, and env vars out of the core, so its output depends only on what it was
handed.

### Extend by adding (open/closed)

A new capability is a new variant (a new command, a new renderer — or, once you've taken the
further step below, a new event type) plus a
**registry entry** — a lookup that maps each variant to its handler, so the variant registers
itself instead of forcing an edit to the central flow. Existing code stays untouched, and
orchestration stays thin because the pipeline just walks the registry.

## The further step — an event-sourced log

The foundation leaves one question deliberately open: how is a state *change* represented?
The plain answer — call a pure function, persist the result through the storage port — is
complete. The further step changes the representation:

- All state changes go through **events**; the ordered, serializable log *is* the state —
  fold the reducer over the ordered events from an initial state to get the current one.
- A **pure fold** is the whole engine: `reducer(state, event) → state` (current state + one
  event → the next state), or `phase(state, choices) → events` (current state + the choices
  available → the events to apply, which then fold back into state).
- You get replay, an audit trail, and undo for free — free once the log's tax below is paid —
  because every intermediate state is a real, inspectable value.
- **Deletes are tombstones, not erasure** — append a "deleted" event; never rewrite history.

### Whether the log pays rent

Take this step only when one of its payoffs is load-bearing for *this* system:

- **Audit** — you must answer "why is it in this state?" from the system's own records.
- **Replay** — reproducing a bug from a log, or time-travel tests, is a real workflow here.
- **Undo / history** — a product feature, not a nice-to-have.

The log has a real tax: everything must serialize, indirection grows, and every change is now
read through an extra representation. When none of the payoffs above are load-bearing, the
foundation alone is the deeper, cheaper boundary (*deep* in Ousterhout's sense: a small
interface hiding a lot of behavior) — stopping there is the recommended default, not a
compromise.

## How it answers Seam's questions

Each layer of the architecture answers part of Seam's [State &
effects](./seam.md#state--effects--what-does-this-actually-do) checklist.

The **foundation** answers:

- **Side-effect safety?** Effects live in the shell, past the pure core; re-running the
  core is always safe because it's pure.
- **Boundary contracts?** The ports pin exactly what crosses each seam, one concern at a time.
- **Consistency?** (Can a read ever be stale?) One in-process core is strongly consistent by
  default; distribution is a
  shell concern you add deliberately, not an accident in the core.

The remaining questions are exactly the **rent test** for the log:

- **Source of truth?** Foundation: whatever the storage port owns — name it. Log: the event
  log, singular by construction; nothing else is writable.
- **Reconstruct why?** Foundation: only if you build an audit trail deliberately. Log: replay
  to any point; the history *is* the explanation.
- **Multi-step work?** (Does a half-finished sequence land somewhere recoverable?)
  Foundation: recovery is a design task per flow. Log: each step is an
  event; a half-finished sequence is just a prefix of the log, always a valid state.

If the second group of questions bites hard for your system, that's the signal the log pays
rent. If they don't, the foundation already answered everything that matters.

That tidiness is exactly why the whole doc is only a *suggestion*: it buys its guarantees by
owning all its state and keeping side effects out of the core. When a system can't do that,
Seam's neutral questions still apply — this set of answers just won't.

## Vocabulary

Plain-language definitions of the event-sourcing terms this doc leans on.

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
