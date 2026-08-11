# Seam in Go

> **At a glance.** [Seam](../seam.md) states its guards in the abstract; this shows each one
> as Go you could paste in. It mirrors the standing checklist section by section, and
> deliberately reuses the same worked examples as [Seam in
> TypeScript](./typescript.md) — the same booking, the same two ids, the same cart — so the
> two files can be read side by side. What changes between them is not whether the invariant
> is guarded but **which rung of the ladder guards it**: Go closes some doors the type
> checker can't close in TypeScript, and leaves others to a linter or a test. Both are the
> value; neither is the value. Snippets assume Go 1.21+ and the standard `testing` package.

## Boundaries & layering — enforce the line

The core declares the narrow **port** it needs. Interfaces in Go are satisfied implicitly, and
the idiom is that the *consumer* writes them — so the adapter below never imports the core,
never names the interface, and cannot leak its own types back across the seam:

```go
// core/schedule.go — the core declares what it needs and imports nothing of the shell
type Clock interface{ Now() time.Time }

func NextRun(last time.Time, clk Clock) time.Time { /* ... */ }
```

```go
// shell/clock.go — satisfies core.Clock without saying so, and without importing core
type SystemClock struct{}

func (SystemClock) Now() time.Time { return time.Now() }
```

The checklist's litmus — *if a test fake needs more than a lambda, the port is too wide* — is
literal here, because a single-method port can be faked by a function:

```go
type ClockFunc func() time.Time

func (f ClockFunc) Now() time.Time { return f() }

// in a test:
got := NextRun(last, ClockFunc(func() time.Time { return fixed }))
```

Make the direction a **build failure**, not a convention. Layering is `depguard`; the
`internal/` rule in *Working in isolation* below is stronger still:

```yaml
# .golangci.yml — the core may not reach into the shell
linters-settings:
  depguard:
    rules:
      core-stays-pure:
        files: ["**/internal/core/**"]
        deny:
          - pkg: "myapp/internal/shell"
            desc: "the core must not depend on I/O"
```

## Illegal states & invariants — close the set, then guard the match

Go has no sum type. The idiom is an interface with an **unexported marker method**, which
closes the set at the package boundary — no package outside this one can add a variant
(`go/ast` does this with `exprNode()`). Think Kotlin's `sealed interface`, scoped to a package:

```go
// Booking is exactly one of the three variants below.
type Booking interface{ isBooking() }

type Pending   struct{ RequestedAt time.Time }
type Confirmed struct{ ConfirmedAt time.Time }
type Cancelled struct{ Reason string }

func (Pending) isBooking()   {}
func (Confirmed) isBooking() {}
func (Cancelled) isBooking() {}
```

A `Booking` still can't be both `Confirmed` and `Cancelled` — that half is identical to the
TypeScript version. What differs is the forced audit: **Go will not fail the build when you
add a fourth variant and forget a case.** So the guard drops a rung, from *compile error* to
*lint rule in CI*, via a `//sumtype:decl` directive and `gochecksumtype`:

```go
//sumtype:decl
type Booking interface{ isBooking() }

func Summarize(b Booking) string {
    switch b := b.(type) { // gochecksumtype fails CI if a variant is missing here
    case Pending:   return fmt.Sprintf("pending since %s", b.RequestedAt.Format(time.RFC3339))
    case Confirmed: return fmt.Sprintf("confirmed at %s", b.ConfirmedAt.Format(time.RFC3339))
    case Cancelled: return "cancelled: " + b.Reason
    default:
        panic(fmt.Sprintf("unhandled Booking variant %T", b))
    }
}
```

That rung is real but weaker, and worth naming out loud rather than papering over: it holds
only as long as the linter runs in CI, where the TypeScript version holds as long as the code
compiles. For a `const`/`iota` enum rather than an interface, the equivalent is the
`exhaustive` linter.

**Distinct types for indistinct values** goes the other way — what costs a phantom brand and a
smart constructor in TypeScript is one line each here, because Go's defined types are nominal:

```go
type UserId  string
type OrderId string

func LoadUser(id UserId) (User, error) { /* ... */ }

var oid OrderId = "ord_123"
LoadUser(oid) // ❌ compile error: cannot use oid (OrderId) as UserId
```

*Limit:* `LoadUser(UserId(oid))` compiles. Conversion is always available, so this stops the
accident, not the intent.

**The zero value** is Go's own illegal-state hazard, and it has no TypeScript counterpart:
every struct is constructible in its empty state whether or not that state means anything.
Unexported fields plus a constructor make the bad value unrepresentable *outside the package*:

```go
// Money's zero value would be 0 cents in no currency at all.
type Money struct {
    cents    int64
    currency string
}

func NewMoney(cents int64, currency string) (Money, error) {
    if currency == "" {
        return Money{}, errors.New("money: currency required")
    }
    return Money{cents: cents, currency: currency}, nil
}
```

The package *is* the boundary here — `var m Money` still compiles inside it — so keep the type
in a package small enough that the invariant stays reviewable.

## Working in isolation — keep features from reaching into each other

[Vertical Slices](../vertical-slices.md) ranks a language module system as the strongest way
to enforce a slice boundary. Go ships one in the build tool, for free, with no config:

```
myapp/
  features/
    billing/
      billing.go            # the published entry point
      internal/
        ledger.go           # importable only from within features/billing/...
    shipping/
      shipping.go
```

An `import "myapp/features/billing/internal/ledger"` from `shipping` **fails the build**. Not
a lint warning, not a rule someone can disable — the `go` tool refuses to resolve it. That
covers reaching into internals; `depguard` still earns its keep for the lateral rule that
slices talk through the foundation rather than to each other.

The canary stays informal, exactly as in TypeScript: if a unit test needs a mountain of setup
to reach the thing it's testing, that's the seam talking — fix the coupling, don't grow the
fixture.

## State & effects — guards as tests

**Idempotence** — applying the same effect twice lands once:

```go
func TestReplayingSamePaymentChargesOnce(t *testing.T) {
    once := Fold(Initial, events)

    replayed := append(slices.Clone(events), events[len(events)-1])
    twice := Fold(Initial, replayed)

    if !reflect.DeepEqual(once, twice) {
        t.Fatalf("replay changed state:\n once=%+v\ntwice=%+v", once, twice)
    }
}
```

The `slices.Clone` is not decoration: `append` may write into the caller's backing array, so
skipping it can make the test mutate `events` and quietly pass for the wrong reason.

**Contract check** — the shape crossing a boundary, pinned as a golden file (the `go` tool
ignores `testdata/`, and the `-update` flag convention regenerates it deliberately):

```go
var update = flag.Bool("update", false, "rewrite golden files")

func TestOrderPayloadStillSatisfiesPublishedContract(t *testing.T) {
    got, err := json.MarshalIndent(BuildOrderPayload(), "", "  ")
    if err != nil {
        t.Fatal(err)
    }
    golden := filepath.Join("testdata", "order.golden.json")
    if *update {
        os.WriteFile(golden, got, 0o644)
    }
    want, err := os.ReadFile(golden)
    if err != nil {
        t.Fatal(err)
    }
    if !bytes.Equal(got, want) {
        t.Errorf("payload drifted from the published contract:\n got: %s\nwant: %s", got, want)
    }
}
```

And one guard with no equivalent anywhere else on this list — concurrency correctness as a
check the toolchain runs:

```sh
go test -race ./...
```

## Pure core — immutability and the fold

(From [Pure Core](../pure-core.md) — the architecture you adopt when you want one.)

```go
type Item  struct{ SKU string; Qty int }
type State struct{ Items []Item }

//sumtype:decl
type Event interface{ isEvent() }

type Added   struct{ Item Item }
type Cleared struct{}

func (Added) isEvent()   {}
func (Cleared) isEvent() {}

func Apply(s State, e Event) State {
    switch e := e.(type) {
    case Added:
        return State{Items: append(slices.Clone(s.Items), e.Item)}
    case Cleared:
        return State{}
    default:
        panic(fmt.Sprintf("unhandled event %T", e))
    }
}
```

Here Go is at its weakest and it's worth being blunt about it. There is no `Readonly`.
Assigning a `State` copies the struct, but the `[]Item` inside shares its backing array, so
`append(s.Items, ...)` without the clone would reach back and mutate the caller's state. The
`slices.Clone` is doing the work that `ReadonlyArray` does in the TypeScript version — and
**nothing checks that you remembered it.** That invariant has no rung above *test*, so write
the test:

```go
func TestApplyDoesNotMutateItsInput(t *testing.T) {
    before := State{Items: []Item{{SKU: "a", Qty: 1}}}
    snapshot := State{Items: slices.Clone(before.Items)}

    _ = Apply(before, Added{Item: Item{SKU: "b", Qty: 2}})

    if !reflect.DeepEqual(before, snapshot) {
        t.Fatalf("Apply mutated its input: got %+v, want %+v", before, snapshot)
    }
}
```

**Seeded determinism** — time and randomness come *in*, so a run replays identically:

```go
// the core takes these; it must not reach for time.Now() or the global rand itself
func Decide(s State, now time.Time, rng *rand.Rand) []Event { /* ... */ }
```

*Guard:* `forbidigo` fails the build on the call itself inside the core, which `depguard`
can't do — the core still legitimately needs the `time` package for `time.Time`:

```yaml
# .golangci.yml
linters-settings:
  forbidigo:
    forbid:
      - p: "^time\\.Now$"
        msg: "the core takes its clock as a parameter"
      - p: "^rand\\.(Int|Float64|Intn)$"
        msg: "the core takes its rng as a parameter"
```
