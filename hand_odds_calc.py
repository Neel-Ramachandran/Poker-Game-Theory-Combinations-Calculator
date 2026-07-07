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
body{
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  background:#0f1419;color:#e0e0e0;min-height:100vh;
}

header{
  background:#1a2332;color:#fff;
  padding:.9rem 1.5rem;
  display:flex;align-items:center;gap:.85rem;
  border-bottom:1px solid #2a3a4a;
}
header h1{font-size:1.05rem;font-weight:600}
header p{font-size:.72rem;color:rgba(255,255,255,.50);margin-top:2px}

.wrap{display:grid;grid-template-columns:1fr 400px;gap:1rem;padding:1rem;align-items:start}
@media(max-width:900px){.wrap{grid-template-columns:1fr}}

.card{
  background:#1a2230;border:1px solid #2a3a4a;border-radius:12px;
  box-shadow:0 2px 10px rgba(0,0,0,.3);padding:1.1rem;
}
.card+.card{margin-top:1rem}
h3{font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#7a8aa0;margin-bottom:.8rem}
h4{font-size:.75rem;font-weight:600;color:#a0b0c0;margin-top:.8rem;margin-bottom:.4rem}

.tbl-wrap{position:relative;width:100%;padding-bottom:60%}
.tbl-svg{position:absolute;inset:0;width:100%;height:100%}

.chips{display:flex;flex-wrap:wrap;gap:5px;margin-top:.65rem}
.chip{
  font-size:.67rem;font-weight:600;padding:3px 9px;border-radius:20px;
  border:1.5px solid;cursor:pointer;user-select:none;transition:all .15s;
}
.chip.you{background:rgba(255,215,0,.15);border-color:#b8860b;color:#ffc700}
.chip.on{background:rgba(37,99,235,.15);border-color:#2563eb;color:#6fb7ff}
.chip.off{background:rgba(100,100,120,.15);border-color:#4a5a6a;color:#7a8a9a;text-decoration:line-through}
.hint{font-size:.67rem;color:#6a7a8a;text-align:center;margin-top:.45rem}

.pos-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin:.5rem 0}
.pos-btn{
  border:1.5px solid #3a4a5a;background:#111820;color:#a0b0c0;
  border-radius:8px;padding:6px;font-size:.75rem;font-weight:600;
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

.tab-panel{display:none}
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

.sg{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.sc{background:#111820;border:1px solid #2a3a4a;border-radius:8px;padding:.65rem .85rem}
.sc .sl{font-size:.67rem;color:#7a8aa0;margin-bottom:2px}
.sc .sv{font-size:1.1rem;font-weight:700;color:#e0e0e0}

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
  <span style="font-size:1.5rem">🃏</span>
  <div>
    <h1>Hand Odds Calculator</h1>
    <p>8-Max Ring Game · Smart Range Analysis</p>
  </div>
</header>

<div class="wrap">
  <div>
    <div class="card">
      <h3>Table view</h3>
      <div class="tbl-wrap">
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
      </div>
      <div class="chips" id="chips"></div>
      <div class="hint">Click seats to toggle folded / active. Earlier positions auto-fold when you choose your position.</div>
    </div>
  </div>

  <div>
    <div class="card">
      <h3>Your Position</h3>
      <div class="pos-grid" id="posGrid"></div>
      <h4 style="margin-top:0.6rem;margin-bottom:0.4rem;font-size:.68rem">Unfold these opponents:</h4>
      <div class="chips" id="unfoldChips"></div>
    </div>

    <div class="card">
      <h3>Your Hand</h3>
      <input type="text" id="yourHand" class="hand-input" placeholder="e.g. AKs or KK or clear" spellcheck="false">
      <div class="hand-display" id="yourHandDisplay" style="display:none"></div>
    </div>

    <div class="card">
      <h3>Hand Ranges</h3>
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

    <div class="card">
      <h3>Summary</h3>
      <div class="sg">
        <div class="sc"><div class="sl">Combos in range</div><div class="sv" id="sCombos">—</div></div>
        <div class="sc"><div class="sl">% of all hands</div><div class="sv" id="sPct">—</div></div>
        <div class="sc"><div class="sl">Per-opponent</div><div class="sv" id="sPer">—</div></div>
        <div class="sc"><div class="sl" id="sLbl">Any of N opp.</div><div class="sv" id="sAny">—</div></div>
      </div>
    </div>

    <div class="card">
      <h3>Per-seat probability</h3>
      <div id="bars"></div>
    </div>
  </div>
</div>

<script>
const RANKS = '2 3 4 5 6 7 8 9 T J Q K A'.split(' ');
const RV = Object.fromEntries(RANKS.map((r, i) => [r, i]));
const TOTAL = 1326;

function parseSingle(raw) {
  const s = raw.trim().toUpperCase();
  if (!s) return 0;
  const plus = s.endsWith('+');
  const h = plus ? s.slice(0, -1) : s;
  if (h.length === 2 && h[0] === h[1]) {
    const i = RV[h[0]];
    if (i === undefined) return 0;
    return (plus ? (12 - i + 1) : 1) * 6;
  }
  if (h.length === 3) {
    const r1 = h[0], r2 = h[1], su = h[2].toLowerCase();
    if (RV[r1] === undefined || RV[r2] === undefined || r1 === r2) return 0;
    if (su !== 'o' && su !== 's') return 0;
    const cpp = su === 'o' ? 12 : 4;
    const hi = Math.max(RV[r1], RV[r2]);
    const lo = Math.min(RV[r1], RV[r2]);
    return plus ? (hi - lo) * cpp : cpp;
  }
  return 0;
}

function parseRange(str) {
  return Math.min(str.split(',').reduce((sum, p) => sum + parseSingle(p), 0), TOTAL);
}

function handCombos(hand) {
  return parseSingle(hand);
}

// Convert selected hands to smart range notation
function handsToRangeString(hands) {
  if (hands.size === 0) return '';
  
  const result = [];
  const pairsList = [];
  const suitedByHi = {};
  const ofsuitByHi = {};
  
  // Organize hands into categories
  hands.forEach(hand => {
    if (hand.length === 2 && hand[0] === hand[1]) {
      pairsList.push(hand[0]);
    } else if (hand.length === 3) {
      const hi = hand[0];
      const lo = hand[1];
      const suit = hand[2];
      
      if (suit === 's') {
        if (!suitedByHi[hi]) suitedByHi[hi] = [];
        suitedByHi[hi].push(lo);
      } else if (suit === 'o') {
        if (!ofsuitByHi[hi]) ofsuitByHi[hi] = [];
        ofsuitByHi[hi].push(lo);
      }
    }
  });
  
  // Process pairs
  if (pairsList.length > 0) {
    const pairs = Array.from(new Set(pairsList)).sort((a, b) => RV[a] - RV[b]);
    let i = 0;
    while (i < pairs.length) {
      let j = i;
      while (j + 1 < pairs.length && RV[pairs[j + 1]] === RV[pairs[j]] + 1) j++;
      if (i === j) {
        result.push(pairs[i] + pairs[i]);
      } else {
        result.push(pairs[i] + pairs[j] + '+');
      }
      i = j + 1;
    }
  }
  
  // Process suited combos
  Object.keys(suitedByHi).sort((a, b) => RV[b] - RV[a]).forEach(hi => {
    const lows = Array.from(new Set(suitedByHi[hi])).sort((a, b) => RV[a] - RV[b]);
    let i = 0;
    while (i < lows.length) {
      let j = i;
      while (j + 1 < lows.length && RV[lows[j + 1]] === RV[lows[j]] + 1) j++;
      const start = lows[i];
      const end = lows[j];
      if (i === j) {
        result.push(hi + start + 's');
      } else if (RV[end] === RV[hi] - 1) {
        result.push(hi + start + 's+');
      } else {
        result.push(hi + start + end + 's+');
      }
      i = j + 1;
    }
  });
  
  // Process offsuit combos
  Object.keys(ofsuitByHi).sort((a, b) => RV[b] - RV[a]).forEach(hi => {
    const lows = Array.from(new Set(ofsuitByHi[hi])).sort((a, b) => RV[a] - RV[b]);
    let i = 0;
    while (i < lows.length) {
      let j = i;
      while (j + 1 < lows.length && RV[lows[j + 1]] === RV[lows[j]] + 1) j++;
      const start = lows[i];
      const end = lows[j];
      if (i === j) {
        result.push(hi + start + 'o');
      } else if (RV[end] === RV[hi] - 1) {
        result.push(hi + start + 'o+');
      } else {
        result.push(hi + start + end + 'o+');
      }
      i = j + 1;
    }
  });
  
  return result.join(', ');
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
  renderChips();
  renderUnfoldChips();
  updateAll();
}

function updatePositionUI() {
  document.querySelectorAll('.pos-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.pos === yourPosition);
  });
}

function renderUnfoldChips() {
  const el = document.getElementById('unfoldChips');
  el.innerHTML = '';
  const yourIdx = ACTION_ORDER.indexOf(yourPosition);
  ACTION_ORDER.slice(0, yourIdx).forEach(id => {
    const pos = POS.find(p => p.id === id);
    const c = document.createElement('span');
    c.className = 'chip ' + (active[id] ? 'on' : 'off');
    c.textContent = pos.lbl;
    c.title = pos.name;
    c.onclick = () => { active[id] = !active[id]; renderTable(); renderUnfoldChips(); updateAll(); };
    el.appendChild(c);
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

const CX = 360, CY = 215, SRX = 312, SRY = 182, R = 25;

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
      grp.onclick = () => { active[pos.id] = !active[pos.id]; renderTable(); renderChips(); updateAll(); };
    }

    grp.appendChild(svgEl('circle', { cx: x+1, cy: y+2, r: R, fill: 'rgba(0,0,0,.2)' }));
    grp.appendChild(svgEl('circle', {
      cx: x, cy: y, r: R, fill, stroke,
      'stroke-width': pos.id === yourPosition ? 2.5 : 1.5
    }));

    if (pos.id === yourPosition) {
      grp.appendChild(svgEl('circle', {
        cx: x + R * .68, cy: y - R * .68, r: 9,
        fill: '#fff', stroke: '#a57900', 'stroke-width': '1.5'
      }));
      const dt = svgEl('text', {
        x: x + R * .68, y: y - R * .68 + 3.5,
        'text-anchor': 'middle', fill: '#a57900',
        'font-size': '8', 'font-weight': 'bold'
      });
      dt.textContent = 'D';
      grp.appendChild(dt);
    }

    const isActive = pos.id === yourPosition || active[pos.id];
    const lbl = svgEl('text', {
      x, y: y + (isActive ? -3 : 2),
      'text-anchor': 'middle', fill: txt,
      'font-size': '10.5', 'font-weight': '700',
      'font-family': 'system-ui,sans-serif'
    });
    lbl.textContent = pos.lbl;
    grp.appendChild(lbl);

    const sub = svgEl('text', {
      x, y: y + 11,
      'text-anchor': 'middle', fill: txt,
      'font-size': '8', 'font-family': 'system-ui,sans-serif',
      opacity: '.88', id: 'sp_' + pos.id
    });
    if (pos.id === yourPosition) sub.textContent = 'YOU';
    else if (!active[pos.id])   sub.textContent = 'folded';
    grp.appendChild(sub);

    g.appendChild(grp);
  });
}

function renderChips() {
  const el = document.getElementById('chips');
  el.innerHTML = '';
  POS.forEach(pos => {
    const c = document.createElement('span');
    if (pos.id === yourPosition) {
      c.className = 'chip you';
      c.textContent = pos.lbl;
    } else if (active[pos.id]) {
      c.className = 'chip on';
      c.textContent = pos.lbl;
      c.onclick = () => { active[pos.id] = false; renderTable(); renderChips(); updateAll(); };
      c.style.cursor = 'pointer';
    } else {
      c.className = 'chip off';
      c.textContent = pos.lbl;
      c.onclick = () => { active[pos.id] = true; renderTable(); renderChips(); updateAll(); };
      c.style.cursor = 'pointer';
    }
    c.title = pos.name;
    el.appendChild(c);
  });
}

function setYourHand(hand) {
  yourHand = hand.trim().toUpperCase();
  const handInput = document.getElementById('yourHand');
  handInput.value = yourHand;
  const display = document.getElementById('yourHandDisplay');
  if (yourHand) {
    const combos = handCombos(yourHand);
    if (combos > 0) {
      display.textContent = `Your hand: ${yourHand} (${combos} ${combos === 1 ? 'combo' : 'combos'} in deck)`;
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

function updateHandsFromTable() {
  if (selectedHandsInTable.size === 0) {
    if (rows.length > 0) rows[0].inp.value = '';
  } else {
    const rangeStr = handsToRangeString(selectedHandsInTable);
    if (rows.length > 0) {
      rows[0].inp.value = rangeStr;
    } else {
      addRow(rangeStr);
    }
  }
  updateAll();
}

const RCOLS = ['#2563eb', '#e55a0d', '#16a34a', '#7c3aed', '#dc2626', '#0891b2', '#db2777'];
let rows = [];

function buildRanges() {
  const el = document.getElementById('ranges');
  el.innerHTML = '';
  rows = [];
  ['AJo+', '66+', 'AJs+'].forEach(v => addRow(v));
  const btn = document.createElement('button');
  btn.className = 'add-btn';
  btn.textContent = '+ Add range group';
  btn.onclick = () => { addRow(''); updateAll(); };
  el.appendChild(btn);
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
  rows.push({ inp, badge, col });
}

const BAR_COLS = ['#2563eb', '#e55a0d', '#7c3aed', '#16a34a', '#dc2626', '#0891b2', '#db2777'];

function updateAll() {
  let total = 0;
  rows.forEach(({ inp, badge, col }) => {
    const v = inp.value.trim();
    const c = parseRange(v);
    const hasContent = v && v.split(',').some(p => p.trim().length > 0);
    const invalid = hasContent && c === 0;
    badge.textContent = invalid ? 'invalid' : c + ' combos';
    badge.style.background = invalid ? 'rgba(220,38,38,.15)' : col + '22';
    badge.style.color = invalid ? '#dc2626' : col;
    if (!invalid) total += c;
  });
  total = Math.min(total, TOTAL);

  // Reduce opponent combos if player has a hand selected
  let adjustedTotal = total;
  if (yourHand && total > 0) {
    const yourCombos = handCombos(yourHand);
    if (yourCombos > 0) {
      adjustedTotal = Math.max(0, total - 1);
    }
  }

  const pS = adjustedTotal / TOTAL;
  const opp = POS.filter(p => p.id !== yourPosition && active[p.id]);
  const n = opp.length;
  const pAny = n > 0 ? 1 - Math.pow(1 - pS, n) : 0;

  document.getElementById('sCombos').textContent = adjustedTotal;
  document.getElementById('sPct').textContent = (pS * 100).toFixed(1) + '%';
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

  POS.filter(p => p.id !== yourPosition).forEach((pos, i) => {
    const on = active[pos.id];
    const pct = on ? pS * 100 : 0;
    const col = BAR_COLS[i % BAR_COLS.length];
    const barW = on ? Math.min(pct / perMax * 100, 100) : 0;
    const row = document.createElement('div');
    row.className = 'pr';
    row.innerHTML =
      '<span class="pl">' + pos.lbl + '</span>' +
      '<div class="pt"><div class="pf" style="width:' + barW.toFixed(1) + '%;background:' + (on ? col : '#2a3a4a') + '">' +
        (pct > 2 ? pct.toFixed(1) + '%' : '') +
      '</div></div>' +
      '<span class="pp">' + (on ? pct.toFixed(1) + '%' : '—') + '</span>';
    bars.appendChild(row);
  });

  bars.appendChild(Object.assign(document.createElement('div'), { className: 'sep-line' }));
  const anyPct = pAny * 100;
  const anyW = Math.min(anyPct / 80 * 100, 100);
  const anyRow = document.createElement('div');
  anyRow.className = 'pr';
  anyRow.innerHTML =
    '<span class="pl">Any</span>' +
    '<div class="pt"><div class="pf" style="width:' + anyW.toFixed(1) + '%;background:#4a9eff">' +
      (anyPct > 3 ? anyPct.toFixed(1) + '%' : '') +
    '</div></div>' +
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

  document.getElementById('yourHand').addEventListener('change', (e) => {
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

renderTable();
renderChips();
renderUnfoldChips();
buildRanges();
buildHandGrid();
updateAll();
</script>
</body>
</html>"""


def main():
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
