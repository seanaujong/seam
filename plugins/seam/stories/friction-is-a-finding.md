# Friction is a finding — a story

> **At a glance.** A field note behind [*make the feeling a value at a
> boundary*](../seam.md#seam-applied-to-itself) and the test-ergonomics canary in the [standing
> checklist](../seam.md#the-standing-checklist) — the same move, extended from *observing* a
> result to *driving* a whole flow. The lesson: when working on something feels like it needs a
> human in the loop — "go click that, go read that email" — that friction is a finding about a
> missing dev seam, not a fact about the task. Find where the human-gated effect becomes a value
> an unattended program can read, and the friction dissolves.

## What happened

Holler signs people in with a one-time code (OTP): you type your email, the server emails you a
six-digit code, you type it back — no password. It's the right product call, but it puts a
human's email inbox in the middle of the most-run flow in the system. Every test, every local
poke, every agent trying to exercise a feature has to get past login first.

So the workarounds arrived, one reasonable patch at a time. Tests minted a session token
directly instead of logging in. A stub captured the code in a variable instead of sending it.
The code generator was pinned to a constant — `"424242"` — so a test could predict it. A roster
of accounts (`alice`, `bob`, `carol`) was pre-seeded so nothing had to sign up. The OAuth check
was swapped for a fake. Each is defensible alone. Together they're a smell.

## The instinct to patch each one

Read as five separate conveniences, every workaround looks fine, so you keep adding the next
one. That's the trap. The move is to stop and ask what *single* thing, if it existed, would make
all five unnecessary at once.

Here the answer is plain: **there was no programmatic way to complete the real login in dev.**
Every workaround is a local detour around that one missing thing.

## Why a seam beats the workarounds

Sending an email *feels* like it escapes into the human world — it lands in an inbox, and now a
person has to go read it. But "lands in an inbox" is just an effect crossing a boundary, and a
boundary is exactly where you can catch an effect as a value. Point the server's mail at
**mailpit** — a fake SMTP server that accepts every message and exposes the inbox over an HTTP
API — and the email headed for a human becomes a JSON record an unattended program can fetch.
Holler wraps that in one helper, `pnpm otp <email>`, which reads the latest code back out of
mailpit "for scripts and agents," plus a headless browser test that drives the *real* sign-in —
type email, send code, read it from mailpit, type it back, land signed-in — start to finish with
no human.

This is the same move as making a rendered frame come back as a string you can diff: an effect
that seemed to live in the human world is pinned to a value at a boundary, and once it's a value
the friction is gone. Build the seam once and all five workarounds collapse into it.

One distinction the workarounds blur: **a bypass is not a seam.** Minting a token directly, or a
"skip auth in dev" flag, makes login *reachable by not running it* — so it exercises a different
path than real users hit, and hides that path's breakage. mailpit makes the *real* path
drivable. Prefer the seam; treat a bypass leaking into non-test code as the sign the seam is
still missing.

And the litmus keeps biting after the seam exists. Holler's real-flow browser sign-in
(`login-shot.ts`) is committed but isn't wired into CI — CI runs `pnpm -r check` (typecheck +
unit tests), so the one guard that drives the *real* login end to end never runs, and nothing
catches the day it breaks. And a doc rotted out of sync: `auth.md` still walks through an "unset
`AUTH_SECRET`, type `000000`" dev login that the code dropped — the server now refuses to boot
without the secret, and a test pins `000000 → 401`. Every newer doc says plainly there's no
bypass; that one walkthrough missed the memo. Both are exactly what this litmus is for.

## The general lesson

- **Friction is a finding.** "Working on this needs a human — go click that, read that email,
  solve that captcha" is not a fact about the task; it's a missing dev seam talking. Same tell
  as the canary: if exercising the thing is painful, that's the architecture, not a chore to
  push through.
- **A human at a UI is just another heavy dependency.** The canary says don't make a test drag
  in half the system; this says don't make a flow drag in a person. One instinct — reach the
  thing without the heavyweight dependency — pointed at the human in the loop.
- **The agent is the strictest reader.** "Can an unattended agent drive this flow end to end in
  dev?" is a strict, honest proxy for "is this easy to work on?" Clear the agent's bar and the
  human developer's quality of life comes free — the way *would it survive becoming its own
  deployment?* is a strict proxy for a clean slice boundary.
- **Catch the effect as a value at a boundary.** Whatever seems to escape into the human world —
  an email, a payment, a rendered frame — crosses a boundary on its way out. Capture it there (a
  fake inbox with an API, a sandbox, a frame-as-string) and it becomes something a program can
  produce and read.
- **A bypass is not a seam.** Skipping the flow tests a different path than the real one and
  hides its breakage. Make the real path drivable instead.
- **Collapse the cluster, then guard it.** A pile of small workarounds usually shares one
  missing seam. Find it, home it once, and put a no-human end-to-end test of the *real* flow in
  CI — so the friction can't quietly creep back.
