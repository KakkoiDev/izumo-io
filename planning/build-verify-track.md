# kakkoi.dev - "Build & Verify" Coding Program: 6-Month Plan + 10-Week Detail

> Honest scope, given your constraints (light workload, ~3-5 hrs/week, students new to JS,
> and your own belief that junior jobs are shrinking).

## Expectation setting (say this to students out loud)

At a **light workload**, 6 months delivers:
- Solid JS fundamentals
- 2-3 shipped, deployed projects (a real portfolio)
- Literacy in reading/verifying AI-generated code (the skill that survives when the junior rung breaks)

It does **not** reliably deliver: "will pass a mid-level interview" or "guaranteed hire." Anyone
who gets hired will have voluntarily done 5-10x the floor below. That voluntary excess is your
real signal for who's serious - let it self-select. Do not brand the program around a job promise.

## The instrument split (important)

- **Exercism** = weekly fundamentals + the effort filter. Not a portfolio.
- **Your Tech Lessons (T01-T39)** = the actual job-prep curriculum (build real apps). You already built it.
- **hellointerview** = self-serve reference for LATER (see caveat). Not core, given light workload + beginner cohort.

---

## 6-Month Arc

| Phase | Weeks | Focus | Output |
|---|---|---|---|
| A. Fundamentals + filter | 1-10 | Exercism JS Learning Mode + T10-T14; git from wk4 | Reads/writes basic JS; ships a mini-project |
| B. Build real things | 11-18 | T05-T18 (HTML/CSS/DOM/fetch/dynamic site) + T19-T20 (git/GitHub) | 1-2 deployed apps, real git history |
| C. Backend + capstone | 19-24 | T21-T27 (Node/API/DB/auth/full-stack AI app) | Graduation project: full-stack AI app |
| D. Interview prep | 25-26 | Fundamentals review, "explain your project" drills, light coding practice, system-design *awareness only* | Can talk through their portfolio |

---

## The 10 Weeks (exact URLs)

Exercism = the floor (1/week min). T-lesson = the real work. Ship by week 10.
Follow the JS track **Learning Mode** - it auto-sequences these in the same order.

| Wk | Concept | Exercism exercise (exact URL) | School lesson | Build / deliverable |
|---|---|---|---|---|
| 1 | Setup + Basics | Warmup: https://exercism.org/tracks/javascript/exercises/hello-world<br>Real: https://exercism.org/tracks/javascript/exercises/lasagna | https://school.kakkoi.dev/lessons/t10.html | The 3-post |
| 2 | Booleans | https://exercism.org/tracks/javascript/exercises/annalyns-infiltration | https://school.kakkoi.dev/lessons/t10.html (review) | 3-post + first peer review |
| 3 | Numbers | https://exercism.org/tracks/javascript/exercises/freelancer-rates | https://school.kakkoi.dev/lessons/t10.html | 3-post |
| 4 | Strings | https://exercism.org/tracks/javascript/exercises/poetry-club-door-policy | https://school.kakkoi.dev/lessons/t11.html + https://school.kakkoi.dev/lessons/t19.html (Git) | Everything now lives in a git repo |
| 5 | Arrays | https://exercism.org/tracks/javascript/exercises/elyses-enchantments | https://school.kakkoi.dev/lessons/t11.html / t12.html | Mini-project kickoff (tiny interactive page) |
| 6 | Conditionals | https://exercism.org/tracks/javascript/exercises/vehicle-purchase | https://school.kakkoi.dev/lessons/t12.html | Project: handle user input |
| 7 | For-loops | https://exercism.org/tracks/javascript/exercises/bird-watcher | https://school.kakkoi.dev/lessons/t13.html | Project: store/display data |
| 8 | While-loops | https://exercism.org/tracks/javascript/exercises/mixed-juices | https://school.kakkoi.dev/lessons/t13.html | Project: iterate/refactor |
| 9 | Type conversion | https://exercism.org/tracks/javascript/exercises/lucky-numbers | https://school.kakkoi.dev/lessons/t14.html | Project: add localStorage persistence |
| 10 | Map/filter + transfer test | https://exercism.org/tracks/javascript/exercises/elyses-analytic-enchantments<br>Transfer test (no scaffolding): https://exercism.org/tracks/javascript/exercises/leap | Deploy via GitHub Pages | **SHIP publicly** + full build write-up = first portfolio piece |

Why `leap` at wk10: it's a scaffolding-free practice exercise with classic edge-case bugs
(divisible by 4 / 100 / 400). Perfect for the "find/explain the bug the AI made and why these
conditions" deliverable. It tests whether understanding transfers, which a concept exercise can't.

### The weekly deliverable (the filter - do not drop)
1. Your solution.
2. Write-up: where you got stuck / what you tried first / (if AI used) one thing it got wrong or you had to fix + how you verified it works.
3. Review of your rotating partner's code: at least ONE concrete finding. "Looks good" is not a review.

---

## Later phases - lesson URLs (for reference)

Phase B (build): https://school.kakkoi.dev/lessons/t11.html through t18.html; git/GitHub: t19.html, t20.html
Phase C (backend + capstone): t21.html (Node) t22.html (API) t23.html (JSON DB) t24.html (SQLite) t25.html (Auth) t26.html (Ollama/Chat) t27.html (Full-Stack AI App)
System design (advanced, your own phase 11): t37.html, t38.html, t39.html

## Graduation project
- Do NOT big-bang one capstone at the end. Ship small early (wk10), bigger in Phase B, then the AI-integrated full-stack capstone in Phase C. 2-3 pieces = range.
- Lean into full-stack + AI (T26-27). That is the differentiated 2026 portfolio, not another CRUD to-do clone.

## hellointerview - placement + caveat
- Home: https://www.hellointerview.com/
- It has a free "System Design in a Hurry" guide under the site's Learn nav (grab the exact link from the nav; I did not verify deep paths).
- Caveat: this is mid/senior interview content. For 6-month beginners at light workload it is **awareness-tier, months 5-6, self-serve** - not a core workload item. If you truly believe junior jobs are vanishing, prioritize portfolio + AI-building over interview cramming, because the reachable path is builder/freelance/internal-tooling, not the FAANG gauntlet hellointerview optimizes for.

## "Become a pro" track on the site - recommendation
- Formalizing = good instinct. But do NOT add a 4th lessons track - it duplicates your existing Tech Lessons (T01-T39), which already ARE a become-a-pro curriculum.
- What's actually new is the **program** (verification deliverable + peer review + rotating pairs + weekly grilling + cohort), layered on the lessons you already have.
- Rename it. "Become a pro" promises an outcome you can't guarantee in a shrinking-junior market at light workload - that's the "job that won't come" false hope you set out to avoid. Name it after the skill you actually deliver: e.g. **"Build & Verify"** / **"Real Code"**. Under-promise.

---
Verification note: Exercism slugs pulled from the track's authoritative config.json. School lesson URLs pulled from school.kakkoi.dev/tech-lessons.html. hellointerview deep links NOT verified - link the homepage and navigate.
