# Poker Odds Calculator

An 8-max poker range analyzer. Pick your position and hole cards, build
opponent ranges on a 13x13 grid, and it computes blocker-adjusted combo
counts and per-seat probabilities.

It's a single Python file with no dependencies. The backend does the
combinatorics and serves an HTML/CSS/JS interface to the browser.

## Run

```
python hand_odds_calc.py
```

It opens in your browser automatically.

## What it does

- SVG poker table with 8 seats and a position selector
- Hand range editor: type ranges or drag-select on the 13x13 grid
- Blocker math: holding an ace drops an opponent's AKo combos from 12 to 9,
  AA from 6 to 3, and so on
- Per-seat probability bars using C(50,2) = 1225 as the denominator
