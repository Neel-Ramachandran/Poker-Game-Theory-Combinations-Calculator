#!/usr/bin/env python3
"""
Hand Odds Calculator — 8-Max Poker Range Analyzer (Fixed Edition)
Run:  python hand_odds_calc.py
"""

import os
import tempfile
import webbrowser
from pathlib import Path

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Hand Odds Calculator</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%}
body{
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  background:#0f1419;color:#e0e0e0;
  display:flex;flex-direction:column;overflow:hidden;
}

header{
  background:#1a2332;color:#fff;
  padding:.55rem 1.25rem;
  display:flex;align-items:baseline;gap:.75rem;
  border-bottom:1px solid #2a3a4a;flex-shrink:0;
}
header h1{font-size:1rem;font-weight:600}
header p{font-size:.72rem;color:rgba(255,255,255,.45)}

/* Everything fits in one screen: the columns shrink, the page never scrolls */
.wrap{
  flex:1;min-height:0;padding:.75rem;
  display:grid;grid-template-columns:minmax(0,1fr) 380px;gap:.75rem;
}
.col{display:flex;flex-direction:column;gap:.75rem;min-height:0}

.card{
  background:#1a2230;border:1px solid #2a3a4a;border-radius:12px;
  box-shadow:0 2px 10px rgba(0,0,0,.3);padding:.9rem 1rem;
}
.card-head{display:flex;align-items:center;justify-content:space-between;gap:.75rem;flex-wrap:wrap;margin-bottom:.5rem}
h3{font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#7a8aa0;margin-bottom:.6rem}
.card-head h3{margin-bottom:0}

.table-card{flex:1;min-height:0;display:flex;flex-direction:column}
.tbl-svg{flex:1;min-height:0;width:100%}
.hint{font-size:.67rem;color:#6a7a8a;text-align:center;margin-top:.25rem}

.pos-grid{display:flex;flex-wrap:wrap;gap:4px}
.pos-btn{
  border:1.5px solid #3a4a5a;background:#111820;color:#a0b0c0;
  border-radius:7px;padding:4px 9px;font-size:.72rem;font-weight:600;
  cursor:pointer;transition:all .15s;
}
.pos-btn:hover{border-color:#2563eb;color:#6fb7ff}
.pos-btn.active{background:#2563eb;border-color:#2563eb;color:#fff}

.hand-input{
  width:100%;border:1.5px solid #3a4a5a;background:#111820;color:#e0e0e0;
  border-radius:8px;padding:6px 9px;font-size:.85rem;font-family:'SF Mono','Fira Code',Menlo,monospace;
  transition:border-color .2s;
}
.hand-input:focus{outline:none;border-color:#2563eb}
.hand-display{font-size:.8rem;margin-top:.4rem;padding:.5rem;background:rgba(37,99,235,.1);
  border-left:3px solid #2563eb;border-radius:4px;color:#a0d0ff}

.tabs{display:flex;gap:0;border-bottom:1px solid #2a3a4a;margin-bottom:.8rem}
.tab{
  flex:1;padding:.6rem;font-size:.75rem;font-weight:600;color:#7a8aa0;
  border:none;background:none;cursor:pointer;transition:all .2s;
  border-bottom:2px solid transparent;
}
.tab:hover{color:#a0b0c0}
.tab.active{color:#6fb7ff;border-bottom-color:#2563eb}

.eq{margin-top:.8rem}
.eq-head{display:flex;justify-content:space-between;align-items:baseline;font-size:.75rem;color:#a0b0c0;margin-bottom:5px}
.eq-head small{color:#6a7a8a}
.eq-head b{font-size:1.2rem;color:#e0e0e0}
.eq .pt{height:12px}
.eq-sub{font-size:.68rem;color:#6a7a8a;margin-top:5px}

.ranges-card{flex:1;min-height:0;display:flex;flex-direction:column}
.tab-panel{display:none;flex:1;min-height:0;overflow-y:auto}
.tab-panel.active{display:block}

.hand-grid{
  display:grid;grid-template-columns:repeat(13,1fr);gap:2px;
  background:#0f1419;padding:.5rem;border-radius:8px;
  user-select:none;
}
.hand-cell{
  aspect-ratio:1;display:flex;align-items:center;justify-content:center;
  background:#111820;border:1px solid #2a3a4a;border-radius:4px;
  font-size:.65rem;font-weight:600;color:#7a8aa0;cursor:pointer;
  transition:all .15s;
}
.hand-cell:hover{background:#1a2a3a;border-color:#3a4a5a}
.hand-cell.selected{background:#2563eb;border-color:#2563eb;color:#fff;font-weight:700}

.rr{display:flex;align-items:center;gap:6px;margin-bottom:6px}
.rr input{
  flex:1;border:1.5px solid #3a4a5a;background:#111820;color:#e0e0e0;
  border-radius:8px;padding:5px 9px;font-size:.82rem;
  font-family:'SF Mono','Fira Code',Menlo,monospace;transition:border-color .2s;
}
.rr input:focus{outline:none;border-color:#2563eb}
.badge{
  font-size:.67rem;padding:2px 8px;border-radius:20px;font-weight:600;
  white-space:nowrap;min-width:76px;text-align:center;transition:all .2s;
}
.del{
  border:none;background:none;color:#6a7a8a;font-size:1.1rem;
  cursor:pointer;padding:0 2px;line-height:1;flex-shrink:0;
  transition:color .15s;
}
.del:hover{color:#ff6b6b}
.add-btn{
  width:100%;margin-top:4px;padding:6px;border:1.5px dashed #3a4a5a;
  background:none;color:#6a7a8a;border-radius:8px;font-size:.77rem;
  cursor:pointer;transition:all .15s;
}
.add-btn:hover{border-color:#2563eb;color:#6fb7ff}

.help-txt{font-size:.69rem;color:#6a7a8a;line-height:1.7;margin-top:.55rem}
.help-txt code{
  background:#111820;padding:1px 5px;border-radius:4px;
  font-family:monospace;font-size:.75rem;color:#a0d0ff;
}

.results{flex-shrink:0;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:1.25rem}
.sg{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.sc{background:#111820;border:1px solid #2a3a4a;border-radius:8px;padding:.55rem .8rem}
.sc .sl{font-size:.67rem;color:#7a8aa0;margin-bottom:2px}
.sc .sv{font-size:1.1rem;font-weight:700;color:#e0e0e0}
.sc .sv small{font-size:.7rem;font-weight:500;color:#7a8aa0}
.sc.hl .sv{color:#ffc700}
.empty{font-size:.75rem;color:#6a7a8a;padding:.4rem 0}

@media(max-width:1000px){
  body{overflow:auto;display:block}
  .wrap{grid-template-columns:1fr}
  .tbl-svg{flex:none;aspect-ratio:720/430}
  .results{grid-template-columns:1fr}
}

.pr{display:flex;align-items:center;gap:7px;margin-bottom:5px}
.pl{font-size:.72rem;font-weight:600;width:40px;flex-shrink:0;color:#a0b0c0}
.pt{flex:1;height:16px;background:#111820;border:1px solid #2a3a4a;border-radius:4px;overflow:hidden}
.pf{
  height:100%;border-radius:3px;display:flex;align-items:center;
  font-size:9px;font-weight:700;color:#fff;transition:width .35s ease;
  min-width:2px;padding-right:5px;justify-content:flex-end;
}
.pp{font-size:.72rem;font-weight:700;width:44px;text-align:right;color:#a0b0c0}
.sep-line{height:1px;background:#2a3a4a;margin:7px 0}

.clear-btn{padding:6px;border:1.5px solid #3a4a5a;background:none;color:#6a7a8a;border-radius:8px;font-size:.75rem;cursor:pointer;transition:all .15s}
.clear-btn:hover{border-color:#dc2626;color:#ff6b6b}
</style>
</head>
<body>

<header>
  <h1>🃏 Hand Odds Calculator</h1>
  <p>8-max ring game · range &amp; blocker analysis</p>
</header>

<div class="wrap">
  <div class="col">
    <div class="card table-card">
      <div class="card-head">
        <h3>Your position</h3>
        <div class="pos-grid" id="posGrid"></div>
      </div>
        <svg id="tsvg" class="tbl-svg" viewBox="0 0 720 430" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <radialGradient id="fg" cx="50%" cy="47%" r="52%">
              <stop offset="0%" stop-color="#2d7a4f"/>
              <stop offset="100%" stop-color="#1a4332"/>
            </radialGradient>
          </defs>
          <ellipse cx="360" cy="215" rx="306" ry="174" fill="#5c3317"/>
          <ellipse cx="360" cy="215" rx="298" ry="166" fill="#3d2008"/>
          <ellipse cx="360" cy="215" rx="268" ry="150" fill="url(#fg)"/>
          <ellipse cx="360" cy="212" rx="215" ry="108" fill="none"
            stroke="rgba(255,255,255,.045)" stroke-width="1"/>
          <text x="360" y="210" text-anchor="middle" fill="rgba(255,255,255,.13)"
            font-size="12" font-family="Georgia,serif" letter-spacing="4">POKER</text>
          <text x="360" y="226" text-anchor="middle" fill="rgba(255,255,255,.08)"
            font-size="8.5" font-family="Georgia,serif" letter-spacing="2.5">8 · MAX RING</text>
          <g id="seats"></g>
        </svg>
      <div class="hint">Picking your position folds everyone who acts before you. Click any seat to fold / unfold it (e.g. if someone opened).</div>
    </div>

    <div class="card results">
      <div>
        <h3>Summary</h3>
        <div class="sg">
          <div class="sc"><div class="sl">Combos in range</div><div class="sv" id="sCombos">—</div></div>
          <div class="sc"><div class="sl">Blocked by your hand</div><div class="sv" id="sBlocked">—</div></div>
          <div class="sc"><div class="sl">Per opponent</div><div class="sv" id="sPer">—</div></div>
          <div class="sc hl"><div class="sl" id="sLbl">Any of N opp.</div><div class="sv" id="sAny">—</div></div>
        </div>
      </div>
      <div>
        <h3>Per-seat probability</h3>
        <div id="bars"></div>
      </div>
    </div>
  </div>

  <div class="col">
    <div class="card">
      <h3>Your Hand</h3>
      <input type="text" id="yourHand" class="hand-input" placeholder="e.g. AKs, KK, or exact cards like AsKh" spellcheck="false">
      <div class="hand-display" id="yourHandDisplay" style="display:none"></div>
      <div class="eq">
        <div class="eq-head"><span>Equity vs range <small>(heads-up, all-in preflop)</small></span><b id="eqVal">—</b></div>
        <div class="pt"><div class="pf" id="eqBar" style="width:0"></div></div>
        <div class="eq-sub" id="eqSub">Enter your hand to see equity.</div>
      </div>
    </div>

    <div class="card ranges-card">
      <h3>Opponent ranges</h3>
      <div class="tabs">
        <button class="tab active" data-tab="manual">Manual Input</button>
        <button class="tab" data-tab="table">Hand Table</button>
      </div>
      
      <div class="tab-panel active" id="manual">
        <div id="ranges"></div>
        <div class="help-txt">
          <code>AJo+</code> <code>A9o+</code> <code>66+</code> <code>AJs+</code> <code>KTs+</code> <code>QQ+,AKs</code><br>
          Need suit: <code>o</code>=offsuit, <code>s</code>=suited. <code>+</code> extends upward.
        </div>
      </div>

      <div class="tab-panel" id="table">
        <div style="font-size:.7rem;color:#7a8aa0;margin-bottom:.6rem">Click or drag to select hands. Pairs on diagonal, suited above, offsuit below.</div>
        <div style="display:flex;gap:6px;margin-bottom:.6rem">
          <button class="clear-btn" onclick="clearHandSelection()" style="flex:1">Clear All</button>
          <button class="clear-btn" style="flex:1;border-color:#2563eb;color:#6a7a8a" onmouseover="this.style.borderColor='#2563eb';this.style.color='#6fb7ff'" onmouseout="this.style.borderColor='#3a4a5a';this.style.color='#6a7a8a'" onclick="selectAllHands()">Select All</button>
        </div>
        <div class="hand-grid" id="handGrid"></div>
      </div>
    </div>
  </div>
</div>

<script>
const RANKS = '2 3 4 5 6 7 8 9 T J Q K A'.split(' ');
const RV = Object.fromEntries(RANKS.map((r, i) => [r, i]));
const SUITS = ['s', 'h', 'd', 'c'];
const SUIT_SYM = { s: '♠', h: '♥', d: '♦', c: '♣' };
const TOTAL = 1326;

// Expand one token (e.g. "66+", "AJo+", "KQs") into hand classes like "AKo".
// Returns null for an invalid token.
function expandSingle(raw) {
  const s = raw.trim().toUpperCase();
  if (!s) return [];
  // Dash ranges: "99-66" or "K9s-K6s" (same top card, same suitedness)
  if (s.includes('-')) {
    const [x, y] = s.split('-').map(p => expandSingle(p));
    if (!x || !y || x.length !== 1 || y.length !== 1) return null;
    const a = x[0], b = y[0];
    if (a.length !== b.length || a[2] !== b[2] || (a.length === 3 && a[0] !== b[0])) return null;
    const pos = a.length === 2 ? 0 : 1;
    const hi = Math.max(RV[a[pos]], RV[b[pos]]), lo = Math.min(RV[a[pos]], RV[b[pos]]);
    const out = [];
    for (let k = lo; k <= hi; k++) out.push(a.length === 2 ? RANKS[k] + RANKS[k] : a[0] + RANKS[k] + a[2]);
    return out;
  }
  const plus = s.endsWith('+');
  const h = plus ? s.slice(0, -1) : s;
  if (h.length === 2 && h[0] === h[1]) {
    const i = RV[h[0]];
    if (i === undefined) return null;
    const out = [];
    for (let k = i; k <= (plus ? 12 : i); k++) out.push(RANKS[k] + RANKS[k]);
    return out;
  }
  if (h.length === 3) {
    const r1 = h[0], r2 = h[1], su = h[2].toLowerCase();
    if (RV[r1] === undefined || RV[r2] === undefined || r1 === r2) return null;
    if (su !== 'o' && su !== 's') return null;
    const hi = Math.max(RV[r1], RV[r2]);
    const lo = Math.min(RV[r1], RV[r2]);
    const out = [];
    for (let k = lo; k <= (plus ? hi - 1 : lo); k++) out.push(RANKS[hi] + RANKS[k] + su);
    return out;
  }
  return null;
}

// Set of hand classes covered by a comma-separated range string.
function parseRange(str) {
  const classes = new Set();
  str.split(',').forEach(p => (expandSingle(p) || []).forEach(c => classes.add(c)));
  return classes;
}

// Every specific two-card combo of a hand class, cards written like "As".
function classCombos(cls) {
  const r1 = cls[0], r2 = cls[1];
  const out = [];
  for (let i = 0; i < 4; i++) {
    for (let j = 0; j < 4; j++) {
      // Pairs: each suit pair once. Suited: same suit only. Offsuit: different suits only.
      if (r1 === r2 ? j <= i : (cls[2] === 's') !== (i === j)) continue;
      out.push([r1 + SUITS[i], r2 + SUITS[j]]);
    }
  }
  return out;
}

// Combos of the given classes that don't use any of the dead cards.
function liveCombos(classes, dead) {
  let n = 0;
  classes.forEach(cls => {
    classCombos(cls).forEach(([a, b]) => { if (!dead.has(a) && !dead.has(b)) n++; });
  });
  return n;
}

// Parse the hero's hand: specific cards ("AsKh") or a class ("AKo").
// A class uses a representative suit combo, which is exact because every
// combo of a class removes the same number of combos from suit-symmetric ranges.
function parseHeroHand(raw) {
  const s = raw.replace(/[ ,]/g, '');
  const m = s.match(/^([2-9TJQKA])([SHDC])([2-9TJQKA])([SHDC])$/i);
  if (m) {
    const c1 = m[1].toUpperCase() + m[2].toLowerCase();
    const c2 = m[3].toUpperCase() + m[4].toLowerCase();
    if (c1 === c2) return null;
    const pretty = c => c[0] + SUIT_SYM[c[1]];
    return { label: pretty(c1) + ' ' + pretty(c2), cards: [c1, c2] };
  }
  if (s.includes('+')) return null;
  const cls = expandSingle(s);
  if (!cls || cls.length !== 1) return null;
  return { label: cls[0], cards: classCombos(cls[0])[0], combos: classCombos(cls[0]).length };
}

// ---- Equity: Monte Carlo over random opponent hands and boards ----

// Cards as ints 0-51: rank * 4 + suit
const cardInt = c => RV[c[0]] * 4 + SUITS.indexOf(c[1]);

// Highest card of a straight in a rank bitmask, or -1 (the wheel A-5 is 5-high)
function straightTop(mask) {
  for (let hi = 12; hi >= 4; hi--) if (((mask >> (hi - 4)) & 31) === 31) return hi;
  return (mask & 0x100F) === 0x100F ? 3 : -1;
}

// The n highest ranks in a bitmask, packed 4 bits each, highest first
function topRanks(mask, n) {
  let v = 0;
  for (let r = 12; r >= 0 && n > 0; r--) if (mask & (1 << r)) { v = (v << 4) | r; n--; }
  return v;
}

const rc = new Int8Array(13), sc = new Int8Array(4), sm = new Int32Array(4);

// Score the best 5-card hand out of 7 cards; higher is better.
// Category (0 = high card ... 8 = straight flush) sits above the 20 tiebreaker bits.
function evalHand(cards) {
  rc.fill(0); sc.fill(0); sm.fill(0);
  let all = 0;
  for (let i = 0; i < cards.length; i++) {
    const r = cards[i] >> 2, s = cards[i] & 3;
    rc[r]++; sc[s]++; sm[s] |= 1 << r; all |= 1 << r;
  }
  // With 7 cards a flush can't coexist with quads or a full house, so check it first
  for (let s = 0; s < 4; s++) {
    if (sc[s] < 5) continue;
    const sf = straightTop(sm[s]);
    return sf >= 0 ? (8 << 20) | sf : (5 << 20) | topRanks(sm[s], 5);
  }
  const quads = [], trips = [], pairs = [];
  for (let r = 12; r >= 0; r--) {
    if (rc[r] === 4) quads.push(r);
    else if (rc[r] === 3) trips.push(r);
    else if (rc[r] === 2) pairs.push(r);
  }
  if (quads.length) return (7 << 20) | (quads[0] << 4) | topRanks(all & ~(1 << quads[0]), 1);
  if (trips.length && (trips.length > 1 || pairs.length)) {
    return (6 << 20) | (trips[0] << 4) | Math.max(trips.length > 1 ? trips[1] : -1, pairs.length ? pairs[0] : -1);
  }
  const st = straightTop(all);
  if (st >= 0) return (4 << 20) | st;
  if (trips.length) return (3 << 20) | (trips[0] << 8) | topRanks(all & ~(1 << trips[0]), 2);
  if (pairs.length > 1) {
    return (2 << 20) | (pairs[0] << 8) | (pairs[1] << 4) | topRanks(all & ~(1 << pairs[0]) & ~(1 << pairs[1]), 1);
  }
  if (pairs.length) return (1 << 20) | (pairs[0] << 12) | topRanks(all & ~(1 << pairs[0]), 3);
  return topRanks(all, 5);
}

// Run a batch of trials: deal each opponent a combo from the range, deal a board,
// and score the showdown (ties split). Returns [equity won, trials completed].
function simTrials(hero, combos, nOpp, trials, used) {
  let eq = 0, done = 0;
  const opp = new Array(nOpp), board = [];
  for (let t = 0; t < trials; t++) {
    // Redeal the whole table on a card clash so multiway deals stay unbiased
    let ok = false;
    for (let attempt = 0; attempt < 100 && !ok; attempt++) {
      used.fill(0); used[hero[0]] = used[hero[1]] = 1;
      ok = true;
      for (let k = 0; k < nOpp && ok; k++) {
        const c = combos[Math.random() * combos.length | 0];
        if (used[c[0]] || used[c[1]]) ok = false;
        else { used[c[0]] = used[c[1]] = 1; opp[k] = c; }
      }
    }
    if (!ok) continue;
    board.length = 0;
    while (board.length < 5) {
      const c = Math.random() * 52 | 0;
      if (!used[c]) { used[c] = 1; board.push(c); }
    }
    const mine = evalHand([hero[0], hero[1], ...board]);
    let best = -1, nBest = 0;
    for (let k = 0; k < nOpp; k++) {
      const s = evalHand([opp[k][0], opp[k][1], ...board]);
      if (s > best) { best = s; nBest = 1; } else if (s === best) nBest++;
    }
    eq += mine > best ? 1 : mine === best ? 1 / (nBest + 1) : 0;
    done++;
  }
  return [eq, done];
}

// Convert a set of hand classes to compact range notation the parser reads back:
// "44+", "99-66", "AJs+", "K9s-K6s", or single hands
function handsToRangeString(hands) {
  const out = [];
  // Joins consecutive ranks (ascending) into runs; top is the highest rank a "+" can reach
  const runs = (ranks, top, fmt, fmtRange) => {
    ranks.sort((a, b) => a - b);
    for (let i = 0; i < ranks.length; ) {
      let j = i;
      while (j + 1 < ranks.length && ranks[j + 1] === ranks[j] + 1) j++;
      if (i === j) out.push(fmt(ranks[i]));
      else if (ranks[j] === top) out.push(fmt(ranks[i]) + '+');
      else out.push(fmtRange(ranks[j], ranks[i]));
      i = j + 1;
    }
  };
  const pairs = [...hands].filter(h => h.length === 2).map(h => RV[h[0]]).reverse();
  runs(pairs, 12, r => RANKS[r] + RANKS[r], (hi, lo) => RANKS[hi] + RANKS[hi] + '-' + RANKS[lo] + RANKS[lo]);
  ['s', 'o'].forEach(su => {
    for (let hi = 12; hi > 0; hi--) {
      const lows = [...hands].filter(h => h.length === 3 && h[2] === su && RV[h[0]] === hi).map(h => RV[h[1]]);
      const f = lo => RANKS[hi] + RANKS[lo] + su;
      runs(lows, hi - 1, f, (a, b) => f(a) + '-' + f(b));
    }
  });
  return out.join(', ');
}

const POS = [
  { id: 'utg',   lbl: 'UTG',   name: 'Under the Gun', angle: 135 },
  { id: 'utg1',  lbl: 'UTG+1', name: 'UTG+1',         angle: 180 },
  { id: 'lj',    lbl: 'LJ',    name: 'Late Jump',     angle: 225 },
  { id: 'hj',    lbl: 'HJ',    name: 'Hijack',        angle: 270 },
  { id: 'co',    lbl: 'CO',    name: 'Cutoff',        angle: 315 },
  { id: 'btn',   lbl: 'BTN',   name: 'Button',        angle: 0   },
  { id: 'sb',    lbl: 'SB',    name: 'Small Blind',   angle: 45  },
  { id: 'bb',    lbl: 'BB',    name: 'Big Blind',     angle: 90  },
];

// Preflop acting order: everyone before your seat is assumed to have folded
const ACTION_ORDER = ['utg', 'utg1', 'lj', 'hj', 'co', 'btn', 'sb', 'bb'];

let yourPosition = 'btn';
let yourHand = '';
let selectedHandsInTable = new Set();
const active = Object.fromEntries(POS.map(p => [p.id, true]));

function setYourPosition(posId) {
  yourPosition = posId;
  const yourIdx = ACTION_ORDER.indexOf(posId);
  ACTION_ORDER.forEach((id, idx) => {
    if (idx < yourIdx) active[id] = false;
    else if (idx > yourIdx) active[id] = true;
  });
  updatePositionUI();
  renderTable();
  updateAll();
}

function updatePositionUI() {
  document.querySelectorAll('.pos-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.pos === yourPosition);
  });
}

const SEAT_STYLE = {
  you:  { fill: '#ffd700', stroke: '#a57900', txt: '#5a3e00' },
  sb:   { fill: '#2563eb', stroke: '#1d4ed8', txt: '#ffffff' },
  bb:   { fill: '#e55a0d', stroke: '#b84509', txt: '#ffffff' },
  def:  { fill: '#e2e8f0', stroke: '#94a3b8', txt: '#374151' },
  off:  { fill: '#3a4a5a', stroke: '#2a3a4a', txt: '#5a6a7a' },
};

function sStyle(pos) {
  if (pos.id === yourPosition) return SEAT_STYLE.you;
  if (!active[pos.id])         return SEAT_STYLE.off;
  return SEAT_STYLE.def;
}

const CX = 360, CY = 215, SRX = 308, SRY = 178, R = 32;

function seatXY(angle) {
  const rad = angle * Math.PI / 180;
  return [CX + SRX * Math.cos(rad), CY + SRY * Math.sin(rad)];
}

function svgEl(tag, attrs = {}) {
  const el = document.createElementNS('http://www.w3.org/2000/svg', tag);
  for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v);
  return el;
}

function renderTable() {
  const g = document.getElementById('seats');
  g.innerHTML = '';
  POS.forEach(pos => {
    const [x, y] = seatXY(pos.angle);
    const { fill, stroke, txt } = sStyle(pos);
    const grp = svgEl('g');
    if (pos.id !== yourPosition) {
      grp.style.cursor = 'pointer';
      grp.onclick = () => { active[pos.id] = !active[pos.id]; renderTable(); updateAll(); };
      grp.appendChild(svgEl('title')).textContent = pos.name + ' (click to fold / unfold)';
    }

    grp.appendChild(svgEl('circle', { cx: x+1, cy: y+2, r: R, fill: 'rgba(0,0,0,.2)' }));
    grp.appendChild(svgEl('circle', {
      cx: x, cy: y, r: R, fill, stroke,
      'stroke-width': pos.id === yourPosition ? 2.5 : 1.5
    }));

    if (pos.id === 'btn') {
      grp.appendChild(svgEl('circle', {
        cx: x + R * .72, cy: y - R * .72, r: 10,
        fill: '#fff', stroke: '#a57900', 'stroke-width': '1.5'
      }));
      const dt = svgEl('text', {
        x: x + R * .72, y: y - R * .72 + 3.5,
        'text-anchor': 'middle', fill: '#a57900',
        'font-size': '8', 'font-weight': 'bold'
      });
      dt.textContent = 'D';
      grp.appendChild(dt);
    }

    const lbl = svgEl('text', {
      x, y: y - 2,
      'text-anchor': 'middle', fill: txt,
      'font-size': '13', 'font-weight': '700',
      'font-family': 'system-ui,sans-serif'
    });
    lbl.textContent = pos.lbl;
    grp.appendChild(lbl);

    const sub = svgEl('text', {
      x, y: y + 13,
      'text-anchor': 'middle', fill: txt,
      'font-size': '10.5', 'font-family': 'system-ui,sans-serif',
      opacity: '.88', id: 'sp_' + pos.id
    });
    if (pos.id === yourPosition) sub.textContent = 'YOU';
    else if (!active[pos.id])   sub.textContent = 'folded';
    grp.appendChild(sub);

    g.appendChild(grp);
  });
}

function setYourHand(hand) {
  yourHand = hand.trim();
  const display = document.getElementById('yourHandDisplay');
  display.style.background = '';
  display.style.borderLeftColor = '';
  if (yourHand) {
    const hero = parseHeroHand(yourHand);
    if (hero) {
      display.textContent = hero.combos
        ? `Your hand: ${hero.label} (${hero.combos} combos in deck)`
        : `Your hand: ${hero.label}`;
      display.style.display = 'block';
    } else {
      display.textContent = 'Invalid hand format';
      display.style.background = 'rgba(220,38,38,.15)';
      display.style.borderLeftColor = '#dc2626';
      display.style.display = 'block';
    }
  } else {
    display.style.display = 'none';
  }
  updateAll();
}

function clearHandSelection() {
  selectedHandsInTable.clear();
  buildHandGrid();
  updateHandsFromTable();
}

function selectAllHands() {
  selectedHandsInTable.clear();
  for (let i = 0; i < 13; i++) {
    for (let j = 0; j < 13; j++) {
      const r1 = RANKS[12 - i];
      const r2 = RANKS[12 - j];
      const hi = RV[r1] > RV[r2] ? r1 : r2;
      const lo = RV[r1] > RV[r2] ? r2 : r1;
      let hand = '';
      if (i === j) {
        hand = r1 + r1;
      } else if (i < j) {
        hand = hi + lo + 's';
      } else {
        hand = hi + lo + 'o';
      }
      selectedHandsInTable.add(hand);
    }
  }
  buildHandGrid();
  updateHandsFromTable();
}

let gridDragState = { isDragging: false, dragMode: null };

// 13x13 grid: pairs on the diagonal, suited above it, offsuit below
function buildHandGrid() {
  const grid = document.getElementById('handGrid');
  grid.innerHTML = '';
  
  for (let i = 0; i < 13; i++) {
    for (let j = 0; j < 13; j++) {
      const r1 = RANKS[12 - i];
      const r2 = RANKS[12 - j];
      const hi = RV[r1] > RV[r2] ? r1 : r2;
      const lo = RV[r1] > RV[r2] ? r2 : r1;
      
      let hand = '';
      if (i === j) {
        hand = r1 + r1;
      } else if (i < j) {
        hand = hi + lo + 's';
      } else {
        hand = hi + lo + 'o';
      }
      
      const cell = document.createElement('div');
      cell.className = 'hand-cell';
      if (selectedHandsInTable.has(hand)) cell.classList.add('selected');
      cell.textContent = hand;
      cell.dataset.hand = hand;
      
      cell.onmousedown = (e) => {
        e.preventDefault();
        gridDragState.isDragging = true;
        gridDragState.dragMode = selectedHandsInTable.has(hand) ? 'remove' : 'add';
        toggleHandInTable(hand, cell);
      };
      
      cell.onmouseenter = (e) => {
        if (gridDragState.isDragging && gridDragState.dragMode && e.buttons === 1) {
          const isSelected = cell.classList.contains('selected');
          if (gridDragState.dragMode === 'add' && !isSelected) {
            selectedHandsInTable.add(hand);
            cell.classList.add('selected');
          } else if (gridDragState.dragMode === 'remove' && isSelected) {
            selectedHandsInTable.delete(hand);
            cell.classList.remove('selected');
          }
        }
      };
      
      grid.appendChild(cell);
    }
  }
}

document.addEventListener('mouseup', () => {
  if (gridDragState.isDragging) {
    gridDragState.isDragging = false;
    gridDragState.dragMode = null;
    updateHandsFromTable();
  }
}, true);

function toggleHandInTable(hand, cell) {
  if (selectedHandsInTable.has(hand)) {
    selectedHandsInTable.delete(hand);
    cell.classList.remove('selected');
  } else {
    selectedHandsInTable.add(hand);
    cell.classList.add('selected');
  }
}

// The grid edits the whole range, so it collapses every group into the first one
function updateHandsFromTable() {
  rows.slice(1).forEach(r => r.div.remove());
  rows = rows.slice(0, 1);
  if (rows.length === 0) addRow('');
  rows[0].inp.value = handsToRangeString(selectedHandsInTable);
  updateAll();
}

const RCOLS = ['#2563eb', '#e55a0d', '#16a34a', '#7c3aed', '#dc2626', '#0891b2', '#db2777'];
let rows = [];

function buildRanges() {
  const el = document.getElementById('ranges');
  el.innerHTML = '';
  rows = [];
  // Button goes in first: addRow inserts each row just above it
  const btn = document.createElement('button');
  btn.className = 'add-btn';
  btn.textContent = '+ Add range group';
  btn.onclick = () => { addRow(''); updateAll(); };
  el.appendChild(btn);
  ['AJo+', '66+', 'AJs+'].forEach(v => addRow(v));
}

function addRow(val) {
  const el = document.getElementById('ranges');
  const ci = rows.length;
  const col = RCOLS[ci % RCOLS.length];
  const div = document.createElement('div');
  div.className = 'rr';

  const dot = document.createElement('span');
  dot.style.cssText = `width:9px;height:9px;border-radius:50%;background:${col};flex-shrink:0`;
  div.appendChild(dot);

  const inp = document.createElement('input');
  inp.type = 'text';
  inp.value = val;
  inp.placeholder = 'e.g. AJo+, 66+, KQs';
  inp.spellcheck = false;
  inp.oninput = updateAll;
  div.appendChild(inp);

  const badge = document.createElement('span');
  badge.className = 'badge';
  badge.style.background = col + '22';
  badge.style.color = col;
  div.appendChild(badge);

  const del = document.createElement('button');
  del.className = 'del';
  del.textContent = '×';
  del.onclick = () => {
    div.remove();
    rows = rows.filter(r => r.inp !== inp);
    updateAll();
  };
  div.appendChild(del);

  el.insertBefore(div, el.lastChild);
  rows.push({ inp, badge, col, div });
}

const BAR_COLS = ['#2563eb', '#e55a0d', '#7c3aed', '#16a34a', '#dc2626', '#0891b2', '#db2777'];

const EQ_TRIALS = 40000;
let eqRun = 0;

// Simulate in small batches so the page stays responsive; any newer call cancels this one
function runEquity(hero, classes, nOpp) {
  const run = ++eqRun;
  const val = document.getElementById('eqVal');
  const bar = document.getElementById('eqBar');
  const sub = document.getElementById('eqSub');
  const reset = msg => { val.textContent = '—'; bar.style.width = '0'; sub.textContent = msg; };

  if (!hero) return reset('Enter your hand to see equity.');
  const dead = new Set(hero.cards);
  const combos = [];
  classes.forEach(cls => classCombos(cls).forEach(([a, b]) => {
    if (!dead.has(a) && !dead.has(b)) combos.push([cardInt(a), cardInt(b)]);
  }));
  if (!combos.length) return reset('Select an opponent range to see equity.');

  const h = hero.cards.map(cardInt);
  const used = new Uint8Array(52);
  const hu = [0, 0], multi = [0, 0];
  const step = () => {
    if (run !== eqRun) return;
    const [w, d] = simTrials(h, combos, 1, 2000, used);
    hu[0] += w; hu[1] += d;
    if (nOpp > 1) {
      const [w2, d2] = simTrials(h, combos, nOpp, 2000, used);
      multi[0] += w2; multi[1] += d2;
    }
    const pct = 100 * hu[0] / hu[1];
    val.textContent = pct.toFixed(1) + '%';
    bar.style.width = pct.toFixed(1) + '%';
    bar.style.background = pct >= 50 ? '#16a34a' : '#e55a0d';
    let txt = (hu[1] / 1000).toFixed(0) + 'k simulated boards';
    if (nOpp > 1) {
      txt = multi[1]
        ? `vs all ${nOpp} active opponents: ${(100 * multi[0] / multi[1]).toFixed(1)}% · ` + txt
        : `Range too narrow to deal all ${nOpp} opponents · ` + txt;
    }
    sub.textContent = txt;
    if (hu[1] < EQ_TRIALS) setTimeout(step, 0);
  };
  // Short delay so fast typing or dragging doesn't start runs that get thrown away
  setTimeout(step, 40);
}

function updateAll() {
  // Your hole cards are dead: opponents can't hold combos that use them,
  // and their two cards come from the 50 left in the deck.
  const hero = yourHand ? parseHeroHand(yourHand) : null;
  const dead = new Set(hero ? hero.cards : []);
  const deckCombos = hero ? 1225 : TOTAL;

  // Union across rows so overlapping groups (e.g. AJo+ and AQo) aren't counted twice
  const allClasses = new Set();
  rows.forEach(({ inp, badge, col }) => {
    const v = inp.value.trim();
    const classes = parseRange(v);
    const hasContent = v && v.split(',').some(p => p.trim().length > 0);
    const invalid = hasContent && classes.size === 0;
    badge.textContent = invalid ? 'invalid' : liveCombos(classes, dead) + ' combos';
    badge.style.background = invalid ? 'rgba(220,38,38,.15)' : col + '22';
    badge.style.color = invalid ? '#dc2626' : col;
    classes.forEach(c => allClasses.add(c));
  });
  const adjustedTotal = liveCombos(allClasses, dead);
  const blocked = liveCombos(allClasses, new Set()) - adjustedTotal;

  // The grid always shows the combined range of every group
  if (!gridDragState.isDragging) {
    selectedHandsInTable = new Set(allClasses);
    document.querySelectorAll('.hand-cell').forEach(c => c.classList.toggle('selected', allClasses.has(c.dataset.hand)));
  }

  const pS = adjustedTotal / deckCombos;
  const opp = POS.filter(p => p.id !== yourPosition && active[p.id]);
  const n = opp.length;
  // Chance at least one opponent has it (treats opponents as independent, a close approximation)
  const pAny = n > 0 ? 1 - Math.pow(1 - pS, n) : 0;

  runEquity(hero, allClasses, n);

  document.getElementById('sCombos').innerHTML = adjustedTotal + ' <small>/ ' + deckCombos + '</small>';
  document.getElementById('sBlocked').textContent = hero ? blocked : '—';
  document.getElementById('sPer').textContent = (pS * 100).toFixed(1) + '%';
  document.getElementById('sAny').textContent = (pAny * 100).toFixed(1) + '%';
  document.getElementById('sLbl').textContent = 'Any of ' + n + ' opp.';

  POS.forEach(pos => {
    const el = document.getElementById('sp_' + pos.id);
    if (!el) return;
    if (pos.id === yourPosition) el.textContent = 'YOU';
    else if (!active[pos.id])    el.textContent = 'folded';
    else                         el.textContent = (pS * 100).toFixed(1) + '%';
  });

  const bars = document.getElementById('bars');
  bars.innerHTML = '';
  const perMax = Math.max(25, pS * 100 * 1.6);

  if (n === 0) {
    bars.innerHTML = '<div class="empty">No opponents left in the hand. Click a seat to unfold it.</div>';
    return;
  }

  // Folded seats are left out so the list stays short
  opp.forEach((pos, i) => {
    const pct = pS * 100;
    const col = BAR_COLS[i % BAR_COLS.length];
    const barW = Math.min(pct / perMax * 100, 100);
    const row = document.createElement('div');
    row.className = 'pr';
    row.innerHTML =
      '<span class="pl">' + pos.lbl + '</span>' +
      '<div class="pt"><div class="pf" style="width:' + barW.toFixed(1) + '%;background:' + col + '"></div></div>' +
      '<span class="pp">' + pct.toFixed(1) + '%</span>';
    bars.appendChild(row);
  });

  bars.appendChild(Object.assign(document.createElement('div'), { className: 'sep-line' }));
  const anyPct = pAny * 100;
  const anyW = Math.min(anyPct / 80 * 100, 100);
  const anyRow = document.createElement('div');
  anyRow.className = 'pr';
  anyRow.innerHTML =
    '<span class="pl">Any</span>' +
    '<div class="pt"><div class="pf" style="width:' + anyW.toFixed(1) + '%;background:#ffc700"></div></div>' +
    '<span class="pp">' + anyPct.toFixed(1) + '%</span>';
  bars.appendChild(anyRow);
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
      const tabName = tab.dataset.tab;
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
      tab.classList.add('active');
      document.getElementById(tabName).classList.add('active');
    });
  });

  document.getElementById('yourHand').addEventListener('input', (e) => {
    setYourHand(e.target.value);
  });

  POS.forEach(pos => {
    const btn = document.createElement('button');
    btn.className = 'pos-btn' + (pos.id === 'btn' ? ' active' : '');
    btn.textContent = pos.lbl;
    btn.dataset.pos = pos.id;
    btn.onclick = () => setYourPosition(pos.id);
    document.getElementById('posGrid').appendChild(btn);
  });
});

setYourPosition(yourPosition);
buildRanges();
buildHandGrid();
updateAll();
</script>
</body>
</html>"""


def main():
    # All the logic lives in the page's JavaScript; Python just writes it to a
    # temp file and opens it in the browser
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.html', delete=False, encoding='utf-8'
    ) as f:
        f.write(PAGE)
        path = f.name

    url = Path(path).as_uri()
    webbrowser.open(url)

    print()
    print("  ╔════════════════════════════════════════════════════════╗")
    print("  ║       Hand Odds Calculator (FIXED)                     ║")
    print("  ╚════════════════════════════════════════════════════════╝")
    print()
    print("  ✓ FIXES APPLIED:")
    print("    • Smart range notation: AJ+, KTs+ instead of listing")
    print("    • Hand order fixed: K2o not 2Ko, A5o not 5Ao")
    print("    • Pairs now update in manual input")
    print("    • Opponent combos reduced when you select a hand")
    print("    • Drag selection working correctly")
    print()
    print("  Close this terminal anytime.")
    print()


if __name__ == '__main__':
    main()
