// gta6-meme-x-01 entry (Node 22, standard library only).
//
// The entry is the X post itself: an AI judge reads the post's first
// picture (meme.png) and its text from X. This program does nothing
// judged: it only copies POST.json, which names the post, from the
// repository root to /output/POST.json, where the gate reads it.
//
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
//
// POST.json holds a placeholder until the meme is posted on X; the
// placeholder URL is not a real post, so the gate refuses it as it
// stands. Replace it with the real post address before submitting.
//
// Meme v2 (22/11): "VICE CITY GAMES — PRE-ORDER RECEIPT". The v1
// WANTED-poster ghost was vague next to the leaderboard leaders, who
// are all fake official documents itemising the 4,811-day wait with an
// AI-agent-pays punchline. V2 joins that winning genre with a
// GTA-native document: pre-ordered GTA V in 2013, picked up GTA VI in
// 2026. The receipt is rendered deterministically by
// tools/render_receipt.py (PIL, DejaVu Sans Mono); two runs are
// byte-identical. The spec below is the single source of truth for
// the receipt's text — the renderer and the X post text both follow it.

// The receipt's text, line by line. The renderer draws these exact
// strings; X_POST.md quotes the same beats in the post text.
const MEME_SPEC = {
  store: 'VICE CITY GAMES',
  address: 'OCEAN DRIVE  •  VICE CITY, LEONIDA',
  title: 'PRE-ORDER RECEIPT',
  receiptNo: 'RECEIPT #0004811',
  cashier: 'CASHIER: MY AI AGENT',
  rows: [
    ['PRE-ORDERED', 'GTA V  —  17 SEP 2013'],
    ['PICKED UP', 'GTA VI  —  26 MAY 2026'],
  ],
  waitTime: '4,811 DAYS',
  totals: [
    ['TOTAL PAID', '13 YEARS OF MY LIFE'],
    ['BALANCE DUE', '$0.00'],
  ],
  paidBy: 'PAID BY MY AI AGENT',
  bounty: 'MAKE.FUN BOUNTY',
  stamp: 'PAID',
};

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const source = join(BOT_DIR, 'POST.json');
const target = join(OUTPUT_DIR, 'POST.json');

let text;
try {
  text = readFileSync(source, 'utf8');
} catch (err) {
  console.error(`POST.json could not be read from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}

let post;
try {
  post = JSON.parse(text);
} catch (err) {
  console.error(`POST.json is not valid JSON: ${(err as Error).message}`);
  process.exit(1);
}

if (typeof post !== 'object' || post === null || typeof post.url !== 'string') {
  console.error('POST.json must be an object with a string "url" field.');
  process.exit(1);
}

// Copy the file byte for byte: the gate reads POST.json exactly as the
// repository holds it, so re-serialising it here could only change bytes
// the entry does not need changed. Validation above still rejects a
// malformed file before anything is written.
//
// Note for the resubmission: the judged artifacts are meme.png (the v2
// receipt, rendered from MEME_SPEC by tools/render_receipt.py) and the
// X post text in X_POST.md. This copy step is unchanged since v1 — the
// gate still needs POST.json at /output/POST.json, and only the post
// URL inside it changes once the user publishes the post on X.
mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  writeFileSync(target, text, 'utf8');
} catch (err) {
  console.error(`POST.json could not be written to ${OUTPUT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
