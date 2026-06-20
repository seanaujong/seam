---
name: seam
description: >-
  Use when working through the design or shape of software at ANY stage: exploring something
  new whose shape isn't settled, understanding or improving a system that already exists, or
  implementing a settled design well. Seam is a full workflow (explore → design the code →
  build) you can enter at any point — the whole arc when the shape is open, or a later stage when it's
  already settled. It makes thinking
  visible (prototypes, diagrams, comparisons), finds the seam and the invariants worth
  guarding, and grounds each finding in a real example for a real person. It meets a codebase
  where it is and never requires a particular architecture.
---

# Seam

Seam is the exploring-and-thinking half of building software: working out *what's worth making*
and *what must hold true* — largely by making things you can actually look at and react to,
rather than arguing in the abstract. It's a **full workflow you can enter at any stage** —
start wherever your situation does:

- **Design the Product** — when the look and feel are still open and the user will know it when
  they see it.
- **Design the Code** — find the seam and the invariants worth guarding. *The same checklist
  run over code that already exists is the "think through this codebase" mode.*
- **Build** — guard what you found, and implement.

Underneath are three bets — **explore before you specify**, **make it visible**, **care about
invariants, not ritual** — loose while you explore, strict once you've found what matters.
Full rationale, the standing checklist, and the vocabulary: [seam.md](./seam.md).

These are **cues, not a script.** Apply judgment to the situation in front of you — pick the
moves that fit, in the order that fits. Don't choreograph a fixed number of subagents or a
rigid sequence; the model is trusted to do the reasonable thing. The spirit is exploration,
not paperwork: the aim is to see and think clearly, not to complete a checklist.

## Place where the user is

First, work out which stage you're entering — **ask the user, or infer it from the context.** A
brand-new idea, a repo to understand, and a settled plan to ship all start in different places:

- the look and feel are still open → **Design the Product**
- a shape to work out, or a system to understand or improve → **Design the Code** (walk the
  checklist as a diagnostic over existing code)
- a settled design → **Build**; the invariants-as-guards still apply

No stage is optional and none gets skipped — you just enter at the one that matches where
things actually are.

## Meet the codebase where it is

Read what the system actually *does*; don't sort it into a type or impose a shape on it. The
companion patterns — [Pure Core](./pure-core.md), [Vertical Slices](./vertical-slices.md) —
are **optional** answers, offered only when someone is building fresh and wants one.
Conventional choices are legitimate, not drifted seams: a by-layer layout is a real
convention, and an ORM model that owns its own persistence is a design decision, not a
mistake. Diagnose such a system on its own terms — surface what's genuinely fragile, and never
recommend a rewrite no one asked for.

## Design the Product

You're here when there's a look or feel to react to — a screen, a flow, an interaction.

- **State the problem before the options.** Name the need the options serve *before* putting
  them up, so they're judged on fit, not just polish — the crux is the rubric. (The crux-first
  move, applied to choices — [story](./stories/lead-with-the-crux.md).)
- **Make it visible, then ask "how does it feel?"** Produce two or three concrete options the
  user can look at and react to — rendered mockups, a clickable sandbox, a side-by-side
  comparison. A thing on screen, not a paragraph. Then ask the question that unlocks taste:
  *how does this feel to use?* (For any diagram, reach for the `ascii-diagram` skill — the
  project's box-diagram renderer — since hand-drawn boxes drift out of alignment.) You can only
  correct what you can react to.
- **Explore outside the existing thing first.** Don't conform to the surrounding system's
  conventions or design language while exploring — anchoring on what exists forecloses the
  better version. Work in a throwaway space away from those constraints; conform later, on
  purpose. (Story: [stories/explore-outside-first.md](./stories/explore-outside-first.md).)
- **Think about who it's for and their stories** — push product sense, not just aesthetics:
  who is this for, why would it spread, what's the shape of the need.
- **Ground product calls in evidence, and name the tier:** agent reasoning alone (a
  hypothesis) → agent reasoning + internet research (grounded outside) → existing
  metrics/data (your own users — best when it exists). Don't pass a guess off as a fact.
- **Done when** the user points at one option — "this, not that" — and can say why.

## Design the Code

- **Draw the picture, don't write the essay.** Produce a **seam map** (the general core | the
  special-case shell | what crosses between them) and a short **picture doc** — a one-page,
  *crux-first* narrative of vision, invariants, and goals as one clean arc (introduce each
  abstraction by the problem it solves, don't assert it as a conclusion). Use the `ascii-diagram` skill
  (the project's box-diagram renderer) for the map; aligned boxes beat hand-counted ones.
- **Find the seam.** Where does the general core meet the special-case shell? If you can't
  draw the line, you haven't found the boundary — that's a finding, not a stall.
- **Walk the [standing checklist](./seam.md#the-standing-checklist).** Read what the system
  actually does and pull the questions that bite — don't force items that don't apply, and
  don't impose the optional patterns (see *Meet the codebase where it is*). For each
  load-bearing item, name three things:
  1. the **invariant** (what must hold),
  2. its **guard** (a check the build runs — a type, a test, a lint rule), and
  3. a **real example, for a named someone** (the dev who'd hit it, the user it protects, the
     stakeholder who'd ask). An abstract finding is a finding deferred.
- **Stress the seam — run toward what breaks.** Don't just assert the seam and invariants
  hold; attack them. Steer into the hard, icky, or unknown case — the edge input, the
  concurrent path, the migration — and choose one where *wrong* code would visibly differ (an
  input where right and wrong agree tests nothing). Clear confounds so a break is attributable,
  and watch each guard fail when reverted. The counterexample you find now is cheap; the one
  production finds isn't.
- **Want a recommended architecture?** If the user is building fresh and wants a default to
  adopt, offer [Pure Core](./pure-core.md) or [Vertical Slices](./vertical-slices.md).
  Otherwise stay neutral on architecture.
- **Done when** there's a seam map, the invariants named as guards, and a green signal —
  enough that implementation could start tomorrow without re-deriving the design.

## Build

Write the code, add the guards for the invariants worth keeping, and write the unit tests
that would make you confident it works — the ones where, if they pass, you'd trust it. This
stage stands on its own: when the shape is already settled, start here — guard the
load-bearing invariants and skip the rest. For the guards as concrete, pasteable code, see
[examples/typescript.md](./examples/typescript.md).

## The litmus for your output

Before you call it done, check: **does the output show the user *why* this way of thinking
helped them — concretely — or does it only tell them to do it?** Explain it the way a good PR
description does: the intuition, and how the code *feels* to work in **before** versus
**after** — not just the mechanical change. Name the real person an invariant protects, the
better version that exploring surfaced — the way the [stories](./stories/) make a *why* vivid. A
method whose payoff the user has *felt* is one they reach for again. Teaching the why is part
of the deliverable, not a flourish.

## Reference (load on demand)

- **[seam.md](./seam.md)** — the bets, the full standing checklist, "Seam applied to itself,"
  and the vocabulary.
- **[pure-core.md](./pure-core.md)** — one architecture to adopt, if the user wants one.
- **[vertical-slices.md](./vertical-slices.md)** — one way to organize folders for
  feature-isolation, if the user wants one.
- **[production-tax.md](./production-tax.md)** — a lens for "what would it cost to take this to
  production?" — sort each concern by layer × reversibility; anticipate the data-shaped few.
- **[examples/typescript.md](./examples/typescript.md)** — each guard as real code.
- **[stories/](./stories/)** — field notes behind the principles.
