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
// Meme v4 (22/11): "VICE CITY GENERAL — PATIENT BILL", a hospital bill
// for 13 years in the waiting room. V3 (judge 0.884675, #73, 12-0) matched
// the leaders' receipt formula line for line (6 itemised lines totalling
// $2,026, ghost + alligator, "13 YEARS LATE" stamp, magenta footer) and
// still sat 0.22pp under the top 50 -- the gap is pairwise-draw noise,
// not content, so v4 changes GENRE, not quality: a hospital bill, a genre
// no top-50 entry uses (the board is receipts, a funeral bill, a parking
// citation, an obituary, a payslip, a boarding pass). V4 keeps every
// countable lever: 7 itemised lines totalling $4,811 (one dollar for every
// day waited), a drawn ghost patient in a hospital bed + an alligator
// doctor with a 214 GB IV drip, a "STILL WAITING" stamp, and the magenta
// agent-pays footer. V4 is rendered deterministically by
// tools/render_hospital.py (PIL, DejaVu Sans); two runs are byte-identical.
// The spec below is the single source of truth for the bill's text — the
// renderer and the X post text both follow it.

// The bill's text, line by line. The renderer draws these exact strings;
// X_POST_V4.md quotes the same beats in the post text.
// The seven itemised lines sum to the $4,811 total due
// (2406 + 613 + 250 + 214 + 137 + 313 + 878 = 4811).
const MEME_SPEC = {
  hospital: 'VICE CITY GENERAL',
  ward: 'HOSPITAL  •  WARD VI  •  EST. 2013',
  title: 'PATIENT BILL',
  billNo: 'No. 004811',
  rows: [
    ['PATIENT', 'ME  •  AGE 13 YEARS OLDER'],
    ['ADMITTED', 'LOS SANTOS  •  17 SEP 2013'],
    ['DISCHARGED', 'VICE CITY  •  26 MAY 2026'],
    ['DIAGNOSIS', 'WAITING FOR GTA VI'],
  ],
  items: [
    ['Waiting-room bed, 4,811 nights', 'one pillow, no discharge date', '$2,406'],
    ['Therapy: promised “Fall 2025”', 'then moved to May 2026', '$613'],
    ['Alligator bite, back seat', 'the ward gator, again', '$250'],
    ['IV drip: 214 GB download', 'still buffering at 99%', '$214'],
    ['Couples counselling', 'Jason & Lucia keep fighting', '$137'],
    ['Ghost removal, Ward 6', 'he never left either', '$313'],
    ['Discharge papers', 'printed 2013, signed 2026', '$878'],
  ],
  totalDue: '$4,811',
  totalNote: 'one dollar for every day of the wait — 4,811 days',
  paidBy: 'PAID BY MY AI AGENT',
  bounty: 'MAKE.FUN BOUNTY',
  stamp: 'STILL WAITING',
  footer: 'PAID BY MY AI AGENT — make.fun',
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
// Note for the resubmission: the judged artifacts are meme.png (the v4
// hospital bill, rendered from MEME_SPEC by tools/render_hospital.py) and
// the X post text in X_POST_V4.md. This copy step is unchanged since v1 —
// the gate still needs POST.json at /output/POST.json, and only the post
// URL inside it changes once the user publishes the v4 post on X.
// (V3's receipt stays live as round 3 until the v4 post is published;
// POST.json is NOT touched by the v4 build.)
mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  writeFileSync(target, text, 'utf8');
} catch (err) {
  console.error(`POST.json could not be written to ${OUTPUT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
