---
name: ascii-diagram
description: >-
  Generate aligned ASCII box-and-arrow diagrams for docs, READMEs, code comments,
  and architecture files. Use this whenever you are creating or editing an ASCII
  diagram built from boxes — layered architectures, component or data-flow
  diagrams, titled boxes with multi-line content, stacked layers joined by
  arrows, or boxes placed side by side — and especially whenever border alignment
  or exact column width matters. Reach for it instead of hand-drawing boxes by
  counting cells, which drifts out of alignment and miscounts wide or ambiguous
  glyphs (─▶, ·, CJK, box-drawing). Provides a small Python module — box, row,
  stack, connector, hrule, and a verify() that fails loudly on any misaligned
  border — with display-width-aware padding.
---

# ascii-diagram

Hand-drawing ASCII box diagrams is deceptively hard: you pad every line to the
same width by counting cells, and one miscount leaves a border one column off —
which a reader sees instantly as crookedness. Worse, the count isn't character
count: a CJK glyph or emoji is **two** terminal columns, a combining mark zero,
and box-drawing/arrow glyphs (`─ ▶ │ ·`) one. This skill does that arithmetic for
you and verifies the result, so you compose layout and never count cells.

## How to use it

Write a short generator script that imports the module, builds the diagram
**bottom-up** (boxes → rows → stack with connectors), prints it, and calls
`verify()`. The module is at `scripts/diagram.py` next to this file.

```python
import sys
sys.path.insert(0, "<this-skill-dir>/scripts")  # the dir containing diagram.py
from diagram import box, row, stack, connector, hrule, render, verify

W = 40  # the diagram's full width — every full-width element must equal this

top = box(["does a thing", "and another"],
          width=W, title="top.py", title_right="(entry)")
a = box(["alpha", "中文 wide"], width=18, title="a.py", title_right="(pure)")
b = box(["beta"],              width=18, title="b.py", title_right="(pure)")

diagram = stack(
    top,
    connector(W // 2, label="calls"),   # a │ then ▼ at that column
    hrule(" modules ", W),              # ──── modules ────, centered to W
    row([a, b], gap=4),                 # side by side: 18 + 4 + 18 == 40 == W
)
print(render(diagram))
verify(diagram, W)   # raises (naming the bad lines) if any border ≠ W
```

Run it, paste the output into the doc, and you're done. (Run `python
scripts/diagram.py` to see this exact example.)

## The primitives

- **`box(body, *, width=None, title=None, title_right="", pad=1)`** — one bordered
  box. `body` is the content lines; `title`/`title_right` sit on a header row
  inside the top border. Omit `width` to auto-size to the widest content. Returns
  a list of strings, each exactly the box width.
- **`row(boxes, *, gap=4)`** — place boxes side by side, `gap` spaces apart,
  padded to equal height.
- **`stack(*blocks, gap=0)`** — concatenate blocks (each a string or list) top to
  bottom, with `gap` blank lines between.
- **`connector(col, *, label="", glyph="▼")`** — a two-line `│` + arrow at a
  column, linking a box to the one below (pass `glyph="▲"` for upward).
- **`fanout(source, targets, *, glyph="▼")`** — a branching connector from one
  source column down to several target columns (a `┌─┬─┴─┬─┐` bus + `│` drops +
  arrows). Use it to join a box above to a row of boxes below; size the boxes and
  gaps so each target column lands on the center of its box in the row.
- **`hrule(label, width, *, fill="─")`** — a centered divider, good as a
  lightweight layer separator.
- **`display_width` / `ljust` / `rjust`** — the display-width-aware building
  blocks, exposed for custom lines (e.g. a bespoke connector or annotation).
- **`verify(lines, width=None)`** — the safety net. With `width`, asserts every
  bordered line is exactly that many columns; without it, just asserts they all
  agree. Raises `ValueError` naming the offending line numbers and widths.

## The one rule that keeps things aligned

**Every full-width element must be the same width** — the top box, each `hrule`,
and each joined `row`. A `row` is only as wide as its boxes plus gaps, so size the
boxes to make the sum match: for three boxes at width `B` with gap `G`,
`3*B + 2*G` must equal the diagram width. Then `verify(diagram, W)` passes because
*every* bordered line (standalone boxes and joined rows alike) is `W`.

If `verify` complains that "bordered lines disagree on width," some row's boxes
don't sum to the diagram width — adjust a box `width` or the `gap`.

## Notes

- **Always finish with `verify()`.** It's the whole point — a miscount fails here,
  loudly, instead of rendering crooked in the committed doc.
- **Wide content just works**: a box containing `中文` or `😀` lines up with an
  ASCII one because padding is by display width, not character count.
- **Title insets**: `title_right` sits flush against the right border; add trailing
  spaces (e.g. `title_right="(pure)  "`) if you want it pulled in.
- **Connectors are free-form**: `connector`/`fanout`/`hrule`/label lines aren't
  checked by `verify` (only lines that *begin* with a border glyph are), so they
  can be any length — keep `fanout`/`connector` indented so their bus doesn't
  start flush-left and get mistaken for a box row.
- This is **explicit layout, not auto-layout** — you decide what goes where. For
  auto-laid-out graphs from a DSL, a tool like `graph-easy` is a different (and
  heavier) approach.
