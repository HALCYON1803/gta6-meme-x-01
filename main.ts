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
mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  writeFileSync(target, text, 'utf8');
} catch (err) {
  console.error(`POST.json could not be written to ${OUTPUT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
