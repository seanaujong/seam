# Beyond superpowers and GSD — a story

> **At a glance.** The motivation behind Seam's bets — especially [*explore before you
> specify*](../seam.md#the-bets) and [*care about invariants, not ritual*](../seam.md#the-bets).
> This is the contrast that made Seam worth building: what the strongest structured AI-dev
> workflows do well, the one phase they all assume away, and why Seam sits *upstream* of them
> rather than against them. The cautionary, contrastive framing lives *here*, in a story — the
> guide itself stays positive.

## The disciplined schools

Two of the strongest AI-dev workflows are deliberately structured, and both are right to be:

- **superpowers** (obra's Claude Code plugin) — test-first: brainstorm, write the failing
  test, make it green, refactor. Rigor through *verification*.
- **GSD** ("Get Shit Done") — a *spec-driven* development system for Claude Code: write a clear
  spec first, then execute it in organized phases with coordinated subagents (it leans on
  careful prompt design and context management to get there). Rigor through *structure*.

Both treat AI coding as an engineering discipline rather than ad-hoc prompting — and that's a
real improvement. Once you know what to build, this is how you build it well: clearly,
verifiably, in order. **Seam doesn't argue with any of that.** It hands off *to* exactly this
kind of execution.

## The phase they both assume away

Look at where each one *starts*: a failing test (superpowers) or a written spec (GSD). Both
presume an intent precise enough to write down. That assumption is sound — except at the moment
it matters most: the start, when you don't yet know what you want and would recognize the right
shape only by seeing it.

You can't write the spec — or the test — for a design you haven't found yet. Specify too early
and you've quietly committed to the first shape that was plausible enough to write down. And
the discipline of producing that spec, or that first failing test, *feels* like rigor — which
makes it easy to mistake "I have a crisp spec" or "I have a red test" for "I'm building the
right thing." The ceremony stands in for the discovery it skipped.

That is Seam's bet 1 and bet 3, stated as what goes wrong without them: you can't specify your
way to a design you haven't explored, and a spec or a test is a *mechanism* — not, by itself,
evidence you're building the right thing.

## Where Seam sits

Seam sits **upstream** of both, and wraps *around* them:

- It **adds the front** they assume away: explore, make it visible, find the shape by reacting
  to something concrete — *before* there's a spec or a test to commit to.
- It **keeps the rigor**, aimed at substance: name the few load-bearing invariants and guard
  each one. A test is welcome — as one way to guard an invariant, not as the ritual you perform
  first.
- It **hands off** to structured execution: once the shape is found and the invariants are
  named, dropping into a spec-driven, test-backed build — superpowers, GSD, or your own — is
  exactly right. Seam can even *start* there when the shape is already settled.

### Who focuses on what

| Concern | Seam | superpowers | GSD |
|---|---|---|---|
| Explore before a spec exists | **its core** | — (starts at the test) | — (starts at the spec) |
| Make the thinking visible — prototypes, diagrams | **yes** | not its job | not its job |
| Find the shape — *what* to build | **its core** | assumed given | assumed given |
| Name the load-bearing invariants | **its core** | implied by the tests | captured in the spec |
| Guard those invariants | yes — a test is one way | **via tests** | via spec + checks |
| Disciplined, structured *execution* | hands off ↦ | **the TDD loop** | **phases + subagents** |

Read top to bottom, the table *is* the thesis: Seam owns the rows above the line — discovery,
and what must hold — and deliberately **hands the last row off**. The execution discipline is
the thing superpowers and GSD already do well; Seam's job is to make sure that, by the time you
reach it, you're executing the right shape with the right invariants named.

So the contrast isn't "rigor versus none" — both schools are rigorous, and Seam keeps their
rigor. The difference is *when* rigor begins. They start once you can specify; Seam supplies
the phase that finds what's worth specifying, then gets out of the way.
