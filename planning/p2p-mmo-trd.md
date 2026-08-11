# Kakkoi Online — Technical Requirements Document (v0.1, for review)

Companion to `p2p-mmo.md` (design rationale + decision log). That doc says *why*; this one says
*what to build*. Links and licences for everything referenced here live in `kakkoi-online-sources.md`. Every number here is a starting default, chosen to be changed.

- **Title:** **Kakkoi Online**.
- **Audience:** lessons must be readable by a 12-year-old. **Chat is preset-phrase only — no free text in v1.**
- **Product:** browser, top-down, serverless P2P creature-battler.
- **Repo:** `kakkoi-online` (new, separate). Lessons stay in `izumo-io`.
- **URL:** `https://mmo.kakkoi.dev`.
- **Scale target:** ~5 concurrent players. Correctness at 2, comfort at 8, no design work beyond that.
- **Status:** nothing implemented. Awaiting review of this document.

---

## 1. Toolchain, repo layout, CI

```
kakkoi-online/
├─ index.html                  Bun entrypoint: canvas + Basecoat shell
├─ src/
│  ├─ main.ts                  boot & wiring
│  ├─ loop.ts                  fixed-timestep loop
│  ├─ input.ts                 keyboard/touch → Intent
│  ├─ world.ts                 tilemap + collision
│  ├─ render.ts                camera, layers, nameplates
│  ├─ sprites.ts               atlas → draw a 16×16 rect (tiles, monsters, NPCs)
│  ├─ audio.ts                 load + play CC0 files (~30 lines, no library)
│  ├─ save.ts                  load / save / migrate / export / import
│  ├─ identity.ts              player id, name, element
│  ├─ net.ts                   trystero wrapper: room, actions, presence
│  ├─ validate.ts              every inbound message passes through here
│  ├─ sync.ts                  position broadcast + interpolation
│  ├─ chat.ts                  preset-phrase chat + mute
│  ├─ ghost.ts                 (v2) async presence notes
│  ├─ npc.ts                   client-local NPCs: waypoints, barks, trainers
│  ├─ battle/
│  │  ├─ rules.ts              PURE: type chart, resolution, damage
│  │  ├─ fsm.ts                turn state machine
│  │  ├─ protocol.ts           commit / reveal / state-hash over the wire
│  │  └─ ai.ts                 local opponent move picker
│  ├─ ui/                      Basecoat-driven DOM panels
│  └─ i18n.ts                  en / ja / pt strings
├─ data/
│  ├─ tuning.json              all balance numbers
│  ├─ type-chart.json          element multipliers
│  ├─ monsters.json            the ~6 monsters: atlas rect, name, element
│  ├─ npcs.json                placement, waypoints, element, difficulty, bark keys
│  └─ maps/town.json           tilemap
├─ vendor/                     trystero, basecoat.css, kenney atlases (Tiny Dungeon + Tiny Creatures)
├─ audio/                      8 CC0 effects (Kenney) + 2 CC0 chiptune loops (OpenGameArt)
├─ tests/                      bun test
├─ .github/workflows/deploy.yml
├─ CNAME                       mmo.kakkoi.dev
└─ Makefile                    dev / check / test / build
```

**Commands**

| Task | Command |
|---|---|
| dev | `bun ./index.html` (TS on the fly, hot reload) |
| typecheck | `bunx tsc --noEmit` — Bun strips types without checking them; this is the real gate |
| test | `bun test` |
| build | `bun build ./index.html --minify --outdir=dist --sourcemap` |

**CI** (`deploy.yml`), on push to `master`: `bunx tsc --noEmit` → `bun test` → `bun build` →
`actions/deploy-pages`. On PR: the first two only. **A red build must not deploy** — the live site is
the students' shared world.

**Dependency rule, enforced by review:** `battle/rules.ts` and `validate.ts` import
nothing from `net.ts`, `render.ts`, or the DOM. They are pure and unit-testable. Everything else may
depend on them, never the reverse.

**Browser support:** Chrome/Edge/Firefox current, Safari 16+. Requires a **secure context** for
`crypto.subtle` (battle commitments) — `https://` in production, `localhost` in dev. Opening
`file://` fails, deliberately, and that's lesson A10.

---

## 2. Data model

```ts
type Element = 'fire' | 'water' | 'earth';
type Dual = 'scald' | 'magma' | 'mire';          // v2 only: fire+water | fire+earth | earth+water

interface Creature {
  monster: number;         // index into data/monsters.json — the player's choice
  // element is NOT stored: it is a property of the chosen monster (monsters.json)
}

interface SaveFile {
  v: 1;
  id: string;              // 'p-' + 8 hex, generated once
  name: string;            // 1..16 chars, validated
  creature: Creature;
  pos: { map: string; x: number; y: number };
  settings: { audio: boolean; lang: 'en' | 'ja' | 'pt' };   // audio defaults to false (classroom)
                                                           // v1 has no free-text chat setting: presets only
  muted: string[];         // player ids
  record: { wins: number; losses: number };   // local diary, unverifiable by design
}
// v2 adds: cosmetics, notes (ghost), creature.level/xp, creature.elements[1], settings.audio
```

`data/tuning.json` holds every balance constant so tuning never touches code:

```json
{
  "hp": 30, "baseDamage": 4,
  "elementAdvantage": 2.0, "elementResist": 0.5,
  "punishMultiplier": 1.5,
  "chargeMultiplier": [1, 2, 3], "maxCharges": 2,
  "blockRewardCharges": 1,
  "maxHitFraction": 0.5,
  "damageRoll": [0.9, 1.0],
  "stallChipDamage": 1, "stallRounds": 3,
  "targetRounds": [4, 12],
  "commitTimeoutMs": 10000,
  "posHz": 10, "posHzLow": 5, "interpDelayMs": 150
}
```

---

## 3. Battle rules (pure, `battle/rules.ts`)

**Type cycle:** water beats fire, fire beats earth, earth beats water. Attacking with advantage ×2,
into resistance ×0.5, otherwise ×1.

**Dual types are v2.** When they arrive: the attacker uses its **best** element (`max` over its
elements) and the defender multiplies over **both** of its elements, so duals flatten variance rather
than add power and pure types stay viable. v1 is one element per creature, which keeps the whole chart
a 3×3 table a child can read.

**Action resolution** (both players choose simultaneously and secretly):

| | vs Strike | vs Block | vs Charge |
|---|---|---|---|
| **Strike** | both take damage | 0 damage, **defender gains 1 charge** | ×1.5 damage, defender's charges stripped |
| **Block** | take 0, **gain 1 charge** | nothing | opponent banks a charge |
| **Charge** | take a punish, charges stripped | bank a charge | both bank |

- Strike beats Charge, Block beats Strike, Charge beats Block. Charge stops the staring contest:
  turtling loses to a charging opponent.
- Charges cap at 2 (×3 damage), spent on your next Strike, stripped when punished.
- **Every win pays in a different currency** — Strike wins tempo, Block converts defence into future
  offence, Charge buys power safely. This is the Yomi principle (see design doc §6.1); a Block that
  paid nothing collapsed the triangle in the first draft.
- **Anti-stall:** 3 consecutive rounds with zero damage → both take 1 chip damage.

**Damage**

```
seed  = revealedNonceA XOR revealedNonceB          // neither side can predict or steer it
roll  = 0.9 + (seed → uniform) × 0.1              // Pokémon-style variance, fully deterministic
dmg   = base × elementMult × chargeMult × actionMult × roll     // no level term: v1 has no levels
dmg   = min(round(dmg), maxHP × 0.5)              // no one-shots from full, ever
```

The nonces already exist for commit–reveal, so reusing them as a shared randomness beacon costs ~5
lines and gives variance without sacrificing determinism. (Same construction as decentralised
lotteries — a good lesson in its own right.)

**v1 has no levels and no stats** (lessons doc §6.1), which deletes the whole self-reported-stats
problem: there is no number for a cheater to inflate. Incoming claims are still clamped on receipt.
Hits-to-KO by design: plain trade ≈8 rounds, advantage hit ≈4, fully charged advantage hit capped at
2 — landing duels at **5–8 rounds**.

**Determinism requirement.** `resolveRound()` is a pure function of `(stateA, stateB, moveA, moveB,
nonceA, nonceB, tuning)`. Both peers must reach byte-identical state. No `Math.random`, no
`Date.now()`, integer damage each round, no float accumulation across rounds.

---

## 3.1 NPCs and the two interfaces that make them free

NPCs are **entirely client-local**: no protocol, no consensus, no authority, not visible to peers. Each
client simulates its own. Two interfaces do the heavy lifting:

```ts
interface Opponent {                        // battle/fsm.ts talks only to this
  readonly kind: 'peer' | 'ai';
  commit(round: number): Promise<Hash>;     // peer: over the wire | ai: local, immediate
  reveal(round: number): Promise<Reveal>;
  readonly profile: { name: string; elements: Element[]; level: number };
}

interface Actor {                           // render.ts draws anything shaped like this
  id: string; x: number; y: number; dir: Dir; moving: boolean;
  creatureSeed: string; name: string; nameplate: 'player' | 'npc';
}
```

Consequence: **the battle FSM cannot tell whether it is fighting a human**, and the renderer cannot tell
a peer from an NPC. `LocalAI implements Opponent` (commit/reveal resolve immediately, no crypto needed —
but keep the nonce so the damage roll works identically). That's the polymorphism lesson, earned rather
than recited.

```ts
interface NpcDef {
  id: string; kind: 'townsfolk' | 'trainer' | 'tutor' | 'board' | 'rest';
  seed: string;                             // appearance, same generator as players
  pos: { x: number; y: number };
  waypoints?: { x: number; y: number }[];   // townsfolk patrol
  barkKeys?: string[];                      // i18n keys, never literal strings
  battle?: { elements: Element[]; level: number; ai: 'random' | 'greedy' | 'reader'; cooldownMs: number };
}
```

**AI tiers = prediction depth**, following the RoShamBo/Iocaine Powder result (design doc §6.2):

| Tier | Algorithm | What it teaches the player |
|---|---|---|
| 1 `random` | uniform mix | unexploitable but dull — the baseline |
| 2 `greedy` | rules: strike when charged, block at low HP | punishes obvious play |
| 3 `frequency` | counts your action frequencies, counters the most common | don't have a favourite move |
| 4 `history` | matches the last 2–3 round pattern ("after Block you Charge") | vary deliberately — the actual skill |
| 5 `meta` | one Iocaine-style meta layer over tier 4 | boss-tier, exactly one NPC |

**Deliberately capped:** tiers 4–5 get a **25% uniform-random floor** and an **8-round memory**. An
uncapped predictor beats humans, because humans are bad at being random, and a frustrating trainer is
worse than no trainer.

No tier peeks: the AI commits before seeing your move, exactly like a peer, and goes through the same
nonce path so the damage roll is identical in PvE and PvP.

**Rules:** NPC nameplates are visually distinct and NPCs never appear in the players-online list — we
do not fake human presence. Barks are i18n keys (en/ja/pt), budget ~8 NPCs × 3 lines.

---

## 4. Network protocol

Transport: trystero over Nostr signaling, one room (`mmo-town-v1`). Action names are kept short
because trystero caps their length. Every inbound message goes through `validate.ts` first — no
exceptions, no shortcuts.

| Action | Direction | Payload | Rate limit |
|---|---|---|---|
| `id` | on peer join, and on change | `{v, id, name, monster}` — element is derived from `monster` locally | 2/s |
| `pos` | broadcast, 10 Hz while moving | `{x, y, dir, moving}` | 15/s |
| `cht` | broadcast | `{phrase: number}` — index into a preset phrase table. **No free-text field exists in v1** | 2/s, burst 5 |
| `duel` | targeted | `{kind: 'invite'\|'accept'\|'decline'\|'forfeit', duelId}` | 1 per 2s |
| `bcm` | targeted | `{duelId, round, hash}` — SHA-256 commitment | 4/s |
| `brv` | targeted | `{duelId, round, move, nonce}` | 4/s |
| `bsh` | targeted | `{duelId, round, stateHash}` — desync check | 4/s |
| `gst` | on join | `{notes: GhostNote[]}` ≤ 5 notes | 1 per 10s |

```ts
interface GhostNote {              // templated, never free text — see design doc §2.4
  id: string;                      // author player id
  map: string; x: number; y: number;
  phrase: number;                  // index into a fixed phrase table
  slot: number | null;             // index into a fixed fill-in table (element, direction, …)
  praise: number;                  // appraisal count, advisory only
}
```

Templated notes give us moderation-by-construction **and** automatic translation: `phrase`/`slot` are
i18n keys, so a note left in Japanese renders natively in Portuguese. Notes are information-only — no
mechanical effect, nothing to grief with.

**Validation rules (all mandatory):** known action name; payload is an object of expected shape; every
string length-capped; every number finite and range-clamped (`level` 1–20, coordinates inside map
bounds, `round` within ±1 of local round); unknown fields ignored; a peer exceeding its rate limit has
messages dropped and, after 20 violations, is auto-muted for the session. **Cheating stats is
tolerated by design; crashing or spamming another client is not.** This is the security spine of the
whole project — one hostile peer must not be able to take down the room.

**Protocol versioning:** `id` carries `v`. Mismatched major version → show "this player is on a
different version" and refuse duels rather than desync. Necessary because students deploy their own
forks at their own pace.

### 4.1 Duel sequence

```
A                                   B
│ duel{invite}         ─────────────▶
│                      ◀───────────── duel{accept}
│  (both build BattleState from the two `id` payloads, clamped)
│ bcm{round:1, H(move‖nonce)} ──────▶      ◀── bcm{...}
│  (wait for both commitments)
│ brv{round:1, move, nonce}   ──────▶      ◀── brv{...}
│  verify SHA-256(move‖nonce) == their commitment      ─── mismatch ⇒ cheat, abort
│  both run resolveRound() locally
│ bsh{round:1, stateHash}     ──────▶      ◀── bsh{...}
│  hashes differ ⇒ desync, abort with a diagnostic
│ …next round until HP ≤ 0
```

Commit-then-reveal exists because whoever sends second would otherwise always win. ~10 lines of
`crypto.subtle.digest`, and it makes the interesting part of the game honest even though position and
stats are not.

**Failure handling:** 10 s commit timer, timeout counts as **Block** (never a free win for the waiter,
never a punish for a lag spike); peer disconnect → forfeit after a 15 s grace; reveal mismatch →
immediate abort labelled "invalid reveal"; state-hash mismatch → abort labelled "desync" with both
states dumped to console for the debugging lesson.

### 4.2 Movement sync

Broadcast `pos` at 10 Hz **only while moving** (5 Hz in low-bandwidth mode); send one final packet on
stop. Remote players render from a 2-sample buffer interpolated **150 ms in the past** — smooth motion
in exchange for a small, invisible delay. Extrapolate for at most 250 ms on packet loss, then freeze.
Teaches: bandwidth vs smoothness, latency hiding, and that what's on your screen is always the past.

---

## 5. Monsters and sprites (`sprites.ts`)

No generation. `data/monsters.json` lists the playable set:

```ts
interface MonsterDef {
  id: number;
  nameKey: string;          // i18n key, so the species name reads in en/ja/pt
  element: Element;         // choosing the monster chooses the element
  atlas: 'creatures';
  rect: [x: number, y: number];   // 16×16 cell in the Kenney Tiny Creatures atlas
}
```

Target ~6 monsters, **2 per element**, so every element has a visual choice without a matrix. NPCs and
the AI trainers draw from the same file, which is why an NPC needs no new art path.

Rendering: one `drawImage` per actor from the atlas, at 2× scale (16×16 source → 32×32 on screen),
`imageSmoothingEnabled = false` so pixels stay crisp. Animation is a vertical bob while moving plus a
horizontal flip for facing — **no directional walk cycles, no spritesheet slicing beyond the atlas grid.**

Appearance travels over the wire as the single `monster` integer in the `id` payload (validated against
the table's length on receipt, like everything else).

**[HONEST]** With ~6 monsters and up to 5 players, two people can look identical. The nameplate is the
disambiguator; a per-player hue tint is a v2 option if it ever matters.

## 6. Presentation

**Render.** 32 px tiles; camera centred on the player and clamped to map bounds; draw order ground →
objects → creatures sorted by `y` → nameplates. Canvas sized to `devicePixelRatio` capped at 2.
Budget: 60 fps with 5 players and ~2,000 visible tiles; no per-frame allocation in the loop.

**Loop.** Fixed 60 Hz simulation step with an accumulator, decoupled from render, so physics never
depends on frame rate.

**World format.** `{ w, h, tileSize, layers: { ground: number[], objects: number[] }, collision:
number[], spawn: {x,y} }` — flat arrays, row-major, indices into a vendored Kenney atlas described by
`{src, tileW, tileH, cols}`. Collision is AABB against solid tiles. Hand-authored small map for v1;
Tiled export is drop-in later since the format matches.

**UI (Basecoat, DOM over canvas).** First-run dialog (name + element + **the safety card**, A18); chat card
with a preset-phrase picker (no text input); players-online popover; battle overlay (two HP bars, charge pips, three action
buttons, round log); settings dialog (export/import save, mute list, safety card link, language);
connection status badge with an explicit **"You're the only one here"** state and a NAT-failure
diagnostic. Nothing silently empty, ever.

**Audio.** CC0 files, no synthesis and no library: `new Audio(src)`, `loop = true`, `play()`. 8 effects
(step, strike, block, charge, duel start, win, lose, chat ping) from Kenney's RPG/UI Audio + Music
Jingles; two seamless chiptune loops from OpenGameArt (calm for the world, faster for duels). Master gain
≈0.3 music / 0.6 effects; `.ogg` with `.mp3` fallback, ~1–2 MB, lazy-loaded after first paint. Autoplay is
blocked until a user gesture — **the first-join dialog is that gesture**. **Off by default** (a classroom
of unmuted laptops), one obvious toggle, persisted.

**Accessibility & i18n.** All UI keyboard-reachable; battle actions bound to `1`/`2`/`3`; chat and
battle log are `aria-live`; element shown by icon **and** colour, never colour alone;
`prefers-reduced-motion` respected. Strings in `i18n.ts` for en/ja/pt to match school.kakkoi.dev —
cheap now, painful to retrofit.

---

## 7. Trust model

| Threat | Verdict | Mitigation |
|---|---|---|
| Edited position / stats | **Tolerated by design** | clamp to legal ranges on receipt; level worth ≤ +40% |
| Peeking at the opponent's move | **Prevented** | commit–reveal |
| Lying at reveal | **Detected** | hash mismatch ⇒ abort + forfeit |
| Rage-quit | Tolerated | forfeit after grace; only your local record changes |
| Impersonating a player id | Possible in v1 | keypair identity in appendix X1 |
| Malformed / flooding packets | **Blocked** | `validate.ts`, rate limits, auto-mute |
| Abusive chat | **Designed out** | preset phrases only — there is nothing arbitrary to say; plus local mute. No moderation is possible, so we removed the need for it |
| Client-local PvE cheating | Irrelevant | it's single-player |

Privacy upside worth stating on the site: no server means **no data collection** — nothing to leak,
nothing to subpoena, no cookie banner.

---

## 8. Testing

- **`bun test` on pure modules:** every cell of the action matrix; type-chart symmetry; damage clamps;
  `maxHitFraction` never exceeded; migration `v0→v1`.
- **Headless battle simulator (the balance regression test):** 1,000 duels per AI pairing — assert no
  crashes, no infinite games (round cap), duel length inside `targetRounds` (4–12), mirror-matchup win
  rate 45–55%, and `reader` beating `random` (if it doesn't, the mechanics carry no readable
  information and the game is a coin flip — that assertion *is* the depth test). Also assert the
  element-advantage matchup wins 60–75%, not 95%: uphill fights must be winnable.
- **Charge-economy check:** assert no strategy dominates — a Block-always bot and a Charge-always bot
  must both lose to `greedy`. This is what catches the "Block pays nothing" class of bug that §6.1
  found by hand.
- **Validator tests:** feed each action garbage (wrong types, huge strings, NaN, missing fields,
  prototype-pollution keys) and assert rejection without throwing.
- **Determinism test:** same inputs → identical state hash across 1,000 rounds.
- **Manual two-tab checklist per milestone.** Second tab needs a distinct identity: `?id=dev2`
  override, since both tabs share one `localStorage` origin.

---

## 9. Milestones and acceptance criteria

| M | Ships | Done when | Lessons |
|---|---|---|---|
| **M0** | canvas, loop, tilemap, collision, movement, procedural creature, save | you walk around, reload, and your creature is identical | A12–A16 |
| **M1** | trystero room, presence, `pos` sync, nameplates, online count | two tabs see each other move smoothly; closing one removes it within 5 s | A17–A21 |
| **M2** | preset-phrase chat, mute, `validate.ts`, rate limits, **safety card on first join** | a garbage-fuzzing peer cannot crash or spam the other client; muting visibly stops phrases arriving | A18, A22 |
| **M3** | duel invite/accept, FSM, commit–reveal, rules, **local AI opponent** | a full duel completes vs a human and vs the AI; a tampered reveal is caught | A23–A25 |
| **M3.5** | **NPCs**: townsfolk with waypoints/barks, tutor, trainer ladder | a first-time visitor alone in the world is taught the triangle and has someone to fight | A26 |
| **M4** | audio, polish, "only one here" state, NAT diagnostic, safety page | an empty world never looks broken; a stranger can arrive, play, and understand it | A27 |

**Deferred to v2 / appendices** (see lessons doc §6.1): levels & XP, dual types & evolution,
cosmetics, wild encounters, ghost notes, whisper, low-bandwidth mode, zones & sharding
(X4), keypair identity (X1), TURN (X2), touch controls (X3), the balance simulator as shipped content
(X6 — the CI assertions in §8 stay).

A10 ships to the live URL **before M0**, so every milestone above is deployed as it lands. Reference
repo gets an `aNN-end` tag plus one screenshot per lesson.

---

## 10. Risks

| Risk | Severity | Response |
|---|---|---|
| **Empty world** — 5 possible players means most visits are solo | **highest** | **NPCs at M3.5** (village feels inhabited, trainer ladder to fight), PvE by M4, explicit "only one here" state, ghost notes, and scheduled Discord play windows — non-technical, and still the real fix |
| Nostr relays flaky or gone | high | signaling isolated in one module; swapping strategy is a one-liner and a lesson |
| ~10% of networks can't connect at all | medium | clear diagnostic; Cloudflare TURN documented as an appendix |
| Combat too shallow | medium | dials in fixed order: signature move → feint → charge visibility. Ship bare first, then play it |
| Maintenance load (16 lessons × 3 languages + a live game) | medium | existing translate pipeline; pin every dependency; CI smoke test |
| Art reads as generic (shared CC0 sprites, two players may match) | low | nameplates disambiguate; ~6 monsters is a `monsters.json` edit away from more; hue tints are a v2 option |
| Fork version drift between students | low | protocol `v` in `id`, refuse cross-version duels |

---

## 11. Not in scope for v1

Spectating duels (needs a broadcast tree), trading, guilds/parties, a shared persistent world,
leaderboards or any ranking (impossible without authority), server-side anything, mobile app
packaging, voice chat.
