# Boundaries buy freedom — a story

> **At a glance.** A field note behind the [*Working in
> isolation*](../seam.md#the-standing-checklist) checklist, and the counterweight to how much of
> Seam's *example* material leans on one technique — the [event-sourced pure
> core](../pure-core.md). The lesson: a hard boundary around shared state isn't only a
> *defensive* move (testable, safe, invariants guarded). It's a *generative* one — the seal
> around global state is exactly what lets you go wild *inside* each box. Freedom scales **with**
> the strength of the boundary, not against it. And it's true whether or not the outside is
> event-sourced, which is the point.

## What happened

In Undertale and Deltarune, every fight happens inside a small bordered rectangle — the battle
box. Your SOUL, a little heart, moves around inside it dodging whatever the current enemy throws.
And what it throws is *wildly* bespoke, fight to fight. Papyrus turns your heart blue and adds
gravity so you jump instead of float. Undyne turns it green and pins it in place behind a shield
you have to rotate toward incoming spears. Mettaton bolts a live rating meter onto the whole
encounter. Sans moves the box itself around the screen and invents "karmic" damage that ignores
the normal rules. Each fight breaks the previous fight's mechanics on purpose. None of them is
"the combat system" — each is its own little authored world.

Now look at what any of that chaos is *allowed to change* on the way out. The persistent state —
the SAVE — is tiny and guarded: HP, gold, items, LOVE and the kill counts, and a handful of
story flags (did you spare this boss or kill them). A whole bespoke bullet-hell encounter,
however strange its interior rules, can only reach the rest of the game through that narrow
result: you won, fled, spared, or died; your HP and inventory changed; one flag flipped. The
gravity, the green-soul shield, the moving box, Mettaton's rating meter — none of it leaks past
the box. It can't corrupt the save. It can't touch the next scene except through the result.

## The instinct to sand off the special cases

The tidy-minded instinct, staring at that list, is to treat the bespoke-ness as a smell. *Five
fights, five different rule sets — shouldn't we unify these? Factor out a general combat engine
and make each fight configuration?* Special-casing feels like debt; surely the disciplined move
is to generalize it away.

That instinct is wrong here, and it's wrong in a way Seam predicts. It reads the interior
freedom as the problem, when the interior freedom is the *product* — it's what makes each fight
memorable. The thing actually doing the work isn't a general engine. It's the box.

## Why the boundary is what buys the freedom

Seam's [*Boundaries & layering*](../seam.md#the-standing-checklist) checklist has a familiar
face: "the general part resolves whatever it's given; special-casing lives in a layer *above*
it." That's the boundary told defensively — keep the special cases *out* of the general core so
the core stays general. True, and only half the story.

The battle box is the *other* half, the dual. Special-casing doesn't only get kept out of
somewhere; it gets a *home* — a sealed leaf where it's not debt but the entire point. And what
makes that home safe to fill with the weirdest logic you can imagine is precisely that its
contract with global state is narrow and honest: a battle can read your HP and items, and on the
way out it can return a result. That's the whole surface. Because the box *can't* leak, nobody
authoring inside it has to reason about the save file, the overworld, or the next fight. They get
to be reckless in a place where recklessness is contained.

So the causality runs opposite to how "boundary" usually feels. The strong line around global
state isn't the tax you pay for safety; it's the thing that *manufactures* the freedom. Weaken it
— let a fight write arbitrary global flags, let the shield mechanic reach into the overworld — and
every fight now has to be designed against every other fight and against the whole save. The
special cases stop being safe to write. **The seal is the enabler.** A designer's "I can do
anything in here" is bought, exactly, by the engine's "and none of it escapes."

This is also why the story sits where it does in Seam. Much of the *example* material —
[Pure Core](../pure-core.md), the TypeScript guards — reaches for an event-sourced fold, and it's
easy to hear "strong boundary" and think that technique is the point. It isn't. The battle box's
global state might be an event log or a plain mutable save struct; the freedom-inside argument
doesn't care. What earns the freedom is the *narrowness of the contract with shared state*, not
the mechanism behind it. Same genus Seam always cares about — a good, honest boundary — shown
without the one species that keeps standing in for it.

## The general lesson

- **A boundary is generative, not just defensive.** The usual pitch for a seam is safety —
  testable in isolation, invariants guarded, blast radius contained. All true, and all
  undersold. The seal around shared state is *also* what lets the interior be free: bespoke,
  hand-tuned, rule-breaking, without fear. Sell the boundary as the thing that buys play, not
  only the thing that prevents harm.
- **Special-casing has a home; it isn't always debt.** "Keep special cases out of the general
  core" and "give special cases a sealed box to thrive in" are the same boundary seen from two
  sides. Inside a leaf whose contract with global state is narrow, bespoke logic is the payoff,
  not a smell to generalize away. Don't reflexively unify five vivid boxes into one pale engine.
- **Freedom scales with the strength of the boundary.** The wilder you want the interior, the
  *harder* the line around global state has to be. Loosen the contract and every box must now be
  designed against every other box; the freedom evaporates. Narrow the contract and the interior
  can hold anything.
- **The contract with global state is the load-bearing invariant — guard *that*, leave the rest
  free.** This is selective enforcement, pointed inward: pour your rigor into the box's tiny,
  honest surface to shared state (what can it read, what result can it return), and deliberately
  guard *nothing* about the interior. *Guard:* a dependency rule that forbids a box reaching
  global state except through that surface — so the seal that buys the freedom can't quietly rot.
- **It's the boundary, not the technique.** Event sourcing, a mutable struct, a database row —
  the freedom-inside argument is indifferent to how global state is stored. What earns it is the
  narrowness of the crossing. Don't mistake the species for the genus.
