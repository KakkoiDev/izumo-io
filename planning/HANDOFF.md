# Kakkoi Online — handoff

Written for **another agent on another computer** picking this up cold. Read this, then
`kakkoi-online-lessons.md` §10 (the build process). Everything below was true at the last commit.

## What this is

Two things being built together:

1. **A game** — `Kakkoi Online`, a serverless P2P browser game. Live: **https://online.kakkoi.dev**
2. **A lesson track** — steps **A09–A23** on https://school.kakkoi.dev, continuing the existing AI
   track, teaching a 12–13-year-old to build that game with an AI assistant.

**Read this before anything else: the plan changed substantially on 2026-08-16.** Five reversals, all
in the design decision log (rows 43–51). If a doc you are reading contradicts them, the log wins.

| What changed | Now |
|---|---|
| Toolchain | **Plain JavaScript. No TypeScript, no npm, no Bun, no build step.** Editor + Live Server extension is the whole thing |
| Lesson size | **One step = one feature you can SEE**, cut into 2–4 named blocks. 21 lessons → 15 steps |
| Code shape | **A standalone demo per step** in `demos/NN-name/`, then a "Put it in the game" section. Not one accreting codebase |
| What the track teaches | **Decomposition.** Cut a feature into blocks you can check one at a time. Everything else is the vehicle |
| Publishing / GitHub | Moved from A09 to **A18**. P2P works fine on localhost, so nothing needs to be online until part 6 |
| Pacing | **Parts** (chapters) and **steps** (sittings). No unit of time appears in any lesson text — 2–3 steps in a sitting must be possible |

## Two repos

| Repo | Path on the original machine | Remote | Holds |
|---|---|---|---|
| `izumo-io` | `/Users/cyril/Code/izumo-io` | `git@github.com:KakkoiDev/izumo-io.git` | The school site: lessons, planning docs, `docs/` (published) |
| `kakkoi-online` | `/Users/cyril/Code/kakkoi-online` | `git@github.com:KakkoiSchool/kakkoi-online.git` | The game itself |

Clone both. They are independent; the planning docs live in `izumo-io/planning/`.

## Read these first, in order

1. `planning/kakkoi-online-design.md` — why every decision is what it is. **A 51-row decision log with
   ten recorded reversals.** Read the log before proposing changes; several "obvious" ideas were already
   tried and rejected for reasons.
2. `planning/kakkoi-online-trd.md` — what to build: data model, network protocol, battle rules,
   milestones, tests.
3. `planning/kakkoi-online-lessons.md` — **§6 is the current list (7 parts, 15 steps)**, plus §2.1 (the
   demo model), the **writing standard (§3.5)**, and **§10, the build process you must follow**. §7's
   per-lesson detail sheets are from the old 21-lesson plan and are marked superseded.
4. `planning/kakkoi-online-sources.md` — every asset pack, library and reference, with licences.

## The rule that matters most

**Docs first, then the demo, then run it in a real browser, then fix, then update the docs, and only
then write the lesson.** Full version in lessons §10.

```
1. Docs current for the step
2. Build the demo in demos/NN-name/  (standalone, one screen of code, plain JS)
3. RUN IT in a real browser          ← generates the truth
   - via ego-browser, driven by a subagent
   - console + network must be CLEAN; a demo that throws still screenshots nicely
   - actually press the keys; open a second window for the peer demos
4. Fix what is actually wrong
5. Screenshot → izumo-io/website/static/img/game/aNN.png
6. Append what went wrong to FAILURES.md
7. Fold the demo into the game
8. Update the docs to match reality
9. NOW write the lesson, using real failures from FAILURES.md. Repeat.
```

A lesson written before the code contains invented verification steps and invented AI mistakes, and
students spot it instantly. **`kakkoi-online/FAILURES.md` is collected while building** — every third
lesson shows students a real mistake, and they cannot be reconstructed later.

## State: done

- **All fifteen steps A09–A23 are written and live, English only.** Each carries `translate: false`;
  drop that flag when a lesson has settled and the pipeline translates it.
- **Eleven demos** in `kakkoi-online/demos/`, every one driven in a real browser with a canary-proven
  console check before its screenshot was taken.
- **Peer-to-peer works.** trystero 0.21.5 vendored as six plain ES modules, no bundler. Verified across
  two tabs: a position of x=448 in one appeared as x=448 in the other.
- **Art and audio sourced**, all CC0 with licence files vendored beside them: Kenney Tiny Dungeon and
  Tiny Town atlases, Kenney Pixel Platformer characters (the only sheet we found with a real walk
  cycle), Clint Bellanger's Tiny Creatures, six sound effects and one music loop.
- Planning docs, TRD and decision log rewritten for the 2026-08-16 restructure.
- `content/ai-phases.yaml` has two parts; every game step is `phase: 2`.
- Translation pipeline: fixed, plus `source_sha` staleness detection and the `translate: false` draft
  flag.

## State: not done

- **Nothing is translated.** Deliberate — Cyril is reviewing the English first.
- **No lesson has been read by a student yet.** The whole set is a first pass awaiting his corrections.
- **The game itself (`src/`) is still the old scaffold.** Every "Put it in the game" section describes
  the fold-in, but the demos have not actually been merged into a single playable game. This is the
  biggest outstanding piece of work.
- **A16 has no collision** — you walk through walls. Joining A15's checking code to A16's map is left
  as the student exercise, and the lesson says so.
- **A14's character art does not match A16's world** (24px platformer vs 16px top-down). Named openly
  in A14. No pack we found offers both a matching world and a character that walks.
- **Lessons run long**: 1,300–1,800 words of prose against the 800–1,200 standard in `-lessons.md`
  §3.5. Consistent across all fifteen, mostly in the alternatives tables and honesty paragraphs.
- A18 and A23 have no screenshot (neither has a demo).

## Environment gotchas (these cost real time)

| Gotcha | Detail |
|---|---|
| **Bun and npm are not installed, and are no longer needed** | The project is plain JS with no build step. To serve locally: `python3 -m http.server 8000`. Do not reintroduce a toolchain |
| **Python 3.9.6 vs `requirements.txt`** | The site build wants `markdown>=3.10`, which needs Python ≥3.10. Local builds were done with `markdown==3.9` in `.venv` (renders fine, not what is pinned). Fix properly: `brew install python@3.12`, recreate `.venv`, `pip install -r requirements.txt` |
| **`make build` needs the venv** | `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`. The Makefile prefers `.venv/bin/python` if present |
| **`master` has a ruleset requiring PRs** | "Protect Master"; bypass list = repository admin only. The owner's pushes report "Bypassed rule violations" and succeed. **`github-actions[bot]` cannot push to master** |
| **Actions cannot create PRs** | Settings → Actions → General → "Allow GitHub Actions to create and approve pull requests" is **off**. The translate workflow therefore pushes a branch and prints a PR link in the run summary instead of failing. Enable with `gh api -X PUT repos/KakkoiDev/izumo-io/actions/permissions/workflow -F can_approve_pull_request_reviews=true` if full automation is wanted |
| **`CNAME` file is inert** | For **workflow-based** Pages the custom domain lives in the Pages config, not in a `CNAME` file. `gh api -X PUT repos/OWNER/REPO/pages -f cname=online.kakkoi.dev`, wait for the cert, then `-F https_enforced=true` |
| **Game repo default branch is `main`**, school repo is `master` | Do not assume either |
| **`curl` in the sandbox could not resolve `online.kakkoi.dev`** while `dig` could | Verify with `curl --resolve online.kakkoi.dev:443:185.199.108.153` |
| **Kenney assets are NOT a browser-only download** (this doc said they were, for days) | The zip URL carries a content hash, and every asset page prints the current one. `curl -sL https://kenney.nl/assets/tiny-dungeon \| grep -o "href='[^']*\.zip'"` then fetch it. The original 404 came from a *guessed* URL, and the wrong conclusion blocked three lessons |
| **`drainEvents()` returns an empty queue** unless `Runtime.enable` / `Log.enable` / `Network.enable` are issued first, and again after every navigation | Three separate agents reported "the console is clean" while reading an empty pipe. **Always prove the checker works** with `js("console.warn('canary')")` before trusting a clean result. Also `Network.setCacheDisabled` or you test a stale copy of your own edit |
| **Nostr relays come and go** | The demos pin four relay URLs rather than trusting trystero's defaults. One died between building A12 and re-checking it. Expect to swap one occasionally; the lesson tells students the same |

## Publishing a lesson

```bash
# 1. write content/ai/aNN.md   (EN only; frontmatter: id, phase, title, desc — no status field in the AI track)
make build                      # regenerates docs/
git add -A && git commit && git push origin master
# 2. the translate workflow fires on content/**.md, generates JA+PT, rebuilds docs/,
#    pushes a branch and prints a PR link in the run summary. Merge it.
# 3. if you merge locally instead, run `make build` again and push, or the JA/PT
#    pages will keep serving English.
```

The workflow **fails loudly** if any lesson is missing a `.ja.md`/`.pt.md` sibling, naming the files.

**Editing an already-translated lesson.** Translations carry a `source_sha` in their frontmatter — a
fingerprint of the English file they were made from. Change the English and the next run sees the
mismatch and **re-translates that file**. Before this existed, editing a lesson left JA and PT
silently describing the old version, which is exactly what happened to A09 and A10.
A translation with *no* `source_sha` is treated as current and simply stamped, so adding the check did
not re-translate the whole site.

**English-only drafts.** `translate: false` in a lesson's frontmatter makes the translate script skip
it and the verify step report it as a draft rather than fail. Use it while a lesson is still being
edited — the /ja/ and /pt/ pages fall back to English. Remove the flag when the lesson has settled and
the next run translates it.

## Decisions a newcomer will be tempted to re-open

All settled, with reasons in the decision log. Do not silently reverse them:

- **No Phaser.** Hand-written canvas. Appendix X7 ports to Phaser *afterwards* as a lesson.
- **No TypeScript and no build step.** Reversal, 2026-08-16. Do not "improve" this back.
- **Demos are standalone, not one growing codebase.** The whole point is that a student whose game
  breaks is not stuck for the rest of the track.
- **No invented bugs.** The "write it naively, feel it break, fix it" shape is only allowed when the
  break really happened to us and is in `FAILURES.md`. One was caught being fabricated already.
- **No procedural art or audio.** A fixed set of ~6 Kenney CC0 monsters, CC0 audio files, no synthesis.
- **Chat is preset phrases only.** No free text at all — the readers are children and there is no
  moderation possible. Abuse is designed out, not policed.
- **`agy` (Antigravity CLI), not Claude Code**, because A01/A02 already install it, it is free, and it
  keeps GitHub's 13+ as the only account rule.
- **Students start from an empty repo**, never a fork, and read our tagged snapshots in a browser if
  stuck. A fork hands them the finished game.
- **v1 has no levels, no dual types, no cosmetics, no wild encounters, no ghost notes.** Scope is
  deliberately tiny.
- **Lessons must be readable by a 12-year-old** (writing standard §3.5). This outranks completeness.

## Who to ask

The owner is `KakkoiDev` (Cyril), teaching one lesson per week to a small class: one 13-year-old, the
rest adults. Class doubles as the multiplayer play window. Open questions worth raising with him:

- Whether A09/A10's voice and reading level are right (everything after inherits it).
- The Kenney downloads, which nobody else can do.
