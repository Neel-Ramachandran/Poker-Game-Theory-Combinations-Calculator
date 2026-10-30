# Poker Odds Calculator

An 8-max poker range analyzer I built to get a better feel for blockers and
card removal when I'm working on preflop ranges. You pick your seat and your
two hole cards, mark out what you think each opponent is holding on a 13x13
grid, and it tells you how many combos of each hand actually remain and how
likely someone still has it.

The whole thing is a single Python file with no dependencies. Python writes a
temporary HTML page and opens it directly in your browser (no local server
involved); all the combinatorics and equity math run in the page's JavaScript.

## Running it

```bash
python3 hand_odds_calc.py
```

(On Windows, use `python` instead of `python3` if the latter isn't on your PATH.)

It opens a temporary HTML file in your default browser automatically. No pip
install and no setup — it only uses the standard library. That HTML file is
written to your OS temp directory and isn't deleted after the script exits,
so your system's normal temp-file cleanup is what eventually removes it.

## What it does

- Poker table drawn in SVG with all 8 seats and a position selector (seats before yours auto-fold, and you can click any seat to toggle it folded/active)
- A 13x13 hand grid where you can drag to select ranges or type them in (like `TT+, AQs+`, `99-66`, `K9s-K6s`). Both views show the same range; editing the grid merges all the typed groups into one
- Combo counts recounted card-by-card for the cards you're holding (blockers)
- Per-seat probability bars showing how likely at least one opponent has a given hand
- Your equity vs the opponent range if you get all-in preflop, heads-up and against every active (non-folded) seat (Monte Carlo, 40k simulated boards)

## The blocker part

This is the reason I made it. Normally an offsuit hand is 12 combos, suited is
4, and a pair is 6. Once you enter your own hole cards, every hand class in
the opponent ranges is recounted with your two cards removed from the deck.
Holding A-2 offsuit, for example, drops AA from 6 combos to 3 and AKo from 12
to 9, while hands that don't share a rank with yours are unchanged. The
per-seat probabilities then use C(50,2) = 1225 as the denominator, since
opponents are dealt from the 50 cards you aren't holding.

You can type a hand class (`AKo`, `76s`, `QQ`) or exact cards (`AsKh`). Exact
suits only matter when your hand overlaps a suited/offsuit class in the
range, e.g. holding A♠K♥ blocks two AKs combos instead of one. Overlapping
range groups are only counted once in the summary.

## Built with

- Python (standard library only)
- HTML / CSS / JavaScript for the front end
- No frameworks or external packages

## Author

Neel Ramachandran
