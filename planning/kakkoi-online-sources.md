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
| **trystero** | MIT | https://github.com/dmotz/trystero | WebRTC peer connections + Nostr signaling. The entire multiplayer layer |
| **Basecoat** | MIT | https://basecoatui.com | UI components. Using the standalone `basecoat.cdn.min.css` — **no Tailwind, no build step** |
| **Bun** | MIT | https://bun.com | Dev server (TS on the fly) + production bundler. Install: `curl -fsSL https://bun.com/install \| bash` |
| **TypeScript** (`tsc --noEmit`) | Apache-2.0 | https://www.typescriptlang.org | Type checking in CI. Bun strips types without checking them |

Deliberately **zero** runtime npm dependencies beyond trystero.

---

## 2. Art assets

| Pack | Licence | Link | Use |
|---|---|---|---|
| **Kenney — Tiny Dungeon** | CC0 | https://kenney.nl/assets/tiny-dungeon | Tiles, terrain, objects. 16×16, drawn at 2× |
| **Kenney — Tiny Creatures** | CC0 | https://opengameart.org/content/tiny-creatures | The ~6 playable monsters + NPCs. 180 sprites, 100+ monsters. **An expansion of Tiny Dungeon**, so terrain and creatures match by construction |

**CC0** means public domain: commercial use, no attribution required. We credit anyway — it's free and it's
right. Kenney's full CC0 catalogue: https://opengameart.org/content/all-cc0-uploader-kenney

**Never:** Pokémon or any Nintendo sprite, name, cry, or track. Not "probably shouldn't" — must not.
Also avoided: LPC asset sets, which are CC-BY-**SA** (share-alike), a licence we don't want to propagate
into every student's fork.

---

## 3. Audio assets

| Pack | Licence | Link | Use |
|---|---|---|---|
| **Kenney — RPG Audio** | CC0 | https://kenney.nl/assets/rpg-audio | Hits, blocks, footsteps (~50 sounds) |
| **Kenney — UI Audio** | CC0 | https://kenney.nl/assets/ui-audio | Clicks, confirms, errors (~50 sounds) |
| **Kenney — Music Jingles** | CC0 | https://kenney.nl/assets/music-jingles | Short stingers: won / levelled (~85) |
| **Juhani Junkala — 5 Chiptunes (Action)** | CC0 | https://opengameart.org/content/5-chiptunes-action | Background loops. **All five loop seamlessly** — the property that matters |

Alternate CC0 music if those don't fit: https://opengameart.org/content/4-chiptunes-adventure ·
https://opengameart.org/content/cc0-chiptune-music · Kenney's audio index:
https://kenney.nl/assets/category:Audio

**Correction on the record:** Kenney has **no background-music pack** — only the short jingles above. An
earlier draft of the design doc assumed a "Music Loops" pack existed. It does not; the category page is the
authority.

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
