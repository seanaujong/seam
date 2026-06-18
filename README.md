# Seam

*A way to design software when you don't yet know what you want — explore it, see it, and
enforce what matters.*

<!-- Seam photo: drag an image of a clothing seam into any GitHub issue/PR comment on this
repo, copy the generated https://github.com/user-attachments/assets/... URL, and paste it as
the src below. (That hosts it on GitHub's CDN without committing the binary to the repo.) -->
![A clothing seam — where two pieces are deliberately joined, the visible, intentional line that gives the whole garment its shape](https://github.com/user-attachments/assets/REPLACE-WITH-UPLOADED-URL)

Most workflows start the moment you can write a spec or a failing test. Seam is about
everything **before** that — and it carries you through to a build you can trust. In plain
terms:

- **It's ok to not know what you want — let's explore.** Design is discovery. You don't need a
  spec to begin; you begin by making something you can react to, and the shape falls out of
  your reaction.
- **Pictures are worth a thousand words.** Seam makes thinking *visible* — a mockup, a diagram,
  a map of the pieces you can point at. You can only correct what you can see.
- **Make a codebase you can move fast in.** Organize so you can change one part without holding
  the whole system in your head, and so a feature could be lifted out on its own.
- **Enforce what you care about.** The few things that must always hold become *guards* — a
  type, a test, a check the build runs — so a promise the design made can't quietly slip.
- **Think about your users.** Every decision lands on a real person — the dev using the API you
  wrote, the user in the product, the stakeholder reading a metric. If you can't name who a
  choice is for, you haven't finished the thought.

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

## Where to look

- **[plugins/seam/seam.md](./plugins/seam/seam.md)** — the method itself: the bets, the standing checklist, the vocabulary.
- **[plugins/seam/SKILL.md](./plugins/seam/SKILL.md)** — the same thing as an agent skill (the cues, not the rationale).
- **[plugins/seam/pure-core.md](./plugins/seam/pure-core.md)** — one architecture to adopt, if you want a recommended one.
- **[plugins/seam/vertical-slices.md](./plugins/seam/vertical-slices.md)** — one way to organize folders so you can move fast.
- **[plugins/seam/examples/typescript.md](./plugins/seam/examples/typescript.md)** — the guards as real code.
- **[plugins/seam/stories/](./plugins/seam/stories/)** — short field notes on *why* it works.

Seam never requires a particular architecture — it meets a codebase where it is. The patterns
above are offered, not imposed.
