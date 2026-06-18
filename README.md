# Seam

<p align="center">
  <img src="https://github.com/user-attachments/assets/d9a6cf80-cd43-42dd-b7d9-8e8263b469ee" alt="A clothing seam — the visible, intentional line where two pieces deliberately join" width="520">
</p>

Most AI coding tools kick in the moment you can write the spec. But the hardest part is
*before* that — when you don't yet know what you want.

**Seam is a way to design software by exploring, not specifying:**

- **It's ok to not know what you want** — make something you can react to, and the right shape
  shows itself.
- **Pictures > paragraphs** — make the thinking visible, then ask the one question that changes
  everything: *"how does this feel?"*
- **Build a codebase you can move fast in** — change one part without holding the whole thing in
  your head.
- **Enforce what you care about** — the few things that must always hold become checks the build
  runs, not hopes.
- **Think about your users** — every decision lands on a real person, or it's not finished.

## How it works

Seam is a workflow you enter at whatever stage matches where you are — a brand-new idea, a
codebase to understand, or a settled plan to build. You won't always start at the first one:

1. **Design the Product** — when the look and feel are still open: make something to look at
   and react to.
2. **Design the Code** — find the *seam* (where the general core meets the special cases) and
   name the invariants worth guarding. Run over code that already exists, this is the
   "think through this codebase" mode.
3. **Build** — guard what you found, and write the tests that make you confident.

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

Underneath are three bets: **explore before you specify**, **make it visible**, and **care
about invariants, not ritual** — loose while you explore, strict once you've found what
matters.

## Install

Seam is a Claude Code plugin — add the marketplace and install, no cloning required:

```
/plugin marketplace add seanaujong/seam
/plugin install seam@seam
```

Claude Code reaches for it on design and exploration work, or you can invoke it by name.
No Claude Code? The docs stand on their own — start here, then [the method](./plugins/seam/seam.md).

## Use it alongside your build workflow

Seam doesn't replace your test-first or spec-driven setup — it runs *upstream* of it. Use Seam
to figure out what to build, find the seam, and name the invariants worth guarding; then hand
off to whatever builds it well — [superpowers](https://github.com/obra/superpowers)' TDD-and-review
loop, [GSD](https://github.com/open-gsd/gsd-core)'s spec-driven execution, or your own. The
invariants you name in Seam become the first tests those workflows enforce. They co-install
cleanly: Seam triggers on the design-and-explore work, your build workflow on the
implementation.

## Where to look

- **[plugins/seam/seam.md](./plugins/seam/seam.md)** — the method itself: the bets, the standing checklist, the vocabulary.
- **[plugins/seam/SKILL.md](./plugins/seam/SKILL.md)** — the same thing as an agent skill (the cues, not the rationale).
- **[plugins/seam/pure-core.md](./plugins/seam/pure-core.md)** — one architecture to adopt, if you want a recommended one.
- **[plugins/seam/vertical-slices.md](./plugins/seam/vertical-slices.md)** — one way to organize folders so you can move fast.
- **[plugins/seam/examples/typescript.md](./plugins/seam/examples/typescript.md)** — the guards as real code.
- **[plugins/seam/stories/](./plugins/seam/stories/)** — short field notes on *why* it works.

Seam never requires a particular architecture — it meets a codebase where it is. The patterns
above are offered, not imposed.
