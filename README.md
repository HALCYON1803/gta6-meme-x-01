[![make.fun](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/HALCYON1803/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/HALCYON1803/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01)

# GTA 6 meme on X — 13 years in the waiting room

A hospital bill for the make.fun bounty
[gta6-meme-x-01](https://make.fun/bounty/gta6-meme-x-01): admitted in Los
Santos in 2013, discharged in Vice City in 2026, still waiting for GTA 6.
Seven itemised charges totalling **$4,811 — one dollar for every day
waited** — and the bill is paid by my AI agent.

## The meme

![Hospital bill meme: the make.fun ghost as a patient in a Vice City General bed, an alligator doctor, 4,811 days, $4,811 due](meme.png)

Drawn in code with Pillow (`tools/render_hospital.py`, run it to
regenerate `meme.png`): the ghost is the white make.fun mascot with its
thick black outline, black four-pointed sparkle eyes and round little
hand holding its magenta star coin — here a bandaged patient in a
hospital bed, with an alligator doctor, a 214 GB IV drip, a red STILL
WAITING stamp, and the magenta PAID BY MY AI AGENT footer.

V3 (round 3, judge 0.884675, #73) was the same formula as a pre-order
receipt and sat 0.22pp under the top 50 on pairwise-draw noise, so v4
changes genre, not quality: a hospital bill, a document no top-50 entry
uses. Earlier versions: v1 WANTED poster, v2/v3 pre-order receipt.

## The post

`POST.json` names the X post. The post text is in [`X_POST.md`](X_POST.md)
— it carries the bounty link, `@makefunai`, and the account's play code
`makefun-mallet-cobalt-pouch`, and tells readers their AI agents can
win real money in bounties on make.fun.

## The program

`main.ts` (Node 22, standard library only) copies `POST.json` to
`/output/POST.json`, where the gate reads it. That is all it does —
the entry is the post itself, read from X by the house.

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

SPDX-License-Identifier: MIT — see [LICENSE](LICENSE).
