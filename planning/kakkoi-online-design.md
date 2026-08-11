# Kakkoi Online — requirements & design (discussion draft)

*Title: **Kakkoi Online**. Repo: `kakkoi-online`. URL: `online.kakkoi.dev`.*

> Status: **discussion document, nothing implemented.** Everything marked **[DECIDE]** needs
> your call before code. Everything marked **[HONEST]** is a limitation we should state to
> students rather than paper over — the limitations are half the teaching value.

Companion docs: `kakkoi-online-trd.md` (technical spec) · `kakkoi-online-lessons.md` (the lesson track) ·
**`kakkoi-online-sources.md` (every asset pack, library, and reference used, with licences)**.

Two deliverables, one project:

1. **The game** — a top-down, serverless, peer-to-peer multiplayer creature-battler, hosted free
   on GitHub Pages at `online.kakkoi.dev`.
2. **The lesson series** — lessons **A09–A29**, continuing the existing AI track on school.kakkoi.dev,
   walking a student from a plan to a deployed game using an AI coding agent, teaching the
   computer-science idea behind each step, why we chose it, what we rejected, and an example prompt.
   **Written so a 12-year-old can follow every sentence.**

---

## 1. Vision in one paragraph

You are a creature (fire, water, or earth). You walk around a shared top-down world with other
real people, you chat with them, and you challenge them to a duel resolved by an
elemental rock-paper-scissors with hidden information. There is no server: your browser talks
directly to the other players' browsers, and your character lives in your own browser's storage.
The whole thing costs nothing to run, forever.

### Non-goals (say these out loud, early)

- **Not a real MMO.** A browser can hold a limited number of WebRTC connections, and a full mesh
  costs `n·(n−1)/2` links. Realistic ceiling is ~8–16 players per zone. We call it an MMO for the
  vibe; we teach *why* real MMOs need servers. Lesson A28 is exactly this postmortem.
- **Not fair, not authoritative.** No referee means no trustworthy stats, no leaderboard, no ranked
  ladder, no economy. Accepted by design (see §7).
- **Not moderated.** No server means no bans, no logs, no reports. Because the readers are 12-year-olds,
  chat is **preset phrases only** — abuse is designed out rather than policed (see §9).
- **Not Pokémon.** No Nintendo assets, names, or sprites — ever. See §12 on licensing.

> **Expected scale: never more than ~5 concurrent players.** (Your call, and I think it's the
> realistic one.) This is load-bearing on the design — see §2.4. Short version: the mesh limit
> stops being a problem, sharding stops being necessary, and the **empty-room problem becomes the
> single biggest risk to the project.**

---

## 2. The three hard constraints (read before designing anything)

Everything downstream is shaped by these. They're also the three best lessons in the series.

### 2.1 No server means no authority

There is nobody to say "that's not true." Every fact in the game is a claim made by a peer about
itself. Your position, your level, your HP — all self-reported. Two consequences:

- Cheating position and stats is trivial. You already accepted this. **[HONEST]**
- Therefore *the fun must not live in the numbers.* If damage scales hard off self-reported stats,
  a cheater one-shots everyone and the game is dead within a week of any popularity. The design
  answer is §6: put the fun in **decisions under hidden information**. v1 removes the problem almost
  entirely by cutting levels and stats altogether (lessons doc §6.1) — there is no number to inflate.

### 2.2 No server means some players simply cannot connect

WebRTC needs a **STUN** server to discover your public address and, behind roughly 8–15% of
network setups (symmetric NAT, strict corporate/mobile networks), a **TURN** relay to proxy
traffic. Free public STUN exists. Free TURN essentially does not — TURN carries all your traffic,
so it costs money.

**[HONEST]** Some students and players will load the page, see zero peers, and it is not their bug.
Options: **[DECIDE]**
- (a) Accept it. Show a clear diagnostic ("couldn't reach peers — your network blocks direct
  connections"). Free forever. Recommended for v1.
- (b) Add Cloudflare's TURN (has a free tier with a monthly GB allowance) — a tiny bit of config,
  no server code, but an account and a key baked into a public page.
- (c) Self-host coturn on a cheap VPS. Breaks the "no server" promise.

I recommend (a) for launch, with (b) documented as an optional lesson appendix. Either way this is
the *best* NAT lesson a student will ever get, because they experience it.

### 2.3 Signaling still needs somebody

"Serverless" is a half-truth we must not tell students. Peers can't find each other from nothing;
they meet on a public pub/sub relay. Trystero supports BitTorrent trackers, **Nostr**, MQTT,
Supabase, Firebase, IPFS, or your own WebSocket relay. Your userscript uses Nostr, so we inherit
that. It is free and needs no account; it is also *someone else's infrastructure* and can be flaky.

**[DECIDE]** Nostr (matches your existing script, zero setup) vs MQTT (public brokers, sometimes
more reliable). Recommendation: Nostr, with the strategy isolated behind one module so swapping is
a one-line lesson exercise.

### 2.4 The real constraint: ~5 concurrent players

A 5-player mesh is 10 connections total, ~2 per browser. **Scale is a non-issue.** What this buys
and costs:

**Simplifies (cut or downgrade to "teach, don't build"):**
- **One room for the whole world in v1.** Zones become a *design* choice (map variety), not a
  networking necessity. Sharding: teach the idea in A21, don't implement it. (§8)
- Bandwidth, tick-rate tuning, interest management: all comfortable. 10 Hz × 4 peers is nothing.
- Lobby population counts become less about capacity and more about **proving someone is there** —
  which raises their value, see below.
- Anti-griefing is mostly social: at 5 players you know who did it. Input validation still matters
  (a malformed packet still crashes you), but rate-limiting is belt-and-braces.

**Makes worse — and this is now the #1 project risk:**
- **The empty room is the default state.** With 5 possible players, the honest expectation is that a
  visitor arrives alone ~90% of the time. A P2P multiplayer game with nobody in it doesn't look
  quiet, it looks *broken* — and a student will conclude their code failed. Nothing in the
  architecture fixes this; it has to be designed around:
  - The game must be **worth opening alone.** That promotes client-local wild creatures (§6) from
    "nice extra" to **required for M-early**, and it's an argument for a single-player-first
    milestone order (§13).
  - Explicit UI state: "**You're the only one here.** Open a second tab to test, or check the
    Discord play hour" — never a silent empty world.
  - **Scheduled play windows** in Discord beat any technical fix. One 30-minute slot after class
    where 5 people are online simultaneously is the entire multiplayer experience.
  - **Async presence — DECIDED, and it should be templated, not free text.** You leave a "ghost": a
    last-seen position plus a note, persisted in *your own* save and re-broadcast when you next meet
    someone. This is the [Dark Souls / Death Stranding Social Strand](https://deathstranding.fandom.com/wiki/Social_Strand_System)
    pattern — asynchronous interaction between players in different sessions, and the proven way to
    make a sparse world feel inhabited. Three things the research changes:
    - **Notes are composed from a preset vocabulary** ("try [element] here", "beware", "nice duel",
      "[direction] leads to…"), exactly as Dark Souls does. This solves **two** of our problems at
      once: unmoderatable free text becomes impossible, **and** a templated note **translates itself
      into all three languages** — a note left by a Japanese student reads naturally to a Brazilian
      one. For a trilingual school project with no server to moderate, this is close to a free win.
    - **Add appraisal** (a "this helped" tap). Dark Souls uses ratings to reward good notes with no
      direct interaction. Cheap, and it's the only positive-feedback loop available to us offline.
    - **Notes carry no mechanical power.** Death Stranding players immediately weaponised helpful
      signs by placing them in harmful spots ([GamesRadar](https://www.gamesradar.com/games/action/death-stranding-2-players-reach-breaking-point-for-hating-signs-as-devious-porters-place-speed-boosts-in-inconvenient-places-i-ran-over-a-quokka-because-of-one-of-those-signs-i-was-devastated/)).
      Ours are information only — no teleports, no buffs, nothing to grief with.
- **Fewer fights.** PvP duels need two humans online at once, which will be rare. Wild creatures
  (client-local) carry the combat loop; PvP becomes the special occasion. Design the combat rules
  to work identically against a simple local AI opponent — same `battle/rules.ts`, different mover.
  Good architecture lesson: the fight doesn't know or care whether its opponent is a person.

---

## 3. Architecture

```
┌─────────────────────── one browser tab = one player ───────────────────────┐
│                                                                            │
│  UI layer (DOM + Basecoat CSS)          World layer (<canvas>)             │
│  login panel, chat, battle HUD          tiles, sprites, movement           │
│                     ↑                            ↑                         │
│                     └────────── game state ──────┘                         │
│                             (plain JS objects)                             │
│                        ↑                        ↑                          │
│              localStorage (your save)      net module                      │
└─────────────────────────────────────────────────┼──────────────────────────┘
                                                  │ WebRTC data channels
                          ┌───────────────────────┴───────────────────────┐
                          │  peer   │  peer   │  peer   │  peer   │ ...   │
                          └───────────────────────────────────────────────┘
                                     ↑ met via a public Nostr relay (signaling only)
```

Deliberate split: **canvas for the world, DOM for the UI.** Canvas is right for a scrolling tile
world and sprites; it is miserable for text input, scrollable chat, and dialogs. Basecoat gives us
real accessible HTML components for those, floating over the canvas. This also keeps the lessons
clean: "draw pixels" and "build interfaces" stay separate skills.

### Module map (target: each file is one lesson's worth of reading)

```
index.html          canvas + Basecoat UI shell (Bun's entrypoint)
src/main.ts         boot, wire modules together
src/loop.ts         fixed-timestep game loop
src/input.ts        keyboard/touch → intent
src/world.ts        tile map, collision
src/render.ts       camera, tiles, sprites, name tags
src/save.ts         localStorage load/save/migrate/export
src/identity.ts     who am I (see §4)
src/net.ts          trystero wrapper: rooms, actions, presence
src/sync.ts         position broadcast + interpolation
src/chat.ts         chat transport + UI
src/battle/fsm.ts   turn state machine
src/battle/rules.ts pure functions: type chart, damage (unit-testable, no I/O)
src/battle/net.ts   commit/reveal protocol
src/battle/ai.ts    local opponent: picks a move (same rules as a human)
src/data/*.json     tile map, species, type chart, tuning numbers
vendor/trystero.js  pinned copy (see §10)
```

`battle/rules.ts` being pure and dependency-free is on purpose: it's the one part we can unit test
without a network, and it's the lesson on separating *decisions* from *plumbing*.

---

## 4. Login / identity

Copying your `trystero-p2p.user.js` model: **there is no login.** On first load you get a random
id, persisted locally; you pick a display name and a creature. That's the account.

- Storage: `localStorage` (per-origin) rather than the userscript's `GM_setValue` (cross-origin) —
  a page can't use GM APIs, and per-origin is what we want here anyway.
- Presence works exactly like your script: a reserved `id` action announces `{userId, name,
  species}` to newcomers on `onPeerJoin`, and we keep a `peerId → player` map, because trystero
  has no "who's in this room" query.
- **[HONEST]** This is *identification*, not *authentication*. Anyone can claim your id and name.
  Impersonation is free.
- **Optional upgrade, an appendix (X1):** generate an Ed25519/ECDSA keypair with WebCrypto,
  keep the private key in storage, let your **public key be your identity**, and sign every
  message. Peers verify signatures. Now nobody can impersonate you without your key — with zero
  servers and zero passwords. This is the single most valuable security idea in the series
  ("identity is key ownership, not a row in a database"), and it's ~40 lines.
  **[DECIDE]** ship in v1, or keep as a later lesson upgrade? I'd build v1 without it and add it as
  a lesson, because the *diff* is the teaching moment.
- Save portability: an **Export / Import save** button (base64 of the JSON). That's how you move
  characters between devices, and how a student recovers from clearing their browser.
  **[HONEST]** clearing site data = character gone. No cloud, no recovery. Say it in the UI.

---

## 5. Save data (JSON in the browser)

```json
{
  "v": 1,
  "id": "user-9f3a2c81",
  "name": "Kai",
  "creature": { "species": "emberling", "types": ["fire"], "level": 3, "xp": 140 },
  "pos": { "zone": "town", "x": 384, "y": 192 },
  "cosmetics": { "hat": "straw", "tint": "#e2b" },
  "settings": { "sfx": true, "lang": "en" },
  "muted": ["user-deadbeef"],
  "stats": { "wins": 12, "losses": 9 }
}
```

Two teaching points baked into the shape:
- **`v` first.** Schema versioning + a migration chain (`migrate1to2`) so the day you add a field
  you don't wipe every student's character. Real product discipline in 15 lines.
- **Wins/losses are local and unverifiable.** They're a diary, not a ranking. Deliberate.

---

## 6. Combat — the design problem you flagged

**No decks, no cards.** (An earlier draft of this doc proposed them; it was over-design for a game
whose goal is "something going." Dropped — kept only as a footnote at the end of this section.)

The real problem is small and specific: **three elements chosen simultaneously is a 33% coin flip.**
Game theory says the optimal strategy is "pick uniformly at random," and if random is optimal there
are no decisions. Two facts from looking at what already works:

- The known failure mode of naive RPS combat is that **nobody wants to attack first** — attacking
  opens you to a counter — so play stalls. The standard, well-trodden fix is a **Charge** action that
  makes aggression pay ([gamedeveloper.com](https://www.gamedeveloper.com/design/rock-paper-scissors---a-method-for-competitive-game-play-design)).
- Pokémon's own depth doesn't come from PP or from a single duel — it comes from **6 creatures × 4
  moves × type coverage**, i.e. team building. With one creature and no switching we don't have that,
  so the fun has to be a **per-round read**. And PP is widely considered its weakest mechanic
  (usually too generous to matter, and annoying when it does) — another reason not to copy it.

The fast, popular, already-proven shape is the three-action duel — Attack / Block / Charge — used by
a pile of small fighting games ([Janken Brawl](https://juanrod707.itch.io/janken-brawl),
[RPS Blitz Duel](https://renlayer.itch.io/rps-blitz-duel),
[Punch, Kick, Block](https://ember44.itch.io/fighting-game)). So:

### The whole system (two axes, three buttons)

**Axis 1 — your element is your identity, chosen once, not per round.** Fire/Water/Earth (later a
dual, §7) sets a static damage multiplier for the fight: attacking with the advantage is ×2, into
resistance ×0.5. Both players see the matchup before accepting the duel. Some fights are uphill,
exactly like Pokémon type matchups, and that's a reason to seek out different opponents.

**Axis 2 — every round, both players secretly pick one of three actions.** This is the whole game:

| | opponent **Strike** | opponent **Block** | opponent **Charge** |
|---|---|---|---|
| **Strike** | both take damage (trade) | blocked — **they gain a charge** | **you punish**: ×1.5 damage, their charges are stripped |
| **Block** | you take nothing, **you gain a charge** | nothing (stall) | they bank a charge safely |
| **Charge** | you get punished, charges stripped | you bank a charge safely | both bank |

A clean triangle: **Strike beats Charge, Block beats Strike, Charge beats Block.** Charge is what
makes it a game rather than a staring contest — turtling behind Block loses to a charging opponent,
so tension builds by itself.

**The "Block gains a charge" rule came out of researching how Yomi does it, and it fixes a real flaw
in my first draft** (§6.1 below): originally a successful Block meant *nothing happened*, which makes
the defensive option pay nothing and quietly collapses the triangle. Now every win pays in a different
currency — Strike wins tempo, Block converts defence into future offence, Charge buys power safely.

Numbers (all in `data/tuning.json`): **HP 30, base damage 4**, advantage ×2, resist ×0.5, punish ×1.5,
charges cap at 2 (×3 damage), level worth at most +40%, and **no single hit may exceed 50% of max
HP**. A duel is **5–8 rounds, under a minute.** Three buttons, ~30 lines of rules.

### 6.1 What comparable games actually do (balance research)

I looked at how designed games solve this exact problem, because my first numbers were guesses.

**[Yomi](https://www.sirlin.net/articles/designing-yomi) (David Sirlin)** is the closest relative: a
card fighting game built explicitly on the fighting-game RPS of attack / throw / block, plus dodge.
Three findings, all of which changed our design:

1. **The asymmetry lives in the *payoffs*, not the damage numbers.** In Yomi, Attack wins deal damage
   and open a combo; Throw wins deal damage but a worse combo; **Block returns the card to your hand
   and draws another** — it pays in *resources*, not damage; Dodge avoids damage and permits one big
   hit but no combo. Each win pays in a **different currency**. My original Block paid nothing at all,
   which is the flaw the table above now fixes: **a successful Block banks a charge.**
2. **Sirlin deliberately makes the payoffs hard to compute** so the game isn't solvable — "extremely
   difficult to compare or even to compute in the first place." **[HONEST]** With 3 options and small
   numbers, ours *is* computable by a determined player. Our mitigation is that the payoff matrix
   **shifts every round** with HP and charge counts, so the correct mix changes constantly. That's a
   genuinely nice thing to teach: the equilibrium is a moving target, not a lookup table.
3. **Yomi caps burst via a "combo point" budget per character.** That's independent confirmation of the
   `maxHitFraction` clamp — designed games explicitly bound the biggest possible hit rather than
   trusting the multipliers to stay sane.

**Pokémon**, for the damage side: competitive play is organised entirely around **2HKO / 3HKO** — how
many hits to a knockout — and the formula includes a deliberate **0.85–1.00 random multiplier**
([Smogon](https://smogon.com/forums/threads/battle-spot-damage-calculator-thread.3597699)). Two
borrowings:

- **Target hits-to-KO explicitly.** With HP 30 / base 4, a plain trade is 13% of HP (≈8 rounds), an
  elemental advantage hit is 27% (≈4), and a fully charged advantage hit is capped at 50%. So the
  duel lands at 5–8 rounds — long enough for reads to matter, short enough to stay fast.
- **A damage roll, derived from the reveal nonces.** Pokémon's variance keeps fights from feeling
  arithmetic. We can have it *without* breaking determinism: XOR both players' revealed nonces into a
  shared seed, and roll 0.9–1.0 from it. Neither player can predict or influence it at commit time,
  and both compute the identical result. That's a **commit–reveal randomness beacon**, the same
  construction decentralised lotteries use — and it costs us about five lines.

**Turn-based RPG practice** more broadly: designers set a target action count per encounter and tune
*to* it (e.g. [4 actions to kill a new monster](https://forums.rpgmakerweb.com/threads/how-to-balance-a-turn-based-rpg.100893/)),
rather than inventing numbers and hoping. Hence the CI simulator asserting duel length 4–12 rounds and
a 45–55% mirror win rate — the target is the spec, and the test enforces it.

### 6.2 NPCs — yes, and they do more work than they look like they do

Adding NPCs (your question) is one of the highest-value additions on the table, because it attacks the
project's #1 risk (§2.4: the empty world) at zero networking cost. NPCs are **purely client-local** —
no consensus, no authority, no protocol — the same argument that makes wild creatures safe.

Five kinds, in value order:

| NPC | Job | Cost |
|---|---|---|
| **Trainer** (duelable) | a difficulty ladder with a *fixed, visible* element, so you learn the type triangle before risking a human | reuses `battle/rules.ts` + `ai.ts`; ~1 data row each |
| **Tutorial trainer** | teaches Strike/Block/Charge in a scripted first duel; the single best retention lever in the game | scripted move list |
| **Townsfolk** | walk waypoints, occasional barks; makes the world *inhabited* rather than abandoned | waypoints + 2–3 lines each |
| **Chalkboard keeper** | reads out ghost notes left by real players (§2.4) — an NPC surfacing human traces | pairs with `ghost.ts` |
| **Rest/heal point** | somewhere to go; a loop | trivial |

Three reasons this is more than set dressing:

- **It makes the world legible when you're alone.** A visitor arriving to an empty map currently
  concludes the game is broken. A visitor arriving to a village with four people wandering around
  concludes the game *works* and that other players exist. Same code, opposite impression.
- **It's a difficulty ladder**, which is what progression needs when PvP is rare. Trainers with fixed
  elements let a player *learn* that water beats fire by losing to it, safely.
- **It's the best architecture lesson in the project.** An `Opponent` interface implemented by both
  `RemotePeer` and `LocalAI` means `battle/fsm.ts` **cannot tell whether it's fighting a person** —
  and an `Actor` interface means `render.ts` can't tell either. Students meet polymorphism as the
  thing that saved them writing the battle system twice, rather than as a vocabulary word.

**The AI difficulty ladder writes itself — and it must be deliberately capped.** The RoShamBo bot
competitions settled what beats humans at RPS: [Iocaine Powder](https://www.metafilter.com/181225/Iocaine-Powder),
the winner of the first International RoShamBo Programming Competition, combines random play,
most-frequent-throw counting, and **history matching**, then wraps any predictor in *meta* layers —
P.0 plays to beat the prediction, P.1 assumes you anticipated P.0, P.2 assumes you anticipated that,
and so on. Two consequences:

- **The ladder is literally prediction depth**, which is a gorgeous mapping for a teaching game:
  tier 1 = uniform random (unexploitable, dull), tier 2 = frequency counting ("you pick Strike a
  lot"), tier 3 = history matching ("after you Block you usually Charge"), tier 4 = one meta layer.
  Each tier is a small, comprehensible algorithm, and beating tier 3 requires the player to
  *deliberately vary* — which is the actual skill the game is about.
- **[HONEST] Left uncapped, this AI beats humans**, because humans are terrible at being random. A
  frustrating trainer is worse than no trainer. So the top tier gets a hard **randomisation floor**
  (~25% of moves chosen uniformly) and a **short memory** (last 8 rounds). We are building a teacher,
  not a champion. Worth stating in the lesson, because it's a real ethical-design idea: you can
  choose to make your AI weaker than you know how to make it.
- Bonus: [rpscontest.com](http://www.rpscontest.com/) is a ready-made playground if a student wants
  to take the prediction lesson further.

Two rules I'd hold to:

- **[HONEST] Never disguise an NPC as a real player.** No fake names in the online list, no bot in the
  chat pretending to be human. Players find out, and it retroactively poisons every real interaction —
  in a game whose entire point is meeting actual people. NPCs look like NPCs.
- **Dialogue is an i18n cost**, ×3 languages. Keep it to ~8 NPCs × 3 short lines (~72 strings). Barks,
  not conversations. Dialogue trees are a v2 idea at best.

### Fairness without a referee: commit–reveal

Simultaneous choice over a network has an obvious hole: whoever sends second sees the other's
move and wins forever. Fix it the way cryptography does:

1. Both peers pick a move, generate a random nonce, and send `SHA-256(move ‖ nonce)` — a
   **commitment**. It reveals nothing but binds you to your choice.
2. When both commitments have arrived, both peers reveal `move` + `nonce`.
3. Each side hashes the other's reveal and checks it matches the commitment. Mismatch = cheat =
   forfeit.

`crypto.subtle.digest` gives us this in ~10 lines, no dependencies. It's the most satisfying
"crypto is useful, not scary" lesson available, and it makes the *interesting* part of the game
(the mind game) genuinely honest even though position and stats are not. Nice contrast to teach:
**you can fix the cheating that matters and shrug at the cheating that doesn't.**

### Determinism & desync

Both peers compute the outcome from the same revealed inputs using the same pure function, then
exchange a hash of the resulting state. If they differ, the fight aborts with "desync." That is
distributed-systems literacy in one button press, and it's how you debug a P2P game.

### Turn shape and failure handling

- ~10 s commit timer — short, to keep it fast-paced. Timeout = you Block (never a free win for the
  waiter, never a punish for a lag spike).
- Disconnect mid-fight = forfeit after a grace period. **[HONEST]** rage-quit is unpunishable
  beyond your local record.
- v1 is 1v1 only, no spectators (spectating needs a broadcast tree — good stretch lesson).

### If it turns out too shallow — the depth dials, in the order I'd turn them

Ship the three buttons first and *play it*. Only if it gets boring, and only one at a time:

1. **A signature move**, 2 uses per fight, element-flavoured (e.g. Fire's burn deals damage over the
   next two rounds). One new button, big decision, no new systems.
2. **Feint** — a fourth action that loses to everything but baits a Block. Classic mixup depth for
   almost no code.
3. **Charge visibility** — show that the opponent is charging but not how many. Information design as
   a difficulty dial.
4. *(The rejected deck idea, if you ever want real deduction:)* finite elemental cards with publicly
   known composition and face-up discards, so players can count what's left. Genuinely deep, and a
   different game — park it.

### Stat influence — deliberately small **[DECIDE]**

Because stats are self-reported (§2.1), level should change outcomes *a little*: e.g. attack scales
`1 + level×0.02`, hard-capped at level 20. A max-level character is ~40% stronger, not 10×, so a
cheater claiming level 9999 is clamped by every honest peer's own validation and gains little.
Rule of thumb to teach: **validate incoming claims against a legal range; clamp, don't trust.**

### Progression

Win → XP → level → stat points, plus **cosmetics** as the real reward (hats, tints, a name colour).
Cosmetics are perfect here: cheatable, and nobody cares, because they're social signals rather than
power. **Wild creatures for solo play: yes, and now non-negotiable** — at ~5 concurrent players
(§2.4) most sessions are solo, so without PvE the game is an empty field. But **client-local only**:
wild encounters are simulated in your own browser, never shared. Shared world monsters would need
agreement on who hit what — i.e. authority, i.e. a server. Good lesson on scoping ambition to your
architecture. Because the local AI opponent plugs into the same `battle/rules.ts` as a human, PvE
costs us almost nothing beyond a move-picking function.

---

## 7. Dual types

Rule: at most two elements, never three. Evolution at some level lets you add a second element
(**[DECIDE]** irreversible choice, or rebindable? Irreversible = identity and consequence;
rebindable = friendlier. I lean irreversible with a "restart character" escape hatch.)

Names — you asked for something more interesting than "mud":

| Combination | Option A (plain) | Option B (with more flavour) |
|---|---|---|
| fire + water | Steam | **Scald** |
| fire + earth | Lava | **Magma** / **Cinder** |
| earth + water | Mud | **Mire** / **Quagmire** / **Silt** |

I'd go **Scald / Magma / Mire** — short, evocative, and non-obvious enough to feel authored.

Mechanics of dual typing — the interesting question is what dual *costs*, since being two things
must not be strictly better than being one:

- **Offence:** your Strike counts as *both* elements and takes the **better** multiplier, so you have
  a favourable matchup against more opponents. That's the upside, and it's plenty.
- **Defence:** incoming attacks resolve against both of your elements and multiply. Fire vs Mire
  (earth+water): fire loses to water (×0.5) and beats earth (×2) → net ×1. Neutral. Whereas fire vs
  pure earth is a clean ×2. So duals are **harder to blow out and harder to dominate with** —
  they flatten variance rather than raise power. This keeps pure types viable, which is what you
  want (a game where everyone evolves into the same thing is a game with one build).
- Full 3×6 chart lives in `data/type-chart.json` — data, not code, so balance changes are edits, not
  rewrites. That's the data-driven-design lesson.

---

## 8. The world

- Top-down tile grid, camera follows player, 16 or 32 px tiles. **[DECIDE]** 32 px is easier to
  find/make art for and easier on the eye; 16 px is more authentically retro.
- Map = JSON: a 2D array of tile indices + a collision layer. Authored by hand or with **Tiled**
  (free, exports JSON). **[DECIDE]** hand-authored tiny map for v1 (fewer moving parts in the
  lesson), Tiled later.
- **Zones: v1 ships ONE room — one connected world.** At ~5 concurrent players (§2.4), splitting the
  population is actively harmful: two people in different zones each see an empty game. Have several
  *map areas* if you want variety, but keep every player on one connection. Everything below is the
  design you'd reach for if it ever got popular — teach it as theory in A21, and in appendix X4, don't build it:
  - **one zone = one trystero room.** Only peers in your zone connect to you, so you only pay for
    connections you can see. That's **interest management**, the exact technique real MMOs use,
    arrived at from first principles.
  - If a zone exceeds the peer cap, shard it: `forest#2`. Players in different shards can't see each
    other. **[HONEST]** exactly how real MMOs handle it, and exactly as awkward.
- A tiny always-joined **lobby room** carrying `{zone}` pings, so the UI can show who's around. At
  this scale its job isn't capacity planning, it's answering "**is anyone here at all?**" — which is
  the most important question in the game (§2.4). **[DECIDE]** I'd include it in v1 for that reason
  alone; if we ship a single room, it collapses to just "N players online."

### Movement sync

- Broadcast your position ~**10 times/second**, not every frame; remote players are **interpolated**
  between the last two known positions (~100 ms behind — invisible, and it makes motion smooth).
- Send nothing while idle.
- Teaches: bandwidth vs smoothness, latency hiding, dead reckoning, and why the thing on your
  screen is always slightly in the past.

---

## 9. Chat, safety, and hostile peers

**v1 chat is preset phrases only.** You pick from a fixed list ("hello!", "good duel", "want to fight?",
"follow me", "bye"), broadcast to the room. No text field exists. Three reasons, in order of importance:

1. **The readers and players are 12-year-olds, and there is no moderation possible** — no bans, no logs,
   no reports, no server to appeal to. Preset phrases make abuse **structurally impossible** instead of
   policed after the fact. This is the same move as the templated ghost notes (§2.4), and it's what
   Nintendo and Roblox do for young players.
2. **It translates itself.** A phrase index renders in EN/JA/PT, so a Japanese kid and a Brazilian kid
   can actually communicate — something free text would never give them on a trilingual site.
3. **It's less code**: no sanitisation, no length caps, no profanity question. Fits "as small as
   possible."

The teachable idea is worth stating plainly to students, because it generalises far beyond chat: **you
can eliminate a whole class of problem by making it impossible, instead of forbidding it.** Designing
out beats policing.

**Still required, unchanged:** never trust a peer's bytes. Every inbound message is validated — known
action, expected shape, phrase index inside the table's range, per-peer rate limit; malformed → drop and
optionally auto-mute. One hostile peer must not be able to crash or spam the room. "Cheating your own
stats is fine" does **not** extend to "crashing my client is fine." This is the security lesson of the
series, in the purest available setting: **every single input is hostile.**

**Local mute list**, persisted in the save, permanent, one tap — the only enforcement mechanism that
exists without a server, and therefore the one we make sure works and teach people to use (A19).

**Privacy upside worth teaching:** no server means **no data collection**. Nothing is stored anywhere,
nothing to leak, nothing to subpoena, no cookie banner. Serverless as a *privacy* architecture, not just
a cheap one. The flip side, stated honestly in A19: nothing is stored, so nobody can check later what
was said — which is exactly why muting is the tool that works.

**Deferred to v2:** whisper/DM, free text of any kind.

---

## 10. Tech stack

### TypeScript **[DECIDED: Bun — real `.ts`, no manual build]**

The only hard fact is that browsers can't execute `.ts`, so *something* must strip the types. Bun
does it transparently in both directions, which gives you real TypeScript with no build step you
ever have to think about (verified against Bun's docs):

```bash
bun ./index.html                                  # dev server: transpiles imported .ts on the fly, hot reload
bun build ./index.html --minify --outdir=docs     # production output, run by CI on push
```

Deploy: a GitHub Action on push to `master` runs the build and publishes. Students `bun ./index.html`
locally and never run a build by hand.

Costs, so they're on the record:
- Bun becomes a prerequisite install (one `curl` line — fine, it joins Claude Code, which A01–A02 already install).
- **Deployed JS is not the source.** Source maps make debugging fine, but "view source and read the
  real code" is gone, and a broken CI build means a broken live site. Worth one lesson paragraph.
- One more moving part for a stuck student. Mitigated by the reference repo's per-lesson tags.

Alternative considered and rejected: plain `.js` + JSDoc types + `tsc --noEmit`. Genuinely zero
build and "view source is the source," but `/** @type {} */` comments are wordier and it teaches
syntax nobody uses at work. Bun's ergonomics win. (Worth keeping the *idea* in the A12 lesson as
"here's the other way, and why types are a development-time tool that never runs" — that insight is
the real lesson either way.)

Note: Node 26 (installed here) also strips types natively, but only for code it runs itself — that
doesn't help the browser. Good footnote for A12.

### Everything else

- **Styling: Basecoat via CDN.** Verified: `basecoat.cdn.min.css` is standalone — no Tailwind, no
  build. (The npm path *does* require Tailwind; we avoid it.) **[DECIDE]** pin the version in the
  URL (yes) and **[DECIDE]** vendor a copy into the repo so the game survives the CDN vanishing?
- **P2P: trystero**, loaded as an ES module. **[DECIDE]** `import` from `esm.sh` at runtime (matches
  your userscript, zero setup) vs **vendor a pinned bundle** into `vendor/`. Strong recommendation:
  **vendor it.** A CDN outage taking down every student's deployed game forever is a bad lesson;
  "pin your dependencies" is a good one.
- **No npm runtime dependencies** beyond trystero. Bun and `tsc` are dev/CI tools only.
- Rendering: hand-written canvas 2D. No engine. **[DECIDE]** confirm — a framework would hide
  exactly the mechanics we're teaching.

---

### 10.1 Libraries considered (Phaser, audio, sprite generation)

Revisited deliberately, because "write it yourself" is only the right answer when the library actually
costs more than it saves.

#### Phaser — **no for v1**, and it becomes an appendix instead

Phaser 4.2.1, MIT, healthy and enormous (npm package unpacked ~112 MB of source/types/docs; the browser
bundle is on the order of 1 MB minified). It would replace our game loop, input, tilemap, camera,
collision, sprite animation, audio, and canvas scaling.

Reasons it loses *here* — note that most of them are specific to this project, not criticisms of Phaser:

- **For our v1 it replaces roughly 150–200 lines.** A top-down grid game with one map, AABB collision
  against solid tiles, and a camera that follows the player is genuinely small. What you take on in
  exchange is Phaser's own surface: `Game`/`Scene` lifecycle, config objects, the preload/create/update
  contract, Arcade Physics bodies, and its asset loader.
- **For a 12-year-old, the framework is the bigger thing to learn.** Learning "what a game loop is" is
  one afternoon; learning "how Phaser wants you to structure a game" is several, and the payoff is
  Phaser-specific rather than transferable.
- **When it breaks, we can't teach the fix from first principles.** The answer becomes "read the Phaser
  docs," which is a different course.
- **We already cut everything Phaser is best at.** Sprite-sheet animation, tweens, particles, physics,
  multiple scenes — all v2 or gone (§6.1 of the lessons doc). Our UI and the whole battle screen are DOM
  + Basecoat, not canvas. So Phaser would be carrying ~1 MB to draw a tilemap and one blob.
- **The lessons that would disappear are the good ones.** A13–A15 are where a child learns what a frame
  is, why movement must be multiplied by elapsed time, and that a map is data. With Phaser those become
  "call this API," and the track's promise — *you understand every part* — weakens.

Where Phaser would clearly win, stated fairly: sprite animation and asset pipelines, mobile scaling and
touch, anything with real physics, and the sheer volume of tutorials and YouTube help available to a kid
who gets stuck. **If the game grows past v1 in the graphical direction, hand-rolled rendering becomes
the liability and porting is the right call.**

So: **appendix X7, "Port it to Phaser."** Build it yourself, then port it and see exactly what a
framework gives you and what it charges. That's the same move as A28 ("what a server would have bought
us") applied to frameworks — framework *literacy* without framework dependence, and it's a better lesson
than either choice alone.

#### Audio — **no library** (superseded)

This subsection previously recommended **ZzFX** (~900 bytes) plus **ZzFXM** (~1.5 kB gzipped) to
synthesise sound and music at runtime, and rejected Tone.js as too heavy. **All reversed** (§12): we load
CC0 audio files with plain `HTMLAudioElement` and add no library at all.

Kept as a record of a changed decision. The synthesis route was genuinely elegant and tiny, and it lost to
a simpler test: *what can go wrong, and can a 12-year-old fix it?* A generated song that sounds bad on one
browser is very hard to debug; an `.ogg` file that plays is either playing or not.

#### Creature sprites — **no library, and no generation at all** (superseded)

This subsection previously recommended
**[pixel-sprite-generator](https://github.com/zfedoran/pixel-sprite-generator)** (MIT) — mask →
randomise → mirror → render, patched to use our seeded PRNG. **That's been reversed** (§12): we ship a
fixed set of ~6 CC0 monsters and let the player pick one, because the name already tells players apart
and a set is far less code than any generator.

Kept here as the record of a decision we changed, since that's exactly the material A11 teaches from:
the generator was the right answer to "how do we make every player unique," and became the wrong answer
the moment we stopped needing that.

Also rejected, for completeness: DiceBear (avatar portraits, not game sprites), Robohash (external
service), and offline tools like [Lospec's generator](https://lospec.com/procedural-pixel-art-generator/)
or Deep-Fold's — those produce a fixed set of assets, which is exactly what Kenney already gives us for
free and with a matching tileset.

---

## 11. Local dev environment

```bash
curl -fsSL https://bun.com/install | bash   # once, in A10
bun ./index.html                            # dev server + TS on the fly + hot reload
bunx tsc --noEmit                           # typecheck (Bun transpiles but does not type-check)
bun test                                    # unit tests for battle/rules.ts
```

- **Bun transpiles, it does not type-check.** Types are stripped and thrown away, errors and all, so
  `tsc --noEmit` in CI is what actually enforces them. That distinction *is* lesson A12.
- Still teach why `file://` fails and a server is needed (A10) — Bun just happens to be the server.
- Add `Makefile` targets (repo convention already): `make dev`, `make check`, `make build`.
- **The two-tab dev loop is the core skill:** open `localhost:8000` twice, and you are two players.
  Teach this in the networking lesson — most students have never debugged two clients at once.
  Note the wrinkle: two tabs on the same machine still connect through real WebRTC, but both share
  a `localStorage` origin, so the second tab needs a distinct identity — one incognito window, or a
  `?id=` override for dev. Small detail, worth a paragraph in the lesson.
- Recommend `git tag g05-end`-style tags (or a branch per lesson) on the reference implementation,
  so a stuck student can `git diff` their attempt against the canonical result. **[DECIDE]** — this
  is extra maintenance for you but hugely valuable, and it's how the "Build & Verify" ethos in
  `planning/build-verify-track.md` extends to a build-along course.

---

## 12. Hosting & assets

- **Repo layout — DECIDED: separate repo** `kakkoi-online`, publishing to Pages with a `CNAME` of
  `online.kakkoi.dev`; DNS `CNAME mmo → kakkoischool.github.io`. The game is a student-forkable artifact;
  mixing it into the lesson site's Python build muddies both. Lessons stay here in `izumo-io`.
- **Lovely property worth building a lesson around:** signaling doesn't care about origin. A student
  who forks the repo and deploys to `their-name.github.io/kakkoi-online/` **can still play with
  everyone else**, because peers meet on the relay, not on your domain. Every student ships their
  own copy of the same living world. That is a genuinely delightful thing to demonstrate, and it
  falls straight out of the architecture.
### Art — DECIDED: a set of CC0 monsters, no generation

**REVERSED** (was: procedurally generated creatures from your player id, then
`pixel-sprite-generator`). Your call, and it's the right one for "as small as possible": **the name is
enough to tell people apart, so we ship a fixed set of monsters and let players pick one.**

**Assets — one coherent family, all CC0** (commercial use, no attribution required; we'll credit anyway):

- **[Tiny Creatures](https://opengameart.org/content/tiny-creatures)** — 180 sprites, **100+ monsters**
  and 50+ animals, 16×16, thick outlines. We need about 6–9 of them.
- **[Tiny Dungeon](https://kenney.nl/assets/tiny-dungeon)** — tiles, items, characters, 130+ sprites.
  Tiny Creatures is an *expansion of it*, so creatures and terrain match by construction — no
  pasted-on look, no art direction work.
- **16×16 drawn at 2× = 32 px on screen** (supersedes the earlier "32 px tiles" row): chunky pixel look,
  readable at desk distance, and 16×16 is what the assets actually are.

**Bind the element to the monster.** Each of the ~6 monsters has a fixed element, so **choosing your
monster chooses your element** — one decision instead of two, one screen instead of two, and it reads
naturally (a fire creature is a fire creature). Two or three monsters per element gives visual variety
without a matrix.

What this simplifies, beyond the obvious:

- **`creature.ts` disappears.** No mask algorithm, no seeded PRNG, no palette blending, no patched
  library, no offscreen caching per seed. Drawing a monster becomes "blit a 16×16 rect from an atlas,"
  which we already do for tiles.
- **The animation question stays solved.** Bob while walking, flip horizontally for left/right. Still no
  directional walk cycles.
- **A16 shrinks from "procedural generation" to "sprite atlases"** — a smaller lesson, and one that
  teaches something we need anyway (a sprite sheet is one image, and you draw a rectangle out of it).

What we give up, honestly:

- **[HONEST] Two players can look identical.** With ~6 monsters and up to 5 players, collisions are
  likely. Mitigation is the nameplate we already draw. If it ever bothers anyone, a per-player hue tint
  is a few lines — but that's v2, not now.
- **Appearance must now be sent over the wire**, since it's a choice rather than a derivation. It's one
  small integer in the `id` payload. Trivial, but it's a real (tiny) loss of the old design's elegance.
- The seeded-PRNG lesson is gone. The determinism idea still appears in A25, where the damage roll is
  derived from both players' nonces.

**Dropped as a result:** `pixel-sprite-generator` (adopted one turn ago, now unnecessary — reversal #5),
DiceBear, Robohash. **Pokémon assets: still never.**

### Audio — DECIDED: CC0 files, no synthesis, no library

**REVERSED** (was: procedural Web Audio, then ZzFX + ZzFXM). Your call: real files can't go subtly wrong
the way a synth can, and there is no "it sounds bad on this browser" failure mode. Reversal #6.

**Sound effects — [Kenney](https://kenney.nl/assets/category:Audio), CC0** (commercial use, no
attribution required; we credit anyway):

- **[RPG Audio](https://kenney.nl/assets/rpg-audio)** (~50 sounds) — hits, blocks, footsteps, doors.
- **[UI Audio](https://kenney.nl/assets/ui-audio)** (~50 sounds) — clicks, confirms, errors.
- **[Music Jingles](https://kenney.nl/assets/music-jingles)** (~85) — short stingers for "you won" /
  "you levelled". Same author as the SFX, so they sit together.

We need maybe 8 sounds total: step, strike, block, charge, duel start, win, lose, chat ping.

**Background music — CC0 chiptune loops from OpenGameArt.** **[HONEST] correction:** Kenney has *no*
background-music pack — only the short jingles above. So the loops come from elsewhere:

- **[5 Chiptunes (Action)](https://opengameart.org/content/5-chiptunes-action)** by Juhani Junkala — CC0,
  and **all five are seamless loops**, which is the property that actually matters.
- Alternatives in the same licence: [4 Chiptunes (Adventure)](https://opengameart.org/content/4-chiptunes-adventure),
  [CC0 Chiptune Music](https://opengameart.org/content/cc0-chiptune-music).
- We need **two**: one calm for the world, one faster for duels.

**No audio library.** Plain `HTMLAudioElement` — `new Audio(src)`, `loop = true`, `play()`. Browsers block
autoplay until the user interacts, and **our first-join dialog already is that interaction**, so the
policy costs us nothing. [howler.js](https://howlerjs.com/) (~9 kB gzip) stays on the shelf in case
mobile playback quirks bite; we don't add it speculatively.

**[HONEST] Harmonisation is the one real risk.** Kenney's SFX and Junkala's chiptunes are different
authors, so they can clash — a realistic recorded thud over 8-bit music sounds wrong. Two mitigations,
in order: pick the more retro/synthetic sounds from RPG Audio, and if it still clashes, take chiptune-style
SFX from the same CC0 chiptune sources. **This is an ear check, not a code problem** — one of the few
things in this project that must be judged by listening rather than tested.

**Mix and weight:** normalise the files, master gain roughly 0.3 for music and 0.6 for effects; one
1–2 minute loop as `.ogg` with an `.mp3` fallback is ~1–2 MB, lazy-loaded after first paint so it never
delays the game appearing.

**Default: OFF, with one obvious toggle** (persisted in the save). Not because the music is bad — it's
composed and good — but because **ten students in one classroom all unmuting at once is chaos**, and your
weekly lesson is exactly that room. A student can turn it on deliberately.

**Dropped as a result:** ZzFX, ZzFXM, Tone.js, `audio.ts`-as-synthesiser. Audio is now **~30 lines and in
v1**, not an appendix — files are so much simpler than synthesis that the whole appendix stopped being
necessary.

---

## 13. Scope ladder — ship in this order

| Milestone | Contents | Playable? |
|---|---|---|
| **M0 Walkabout** | canvas, tile map, movement, collision, save, name tag | solo |
| **M1 Together** | trystero room, presence, position sync, name tags over peers | yes — this is the wow moment |
| **M2 Talk** | chat, mute, validation, rate limits | yes |
| **M3 Duel** | challenge/accept, turn FSM, commit–reveal, type chart, damage — **plus the local AI opponent** | yes — the game exists |
| **M4 Depth** | decks, intents (Strike/Charge/Guard), XP, levels, wild encounters in the world | yes, **and worth opening alone** |
| **M5 Identity** | dual types, evolution, cosmetics | yes |
| **M6 Presence** | players-online indicator, "you're alone here" state, **[DECIDE]** ghost/chalkboard messages | yes |
| **M7 Polish** | keypair identity, save export/import, mobile/touch, sfx | yes |

M1 is deliberately early: "I can see another human being move" is the moment that makes a student
finish the course. Keeping it early also means networking questions get answered while the codebase
is still tiny. **[DECIDE]** does that ordering feel right, or do you want a complete single-player
game before any networking? Note the ~5-player reality (§2.4) argues both ways: multiplayer is the
*point*, but solo play is what most sessions will actually be — M3/M4 shipping the local opponent is
how we serve both. Zone sharding is gone from the ladder entirely; it's theory now, not work.

---

## 14. The lesson series

**Superseded — see `kakkoi-online-lessons.md`.** This section previously carried a G-numbered draft
lesson list; keeping two lesson lists in two documents guarantees they drift, so it's gone rather than
updated. What survives here is the summary:

- The track is **A09–A29** (21 lessons), continuing the **existing AI track** — not a new track. No
  build changes needed: `content/ai/*.md` is a flat list sorted by id.
- The install lesson already exists as **A01/A02**.
- **A09** gets the tools and a GitHub account; **A10 deploys a live URL in week two**; **A11** plans.
- **A19 "Playing with strangers"** is the safety lesson, placed before the first peer connection.
- **Age limits are real and stated plainly in A09:** GitHub is 13+, Claude is 18+, so an adult owns the
  accounts and under-13s publish through a class organisation. Local play needs no account at all.
- Every lesson: one CS idea, a physical analogy, why-we-chose-it, what-we-rejected, an example prompt
  plus what to verify, an observable two-tab test, and one "your turn" extension the prompt doesn't
  produce.
- **Written so a 12-year-old understands every sentence** — the deep idea stays, the gatekeeping
  vocabulary goes, and each lesson ends by naming the real term.
- Lessons are written **after** the matching code works, from real AI failures collected during the
  build.

---

## 15. Decision log — every question answered

All defaults are now **set**, per your instruction. Inline `[DECIDE]` markers earlier in this doc are
superseded by this table. Each row is a default, not a commitment — overturn any of them and I'll
propagate the consequences.

| # | Question | Default | Why |
|---|---|---|---|
| 1 | TypeScript | **Bun**: real `.ts`, `bun ./index.html` in dev, CI builds on push | your call, and it works; §10 |
| 2 | Repo | **Separate `kakkoi-online`** + `CNAME online.kakkoi.dev` | student-forkable; keeps the Python site build clean |
| 3 | Dependencies | **Vendor** trystero + Basecoat, pinned, in-repo | a CDN outage must not brick every student's deployed game |
| 4 | Creature art | **A fixed set of ~6 CC0 monsters (Kenney Tiny Creatures); player picks one** | the name is enough for identity; deletes the whole generation module (§12) |
| 5 | Environment art | **Kenney Tiny Dungeon** (CC0), vendored — same family as Tiny Creatures | creatures and terrain match by construction |
| 6 | Audio | **CC0 files: Kenney SFX/jingles + OpenGameArt CC0 chiptune loops. No synthesis, no library.** Off by default | files can't go subtly wrong; default-off because a classroom of unmuted laptops is chaos (§12) |
| 7 | Combat | **Strike / Block / Charge**, element = static multiplier, commit–reveal | proven, fast, 3 buttons, ~30 lines |
| 8 | Combat depth | ship bare, then dials in order: signature move → feint → charge visibility | play it before adding to it |
| 9 | Dual-type names | **Scald / Magma / Mire** | short, evocative, authored-sounding |
| 10 | Evolution | **Irreversible**, with a "restart character" escape hatch | consequence matters; escape hatch removes the cruelty |
| 11 | Stat influence | **Capped at ~+40% total**, clamp all incoming claims | cheating is allowed, so numbers must not decide fights |
| 12 | PvE | **Yes, client-local wild creatures**, same rules module as PvP | most sessions are solo at 5 players |
| 13 | Async presence | **Yes — ghost/chalkboard notes**, M6 | cheapest fix for the empty world |
| 14 | Signaling | **Nostr**, isolated behind one module | matches your userscript; swapping is a lesson exercise |
| 15 | TURN | **Accept the ~10% who can't connect**; clear diagnostic UI; Cloudflare TURN as an appendix | free forever beats universal |
| 16 | Keypair identity | **Not in v1** — appendix X1 | the *diff* is the teaching moment |
| 17 | Players-online | **Yes, v1** | answers the game's most important question: is anyone here |
| 18 | Whisper/DM | **Yes, v1** | trivial in trystero, teaches unicast vs broadcast |
| 19 | Tile size | **16×16 assets, drawn at 2× (32 px on screen)** | matches what the CC0 packs actually are |
| 20 | Zones | **One room in v1**; sharding is theory only | splitting 5 players is self-harm |
| 21 | Chat safety | **Notice on first join + local mute + rate limit + length cap**; chat locked until a name is set | minors arrive from school.kakkoi.dev |
| 22 | Lessons | **21: A09–A29**, inside the existing AI track | superseded row 34; small lessons, small game (§6.1 of the lessons doc) |
| 23 | Reference repo | **Per-lesson git tags** (`g05-end`) | a stuck student can diff against canonical |
| 24 | Track prefix | **G**, page `game-lessons.html` | reads cleanly against T / R / A |
| 25 | Milestones | **M0 solo → M1 multiplayer early**, PvE by M4 | seeing another human move is what makes students finish |
| 26 | Delivery | **Self-serve pages + one lesson taught per week in class** — the class *is* the play window | solves the empty-world problem with no scheduling machinery; students may run ahead alone (lessons doc §13) |
| 27 | Name | **Kakkoi Online** / repo `kakkoi-online` / URL `online.kakkoi.dev` | your call; `-online` is the honest genre signal that `-mmo` overclaims |
| 28 | Block payoff | **A successful Block banks a charge** | Yomi: every win must pay in a *different currency*; a Block paying nothing collapses the triangle (§6.1) |
| 29 | Damage variance | **0.9–1.0 roll seeded from XOR of both reveal nonces** | Pokémon-style texture, zero determinism cost, ~5 lines — a commit–reveal randomness beacon |
| 30 | NPCs | **Yes — trainers, tutor, townsfolk, board keeper, rest point**; client-local | attacks the empty-world risk at zero networking cost, gives a difficulty ladder, and earns the polymorphism lesson |
| 31 | NPC honesty | **NPCs never impersonate players** — distinct nameplates, absent from the online list | faking human presence poisons the real thing in a game about meeting people |
| 32 | Ghost notes | **Templated phrases, not free text** + appraisal taps + no mechanical effect | Dark Souls' answer: moderation-by-construction *and* automatic translation across en/ja/pt (§2.4) |
| 33 | AI difficulty | **Ladder = prediction depth** (random → frequency → history → one meta layer), with a 25% random floor and 8-round memory | Iocaine Powder shows an uncapped predictor beats humans; we're building a teacher, not a champion (§6.2) |
| 33b | Assistant | **`agy` (Antigravity CLI), free** — as A01/A02 already install. Claude Code optional | leaves GitHub's 13+ as the only account rule, and costs students nothing |
| 33c | Student repos | **Empty repo each + `reference` remote with per-lesson tags** — no forking | a fork hands over the finished game; the tags still give the diff-when-stuck path |
| 34 | Lesson track | **Continues the AI track as A09–A29** (21 lessons) — zero build changes. A09 sets up tools + GitHub account, A10 goes live | see `kakkoi-online-lessons.md` |
| 35 | Reading level | **A 12-year-old must understand every sentence** | outranks completeness; also makes JA/PT translation far better |
| 36 | v1 scope | **Cut levels/XP, dual types, cosmetics, audio, wild creatures, ghost notes, whisper, zones, keypairs, simulator** | "as small as possible"; each cut shortens every lesson (lessons doc §6.1) |
| 37 | Chat | **Preset phrases only in v1 — no free text at all, not even as a setting** | readers are children and there is no moderation, no bans, no logs; presets also translate themselves, and it's less code (lessons doc §3.6) |
| 37b | Safety | **A19 "Playing with strangers"** — a lesson placed *before* the first connection, and an in-game safety card on first join | the same words must reach players who never read the lessons |
| 38 | Screenshots | **One per lesson, English only, captured from the reference build** | no videos; reused across all three languages |
| 39b | Game theory content | **Two short sidebars inside A26 and A27. No R-track essay** | the R track is Cyril's own voice; a borrowed game-theory essay would be pretending to be that. Sidebars also reach a 12-year-old better — 90 words attached to a thing they just built (lessons doc §6.2) |
| 40 | Phaser | **No for v1** — replaces ~150–200 lines of ours with a ~1 MB bundle and a bigger API to learn; deletes the best lessons (A13–A15). **Appendix X7 ports to it instead** | §10.1 |
| 41 | Audio lib | ~~ZzFX + ZzFXM~~ **None — plain `Audio` elements** | reversal #6: generation was clever but riskier and no smaller in practice than loading files |
| 42 | Sprite lib | ~~`pixel-sprite-generator`~~ **Dropped — no generation at all** | set monsters instead; element is bound to the monster you pick |
| 39 | Owner presence | **The canonical world at `online.kakkoi.dev` is the showcase**; you log in and students see it working | inspiration is the point; note that without keypairs (X1) your name is impersonable |

---

## 16. Things you didn't mention that I think matter

- **The empty-room problem.** Promoted to §2.4 — with ~5 concurrent players this is *the* defining
  constraint, not a footnote. It is a product problem architecture cannot fix.
- **Mobile.** Half your students will open it on a phone. Touch controls (a virtual d-pad) and a
  canvas that scales are M7, but the *layout* should not assume a keyboard from day one.
- **Accessibility.** Basecoat gives us accessible DOM components for free; canvas gives us nothing.
  At minimum: keyboard-navigable UI, don't encode meaning in colour alone (the type triangle needs
  icons, not just red/blue/brown), respect `prefers-reduced-motion`.
- **Bandwidth on mobile data.** At 10 Hz × 4 peers this is a rounding error, so it's no longer a
  real concern — but a "low bandwidth" toggle dropping to 5 Hz is two lines and a good lesson about
  caring, so it's worth a mention rather than an implementation.
- **Don't build for success you don't expect.** Earlier drafts of this doc had sharding in the
  milestone ladder. At ~5 players that's speculative engineering — the exact failure mode the course
  should be teaching students to avoid. Sharding stays in the lessons as *theory*, with the honest
  framing: "here's what we'd do, here's why we didn't, here's how we knew not to." That's a better
  lesson than the code would have been.
- **Your own maintenance cost.** Trilingual ×22 lessons plus a reference implementation is a
  serious body of work. The translation pipeline exists, but the reference game needs to keep
  working as browsers change. Recommend pinning everything and adding one smoke test.
