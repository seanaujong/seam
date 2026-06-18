# Seam in TypeScript

> **At a glance.** [Seam](../seam.md) states its guards in the abstract; this shows each one
> as TypeScript you could paste in. It mirrors the standing checklist section by section —
> read a guard there, find its concrete form here. The point isn't that TypeScript is the
> right language; it's that an abstract guard is only real once it's a check the build runs,
> and seeing one language makes the shape obvious. Snippets assume modern TypeScript with
> `strict` on; test snippets use a generic `test` / `expect` you can read as any runner.

## Boundaries & layering — enforce the line

Strict mode is the baseline every other guard leans on:

```jsonc
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  }
}
```

The center talks to **ports**; the shell supplies **adapters**, so I/O is swappable and the
core never imports it:

```ts
// core/ports.ts — the core depends only on this shape
export interface Clock { now(): Date }

// core/schedule.ts — pure, no I/O; takes the port
export function nextRun(last: Date, clock: Clock): Date { /* ... */ }

// shell/systemClock.ts — the concrete adapter lives outside the core
export const systemClock: Clock = { now: () => new Date() };
```

Make the boundary a **build failure**, not a convention — an import linter forbids the core
reaching into the shell:

```js
// .dependency-cruiser.cjs
module.exports = {
  forbidden: [{
    name: "core-stays-pure",
    severity: "error",
    from: { path: "^src/core" },
    to:   { path: "^src/(shell|adapters|ui)" },
  }],
};
```

## Illegal states & invariants — make the bad case not compile

A **tagged union** with an **exhaustiveness check**: adding a variant later breaks the build
at every site that forgot it.

```ts
type Booking =
  | { kind: "pending";   requestedAt: Date }
  | { kind: "confirmed"; confirmedAt: Date }
  | { kind: "cancelled"; reason: string };

function summarize(b: Booking): string {
  switch (b.kind) {
    case "pending":   return `pending since ${b.requestedAt.toISOString()}`;
    case "confirmed": return `confirmed at ${b.confirmedAt.toISOString()}`;
    case "cancelled": return `cancelled: ${b.reason}`;
    default: {
      // add a 4th variant and this line stops compiling — the forced audit
      const _exhaustive: never = b;
      return _exhaustive;
    }
  }
}
```

A `Booking` here can never be both `confirmed` and `cancelled` — the union makes that state
unwriteable, so the dev consuming this type can't construct the contradiction.

**Distinct types for indistinct values** — two ids that are both strings, kept unmixable:

```ts
type Brand<T, B extends string> = T & { readonly __brand: B };
type UserId  = Brand<string, "UserId">;
type OrderId = Brand<string, "OrderId">;

const userId = (s: string): UserId => s as UserId;

declare function loadUser(id: UserId): User;
const oid = "ord_123" as OrderId;
loadUser(oid); // ❌ compile error: OrderId is not assignable to UserId
```

## Working in isolation — keep features from reaching into each other

Each feature exposes a public entry point; a lint rule forbids deep imports into another
feature's internals, so slices can't quietly grow into each other:

```jsonc
// .eslintrc — features talk only through each other's index, never internals
"no-restricted-imports": ["error", {
  "patterns": ["@/features/*/*"]   // allow @/features/x, block @/features/x/internal/*
}]
```

The canary stays informal: if a unit test needs a mountain of setup to reach the thing it's
testing, that's the seam talking — fix the coupling, don't grow the fixture.

This rule enforces the pattern in [Vertical Slices](../vertical-slices.md).

## State & effects — guards as tests

**Idempotence** — applying the same effect twice lands once:

```ts
test("replaying the same payment event charges once", () => {
  const once  = events.reduce(reduce, initial); //         [payment]
  const twice = [...events, events.at(-1)!].reduce(reduce, initial); // [payment, payment]
  expect(twice).toEqual(once); // same idempotency key ⇒ no double charge
});
```

**Contract check** — the shape crossing a boundary is pinned, and a test fails the build if a
producer drifts from it:

```ts
import { z } from "zod";

export const Order = z.object({ id: z.string(), totalCents: z.number().int() });
export type Order = z.infer<typeof Order>;

test("the order payload still satisfies the published contract", () => {
  expect(() => Order.parse(buildOrderPayload())).not.toThrow();
});
```

## Pure core — immutability and the fold

(From [Pure Core](../pure-core.md) — the architecture you adopt when you want one.)

State is `Readonly`; the engine is a pure fold that returns new state instead of mutating:

```ts
type Item  = Readonly<{ sku: string; qty: number }>;
type State = Readonly<{ items: ReadonlyArray<Item> }>;
type Event = { kind: "added"; item: Item } | { kind: "cleared" };

const reduce = (s: State, e: Event): State => {
  switch (e.kind) {
    case "added":   return { ...s, items: [...s.items, e.item] };
    case "cleared": return { ...s, items: [] };
    default: { const _x: never = e; return _x; }
  }
};
```

*Guard* the immutability with the type system (`Readonly` / `ReadonlyArray` on every state
type) plus a lint rule that flags mutable fields, so a stray `push` doesn't slip in.

**Seeded determinism** — time and randomness come *in*; the core never reaches for a global,
so a run replays identically:

```ts
type Rng = () => number;
// core takes these; it must not call Date.now() or Math.random() itself
function decide(s: State, now: Date, rng: Rng): Event[] { /* ... */ }
```

*Guard:* a lint rule banning `Date.now` and `Math.random` inside `src/core`, so the only time
and randomness in the core are the ones passed to it.
