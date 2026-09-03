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
python hand_odds_calc.py
```

It opens a temporary HTML file in your default browser automatically. No pip
install and no setup, it only uses the standard library.

## What it does

- Poker table drawn in SVG with all 8 seats and a position selector
- A 13x13 hand grid where you can drag to select ranges or type them in (like `TT+, AQs+`)
- Combo counts that adjust for the cards you're already holding
- Per-seat probability bars showing how likely at least one opponent has a given hand

## The blocker part

This is the reason I made it. The number of combos for any hand changes based
on the cards you can see. Normally an offsuit hand is 12 combos, suited is 4,
and a pair is 6. If you're holding a card that's part of that hand, the count
drops:

- Holding one ace takes an opponent's AKo from 12 down to 9, and AA from 6 down to 3
- Holding A2o takes their A2o from 12 down to 7

The tool does this automatically across all 169 hand classes based on whatever
hole cards you enter, then uses C(52,2) = 1326 as the denominator for the
probabilities.

## Built with

- Python (standard library only)
- HTML / CSS / JavaScript for the front end
- No frameworks or external packages

## Author

Neel Ramachandran
