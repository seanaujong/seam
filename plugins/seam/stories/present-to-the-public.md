# Present to the public — a story

> **At a glance.** A field note behind Seam's [*every check lands on a real example, for a
> named someone*](../seam.md#seam-applied-to-itself) rule and the [output
> litmus](../SKILL.md#the-litmus-for-your-output) — pointed at how you *hand back* a change. The
> lesson: a change request is a **presentation to the public**, and the public is whoever sits on
> the **far side of the seam you touched** — a downstream dev, an analyst querying your table, an
> end user. Lead with *their* experience — walk through what they go through, before versus after
> — not the mechanical diff. At a company where your reader has no context on your subsystem, the
> user's journey is the one thing they *can* read.

## What happened

A Holler change adds a projection: `message_counts_by_channel`, a small read model that folds
`MessagePosted` / `MessageDeleted` events into a per-channel count. There are two ways to hand it
back, and they use the *same diff*.

The first is the one that comes out by default — describe what the code does:

> Added a projection folding `MessagePosted`/`MessageDeleted` into a per-channel count read
> model; wired it into the change-feed consumer; snapshots every N events.

Every word is true. And to a reviewer who doesn't live in Holler's projection layer, it is
*unrankable* — they can't tell who it's for, whether it matters, or whether the shape is right.
It's a description of the machine, handed to someone who hasn't seen the machine.

The second one names the public first. This change touched a **read model**, so the public on the
far side of that seam is the **analyst** who queries it. Lead with them:

> An ops analyst asking *"which channels are busiest this week?"* used to export the whole event
> log and hand-write a 40-line fold. Now it's one `SELECT`. Here's what they go through, before
> and after:

```
┌────────────────────────────────────────────────────┐
│ THE ANALYST GOES THROUGH  —  before                │
└────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────┐
│ asks: which channels are busiest this week?        │
└────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────┐
│ exports the whole event log                        │
└────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────┐
│ hand-writes a 40-line fold, by channel             │
└────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────┐
│ debugs it, re-runs                                 │
└────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────┐
│ an answer — hours later                            │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│ THE ANALYST GOES THROUGH  —  after                 │
└────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────┐
│ asks: which channels are busiest this week?        │
└────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────┐
│ SELECT channel, count FROM counts_by_channel       │
│ ORDER BY count DESC                                │
└────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────┐
│ a ranked answer — seconds                          │
└────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────┐
│ if the projection lags the log:                    │
│ served with a freshness stamp — staleness known    │
└────────────────────────────────────────────────────┘
```

Same diff, same code. The second version leads with a person and the arc they walk. A reviewer
who has never opened the projection layer can still judge it — because "40 lines of fold became
one query" needs no context to understand, and "does the freshness stamp cover the staleness the
analyst cares about?" is now a question they can actually ask.

## Who is the public? Whoever's on the far side of the seam you touched

"Think about the user" stalls on *which* user. Seam already has the answer in its own metaphor:
the public of a change is the consumer that sits on the far side of the seam your change crossed.

```
┌──────────────────────────────────────────────────────────────────────┐
│ THE PUBLIC                                                         │
│ whoever is on the far side of the seam you touched                 │
└──────────────────────────────────────────────────────────────────────┘
──────────────────────────────────────────────────────────────────────
┌──────────────────────────────────────────────────────────────────────┐
│ touch the pure core        →  a DEV: a new failing test            │
└──────────────────────────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────────────────────────┐
│ touch a projection / table →  an ANALYST: one query, not a fold    │
└──────────────────────────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────────────────────────┐
│ touch the shell / UI       →  an END USER: what they see & click   │
└──────────────────────────────────────────────────────────────────────┘
```

Change the pure core and the public is the **dev** who calls it — a new exhaustiveness error or a
new failing test *is* the core telling them something. Change a projection and it's the
**analyst**. Change the shell and it's the **end user**. So "who benefits?" is answered by "which
side of which seam did I move?" — often *not* the end user. This is why the taxonomy isn't a bolt-on
rule: it's `name the consumer the seam serves`, already in the [standing
checklist](../seam.md#the-standing-checklist), turned into a *presentation order*.

## Why leading with the journey matters more the less context your reader has

The default framing — describe the machine — quietly assumes the reader already knows the machine.
That assumption holds when you're pairing with the person who wrote the projection layer. It
collapses in the room you actually ship into: a midsize company where most reviewers have **no
context** on your subsystem and no time to acquire it. To them, the mechanical diff is a wall of
proper nouns. The *journey* — a named person, trying to do a thing, before and after — is the one
artifact that reads without a prerequisite.

This is the old discipline behind a use case. Alistair Cockburn's *Writing Effective Use Cases*
makes the point that a use case earns its keep by being **readable to any stakeholder** — an
engineer, a PM, the analyst themselves — not just to the author. That readability is exactly what
you need in a low-context room. (Cockburn is also the ports-and-adapters author whose I/O-boundary
metaphor Seam already leans on; the same instinct — name the actor on the outside of the boundary —
shows up on both sides of his work.)

Don't over-formalize it, though. You don't need Cockburn's full template — actor, scope, goal
level, numbered main-success-scenario with lettered extensions. A **flowchart** or a **numbered
walkthrough** is plenty. The whole discipline is: *name the person, name what they're trying to do,
and walk the path they take — including where it forks or fails.* The failure branch matters
(the analyst hitting a lagging projection is where the interesting design question lives), but a
tidy three-step list beats a rigorous artifact nobody reads.

## Why this is a Seam rule, not just PR etiquette

Seam's litmus already says: explain the way a good PR description does — the before/after *feel*,
not the mechanical change — and ground every finding in a real example for a named someone. This
story is those two rules fused and given an order:

- **Named someone → the public on the far side of the seam.** The abstract "someone" gets a
  concrete address: the consumer your seam serves.
- **Before/after feel → walk their journey.** The vivid form of "how does it feel" for a change is
  the arc the affected person walks, drawn as steps you can point at.
- **Make it visible → aimed at the user, not the architecture.** The seam map makes the *structure*
  visible; the journey flowchart makes the *experience* visible. Both are the same bet — a thing on
  screen beats a paragraph — pointed at different things.

## The general lesson

- **A change request is a presentation to the public.** Lead with how the public experiences the
  change, not with the diff. The diff is the evidence; the experience is the point.
- **The public is whoever's on the far side of the seam you touched.** Core → a dev (a new failing
  test). Table/projection → an analyst (one query, not a fold). Shell → an end user. Answer "who
  benefits?" by "which seam did I move?" — often not the end user.
- **Walk the journey; don't just name the user.** A flowchart or a numbered walkthrough of what the
  person goes through — before and after, including where it forks or fails — is the artifact. Name
  the actor and their goal, then trace the path.
- **The less context your reader has, the more the journey carries.** In a low-context room a
  mechanical diff is unrankable; a named person's before/after reads with no prerequisite. That's
  the old use-case discipline (Cockburn) — readable to any stakeholder — not a rigid template.
- **It's usually re-framing, not re-doing.** The same diff, announced two ways. Move the person and
  their journey to the front and a reviewer who's never seen your subsystem can still judge it.
