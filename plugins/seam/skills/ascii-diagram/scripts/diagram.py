"""Primitives for aligned ASCII box-and-arrow diagrams.

Explicit layout, not auto-layout: you place the boxes; these helpers handle the
tedious, error-prone parts — padding every line to a consistent display width,
stacking and joining boxes so borders line up, and verifying nothing drifted.

The one subtlety that makes hand-drawing these painful is *display width* vs.
character count: a CJK glyph or emoji occupies two terminal columns, a combining
mark zero, and box-drawing/arrow glyphs (─ ▶ │ ·) one. `display_width` accounts
for that, and every helper pads by it, so a box containing "中文" lines up with
one containing "hello". Always finish with `verify()` — it's the cheap check that
catches a miscount before it ships.

Typical use: write a short generator script that imports this module, builds the
diagram bottom-up (boxes → rows → stack with connectors), prints it, and calls
`verify(lines, width)`.
"""

from __future__ import annotations

import unicodedata
from typing import Iterable, Sequence

# Glyphs that begin a "bordered" line — used by verify() to know which lines must
# share the target width (connector/label lines are free to be shorter).
_BORDER_STARTS = "┌┐└┘├┤┬┴┼│"


def display_width(text: str) -> int:
    """Terminal columns `text` occupies.

    East-Asian Wide/Fullwidth count as 2; combining marks as 0; everything else
    (ASCII, box-drawing, arrows, middots, and East-Asian *Ambiguous*) as 1.
    Treating Ambiguous as 1 matches how a normal (non-CJK-locale) terminal
    renders the box-drawing and arrow glyphs these diagrams are built from.
    """
    width = 0
    for ch in text:
        if unicodedata.combining(ch):
            continue
        width += 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
    return width


def ljust(text: str, width: int) -> str:
    """Left-justify to `width` *display* columns (pads with spaces)."""
    return text + " " * max(0, width - display_width(text))


def rjust(text: str, width: int) -> str:
    """Right-justify to `width` *display* columns."""
    return " " * max(0, width - display_width(text)) + text


def box(
    body: Sequence[str],
    *,
    width: int | None = None,
    title: str | None = None,
    title_right: str = "",
    pad: int = 1,
) -> list[str]:
    """A single bordered box.

    `body` is the content lines. `title` (left) and `title_right` (right) sit on a
    header row just inside the top border. `width` is the total box width incl.
    borders; omit it to size to the widest content. `pad` is the left indent
    inside the border (content gets `pad` leading spaces, then fills to the right
    edge). Returns a list of strings, each exactly `width` display columns wide.
    """
    lead = " " * pad
    needed = [display_width(lead + line) for line in body]
    if title is not None:
        # +1 guarantees at least one space between title and title_right.
        needed.append(
            display_width(lead + title) + (display_width(title_right) + 1 if title_right else 0)
        )
    inner = (width - 2) if width is not None else max(needed + [1])
    total = inner + 2

    out = ["┌" + "─" * inner + "┐"]
    if title is not None:
        left = lead + title
        header = left + rjust(title_right, inner - display_width(left))
        out.append("│" + ljust(header, inner) + "│")
    for line in body:
        out.append("│" + ljust(lead + line, inner) + "│")
    out.append("└" + "─" * inner + "┘")
    assert all(display_width(line) == total for line in out)
    return out


def _box_width(box_lines: Sequence[str]) -> int:
    return display_width(box_lines[0])


def pad_height(box_lines: Sequence[str], height: int) -> list[str]:
    """Grow a box to `height` lines by inserting blank interior rows just above
    its bottom border, so unequal-height boxes can sit in one aligned row."""
    out = list(box_lines)
    inner = _box_width(out) - 2
    blank = "│" + " " * inner + "│"
    while len(out) < height:
        out.insert(len(out) - 1, blank)
    return out


def row(boxes: Sequence[Sequence[str]], *, gap: int = 4) -> list[str]:
    """Place boxes side by side, separated by `gap` spaces, padded to equal
    height. Returns the combined lines."""
    height = max(len(b) for b in boxes)
    padded = [pad_height(b, height) for b in boxes]
    spacer = " " * gap
    return [spacer.join(parts) for parts in zip(*padded)]


def connector(col: int, *, label: str = "", glyph: str = "▼") -> list[str]:
    """A two-line vertical connector at column `col`: a `│` (with optional label)
    then an arrow (`▼` by default; pass `▲` for upward). Use to link a box to the
    one below it."""
    bar = " " * col + "│" + (f" {label}" if label else "")
    return [bar, " " * col + glyph]


# Box-drawing junction for a (up, down, left, right) set of connections.
_JUNCTION = {
    (False, True, False, True): "┌",
    (False, True, True, False): "┐",
    (True, False, False, True): "└",
    (True, False, True, False): "┘",
    (False, True, True, True): "┬",
    (True, False, True, True): "┴",
    (True, True, False, True): "├",
    (True, True, True, False): "┤",
    (True, True, True, True): "┼",
    (False, False, True, True): "─",
    (True, True, False, False): "│",
    (True, False, False, False): "│",
    (False, True, False, False): "│",
}


def fanout(source: int, targets: Sequence[int], *, glyph: str = "▼") -> list[str]:
    """A branching connector: one source column fanning down to several target
    columns — the join under a box that feeds a row of boxes below it.

    Returns three lines — a bus (`┌─┬─┴─┬─┐`-style junctions, with `┴` where the
    source meets it), a row of `│` drops, and a row of arrows. Keep source/targets
    indented (> 0) so the bus isn't flush-left; `verify` only checks lines that
    *begin* with a border glyph, and an indented bus starts with a space, so it's
    correctly treated as a free-form connector rather than a box row.
    """
    targets = sorted(targets)
    lo, hi = min([source, *targets]), max([source, *targets])
    tset = set(targets)
    bus = []
    for c in range(hi + 1):
        if c < lo:
            bus.append(" ")
            continue
        up, down, left, right = c == source, c in tset, c > lo, c < hi
        bus.append(" " if not any((up, down, left, right)) else _JUNCTION.get((up, down, left, right), "─"))
    drops = "".join("│" if c in tset else " " for c in range(hi + 1))
    arrows = "".join(glyph if c in tset else " " for c in range(hi + 1))
    return ["".join(bus), drops, arrows]


def hrule(label: str, width: int, *, fill: str = "─") -> str:
    """A centered divider — `label` centered in `fill` to `width` columns. Good as
    a lightweight layer separator (e.g. "──── pure modules ────")."""
    pad = max(0, width - display_width(label))
    left = pad // 2
    return fill * left + label + fill * (pad - left)


def stack(*blocks: str | Sequence[str], gap: int = 0) -> list[str]:
    """Concatenate blocks (each a string or list of strings) vertically, with
    `gap` blank lines between them."""
    out: list[str] = []
    for i, block in enumerate(blocks):
        if i and gap:
            out.extend([""] * gap)
        out.extend([block] if isinstance(block, str) else list(block))
    return out


def render(lines: Iterable[str]) -> str:
    return "\n".join(lines)


def verify(lines: Sequence[str], width: int | None = None) -> int:
    """Check that every bordered line shares one display width.

    Pass `width` to assert a specific target (e.g. 80); omit it to just require
    all bordered lines agree. Raises ValueError naming the offending lines — so a
    miscount fails loudly here instead of rendering crooked in the doc. Returns
    the verified width.
    """
    by_width: dict[int, list[int]] = {}
    for i, line in enumerate(lines):
        if line and line[0] in _BORDER_STARTS:
            by_width.setdefault(display_width(line), []).append(i)

    if not by_width:
        return 0
    if width is None:
        if len(by_width) > 1:
            raise ValueError(
                "bordered lines disagree on width: "
                + ", ".join(f"{w}px×{len(idx)}" for w, idx in sorted(by_width.items()))
            )
        return next(iter(by_width))

    bad = [i for w, idxs in by_width.items() if w != width for i in idxs]
    if bad:
        widths = {i: display_width(lines[i]) for i in bad}
        raise ValueError(f"bordered lines not {width} cols wide (line: width): {widths}")
    return width


if __name__ == "__main__":
    # Self-test: a tiny layered diagram where every full-width element — the top
    # box, the rule, and the joined row of two boxes — is exactly W columns.
    # Joined row math: 18 + gap 4 + 18 == 40, so it matches the W=40 top box.
    W = 40
    top = box(
        ["does a thing", "and another"], width=W, title="top.py", title_right="(entry)"
    )
    a = box(["alpha", "中文 wide"], width=18, title="a.py", title_right="(pure)")
    b = box(["beta"], width=18, title="b.py", title_right="(pure)")
    diagram = stack(
        top,
        connector(W // 2, label="calls"),
        hrule(" modules ", W),
        row([a, b], gap=4),
    )
    print(render(diagram))
    verify(diagram, W)  # Every bordered line is exactly W; raises if not.
    print("\nself-test OK")
