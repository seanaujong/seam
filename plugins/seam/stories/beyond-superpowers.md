# Seam next to superpowers and GSD — a story

> **At a glance.** The motivation behind Seam's bets, and an honest place to put the
> comparison. superpowers and GSD are both excellent, and both do far more than "just build" —
> each has real idea-exploration, and even visual-mockup, phases. So the difference is *not*
> that they skip discovery. It's where each one's **center of gravity** sits, and what it asks
> you to care about. The contrastive framing lives here, in a story; the guide stays positive.

## Credit where it's due

- **superpowers** (obra) is a disciplined methodology shipped as composable skills. It opens
  with a *mandatory* `brainstorming` step that "explores user intent, requirements and design,"
  proposes 2–3 approaches, and writes an approved design doc — it even has a visual-mockup
  companion — then hard-gates into small-task planning and **strict, Iron-Law TDD** ("no
  production code without a failing test first"), with every change reviewed on two axes. Its
  center of gravity is **disciplined, verifiable, hands-off execution**.
- **GSD** ("Get Shit Done") is a context-engineering, spec-driven system. Optional
  `/gsd-explore` (Socratic ideation), `/gsd-sketch` ("explore design directions through
  throwaway HTML mockups… 2–3 interactive variants… so I can click around"), and `/gsd-spike`
  (feasibility) sit in front of a five-phase Discuss → Plan → Execute → Verify → Ship loop, run
  by fresh-context subagents writing to a committed `.planning/` folder. Its center of gravity
  is **executing a spec at scale without losing the thread** — beating context-rot through
  subagent orchestration.

Both, in other words, *can* explore, sketch, and react to mockups. Claiming "they jump straight
to tests and skip figuring out what to build" would simply be false — and worth saying plainly,
because the honest differences are sharper than the false one.

## What's actually different

Not "we explore and they don't." Three real things:

1. **Center of gravity.** For both, idea-exploration is a *front porch* to an execution engine —
   and the engine is the point (TDD-and-review discipline for superpowers; context-engineered
   orchestration for GSD). For Seam, the front porch *is* the house: finding the shape and
   naming what must hold is the whole method, and execution is what it hands off. GSD says it of
   itself — it "refines and operationalizes rather than discovers the core product vision." Seam
   is the part that discovers.

2. **The few invariants you care about, not a blanket ritual.** superpowers wants a failing test
   before *every* line; GSD wants the spec captured *exhaustively* up front. Both are forms of
   "write it all down, cover it all." Seam's bet is narrower: name the *few* load-bearing
   invariants you actually care about and guard those — a test is one mechanism, not a law — and
   otherwise write the tests that make you confident. Selective enforcement of what matters over
   uniform ceremony.

3. **A way of thinking you carry, not a machine you operate.** GSD is ~60 commands, a dozen
   subagents, and a `.planning/` apparatus; superpowers is a gated pipeline with hooks and
   orchestrated subagents. That machinery is real value — and real surface area. Seam is
   deliberately the opposite: a handful of cues and one question ("how does this feel?"), with
   **cue, don't choreograph** as a rule — no fixed subagent counts, no command surface. If
   subagent orchestration is the part you care about, GSD is built for it; Seam is the taste you
   bring *to* whatever you build with.

And one quieter difference: Seam runs as a **neutral diagnostic over a codebase that already
exists**, imposing no architecture — where these are oriented toward building.

## Where Seam sits

Seam sits **upstream** and hands off cleanly. Its exploration is wider and more open ("it's ok
to not know what you want," product and market evidence, not just design intent), and its rigor
is *selective*. Once the shape is found and the invariants named, dropping into superpowers'
TDD-and-review discipline, or GSD's context-engineered execution, is exactly the right next
move — Seam can even *feed* their brainstorm or spec step. What Seam deliberately does **not**
try to be is the execution harness: the autonomous TDD loop, the context-engineering, the
verification gates. Those are theirs, and they're good at them.

## Who focuses on what

| Concern | Seam | superpowers | GSD |
|---|---|---|---|
| Idea exploration before code | **the whole point** | yes — gated `brainstorming` | yes — optional `/gsd-explore` |
| Visual mockups to react to | yes — "how does it feel?" | yes — visual companion | yes — `/gsd-sketch` |
| Product / market sense (users, evidence) | **foregrounded** | design-level only | mostly not |
| What it enforces | the *few* invariants you care about | a failing test before all code | a fully captured spec |
| Execution machinery (subagents, context) | hands off ↦ | **autonomous TDD + review** | **context-engineered orchestration** |
| Architecture imposed | none | none | none |
| Diagnostic over existing code | **yes** | oriented to building | onboarding → build |

Read honestly, the top rows are *not* "us vs —": all three explore, sketch, and react to
mockups. The real split is the middle and bottom — *what each one enforces*, and *whether the
heavy execution machinery is the point*. Seam keeps the front wide, the enforcement selective,
and hands the machinery off.
