# Poker Odds Calculator

An 8-max poker range analyzer I built to get a better feel for blockers and
card removal when I'm working on preflop ranges. You pick your seat and your
two hole cards, mark out what you think each opponent is holding on a 13x13
grid, and it tells you how many combos of each hand actually remain and how
likely someone still has it.

The whole thing is a single Python file with no dependencies. Python handles
the combinatorics and writes a temporary HTML page, which it then opens
directly in your browser (no local server involved).

## Running it

```
python3 hand_odds_calc.py
```

It opens a temporary HTML file in your default browser automatically. No pip
install and no setup — it only uses the standard library. That HTML file is
written to your OS temp directory and isn't deleted after the script exits,
so your system's normal temp-file cleanup is what eventually removes it.

## What it does

- Poker table drawn in SVG with all 8 seats and a position selector (seats before yours auto-fold, and you can click any seat to toggle it folded/active)
- A 13x13 hand grid where you can drag to select ranges or type them in (like `TT+, AQs+`)
- Combo counts that adjust for the cards you're already holding
- Per-seat probability bars showing how likely at least one opponent has a given hand

## The blocker part

This is the reason I made it. Normally an offsuit hand is 12 combos, suited is
4, and a pair is 6, and these are the counts the range grid and combo badges
show. Once you enter your own hole cards, the summary combo count is reduced
by 1 (since you're now holding cards you know can't be in an opponent's
range) before the per-seat probabilities are computed against the C(52,2) =
1326 denominator. It isn't yet a full per-hand-class recount for every one of
the 169 hand classes based on your specific hole cards — just a flat
adjustment to the overall total.

## Built with

- Python (standard library only)
- HTML / CSS / JavaScript for the front end
- No frameworks or external packages

## Author

Neel Ramachandran
