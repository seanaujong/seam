# Seam

> **At a glance.** Seam is a way of *thinking through* a system — what it does and what it's
> for — whether you're designing something new or trying to understand code that already
> exists. Its premise: **design is discovery, not transcription.** You rarely know the right
> shape in the abstract; you recognize it when you see it. So Seam makes thinking concrete —
> it produces artifacts you can look at, use, and push against — and lets the picture, the
> invariants, and the goals fall out of your reaction. What you find, you keep: the
> load-bearing *invariants* (things that must always hold) become *guards* — an automated
> check (a type, a test, a lint rule) that fails loudly when one breaks — so they can't erode
> silently. Seam doesn't prescribe an architecture; if you want a recommended one to *adopt*,
> that's a separate concern — see **[Pure Core](./pure-core.md)**.

## The bets

Seam rests on three bets, and holds a tension between them on purpose: be **loose** while you
explore, make it **visible** so there's something real to react to, and turn **strict** once
you've found what matters.

**1. Explore before you specify.** The hard part of building something isn't writing it down;
it's figuring out what's worth writing down, and you rarely know that in the abstract. You
know it when you see it: a layout feels wrong the moment it's on screen; a boundary feels
right the moment you can trace something across it. So the highest-leverage early work is
discovery, not transcription — the aim is to hold the shape open until you've found the one
worth committing to. Existing standards count here too: the better version often lives just
outside the house style and the surrounding system. So explore deliberately *outside* the existing
thing — a throwaway sandbox, away from its conventions — then conform later, on purpose.
Looking outside is how you make the inside better. (For a story of this, see [Explore outside
first](./stories/explore-outside-first.md).)

**2. Make it visible.** The output of thinking should be something you can *look at* — a
rendered screen, a diagram, a comparison, a seam map — not prose you take on faith. You can
only correct what you can react to, and an abstract intention gives you nothing to react to.
This is why even "design the code" produces a picture, not an essay: a thing on screen draws
out the disagreement that a paragraph hides.

**3. Care about invariants, not ritual.** The discipline that matters isn't writing tests up
front; it's caring about the **invariants** — the few things that must always hold — along
with the shape, the seam, and the people it serves. A test is a *mechanism*, one way to guard
an invariant — the invariant is the thing you care about. So strictness is aimed at substance,
and it comes *after* exploration: explore loosely to find the shape and what must hold, then be
strict about guarding what you found. (How, in [On tests](#on-tests); why, as a story, in
[Beyond superpowers](./stories/beyond-superpowers.md).)

## Why "Seam"

Three words run through everything below, so pin them down first. The **core** is the
general engine that resolves whatever input it's given without knowing the specifics — a
chess engine that can play any position. The **shell** is the thin outer layer wrapped
around it that handles the specific cases, the I/O, and the framework glue — the app that
picks which game to load and draws the board. The **seam** is the line between them — and
it can fall at any scale: between two functions, two modules, or two services.

- **The core/shell boundary.** A seam is where the general core meets the special-case
  shell. The central act is finding where that seam goes — by exploring, not by asserting it
  up front. If the core ends up needing to know what a special case *is*, the seam drifted.
- **Visible and intentional.** A seam is something you can see — where two pieces
  deliberately join. Hence visual exploration: thinking should surface as something to look
  at, not a paragraph to trust.
- **Where the invariants get pinned.** Once found, the seam is also where the things you
  care about get guarded — the boundary you write a type or a test against so it can't
  quietly break.

## Two steps, kept separate

Seam is two distinct steps, and keeping them apart reuses the core/shell instinct one level
up: **"design the product" plays the shell role** — the felt, special-case surface a human
reacts to — **and "design the code" plays the core role** — the engine underneath that has
to resolve cleanly. Letting aesthetics leak into architecture — or architecture constrain
what the product could feel like before it's explored — is a drifted seam. Run them as
separate passes with a clean boundary between.

```
┌────────────────────────────────────────────────────────────┐
│  Design the Product                        the felt shell  │
│ when there's a look or feel to react to                    │
│ explore by reacting: rendered prototypes / mockups         │
│ done when: human points at one — 'this, not that'          │
└────────────────────────────────────────────────────────────┘
                               │   a shape chosen — now design how it works
                               ▼
┌────────────────────────────────────────────────────────────┐
│  Design the Code                       the resolving core  │
│ picture doc (vision · invariants · goals, one arc)         │
│ + seam map (core | shell | what crosses)                   │
│ done when: implementation could start tomorrow             │
└────────────────────────────────────────────────────────────┘
                               │   seam found + invariants worth guarding named
                               ▼
┌────────────────────────────────────────────────────────────┐
│  Build                                         downstream  │
│ build it; guard the load-bearing invariants                │
│ + the unit tests that would make you confident             │
└────────────────────────────────────────────────────────────┘
```

### Design the Product

- **When.** The thing has a felt surface — "does this look pretty? does it feel good to
  use?" — that can only be *reacted to*, not reasoned about.
- **Output.** Rendered prototypes / mockups you can actually look at and use. The rendered
  artifact *is* the value at a boundary; that's what keeps this step honest instead of a
  conversation about taste. No vibes — a thing on screen.
- **No felt surface?** An engine, a library, or a pure core has nothing to *react to* — there
  the design starts at Design the Code instead.
- **Push product sense here**, not just aesthetics: who is this for, why would it spread,
  what's the market shape. This is the step that exists to counter "build the thing that's
  technically interesting to me" — it forces a reaction from a *user's* point of view.
- **Ground product calls in evidence — and name the tier.** Taste is a hypothesis, not a
  verdict. Reach for the strongest evidence available, and say which one a claim rests on,
  so a guess isn't mistaken for a fact:
  - *Agent reasoning, no research.* The model reasons from what it already knows —
    comparable products, common patterns, likely failure modes. Instant and free; a starting
    hypothesis, never a fact.
  - *Agent reasoning + internet research.* Back the hypothesis with real sources —
    competitors, reviews, what users actually complain about, rough market size. Slower, but
    grounded in the outside world.
  - *Existing metrics / data.* If you already have usage data, funnels, support tickets, or
    prior A/B results, that beats any outside guess — it's *your* users, not a proxy. When it
    exists, start here.

### Design the Code

- **Output.** A **picture doc** — vision, invariants, and goals narrated as one clean arc —
  plus a **seam map**: the general core, the special-case shell, and what crosses the
  boundary between them.
- **The work is to walk the standing checklist below**; Design the Code is that walk turned
  into a step. Two falsifiable checks keep it honest rather than a diagram exercise:
  - *If you can't draw the seam, you haven't found the boundary.* Inability to place the
    core/shell line is a finding, not a stall.
  - *If a want isn't yet a predicate, it will erode.* Every invariant the design leans on
    gets named as something a type, a test, or a lint rule could enforce — even before
    there's code to enforce it against.
- **The seam map is the contract.** It's the artifact the code answers to. When code and
  design later diverge, change the map first — on purpose — then make the code match it, so
  the picture never silently lies.

## On tests

Seam has no test ritual, because tests aren't the point — *the things you care about* are.
Among everything a design leans on, a few invariants are both load-bearing and silently
breakable; those get promoted to a guard (a type, a test, a lint rule) that fails loudly
when violated. That's the whole discipline: deciding **which** invariants are worth
guarding, and naming the check for each.

Beyond those guards, write the unit tests that would make *you* confident the code does what
you think it does — the cases where a green result earns your trust, and where a wrong
implementation would actually fail (not one that passes whether the code is right or wrong).
If you can't name a test that would make you confident, that's the gap to fill. Seam doesn't
ritualize this; it just insists the load-bearing invariants are guarded, so a promise the
design made can't quietly rot.

## The standing checklist

A catalog of things worth *considering*, and the heart of the method. Walk it, decide which
are load-bearing *for this system*, and (as *On tests* says) name a **guard** for each one
that is.

Each item is a prompt, not a verdict. When one applies, instantiate it against *this*
system — the real field, boundary, or side effect, and the consumer it serves: a dev calling
an abstraction we wrote, a user in the product, a stakeholder reading a metric. The generic
category never lands until it's that concrete (see [Seam applied to
itself](#seam-applied-to-itself)).

This works just as well **over code that already exists** as over a new design. You don't
need a new architecture to get value: walking the list against what's there is a diagnostic —
it points at the ambiguous source of truth, the contract that can break, the side effect
that isn't safe to repeat. Don't sort the system into a *type* ("micro­services," "monolith,"
"legacy"); read what it actually does and pull the questions that bite.

*(New to a term below? There's a plain-language [Vocabulary](#vocabulary) at the bottom. Want
the guards as real code? See [Seam in TypeScript](./examples/typescript.md).)*

### Boundaries & layering — where the seam goes

- The general part resolves whatever it's given; special-casing lives in a layer *above* it.
  The center never branches on input kind, mode, API variant, or policy — those arrive as
  injected data or pluggable adapters. If the center has to know what a special case *is*,
  the seam drifted.
- Keep I/O and framework *concentrated and intentional* — at named edges, not scattered
  through the logic. Some designs legitimately fuse resolution and I/O (an ORM model that owns
  its own persistence is a choice, not a drifted seam); the test is whether I/O is contained
  and deliberate, not whether it's absent. Where the line *can* be drawn hard (a pure core —
  see [Pure Core](./pure-core.md)), enforce it at build time (an import/dependency linter, or
  a module boundary the type checker enforces) so a violation fails the build, not just review.
- Dependencies point inward; edges (shells, adapters, renderers) depend on the center, never
  the reverse. Fix a bug in the layer that *owns* the invariant, not the one that surfaces
  it.
- I/O lives behind thin **ports & adapters**, one per concern (one storage adapter, one API
  adapter); the center depends on the abstract port, the shell supplies the concrete adapter.

### Illegal states & invariants — what to guard

- Can the design represent an illegal state? Prefer a tagged union (a finite set of variants
  each marked by a discriminator) over a bag of optional flags; match it exhaustively, so
  adding a variant *forces* every consumer to handle it. *Guard:* a type system that can make
  the missing case a build error.
- Give distinct types to values that share a representation but shouldn't be interchangeable
  (two kinds of id), so the type system rejects mixing them.
- Turn the type checker's strictness up from the start, and treat dynamic or untyped values
  as something to narrow at the boundary rather than spread inward. Don't retrofit strictness
  later.
- Is each load-bearing invariant enforced by a type/test/lint rule — or just held in our
  heads?

### Clarity & naming

- Judge each piece by how clearly it shows its central idea; the happy path should read
  simply, without apology.
- Name the concept, not the implementation; one name per concept (an overloaded name is two
  concepts wearing one); domain words, no invented jargon.
- Failure modes visible, not silent. No duplicated logic.
- Escape hatches — anything that bypasses the type checker or a sensible default (an
  unchecked cast, a non-null assertion, a memo/cache, a suppressed lint rule, a magic number)
  — carry a written rationale inline: an explicit contract, not a silent "trust me."

### Reversibility & removability

- Which choices are hard to reverse later? Is each feature removable without dangling
  scaffolding? If a delete leaves orphans, the abstraction leaked.
- Extend by adding (open/closed): a new capability is new code (a new variant, a new
  handler, a new service) plus wiring, not a rewrite of what's there. If adding a feature
  means editing the center, something is layered wrong.
- Start concrete; earn each abstraction against a real second use (rule of three). No
  speculative wrappers; keep each type to a single responsibility — ask "does the center
  actually read this?" before adding a field.
- Auditable — can you trace *why* from the system's own records?
- When the reversibility question is specifically *"what would it cost to take this to
  production?"*, see [Production tax](./production-tax.md) — the same lens, pointed at going live.

### Working in isolation — can you change one part without holding all of it?

One question from three angles; a "no" on any of them is the architecture talking, not a
chore to push through.

- **Test ergonomics — the canary.** When you write a test, does it reach the thing under test
  directly, or must it drag in a heavy dependency, stand up half the system, or wade through
  unrelated ground first? Awkward, sprawling setup is a design signal: the seam is in the
  wrong place, or the unit is too coupled to reach on its own. Treat "this test is painful to
  write" as a finding about the structure, not a fact about testing.
- **Add-a-feature walkthrough.** Take a plausible next feature and trace what it would
  actually take. Does it land as a vertical slice — a feature added top to bottom through the
  layers it needs, mostly as new pieces — or does it force edits threaded across many layers
  and files? If adding a feature means touching everything, the system is sliced by layer
  where it wants to be sliced by feature.
- **Locality of change.** Can someone work on one feature holding only that feature in their
  head, or must they reason about the whole system at once? Colocate what changes together so
  a slice is findable and changeable on its own. *Guard:* a dependency rule that forbids one
  feature reaching into another's internals, so slices can't quietly grow into each other.
  (For a concrete pattern — feature-vertical folders with enforced boundaries — see [Vertical
  Slices](./vertical-slices.md).)

### State & effects — what does this actually do?

This is where systems differ most, so don't label the system — read it. Pull whichever
questions bite, name the real instance, and guard it:

- **Source of truth.** What owns each fact, and is it singular? Litmus: could you *rebuild*
  every other copy from this one, is there a *single writer*, and when copies disagree is one
  right *by definition*? Pass all three and the fact has one owner; everything else is a
  projection that defers to it. *Guard:* ownership named per fact; a check that flags divergence.
- **How state changes — and whether you can reconstruct why.** An event log, an audit table,
  or just mutable rows? Whatever it is, can you answer "why is it in this state?" from the
  system's own records? *Guard:* the trail that makes "why" traceable.
- **Side-effect safety.** Where do the side effects happen? What makes one safe to repeat —
  running it twice has the same effect as once (idempotence), the way pressing an elevator
  button again doesn't summon a second elevator — and safe to fail partway through? *Guard:* a
  test that repeats the effect and asserts it lands once.
- **Boundary contracts.** What crosses each seam between parts, and does that shape stay
  compatible as both sides change independently? *Guard:* contract / schema checks in CI.
- **Multi-step work.** Does a half-finished sequence land somewhere recoverable, or can it
  corrupt? *Guard:* failure-injection across the steps; a defined way to roll back or
  compensate.
- **Consistency on purpose.** Where can a read be stale, and does everyone reading it know?
  Strong vs eventual should be a decision, not an accident. *Guard:* the tolerated staleness
  documented and tested.

**The guards run in order.** Cheapest, earliest-failing checks first: types / schemas →
boundary & contract checks → unit tests → integration. A structural violation should fail
before a behavioral test ever runs.

## Seam applied to itself

Beyond the system under work, the *method* holds itself to the same rules:

- **Diverge before you converge.** Explore options as concrete artifacts and hold the choice
  open until the right one shows itself.
- **Make the feeling a value at a boundary.** "Feels good," "looks right," "this flows" —
  push each until it's something you can point at: a rendered frame, a diagram, a
  walkthrough you can diff. What you can point at, you can correct; what stays abstract, you
  can't.
- **Ask "how does it feel?"** The most transformative move in the method is the simplest
  question: *how does this feel — to use, to work in, to read?* It shifts thinking from
  mechanical ("what does it do") to experiential ("is this right"), which is where taste and
  judgment live. Ask it of a prototype, of a design, of the code you're about to change — and
  answer it in the before/after terms a good PR description uses.
- **Run toward what breaks.** "How does it feel?" is the generative question; its adversarial
  twin is *"where does it break?"* A seam or an invariant looks fine until you attack it — so
  steer the system into the icky, hard, or unknown case on purpose and watch what gives. Make
  the attack real: pick an input where *wrong* code would give a *different* answer (one where
  right and wrong agree proves nothing); clear the confounds first so a divergence is
  attributable, not noise; and watch the guard *fail* when you revert the fix. The bug hides
  where you're not running — a clean invariant on inputs that never reach the effect is a no-op,
  not a proof.
- **Every check lands on a real example, for a named someone.** A catalog item raised in the
  abstract — "watch your source of truth" — changes nothing. When a check fires, Seam names
  the concrete instance in *this* system and who it serves: the dev who could construct an
  illegal `Booking` against the type we wrote, the user left on a spinner when checkout times
  out, the stakeholder asking "how many active users?" who needs one number the system stands
  behind. Tie the invariant to the consumer whose experience it protects — and, where it
  helps, show the guard as code you could paste in. An abstract finding is a finding
  deferred: ground it or drop it.
- **Show the why, not just the move.** Suggesting the thinking isn't enough — the output
  should let the user *see why it paid off here*: the bug avoided, the payoff a short story
  makes vivid (the kind in `stories/`). A method whose value the user has *seen* travels with
  them and gets reused. (This is the previous rule aimed at the *method itself*, not just a
  single finding.)
- **Write the way you design.** The bets apply to prose, not just product: make it visible (a
  concrete example or a diagram beats an abstract paragraph), lead with the intuition and the
  before/after *feel*, say the *why* before the *what*, and write for a named reader. An
  explanation you can't picture is one you haven't finished — the same test as a design you
  can't draw.
- **Keep the process thin; the thinking lives in the artifacts.** The methodology is a thin
  pass over the prototype, the picture doc, and the seam map. If the *process* is getting
  complicated, the thinking is in the wrong place.
- **Cue, don't choreograph.** Name the moves worth considering — draw a picture, make a
  comparison, name an invariant — and trust the model to apply judgment to the situation in
  front of it. Don't hard-code mechanics ("spawn exactly three subagents, in this order"); an
  over-specified process substitutes ritual for the thinking it's meant to support. The method
  says *what's worth doing*; how much, and how, is the model's call.
- **Product and code stay separate.** The boundary between the two steps is load-bearing.
  Guard it.

## Done — the green signal

Each step names what "done" looks like so you know when to stop exploring:

- **Design the Product** is done when there's a rendered artifact the human has reacted to
  and can point at — "this one, not that one," with a reason.
- **Design the Code** is done when there's a seam map, a list of invariants each expressed
  as a future predicate, and a named *green signal* for the build (the specific check, test, or
  build result that will say "done") — enough that implementation could start tomorrow without
  re-deriving the design.

Past that line, it's just building: write the code, write the guards for the invariants
worth keeping, write whatever ordinary tests the code obviously wants. Seam's promise is
that by then you're building a shape you *found* by exploring — and the things you care
about are enforced, not merely hoped for.

## Vocabulary

Plain-language definitions of the terms the checklist leans on, once. (The terms specific to
the pure-core architecture — *fold*, *event sourcing*, *tombstone*, and so on — live in
[Pure Core](./pure-core.md).)

- **Tagged union + exhaustiveness check.** A type that is exactly one of a finite set of
  variants, each marked by a discriminator. Matching *every* variant exhaustively lets the
  type system reject the code the moment someone adds a variant and forgets to handle it —
  turning a forgotten case into a build error instead of a runtime surprise.
- **Distinct types for indistinct values.** Giving two values that share a representation
  (say, two kinds of id) separate types, so the type system refuses to let you pass one where
  the other is expected.
- **Ports & adapters (hexagonal architecture).** The center talks only to abstract interfaces
  (*ports*); the shell plugs in concrete implementations (*adapters*). I/O — a database, an
  API, a file — can be swapped without touching the center.
- **Open/closed.** Extend behavior by *adding* new code (a new variant, a new handler), not
  by editing existing code.
- **Strict type checking.** Turning the type checker's optional safety settings on from the
  start, so more mistakes surface as build errors instead of runtime bugs.
- **Import / dependency linter.** A check that scans which modules import which and fails the
  build when a forbidden cross-layer dependency appears — one way to make a layering boundary
  an enforced check rather than a convention.
- **Idempotence.** An operation is *idempotent* if applying it twice has the same effect as
  applying it once — so a retry or a duplicate delivery is harmless.
- **Contract / schema check.** The agreed shape of the data crossing a boundary (an API, an
  event, a stored record). A *contract check* fails the build when a change would break a
  consumer that depends on that shape.
- **Strong vs eventual consistency.** Under *strong* consistency a read always reflects the
  latest write; under *eventual* consistency copies converge over time, so a read may briefly
  be stale — a deliberate trade for availability and scale.
