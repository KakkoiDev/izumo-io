# Kakkoi Online — sources, assets, and references

Fourth document in the set. Every external thing this project uses, considered, or learned from, with its
licence and why it's here. Three jobs:

1. **Attribution and licence provenance** — for a project students will fork and redeploy, "where did this
   file come from and may I ship it?" must have an answer that isn't someone's memory.
2. **A citation list for the lessons.** Several lessons point students at these directly.
3. **A record of what we rejected**, which is A11's teaching material.

Keep this updated as the build proceeds. If something new gets vendored, it gets a row here in the same
commit.

---

## 1. Shipped in the game (runtime dependencies)

All vendored — pinned copies committed to `kakkoi-online/vendor/`, never hot-linked, so a CDN outage or a
deleted package can't break every student's deployed game.

| Thing | Licence | Link | Role |
|---|---|---|---|
| **trystero** `0.21.5` | MIT | https://github.com/dmotz/trystero | WebRTC peer connections + Nostr signaling. The entire multiplayer layer. **Vendored 2026-08-16** as six ES modules in `vendor/trystero/` (from `esm.sh/trystero@0.21.5/es2022/*` plus `esm.sh/node/crypto.mjs` and its chunk), import specifiers rewritten to relative `.js` paths — no bundler exists any more. Exact URLs in `vendor/README.md` |
| **Basecoat** | MIT | https://basecoatui.com | UI components. Using the standalone `basecoat.cdn.min.css` — **no Tailwind, no build step** |
| **Bun** | MIT | https://bun.com | Dev server (TS on the fly) + production bundler. Install: `curl -fsSL https://bun.com/install \| bash` |
| **TypeScript** (`tsc --noEmit`) | Apache-2.0 | https://www.typescriptlang.org | Type checking in CI. Bun strips types without checking them |

Deliberately **zero** runtime npm dependencies beyond trystero.

---

## 2. Art assets

All four atlases below are **vendored and verified** (2026-08-16). Sizes and grids were measured by
loading each file in a real browser, not read off a readme.

| Vendored as | Pack | Author | Licence | Real size / grid |
|---|---|---|---|---|
| `vendor/kenney/tiny-dungeon.png` | Kenney — Tiny Dungeon | Kenney | CC0 | 192×176 · 16×16 · 12 cols × 11 rows = 132 |
| `vendor/kenney/tiny-town.png` | Kenney — Tiny Town | Kenney | CC0 | 192×176 · 16×16 · 12 cols × 11 rows = 132 |
| `vendor/kenney/pixel-platformer-characters.png` | Kenney — Pixel Platformer 1.2 | Kenney | CC0 | 216×72 · 24×24 · 9 cols × 3 rows = 27 |
| `vendor/opengameart/tiny-creatures.png` | Tiny Creatures 1.0 | Clint Bellanger | CC0 | 160×288 · 16×16 · 10 cols × 18 rows = 180 |

**Exact download URLs** (Kenney's zip URLs carry a content hash and change on re-upload; they are not
guessable — read them off the asset page, where they sit behind "Continue without donating"):

| File | Zip | Path inside |
|---|---|---|
| tiny-dungeon | https://kenney.nl/media/pages/assets/tiny-dungeon/f8422efb44-1674742415/kenney_tiny-dungeon.zip | `Tilemap/tilemap_packed.png` |
| tiny-town | https://kenney.nl/media/pages/assets/tiny-town/a415fbeb49-1735736916/kenney_tiny-town.zip | `Tilemap/tilemap_packed.png` |
| pixel-platformer | https://kenney.nl/media/pages/assets/pixel-platformer/33bb4921eb-1696667883/kenney_pixel-platformer.zip | `Tilemap/tilemap-characters_packed.png` |
| tiny-creatures | https://opengameart.org/sites/default/files/tiny-creatures.zip | `tiny-creatures/Tilemap/tilemap_packed.png` |

Asset pages, which are where each licence is **stated**:
https://kenney.nl/assets/tiny-dungeon · https://kenney.nl/assets/tiny-town ·
https://kenney.nl/assets/pixel-platformer (each has a **License** row reading "Creative Commons CC0",
linking `https://creativecommons.org/publicdomain/zero/1.0/`) ·
https://opengameart.org/content/tiny-creatures (page reads `License(s): CC0`). Each pack's own
`License.txt` says the same and is committed next to the image as `*-LICENSE.txt`.

**Two corrections on the record:**

1. **There is no Kenney pack called "Tiny Creatures."** Kenney's Tiny series is farm, town, battle,
   ski, dungeon. *Tiny Creatures* is a real, CC0, 180-sprite set — but it is by **Clint Bellanger**,
   published on OpenGameArt, and built as a deliberate expansion of Kenney's Tiny Dungeon and Tiny
   Town *"made with Kenney's permission"* (his `License.txt`). So terrain and creatures still match
   by construction; the attribution was wrong, not the plan.
2. **Tiny Dungeon has no walk cycle.** Its 20 characters (cells 84–88, 96–100, 108–112, 120–124) are
   one pose each, and Tiny Creatures' 180 monsters are also one pose each. A14 needs at least two
   frames, so **Kenney Pixel Platformer's character sheet** was added: 24×24 cells laid out as
   adjacent pairs (0/1, 2/3, 4/5, 6/7 = four characters, legs-together and legs-apart). It is a
   different art style from the 16 px dungeon set — a known compromise, flagged here so A14 can say
   so out loud.

For A16, in `tiny-dungeon.png`: cell **48** is a plain sandy floor, cell **40** is a solid stone wall.

Always take the **`*_packed.png`** variant. Kenney's packs also ship a plain `tilemap.png` with a 1 px
gap between tiles, which breaks the `x = (n % cols) * cell` arithmetic the lessons teach.

**CC0** means public domain: commercial use, no attribution required. We credit anyway — it's free and it's
right. Kenney's full CC0 catalogue: https://opengameart.org/content/all-cc0-uploader-kenney

**Never:** Pokémon or any Nintendo sprite, name, cry, or track. Not "probably shouldn't" — must not.
Also avoided: LPC asset sets, which are CC-BY-**SA** (share-alike), a licence we don't want to propagate
into every student's fork.

---

## 3. Audio assets

### Shipped — vendored and verified 2026-08-16

Seven files, ~700 kB total, all CC0, all confirmed to load **and actually play** in a real browser.

| Vendored as | Length | Original file | Pack |
|---|---|---|---|
| `audio/step-soft.wav` | 0.273 s | `Audio/footstep05.ogg` | Kenney — RPG Audio |
| `audio/step.wav` | 0.049 s | `Movement/Footsteps/sfx_movement_footsteps1a.wav` | 512 Sound Effects (8-bit style) |
| `audio/strike.wav` | 0.111 s | `Weapons/Melee/sfx_wpn_sword1.wav` | same |
| `audio/block.wav` | 0.046 s | `General Sounds/Impacts/sfx_sounds_impact3.wav` | same |
| `audio/charge.wav` | 0.188 s | `General Sounds/Positive Sounds/sfx_sounds_powerup15.wav` | same |
| `audio/ping.wav` | 0.039 s | `General Sounds/Menu Sounds/sfx_menu_move1.wav` | same |
| `audio/win.wav` | 0.280 s | `General Sounds/Fanfares/sfx_sounds_fanfare2.wav` | same |
| `audio/music-loop.mp3` | 46.8 s | `happy_adveture.mp3` | Happy Adventure (Loop) |

| Pack | Author | Licence | Page (where the licence is stated) | Direct file |
|---|---|---|---|---|
| **512 Sound Effects (8-bit style)** | SubspaceAudio / Juhani Junkala | CC0 | https://opengameart.org/content/512-sound-effects-8-bit-style (`License(s): CC0`) | `https://opengameart.org/sites/default/files/The%20Essential%20Retro%20Video%20Game%20Sound%20Effects%20Collection%20%5B512%20sounds%5D.zip` (20.6 MB, 512 WAVs, 44.1 kHz/16-bit/mono) |
| **Happy Adventure (Loop)** | TinyWorlds | CC0 | https://opengameart.org/content/happy-adventure-loop (`License(s): CC0`) | `https://opengameart.org/sites/default/files/happy_adveture.mp3` |
| **Kenney — RPG Audio** | Kenney Vleugels | CC0 | https://kenney.nl/assets/rpg-audio (page **License** row reads "Creative Commons CC0"; the zip's own `License.txt` says "License (Creative Commons Zero, CC0)") | `https://kenney.nl/media/pages/assets/rpg-audio/8e99002d76-1677590336/kenney_rpg-audio.zip` (1.0 MB, 52 OGGs) |

The 512-sounds pack's own `INFO.txt` also states CC0; it is committed as `audio/sfx-512-LICENSE.txt`.
Kenney's `License.txt` is committed as `audio/kenney-rpg-audio-LICENSE.txt`.

**Footstep replaced 2026-08-16 (owner feedback).** The 8-bit `step.wav` was too harsh and too frequent
for a sound that fires the whole time you walk. `audio/step-soft.wav` is Kenney's `footstep05.ogg` — a
recorded, muted dirt step — decoded to 16-bit mono 22.05 kHz WAV with macOS's own
`afconvert -f WAVE -d LEI16@22050 -c 1`, and otherwise unedited. 16 kB. That contradicts the "no OGG
converter on this machine" note below: there is no `ffmpeg`/`sox`/`oggenc`, but `/usr/bin/afconvert`
ships with macOS and **does** decode Ogg Vorbis, so Kenney's OGG-only packs are usable after all as
long as what ships is the converted WAV. `audio/step.wav` stays in the repo unchanged because
`demos/17-sound/` loads it by name and demos are not to be modified; the game no longer uses it.

### Not used, but confirmed downloadable

Kenney's audio packs are CC0 and their zips **do** fetch with plain `curl` once you read the hashed URL
off the asset page:

| Pack | Licence | Page | Zip |
|---|---|---|---|
| **Kenney — UI Audio** | CC0 | https://kenney.nl/assets/ui-audio | `https://kenney.nl/media/pages/assets/ui-audio/490d233f68-1677590494/kenney_ui-audio.zip` |
| **Kenney — Music Jingles** | CC0 | https://kenney.nl/assets/music-jingles | `https://kenney.nl/media/pages/assets/music-jingles/f37e530b9e-1677590399/kenney_music-jingles.zip` |
| **Juhani Junkala — 5 Chiptunes (Action)** | CC0 | https://opengameart.org/content/5-chiptunes-action | `https://opengameart.org/sites/default/files/5%20Action%20Chiptunes%20By%20Juhani%20Junkala.zip` (50 MB, **WAV only**) |
| **Juhani Junkala — 4 Chiptunes (Adventure)** | CC0 | https://opengameart.org/content/4-chiptunes-adventure | `https://opengameart.org/sites/default/files/Juhani%20Junkala%20%5BChiptune%20Adventures%5D%20OGG.zip` (8 MB, OGG) |

They were skipped on **format**, not licence: the Kenney packs ship `.ogg` only, and OGG Vorbis is the
one common audio format with patchy Safari support. There is no `ffmpeg`, `sox` or `oggenc` on the
build machine — but `/usr/bin/afconvert` does decode Ogg Vorbis (see the footstep note above), so
"cannot be converted locally" was wrong. What ships is still WAV/MP3; the conversion happens here.
Choosing WAV (tiny, because these effects are all under 0.3 s) plus one MP3 gives universal playback
with no second copy of every file. The 5-Chiptunes pack is WAV-only and 50 MB, so it cannot be the
music loop either.

**Correction on the record:** Kenney has **no background-music pack** — only the short jingles above. An
earlier draft of the design doc assumed a "Music Loops" pack existed. It does not; the category page
(https://kenney.nl/assets/category:Audio) is the authority: casino-audio, digital-audio,
impact-sounds, interface-sounds, music-jingles, rpg-audio, sci-fi-sounds, ui-audio, voiceover-pack,
voiceover-pack-fighter. Loops come from OpenGameArt.

**No audio library.** Plain `HTMLAudioElement`. On the shelf if mobile playback quirks appear:
**howler.js** (MIT, ~9 kB gzip) https://howlerjs.com

---

## 4. Considered and rejected

The reasoning lives in `kakkoi-online-design.md` §10.1 and §12; this is the index.

| Thing | Licence | Link | Why not |
|---|---|---|---|
| **Phaser** | MIT | https://phaser.io | Replaces ~150–200 lines of ours with a ~1 MB bundle and a larger API to learn; deletes lessons A13–A15, which are the good ones. **Appendix X7 ports to it instead** |
| **ZzFX** | MIT | https://github.com/KilledByAPixel/ZzFX | Synthesised SFX in ~900 bytes. Elegant, but a generated sound that's wrong on one browser is very hard for a 12-year-old to debug. Files can't fail that way |
| **ZzFXM** | MIT | https://keithclark.co.uk/articles/zzfxm/ | Same, for music (~1.5 kB gzip for 2–3 minutes). Same reason |
| **Tone.js** | MIT | https://tonejs.github.io | ~200 kB and a large API. Right for a music app, overkill for eight bleeps |
| **pixel-sprite-generator** | MIT | https://github.com/zfedoran/pixel-sprite-generator | Procedural pixel creatures from a mask. Became unnecessary when we chose a fixed monster set — the name carries identity |
| **DiceBear** | MIT core, per-style licences | https://www.dicebear.com | Deterministic avatars from a seed, but **portraits, not walking game sprites** |
| **Robohash** | free service | https://robohash.org | Has a monster set, but it's an external service with no spritesheet |
| **Lospec procedural pixel art generator** | tool | https://lospec.com/procedural-pixel-art-generator/ | Produces a fixed set of assets — which Kenney already gives us, with a matching tileset |

---

## 5. Design research (the reasoning behind the game)

Each of these changed a decision. Not background reading — provenance.

| Source | Link | What it changed |
|---|---|---|
| **Sirlin — "Designing Yomi"** | https://www.sirlin.net/articles/designing-yomi | The big one. Each option must pay in a **different currency** → our Block now *banks a charge* instead of doing nothing. Also: cap burst damage explicitly (Yomi's combo-point budget → our `maxHitFraction`) |
| **Game Developer — RPS as competitive design** | https://www.gamedeveloper.com/design/rock-paper-scissors---a-method-for-competitive-game-play-design | Naive RPS stalls because attacking first exposes you. The standard fix is a **Charge** action — which is why our third button exists |
| **Iocaine Powder (RoShamBo winner)** | https://www.metafilter.com/181225/Iocaine-Powder | Frequency + history matching + meta layers beats humans. Became our **AI difficulty ladder = prediction depth**, plus the decision to **cap it** (25% random floor, 8-round memory) |
| **rpscontest.com** | http://www.rpscontest.com/ | Playground for students who want to take the prediction idea further |
| **Smogon damage calculator thread** | https://smogon.com/forums/threads/battle-spot-damage-calculator-thread.3597699 | Pokémon's 2HKO/3HKO vocabulary and its deliberate 0.85–1.00 damage roll → our **hits-to-KO target** and the nonce-seeded 0.9–1.0 roll |
| **RPG Maker forums — balancing turn-based RPGs** | https://forums.rpgmakerweb.com/threads/how-to-balance-a-turn-based-rpg.100893/ | Set a target action count and tune *to* it → the CI simulator asserting 4–12 round duels |
| **Death Stranding — Social Strand System** | https://deathstranding.fandom.com/wiki/Social_Strand_System | Asynchronous presence makes a sparse world feel inhabited → ghost notes (v2) |
| **GamesRadar — players weaponising helpful signs** | https://www.gamesradar.com/games/action/death-stranding-2-players-reach-breaking-point-for-hating-signs-as-devious-porters-place-speed-boosts-in-inconvenient-places-i-ran-over-a-quokka-because-of-one-of-those-signs-i-was-devastated/ | Any sign with mechanical power gets abused → our notes are **information only** |

### Games that use the mechanic we're using

Worth playing before finalising the duel — this is the genre we're in.

| Game | Link |
|---|---|
| **Janken Brawl** | https://juanrod707.itch.io/janken-brawl |
| **RPS Blitz Duel** | https://renlayer.itch.io/rps-blitz-duel |
| **Punch, Kick, Block** | https://ember44.itch.io/fighting-game |

---

## 6. Reference docs for things we build on

| Topic | Link |
|---|---|
| GitHub ToS — minimum age 13 (A09) | https://docs.github.com/en/site-policy/github-terms/github-terms-of-service |
| Anthropic consumer terms — minimum age 18 (A09) | https://www.anthropic.com/legal/consumer-terms |
| GitHub Classroom — teacher-owned student repos (students still need 13+ accounts) | https://classroom.github.com/ |
| GitHub plans — free orgs get unlimited public repos + members | https://docs.github.com/en/get-started/learning-about-github/githubs-plans |
| Actions billing — free/unlimited on public repos, standard runners | https://docs.github.com/billing/managing-billing-for-github-actions/about-billing-for-github-actions |
| Bun HTML entrypoints / dev server & bundler | https://bun.com/docs/bundler/html |
| trystero API, strategies, TURN config | https://github.com/dmotz/trystero |
| Basecoat installation (CDN, no Tailwind) | https://basecoatui.com/installation/ |
| Web Crypto `subtle.digest` (commit–reveal, A24) | https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/digest |
| WebRTC / NAT / STUN & TURN background (A20) | https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API |
| GitHub Pages + custom domain (A10) | https://docs.github.com/en/pages |

---

## 7. This project's own documents

| Doc | Contents |
|---|---|
| `kakkoi-online-design.md` | Design rationale, constraints, the decision log (42 rows, including six recorded reversals) |
| `kakkoi-online-trd.md` | Technical requirements: data model, protocol, battle rules, milestones, tests |
| `kakkoi-online-lessons.md` | The 21-lesson track (A09–A29), writing standard, safety, build process |
| `kakkoi-online-sources.md` | This file |
| `build-verify-track.md` | The wider programme this fits inside |

---

## 8. Housekeeping

- **Licence audit before launch:** every file in `vendor/` and `audio/` traced to a row above. A student
  forking this repo inherits our licence choices, so they must all be CC0/MIT.
- **A `CREDITS.md` in the game repo**, plus an in-game credits screen listing Kenney, Junkala, trystero,
  and Basecoat. CC0 doesn't require it; doing it anyway is what we want students to copy.
- **Pin everything.** Versions recorded here when vendored, so "it broke and I don't know what changed"
  never happens.
- **[OPEN]** Does the site want a public credits page too, or is the in-game screen plus this file enough?
