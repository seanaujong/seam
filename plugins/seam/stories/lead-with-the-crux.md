# Lead with the crux — a story

> **At a glance.** A field note behind Seam's [*write the way you
> design*](../seam.md#seam-applied-to-itself) rule, and the *crux-first* picture doc. The
> lesson: explaining a system by handing over your **conclusions** ("we use a pure
> event-sourced core") teaches memorization; explaining it **crux-first** — stating the problem
> each piece solves *before* naming the piece — lets the reader re-derive the design, which is
> the only version they actually understand. The model is OSTEP, a textbook that distills an
> entire operating system this way.

## What happened

Someone looked at a real project — Holler, an event-sourced chat system with *lots* of concepts
(event logs, folds, projections, snapshots, upcasting, privacy-by-absence, a control plane, …)
— and asked: *could this be distilled and explained the way OSTEP explains an OS?*

The project's `architecture.md` was good. But read closely, it opened with **answers**:

> "A pure event-sourced core wrapped in a thin shell." · "Privacy is enforced by absence, not
> by a guard."

Each line is *true*, and each is a **conclusion** — the end of a thought, handed to the reader
to accept. A reader can memorize "privacy by absence," but they can't tell you *what problem it
solves*, *what would break without it*, or *how to re-derive it* under different constraints.
The understanding that produced the line didn't travel with it.

## What OSTEP actually does

*Operating Systems: Three Easy Pieces* is famous for two moves, and neither is "explain an OS":

1. **Distillation.** It claims an entire OS reduces to **three problems** — virtualization,
   concurrency, persistence — and every mechanism you learn is "just" a technique answering one
   of the three. The three aren't chosen for tidiness; they're *forced by the hardware* (you
   have a CPU, memory, a disk). Distillation collapses a sprawl of concepts onto a few problems
   you can hold in your head.

2. **Crux-first.** Every chapter opens with a boxed **"The Crux of the Problem"** — the
   motivating question stated *before* any solution — and then the mechanism *falls out* of the
   crux. You don't memorize the page table; you feel the problem it answers, and the page table
   becomes the obvious move.

Holler turned out to distill cleanly the same way — its ~25 nouns collapse onto three forced
problems, with the leftover machinery as a "shell" the way OSTEP treats I/O devices:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ HOLLER  ·  Three Easy Pieces                                          taught through one codebase  │
│ every concept below is a technique for exactly one of three problems                               │
└────────────────────────────────────────────────────────────────────────────────────────────────────┘
                ┌──────────────────────────────────┼──────────────────────────────────┐
                │                                  │                                  │
                ▼                                  ▼                                  ▼
┌──────────────────────────────┐   ┌──────────────────────────────┐   ┌──────────────────────────────┐
│ 1 · TRUTH       ≈ Persistence│   │ 2 · ISOLATION    ≈ Virtualize│   │ 3 · AGREEMENT   ≈ Concurrency│
│ Crux: state can lie;         │   │ Crux: one engine,            │   │ Crux: who wins when          │
│ events can't.                │   │ many private worlds.         │   │ writes collide?              │
│                              │   │                              │   │                              │
│ • event log (Recorded<E>)    │   │ • viewFor / canWitness       │   │ • per-stream seq             │
│ • apply   — the fold         │   │ • workspaces (islands)       │   │ • expectedVersion→conflict   │
│ • decide  — the rules        │   │ • invariant walls            │   │ • idempotency keys           │
│ • snapshots / upcasting      │   │ • knowledge vs control       │   │ • async boundary (submit)    │
│ • projections                │   │ • privacy by absence         │   │ • change feed                │
└──────────────────────────────┘   └──────────────────────────────┘   └──────────────────────────────┘
                                                   │ all reads & writes flow through
                                                   ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ SHELL — the ports                                                                    ≈ I/O devices │
│ Memory / SQLite / Postgres stores  ·  transport & identity  ·  SSE delivery  ·  rankers / answerers│
└────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

The distillation is also a *self-test*: every noun landed in exactly one box, and the only
things that resisted (offboarding sagas, ownership transfer) are the "advanced chapters" — which
is the spine confirming itself. If a concept won't sit in one box, the decomposition is wrong.

## What a crux looks like

"Crux" stays abstract until you see the same concept explained both ways. Here is one piece of
Holler — *the event log* — answer-first versus crux-first:

```
┌────────────────────────────────────────────────────────────────────────┐
│ WHAT IS A CRUX?                                                        │
│ Same concept — "the event log" — two ways to land it                   │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────┐      ┌────────────────────────────────┐
│ ANSWER-FIRST   ✗               │      │ CRUX-FIRST   ✓                 │
│ "Holler uses a pure            │      │ "State can lie. How do you     │
│ event-sourced core; state      │      │ build something whose          │
│ is derived by replaying        │      │ history can't?"                │
│ events."                       │      │             │                  │
│                                │      │             ▼                  │
│ Reader: "...ok. why that?"     │      │ store what happened,           │
│ Nothing to re-derive —         │      │ derive state  →  event log     │
│ a conclusion to memorize.      │      │ Reader re-derives the core.    │
└────────────────────────────────┘      └────────────────────────────────┘
```

The content is *identical*. Only the ordering changed — and with it, whether the reader leaves
able to rebuild the idea or merely to recite it.

## Why this is a Seam rule, not just writing advice

Crux-first isn't a separate principle bolted on; it's Seam's own bet pointed at prose. Seam's
deepest claim is **design is discovery, not transcription** — you find a shape by exploring,
you don't transcribe one you already had. An **answer-first doc is the prose version of
asserting the seam up front instead of finding it**: it presents the destination and hides the
discovery, the exact drift Seam warns about in code. A crux-first doc hands the reader the
discovery, so they walk the same path and arrive understanding *why this shape and not another*.

It's also the sharpest form of Seam's "say the *why* before the *what*." The why isn't a
justification appended *after* the answer — it's the **problem stated first**, with the answer
emerging from it.

## The general lesson

- **Lead with the crux.** State the problem each abstraction solves *before* the abstraction.
  "State can lie — how do you build something whose history can't?" beats opening with "we use
  an event-sourced core."
- **It generalizes from explaining to deciding: state the problem before the
  options/solutions.** The same move that makes one solution understandable also makes several
  *comparable* — whenever you put alternatives up (mockups, approaches, architectures), lead
  with the problem they compete to solve. Without the crux in view, options get ranked on polish
  or familiarity; with it, the crux is the rubric.
- **A conclusion without its crux is memorization.** The reader can recite it but can't
  re-derive it, can't say what's load-bearing, can't adapt it when the problem changes.
- **Falsifiable test:** delete a section's conclusion. Does the problem still motivate
  re-deriving it? If the section only reads when you already know the answer, it's answer-first.
- **Distillation pairs with it.** Collapse many concepts onto a few forced problems (OSTEP's
  three; Holler's Truth / Isolation / Agreement), then teach each problem crux-first. A clean
  distillation is itself a self-test — a concept that won't sit in one box means the spine is
  wrong.
- **It's usually re-sequencing, not rewriting.** The content of an answer-first doc is often
  right; the ordering is conclusion-first. Move the crux to the front and the rest follows.
