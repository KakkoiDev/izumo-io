# Kakkoi Online — lesson series specification

Third document in the set:

- `kakkoi-online-design.md` — design rationale + decision log (*why*)
- `kakkoi-online-trd.md` — technical requirements (*what to build*)
- `kakkoi-online-sources.md` — every asset pack, library, blog, and game referenced, with licences
- **this file** — the lesson series (*how it gets taught*)

Nothing is implemented, by design: **we write code only once the game exists in these documents.**
See §10 for the build/iterate process that follows.

---

## 1. What this track is

The **second half of the AI track** on school.kakkoi.dev (A09–A29): having learned to use an AI
assistant in A01–A08, the student now builds one real thing with it — a deployed, multiplayer,
serverless game at their own URL — understanding each computer-science idea underneath it.

**Delivery — DECIDED: self-serve, and you teach one lesson per week in class** (see §13 for what that
implies). Nothing is gated: a student who wants to run ahead alone can.

**Audience — DECIDED: a 12-year-old must be able to read and follow it.** Trilingual (EN/JA/PT),
light workload (~3–5 hrs/week). This is the strictest constraint in the whole project and it outranks
completeness: if a sentence can't be understood by a bright 12-year-old, it gets rewritten or cut. See
§3.5 for the writing standard, and §3.6 for the safety consequences — which are not optional.

**Prerequisites.** A01–A08 (the agent is installed and they can drive it), plus T10–T14 (JS, DOM,
persistence) and T19 (git). Stated at the top of A09, not enforced. **A09 re-checks the tooling** and adds
the GitHub account, so a student arriving cold has one clear place to start.

**[OPEN] The 12-year-old tension.** T10–T14 is a real prerequisite for *understanding*, and a 12-year-old
probably hasn't done it. Two ways out, and I lean hard on the first:
- **Explain in place, briefly, every time.** When a lesson uses an array or a function, one plain
  sentence reminds them what it is. Costs a few lines per lesson; makes the track self-contained.
- Gate the track behind T10–T14. Cleaner for us, and it turns away exactly the reader you asked for.

**A practical note:** Claude Code needs a paid subscription and a computer they can install software on.
For a 12-year-old that means a parent is involved. A01 should say so plainly.

**The promise:** "you will ship a real multiplayer game and be able to explain how every part works."
**Not promised:** a job, a portfolio guarantee, or that AI wrote it all for you. Under-promise, per
your existing philosophy.

**Why this project is a good teaching vehicle** — it's not an arbitrary choice:

- Multiplayer forces **distributed-systems reality** (latency, trust, consistency) which single-player
  CRUD apps never surface.
- No server means **no black box**: every mechanism is visible in the student's own code.
- The constraints are honest and *felt*, not asserted — the student personally experiences NAT
  failure, desync, and hostile input.
- It's **fun to show people**, which is what makes a student finish an 18-lesson track.

---

## 2. How it differs from the existing tracks

| Track | Shape |
|---|---|
| T (tech) | one concept per lesson, small isolated examples |
| R (theory) | essays, no code |
| A01–A08 (AI) | how to use AI tooling |
| **A09–A29 (this one)** | **one continuous artefact**, built across every lesson; each lesson adds a working feature to the same repo |

The difference that matters: **lesson N+1 depends on lesson N's code existing.** That creates two
obligations we must design for — a reference repo with per-lesson tags (§8), and a "if you're joining
here, start from this tag" line at the top of every lesson. It is also why lessons stay small: a
student must be able to hold the whole codebase in their head at every step, not just the diff.

---

## 3. Pedagogical principles

1. **One CS idea per lesson.** Never two. If a lesson needs two, it's two lessons.
2. **The idea comes with a physical analogy**, matching how `content/phases.yaml` already works
   (workbench, time machine, kitchen).
3. **Every lesson ships something runnable.** No lesson ends with "we'll wire this up next time."
4. **Alternatives are mandatory content.** Every lesson names 2–3 rejected approaches and what each
   would have cost. This is the section that separates an engineer from a prompt typist, and it is
   the reason a student can later make decisions we never taught them.
5. **The prompt is a specimen, not a script.** We give a full example prompt *and* what to verify in
   the output. Students who paste blindly will hit the verification step and fail it.
6. **AI failure is curriculum.** Every third lesson includes a real "here's what the agent produced
   that was subtly wrong, and how I caught it" — this is `build-verify-track.md`'s ethos applied.
   These must be **real** failures collected while building the reference implementation (§10), not
   invented ones.
7. **Verification is observable.** Every lesson ends with a two-tab test whose result you can see,
   not "it should work now."
8. **Honesty about limits is content, not a caveat.** The NAT lesson, the "no moderation is possible"
   lesson, and the closing "what a server would have bought us" are among the most valuable in the
   track.

---

## 3.5 Writing standard: a 12-year-old must understand it

Rules, applied to every sentence of every lesson. These also make the Japanese and Portuguese
translations dramatically better, because simple direct sentences survive translation and idioms do not.

1. **Short sentences.** One idea each. If there's an "and" joining two thoughts, make two sentences.
2. **Every new word gets defined the first time, in plain language, in the same sentence.** Not in a
   glossary the reader won't open.
3. **Concrete before abstract, always.** Show the thing happening, then name it. Never open a lesson
   with a definition.
4. **No idioms, no sarcasm, no cultural references.** "Yak-shaving," "the elephant in the room," sports
   metaphors — all out. They confuse 12-year-olds and they break translation.
5. **Active voice, second person.** "You send your position ten times a second," not "positions are
   broadcast at 10 Hz."
6. **Numbers with meaning attached.** "10 times a second — about as often as you blink," not "10 Hz."
7. **Pictures beat paragraphs.** A mermaid diagram or the lesson's screenshot instead of a description
   of what the screen looks like.
8. **Name the feeling.** "This part is confusing for everyone the first time" keeps a 12-year-old from
   concluding they're stupid and quitting. This matters more than any technical accuracy.
9. **Keep the deep idea; drop the vocabulary.** We do not water down the computer science. We stop using
   the words that gatekeep it — and then, at the end of the lesson, we name it: *"grown-up programmers
   call this X, so now you know that word too."* That last move is what makes a kid feel let in.

**The translation table.** Same ideas, different words. The right column is what goes in the lesson; the
left column appears once, at the end, as "the real name for this."

| The real name | How the lesson says it |
|---|---|
| Sprite atlas / texture atlas | "All the pictures live in one big image. You tell the computer which little square to copy out" |
| Fixed timestep game loop | "The game does its thinking a set number of times a second, so it works the same on a fast or slow computer" |
| O(n²) full mesh | "Everybody has a phone line to everybody else. Add one person, and *everyone* needs a new line. That gets out of hand fast" |
| NAT / STUN / TURN | "Your home router hides your computer from the internet, like a flat with no letterbox. STUN is asking a friend 'what's my address?' TURN is paying someone to carry your post" |
| Interpolation / dead reckoning | "You show other players a tiny bit in the past — about a blink — so their movement looks smooth instead of jumpy" |
| Commit–reveal hashing | "You both write your move on paper, fold it, put it down, *then* unfold. Nobody can peek and change their mind" |
| Mixed strategy equilibrium | "If you always pick the same move, people learn it and beat you. So the good players mix it up on purpose" |
| Schema versioning / migration | "Your save file has a version number, so when we change the game, old save files still work" |
| Polymorphism | "The fight code doesn't know or care whether it's fighting a person or the computer. Both answer the same questions" |
| Untrusted input validation | "Never believe what another computer tells you. Check it first, every single time" |
| Deterministic result from a seed | "The same starting number always gives the same answer — like a recipe" |

**Length target:** 800–1,200 words per lesson, one screenshot, one diagram where it helps. A lesson that
runs long is a lesson that should be two lessons.

## 3.6 Safety, because the readers are children

A 12-year-old audience changes the riskiest part of this project, and the change is not optional.

**Free-text chat with strangers, in a game with no server and therefore no moderation, no bans, no
logs, and no reports, aimed at 12-year-olds, is not something we should ship as the default.** I
recommended local mute and a notice earlier; that was calibrated for an older audience.

**Recommendation: preset-phrase chat by default.** The same trick as the ghost notes (design §2.4): you
pick from a fixed list of phrases ("hello!", "good duel", "want to fight?", "follow me", "bye"). This is
what Nintendo and Roblox do for young players, and it gives us three things at once:

- **Abuse becomes structurally impossible** rather than moderated after the fact. There is nothing to
  moderate, because there is nothing arbitrary to say.
- **It translates itself.** A phrase index renders in EN/JA/PT, so a Japanese kid and a Brazilian kid
  can actually talk to each other. Free text would never give them that.
- **It's a smaller lesson.** No text sanitisation, no length caps, no profanity questions — the
  networking idea (send a message, validate it, show it) stays intact with less code.

Free text becomes a **setting the player turns on**, with the honest warning attached. The validation
lesson (A23) is unchanged and still teaches "never trust what another computer sends you" — that lesson
is about hostile *data*, not rude words.

**DECIDED, both:**
- **v1 is preset-only. There is no free-text chat at all** — not even as a setting. Less code, nothing
  to sanitise, no length caps, no profanity question, and no way for an adult stranger to say anything
  arbitrary to a child. Free text, if it ever arrives, is a v2 decision made with fresh eyes.
- **The safety page is a lesson: A19 "Playing with strangers"**, placed deliberately *before* A20, the
  lesson where the student first connects to another human. It's also the in-game safety card shown on
  first join, so the same words reach players who never read the lessons.

---

## 4. The lesson template

Every lesson, same seven beats, same order. Frontmatter matches what `content/ai/*.md` actually uses —
**`id` / `title` / `desc` only**, no `phase`, no `status` (verified against `a01.md`).

```markdown
---
id: "A15"
title: "The Map"
desc: "Grids as data, AABB collision, and why the map is JSON instead of code."
---
# A15: The Map

[Intro: what the game can't do yet, and what it will do by the end.]
{: .lesson-intro }

## Where we are
Start from tag `a14-end`. Screenshot: before → after.

## The idea: a grid is a data structure
[ONE concept. Physical analogy. A mermaid diagram where it helps.]

## Why we chose this
[The constraint that forced it.]

## What we could have done instead
| Alternative | Cost |
|---|---|
| ... | ... |

## The prompt
[A full example prompt to the agent.]
**Check the output for:** [3 specific things — the failure modes we actually hit.]

## Verify it works
1. `bun ./index.html`
2. [Observable check. Two tabs where relevant.]
3. `bunx tsc --noEmit && bun test`

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul><li>...</li></ul>
</div>

## Your turn
[One small extension the prompt above does NOT produce.]
```

**"Your turn" is deliberate.** If a student only runs our prompt, they've watched a video. The
extension must be something the given prompt does *not* produce.

---

## 5. Track integration — it's the AI track, continued (A09+)

**DECIDED: this is not a new track.** It continues the existing AI lessons as **A09 onwards**, framed
as "use an AI chatbot to build an online multiplayer game." Verified against the codebase, this costs
**zero build work**:

- `content/ai/*.md` is a **flat list with no `phase` field**, sorted by id number
  (`content_loader.py:172`). Dropping `a09.md` in makes it appear. No loader change, no `build.py`
  change, no `phases.yaml` entry, no new nav item, no new page.
- `scripts/translate_content.py` already covers `content/ai/`.
- Only real edit: a line in `content/ui.yaml` describing the AI track's new second half, ×3
  languages, plus a **"Play the game"** link to `online.kakkoi.dev`.

Two happy consequences of living inside the AI track:

- **We don't rewrite the install.** A01/A02 already cover installing the assistant and the risk rules,
  translated and shipped. **A09 links to them** and adds only what's new and specific to shipping a
  game: a **GitHub account**, `gh` signed in, and an empty repo ready for A10 to deploy from. If a
  student came through A01–A08 they'll finish A09 in minutes; if they arrive cold, A09 is where they're
  sent back.
- The framing is honest: this *is* an AI-lessons capstone. A08 is currently "Capstone: your AI
  toolkit"; A09+ becomes "now build something real with it."

**Screenshots — DECIDED, no videos.** One screenshot per lesson, captured from the running reference
build during §10's loop, stored in `website/static/img/game/aNN.png`. Captured in **English only** (§9)
so translations reuse the same images. No screencasts, no per-language image work.

---

## 6. The definitive lesson list — 21 lessons, A09–A29

Two constraints from you shape this list: **each lesson stays small enough to read and understand in
one sitting**, and **the game itself stays as small as possible**. So the list is *not* shortened by
merging lessons — it's shortened by **cutting game features** (§6.1). Small lessons, small game.

Milestone column refers to TRD §9.

### Getting ready (A09–A12)

| # | Title | The one idea | Builds | M |
|---|---|---|---|---|
| A09 | Get your tools | **The two accounts a programmer needs**: the assistant, and somewhere to put your work | Claude Code working, GitHub account, empty repo | — |
| A10 | Ship an empty page | HTTP vs `file://`, origins, secure contexts, **deploy in week two** | Bun dev server + **your live URL, working** | — |
| A11 | Plan before you prompt | Requirements vs implementation; **a spec is what makes an agent useful** | your own `DESIGN.md`, committed | — |
| A12 | Types that never run | Static vs dynamic typing; **something has to strip the types** | `tsc --noEmit` in CI, first typed module | — |

Shipping in A10 rather than at the end is deliberate: the student has a public URL from lesson two,
every later lesson redeploys, and the scariest step (does it work outside my laptop?) is answered
while the code is 20 lines long instead of 2,000.

### A world (A13–A17)

| # | Title | The one idea | Builds | M |
|---|---|---|---|---|
| A13 | The game loop | Fixed timestep; **why frame-rate-dependent movement breaks** | 60 Hz loop, delta time | M0 |
| A14 | Moving around | Event-driven vs polling; input state | walking with held keys | M0 |
| A15 | The map | A grid is a data structure; AABB collision; **data-driven design** | JSON tilemap, camera, walls | M0 |
| A16 | Pick your monster | **A sprite sheet is one image you draw rectangles out of** | the ~6 CC0 monsters, a picker, your monster on screen | M0 |
| A17 | Remembering you | Serialisation; **schema versioning** | localStorage save, `v` field | M0 |

### Other people (A18–A24)

| # | Title | The one idea | Builds | M |
|---|---|---|---|---|
| A18 | Who are you? | **Identification vs authentication** | name + element, persisted id | M1 |
| A19 | Playing with strangers | **Nobody is in charge here** — what other people can and cannot see, and what to do if someone is unkind | the in-game safety card, shown on first join | M1 |
| A20 | Two browsers, one wire | NAT, STUN/TURN, signaling vs data plane; **"serverless" is a half-truth** | first real peer connection | M1 |
| A21 | Seeing each other | Full mesh is **O(n²)**; join/leave; eventual consistency | other players visible, online count | M1 |
| A22 | Moving together | Tick rate, **interpolation**; latency hiding | smooth remote players at 10 Hz | M1 |
| A23 | Chat, and hostile input | **Every input is hostile**: schemas, clamps, rate limits, mute | working chat | M2 |

A21 is the payoff lesson of the whole track — the first time a student sees another human being move
on their own screen, in their own code, with no server. Everything before it is setup and everything
after it is depth.

### The duel (A24–A27)

| # | Title | The one idea | Builds | M |
|---|---|---|---|---|
| A24 | A fight is a state machine | FSM; **pure functions vs I/O** | invite/accept, turn phases | M3 |
| A25 | Fair play with no referee | **Commit–reveal hashing**, WebCrypto; classes of cheating | honest simultaneous moves | M3 |
| A26 | Three buttons | Game theory: **if playing randomly is optimal, there's no game** | Strike/Block/Charge + type triangle | M3 |
| A27 | Someone to fight | **Polymorphism earned**: the battle can't tell human from AI | NPC trainer + townsfolk | M3.5 |

### Sound and reflect (A28–A29)

| # | Title | The one idea | Builds | M |
|---|---|---|---|---|
| A28 | Sound | **Loading a file is not the same as playing it** — browsers refuse to play audio until you interact with the page | 8 CC0 effects + two music loops, muted by default | M4 |

| # | Title | The one idea |
|---|---|---|
| A29 | What we didn't build | Authority, persistence, moderation, matchmaking — what a server buys, what it costs, and **why we cut features on purpose** |

A29 is the honest close, and it doubles as the design lesson: every item in §6.1's cut list is an
example of scoping to what you can actually finish.

**Appendix X7 is the same move applied to tools.** Having hand-written the loop, input, map, and camera,
the student ports the game to Phaser and measures both sides: how much code disappeared, how much bundle
size arrived, and what they can no longer explain. Framework literacy without framework dependence — and
it only works *because* they built it themselves first. If we had started with Phaser, this lesson would
be impossible.

### Appendices (English only, written if wanted)

| # | Title |
|---|---|
| X1 | Keypair identity — signatures, so nobody can impersonate you |
| X2 | When P2P won't connect — TURN and the ~10% |
| X3 | Phones — touch controls |
| X4 | If 500 people showed up — sharding we chose not to build |

| X6 | Balance as a test — the 1,000-duel simulator |
| X7 | **Port it to Phaser** — rebuild what you wrote using a real game framework, and measure what you gained and lost |

## 6.2 Game theory: sidebars inside the lessons, not an R essay

**REVERSED (was: a standalone R22 essay).** The R track is *your* voice — life lessons you actually
hold. Borrowed game theory dressed as one of those would be pretending, and a reader who knows the rest
of the R track would feel the difference. So the material goes where it's earned: **short sidebars inside
the lessons that use it.**

This is also better for a 12-year-old. The idea arrives attached to a thing they just built, in 80 words,
rather than as an essay they must hold in their head and apply later.

**Mechanism — no new CSS needed.** `.lesson blockquote` already exists in `website/static/style.css:648`
(accent left border, muted italic), so a markdown `>` block renders as a sidebar today. **[OPEN]** if you
want a titled box instead, adding a `.sidebar` rule mirroring `.takeaways` (`style.css:656`) is about five
lines of CSS — worth it only if we end up with many sidebars.

### Where each piece lands

**A26 "Three buttons" — the main sidebar (~90 words).** Placed right after the three actions are
explained:

> **Why three buttons and not one?**
> Play rock-paper-scissors with a friend. After ten rounds they win almost every time — not because they
> are lucky, but because they noticed you keep picking rock. Having a favourite makes you predictable,
> and being predictable is the only way to lose a fair game. So the best players have no pattern at all.
> That is hard: people are bad at being random. It is also why our Block does not just save you, it
> *earns* you a charge — three options that all did the same thing would give you nothing to think about.
> Grown-ups call this a **mixed strategy**.

**A27 "Someone to fight" — a second sidebar (~70 words),** where the NPC prediction tiers are introduced:

> **The computer is watching your habits**
> The tougher trainers keep a list of what you have done and bet on your favourite. Programs like this
> once won a famous rock-paper-scissors competition, because computers spot patterns far better than
> people hide them. And if it can guess you, you can guess its guess — Japanese has a word for
> reading-the-other-person: **yomi**. We deliberately made the toughest trainer play randomly a quarter
> of the time, so it stays beatable. You can choose to make your program weaker than you know how.

**A11 "Plan before you prompt"** already carries the design half of this — the Block-pays-nothing reversal
is one of its worked examples of changing your mind for a reason.

**Cut entirely:** penalty kicks, poker, negotiation, Nash equilibrium, imperfect information. Those were
the essay's reason to exist, and without the essay they are padding. The two sidebars keep everything
that changes how the student understands *their own game*, which is the only claim the lessons need.

## 6.1 What v1 does NOT include (and why that's the point)

Cut, per "as small as possible." Each is a fine v2 or appendix, and each removal makes every lesson
shorter:

| Cut | Why it's safe to cut |
|---|---|
| **Levels & XP** | Also removes the level term from the damage formula and the stat-clamping logic. A local win/loss counter is enough |
| **Dual types / evolution** | v1 is one element per creature. The type triangle still works completely |
| **Cosmetics & per-player tints** | The name tag already tells people apart |
| **Procedural creature generation** | Reversed on purpose: a set of ~6 CC0 monsters is smaller, matches the tiles, and the name carries identity |

| **Wild encounters** | The NPC trainer already gives you something to fight |
| **Ghost notes** | → v2. NPCs already make the world feel inhabited |
| **Whisper/DM, low-bandwidth mode** | Broadcast chat is enough at 5 players |
| **Zones, sharding** | One room, one map → X4 |
| **Keypair identity** | → X1 |
| **Balance simulator** | → X6. Ship the mechanics, fix them from play |

**Consequence for the damage formula** (TRD §3): with levels gone it becomes
`base × element × charge × action × roll`, clamped to 50% of max HP. Fewer moving parts, same triangle.

**And explicitly accepted:** we are not gating on "is it still fun after 20 duels." Per your call —
**the game existing and working is the success.** Mechanics are data in `tuning.json`; they get fixed
from real play later, and that fixing is itself lesson material.

## 7. Per-lesson detail: what "written down" means

Each lesson gets a detail sheet before it is written. Template, then the first three filled in as
specimens; the rest get filled during §10's build loop, because the real AI failure modes and the real
verification steps can only be collected by actually building it.

```
ID / title / prerequisite tag
Goal (one sentence, student-facing)
CS idea + analogy
Builds (files touched, feature added)
Why this solution (the forcing constraint)
Alternatives + cost (2–3)
Example prompt (full text)
Verify (observable steps)
Common AI failure to catch (collected during the build)
Takeaways (3–5)
Your turn (extension)
Time estimate
```

### A09 — Get your tools

- **Goal:** the assistant works, you have a GitHub account, and you have an empty repo. Nothing else.
- **Idea:** **a programmer needs two things — something that helps you write, and somewhere to keep your
  work.** The second one is what lets other people see it. (Analogy: a workshop and a shop window.)
- **Builds:** Claude Code installed and signed in (linking to A01/A02, not repeating them), a GitHub
  account, `gh auth login`, `git config` name and email, and an empty `kakkoi-online` repo — public,
  with Pages ready to switch on next lesson.
- **Why an empty repo now:** so A10 can deploy in the same sitting it starts. The student sees their own
  URL in week two, which is the thing that makes them come back for week three.
- **Alternatives:** deploy at the end (the usual course shape — and the reason so many students never
  see their work live); zip files by email (no history, no URL); a paid host (money, and unnecessary).
- **Verify:** `claude` runs and answers; `gh repo view` shows your repo; the repo page loads in a browser.
- **Your turn:** write one sentence in your repo's README saying what you're about to build.

#### ⚠️ Age limits — this must be stated plainly, not buried

I checked the terms rather than guessing, and they matter for a 12-year-old audience:

- **GitHub requires you to be 13 or older.** ToS §B.3: *"You must be age 13 or older."*
- **Claude requires 18 or older** (or your local minimum consent age, whichever is higher) per
  Anthropic's consumer terms.

So a 12-year-old **cannot** hold either account themselves. Pretending otherwise would be teaching kids
to lie about their age in lesson one, which is not a thing this course should do. The honest structure:

- **The adult owns the accounts.** In class, that's your Claude subscription on the machines the students
  use, with you present. At home, it's a parent's account with the parent involved.
- **For under-13s, the work lives in an adult's repo.** Practical options: a **class organisation** you
  own with one repo per student, or [GitHub Classroom](https://classroom.github.com/), which exists for
  exactly this. Their site still goes live at a real URL — it's just hosted under the class account.
- **Everything else is unaffected.** Local development, the whole game, and the two-tab multiplayer test
  need no account at all. Only *publishing* does.
- **13–17:** own GitHub account is fine; the Claude account still needs an adult.

#### Can a free organisation host one repo per student? **Yes — cost is not the problem**

Verified against the docs, not assumed:

| Thing | Free plan reality |
|---|---|
| Repos in a free org | **"unlimited collaborators on unlimited public repositories with a full feature set"** — so one repo per student is fine |
| Org members | Unlimited on GitHub Free |
| **GitHub Pages** | *"available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team…"* → **free for us, because our repos are public anyway** |
| GitHub Actions (our deploy) | **Free and unlimited for public repos on standard runners**, on every plan. A private repo would eat the org's 2,000 min/month; public doesn't |
| Pages limits | Documented soft limits are roughly 1 GB per site, ~100 GB bandwidth/month, ~10 builds/hour. **[unverified this session — treat as approximate]** Our game is 1–2 MB, so irrelevant either way |

So: a free `kakkoi-school` org, one public repo per student, each with its own Pages URL, each deploying
via Actions. **Zero cost, no plan upgrade, no card.**

**The catch is the age floor, not the price.** Pages being free doesn't create accounts. Every student who
wants to push needs their own GitHub account, and that still means 13+. Two further wrinkles:

- **GitHub Classroom does not solve this** — it manages student repos, but students still need accounts.
  It's genuinely good for a 13+ class and useless for a 12-year-old one.
- **Sharing one login is against the ToS** (*"Your login may only be used by one person"*), so a single
  class account for everyone isn't a legitimate workaround.

**So, by age:**

| Students | Setup |
|---|---|
| **13+** | Free org, one public repo each, students are members and push themselves. Or GitHub Classroom. Everything works as written |
| **Under 13** | Free org, one public repo each — **an adult publishes.** The student writes all the code locally (needs no account at all), and you push. They still get their own live URL, which is the part that motivates them |

**SETTLED for this class: everyone is 13+** (one 13-year-old, the rest adults). That resolves it:

- **Every student owns their own GitHub account and pushes their own work.** No adult-publishes step, no
  per-student repo admin for you.
- **The org already exists: `KakkoiSchool`** (free plan, created 2026-05-06, members `KakkoiDev`,
  `davidrobel`, `roversi`). Nothing to create.
- **Split of ownership:** the **canonical game lives in the org** at `KakkoiSchool/kakkoi-online` with the
  `online.kakkoi.dev` CNAME. **Students fork it to their own accounts** and deploy to
  `their-name.github.io/kakkoi-online/`. They own their work, it survives the course, and it sits on their
  own profile.
- **Fork, not "use this template".** A fork keeps the upstream link, so a stuck student can
  `git fetch upstream && git diff a14-end` against the reference tags. That's the whole point of tagging
  each lesson, and a template repo throws it away.
- **Claude is the only account with an adult in the loop** — 18+ means the 13-year-old works under a
  parent's or your subscription, with you present. The adults use their own.
- **Optional and cheap: a class gallery.** A markdown list of everyone's live URLs (in `izumo-io`, or a
  page on school.kakkoi.dev). Costs nothing, and seeing five classmates' games side by side does more for
  motivation than any lesson text. It's also how you find out whose deploy broke.

The lesson text still states the general age rules, because the published lessons are read by strangers
and some will be under 13 — but no part of *our* class needs the adult-publishes path.

**One privacy point worth deciding now:** free Pages requires **public** repos, so a student's code and
repo name are world-visible. Use handles, not real names — and mention it in A09, since a 12-year-old
won't think of it. (This also matches the fork-and-play property we want: public is a feature here, not
just a constraint.)

**Mixed-age class, one useful consequence.** Writing for a 13-year-old keeps the main path readable for
everyone — adults are not insulted by clarity, only by padding, and the writing standard (§3.5) forbids
padding. Depth for the adults goes in the **appendices** (X1 keypair identity, X6 the balance simulator,
X7 the Phaser port), which they can take at their own pace without slowing the class. That's the mixed-age
answer: one clear main line, optional depth beside it.

**Tone note:** frame this as *"here are the rules these companies have, and here's how we work with
them"* — matter-of-fact, one short box. Not a warning, not an apology.

### A10 — Ship an empty page

- **Goal:** a dev server, a repo, and a **live public URL** — on day one.
- **Idea:** why `file://` fails and `http://` works: origins and **secure contexts** (`crypto.subtle`
  needs one, which A25 will need).
- **Builds:** Bun install, `bun ./index.html`, blank canvas, git repo, Pages + CI deploy.
- **Why deploy now:** it answers "does it work outside my laptop" while the code is 20 lines instead of
  2,000, and the student has something to show from lesson two. Deployment stops being a scary finale.
- **Alternatives:** double-clicking the file (breaks modules, crypto, fetch); `python3 -m http.server`
  (fine, but no TS); a bundler + config (a day of yak-shaving).
- **Verify:** loads at `localhost`; **loads at the public URL**; `file://` visibly fails — make them
  *see* the error rather than be told about it.
- **Your turn:** explain in one sentence why the browser refuses `file://`.

### A11 — Plan before you prompt

- **Goal:** produce a design doc for the game *before* any code.
- **Idea:** requirements vs implementation. **A spec is what makes an agent useful** — vague prompts get
  plausible nonsense, and the fix is upstream of the prompt. Analogy: you don't hand a builder a mood
  board and expect a house.
- **Builds:** the student's own `DESIGN.md` from a template (scope, non-goals, constraints, open
  questions).
- **Why:** an agent will build the wrong thing faster than you can review it. The spec is the brake.
- **Alternatives:** start coding and refactor (fine solo, collapses when the agent generates 500 lines
  an hour); design everything up front (guesses what only play can teach you).
- **Teaching material we already have:** this project's own three planning documents, **including the
  reversals** — decks → three actions, Block-pays-nothing → Block-banks-a-charge, free text → templated
  notes, and the whole §6.1 cut list. Showing a student a decision we *changed*, with the reason, is
  worth more than showing them a clean plan.
- **Verify:** their doc names its non-goals and at least one thing they chose not to build.
- **Your turn:** write one requirement that differs from ours, and its consequence.

### A12 — Types that never run

- **Goal:** typed code, checked in CI, no build step in dev.
- **Idea:** types are a **development-time tool that never runs**. Bun strips them and throws them away,
  errors included — so `tsc --noEmit` is the only thing that actually checks anything.
- **Builds:** strict `tsconfig.json`, one typed module, CI typecheck job.
- **Alternatives:** JSDoc + `tsc` (zero build, wordier, unusual syntax); no types (fast until the agent
  hands you 800 lines); in-browser transpiling (slow, fragile).
- **Verify:** introduce a deliberate type error — **the page still runs, CI goes red.** That contrast is
  the entire lesson.
- **Your turn:** find a type error the agent introduced in earlier code.

### A19 — Playing with strangers (the safety lesson)

Written out in full here rather than left to the build loop, because it is the one lesson where getting
the tone wrong does real harm. It must not read like a warning label a child skips.

- **Goal:** before you connect to another person, know exactly what they can see, what they can't, and
  what to do if someone is unkind.
- **Idea:** **nobody is in charge here.** In most games a company can ban people. In this one there is
  no company and no server — which is why the game only lets people say fixed phrases, and why the
  controls that protect you live on your own computer.
- **Tone rules:** plain, calm, specific. No scare stories. No "the internet is dangerous." Assume the
  reader is sensible and tell them the mechanics, the same way we explain collision detection.
- **What it actually says:**
  - **What others can see:** the name you chose, your creature, where you are standing, and the phrases
    you send. That's the whole list.
  - **What others cannot see:** your real name, where you live, your IP-as-identity, your files, or
    anything else on your computer. (Honest footnote for an older reader: a direct connection does
    reveal a network address, which is how the internet works; it is not your home address and it isn't
    shown in the game.)
  - **Why you can only pick from a list of phrases:** so that nobody can say something cruel or ask you
    for anything. It's a design decision, not a limitation of our skills. **This is the lesson's real
    computer-science idea:** you can prevent a whole class of problem by making it impossible instead of
    forbidding it. Grown-up programmers call that *designing out* the problem.
  - **What to do if someone is unkind or follows you around:** mute them (one tap, it's permanent and
    it's yours), leave and come back, and tell an adult you trust. Add: **you never owe anyone a duel.**
  - **A name is not proof.** Anyone can type any name, including your friend's, including the teacher's.
    Callback to A18.
  - **Nothing you type is stored anywhere.** No history, no logs, no accounts. Good for privacy, and it
    means nobody can check later what was said — which is exactly why muting is the tool that works.
- **Builds:** the in-game safety card (Basecoat dialog) shown once on first join, with a permanent link
  in settings, and the mute button it describes.
- **Verify:** open two tabs, mute one from the other, confirm the phrases stop arriving. **They must see
  the tool work**, not just read that it exists.
- **Your turn:** write one sentence explaining to a friend what other players can see about them.
- **[OPEN]** Should this page also exist outside the track as a plain page parents can read? It costs a
  `website/pages/` entry and one nav line. My lean: yes, eventually, low priority.

---

## 8. Reference implementation & the student's repo

- One canonical repo, `kakkoi-online`, tagged **`a09-end` … `a29-end`**. Every lesson header says
  "start from `aNN-end`", so a student can join mid-track or recover from a mess with
  `git diff a15-end`.
- **[OPEN]** Tags on `master` vs a branch per lesson. Tags are simpler; branches let you fix an early
  lesson without rewriting history. Leaning tags plus a `lesson-fixes` process where a correction
  moves the tag and bumps a `CHANGELOG` line.
- Students **fork** and work in their own repo, deploying to `their-name.github.io/kakkoi-online/`.
  Their fork **still plays with everyone else's** — peers meet on the relay, not on a domain. This is
  the single best demo in the track (A10 sets it up; A20–A21 make it visible).
- Submissions flow through the existing `/submissions/<handle>/` PR mechanism in `izumo-io`: per
  lesson, the student's repo URL, their live URL, plus the `build-verify` three-post (solution,
  write-up including one thing the AI got wrong, and a review of a partner's).

---

## 9. Trilingual production

- 18 lessons × 3 languages = 54 files, plus phases/UI strings. `scripts/translate_content.py` exists
  and the pipeline is proven on T/R/A.
- **In-game strings are separate** and live in the game repo's `i18n.ts` (en/ja/pt), including NPC
  barks and ghost-note phrases. Budget ~8 NPCs × 3 lines + ~20 note phrases + UI.
- **Screenshots: English only, one per lesson, reused across all three languages** (decided). Keeping
  in-game text out of the framing where possible makes them language-neutral; where UI text is visible,
  English is acceptable and avoids 3× the image work.
- **[HONEST] Sizing:** one lesson per week including its reference implementation is ~4–5 months. The
  §6.1 cuts and the no-new-track decision both pulled this down; it is still the largest content
  commitment on the site after T01–T39. Two
  ways to de-risk: publish phase by phase (A–B first) with later lessons `status: coming-soon` (the
  frontmatter already supports it), and write EN first, translating a phase at a time.

---

## 10. The build process (your loop, written down)

Explicitly: **no code until the game exists in these documents.** Then per milestone:

```
1. Docs are current for milestone M         (design + TRD updated, decisions recorded)
2. Build the MVP slice for M                (reference repo, real code)
3. Play it. Two tabs, then with a person.   ← the step that generates truth
4. Fix what's actually wrong                (mechanics, numbers, bugs)
5. Update the TRD + design doc to match     (docs follow reality, never diverge)
6. NOW write the lesson(s) for M            (with the real AI failures + real verify steps)
7. Screenshot + tag aNN-end. Repeat.
```

Rules that make this work:

- **The lesson is written last**, from a working implementation. A lesson written before the code
  contains invented verification steps and invented AI failures, and students find out immediately.
- **Docs are the source of truth, and they get corrected, not appended.** If play shows HP 30 is
  wrong, the TRD changes. A design doc that disagrees with the code is worse than no design doc.
- **Every reversal gets recorded with its reason** in the decision log. Those entries are literally
  A11's teaching material — this document set already contains three (decks → three actions,
  Block paying nothing → Block banks a charge, free-text notes → templated notes).
- **Collect AI failures as you go**, in a running `FAILURES.md` in the game repo. They are curriculum
  and they are impossible to reconstruct later.
- **Balance changes must move numbers in `tuning.json` and re-run the simulator**, never edit rules
  code ad hoc. The CI assertions (duel length, mirror win rate, `history` beating `random`) are the
  guardrail (TRD §8).

---

## 13. Delivery: self-serve pages, one taught lesson a week

**Self-serve** — every lesson is public, nothing is gated, no start date, no waiting. **Plus one lesson
taught per week in class**, which is where the multiplayer actually comes alive.

Three consequences worth designing for:

- **The weekly class *is* the play window.** This quietly solves the empty-world problem (design §2.4)
  without any scheduling machinery: from the week the class reaches A20–A21, the world has a whole room
  of people in it at a known time each week. No Discord slot needed at first — the lesson is the event.
  Worth saying to students plainly: *"the world is busiest during class."*
- **Every lesson must survive being done alone**, because students are explicitly invited to run ahead.
  That raises the value of three things already in the plan: the "start from tag `aNN-end`" line, the
  observable verification step (a student with no teacher needs to know for certain whether it worked),
  and the two-tab test (so solo students can test multiplayer without another person).
- **Students will be at different lessons.** Someone who ran ahead to A25 is already duelling while the
  class is on A21 — which is *good* (they populate the world and demo what's coming), and is only
  possible because the game is one shared world with no version gate beyond the protocol `v` check.

**Pace:** 21 lessons at one per week is ~5 months, which lines up with the 6-month arc in
`build-verify-track.md`. **[OPEN]** how long is your class session? Lessons are budgeted at 800–1,200
words plus a "your turn" extension, which suits roughly 60–90 minutes of guided work. If your session is
shorter, the lesson list splits further rather than the lessons getting denser.

**Between classes:** a student who does nothing keeps up next week (each lesson starts from a tag).
A student who wants more has the "your turn" extension, the appendices, and the option of running ahead.
Nothing punishes either choice — that's what self-serve buys.

---

## 11. Open questions

1. ~~Lesson count?~~ **Settled: 21 (A09–A29).** Shortened by cutting game features (§6.1), not by
   merging lessons — small lessons *and* a small game.
2. ~~Videos?~~ **Settled: screenshots only**, one per lesson, English, reused across languages.
3. ~~Track phases?~~ **Settled: none needed** — AI lessons have no `phase` field. The five groupings in
   §6 are editorial headings only.
4. **Tags vs branches** for the reference repo (§8).
5. ~~Cohort or self-serve?~~ **Settled: self-serve, with one taught lesson per week** (§13).
6. ~~Screenshots in English only?~~ **Settled: yes.**
7. **Do we publish the reference game as the canonical one at `online.kakkoi.dev`, or is the live URL a
   student's build?** Recommend ours is canonical, forks are equals — but only ours is in the lessons.
8. **Prerequisite enforcement:** state T10–T14/T19 and let people through, or gate the track?
9. ~~Where does the balance research live?~~ **Settled: two short sidebars in A26/A27, no R essay** —
   the R track is your voice and this isn't (§6.2).
10. **What happens when Bun, trystero, or a Nostr relay breaks in 18 months?** A CI smoke test tells
    us; the lessons still need an owner. Worth deciding now who that is.

---

## 12. Still-unclear gameplay areas (research continues)

Recorded here because they affect lesson content, not just the game:

- **Does the duel actually stay interesting for 20 fights?** Unknown until played. The CI depth test
  (`history` AI must beat `random`) is a proxy, not proof. **This is the biggest untested assumption in
  the whole project** and the reason M3 exists before any lesson in Phase D is written.
- **Is one map enough content?** At 5 players, probably — but "walk around" needs a reason. Wild
  encounters and trainer NPCs are the current answer; whether that sustains a week of play is unknown.
- **Progression pacing.** Level 1→20 over how many duels? Untested. Needs the simulator plus a real
  session.
- **How long is a session?** If a duel is 60 s and there's nobody online, the honest answer might be
  "5 minutes," which is fine for a teaching artefact and should be *designed for* rather than
  discovered.
- **Ghost-note vocabulary.** Which ~20 phrases? Dark Souls' vocabulary took iteration; ours should
  start tiny and grow from what players actually want to say.
