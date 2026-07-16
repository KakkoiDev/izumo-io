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

## Discord launch message (week 1, #code-challenge)

```
**新トラック（任意）：AIを「使う」だけでなく「理解する」**
就職を目指す人向け。週1問、AI使用OK。

**今週**
・準備運動: Hello World → https://exercism.org/tracks/javascript/exercises/hello-world
・本番: Lasagna（変数・関数・戻り値）→ https://exercism.org/tracks/javascript/exercises/lasagna
・基礎レッスン → https://school.kakkoi.dev/lessons/t10.html （参照用、写経禁止）

**AIは一瞬でコードを書ける。だから基準は「合格した」ではなく「理解している証明」。**

**#code-challenge に3つ投稿:**
1. 解答
2. メモ：どこで詰まったか／最初に試したこと／(AI使用時)AIが間違えた点と動作確認の方法
3. ペアのレビュー：具体的な指摘を1つ以上（バグ・抜けてるケース等。「いいね」は不可）

今週だけ、僕が全員のペアになります。来週からはペアを毎週交代。
週1の授業で一緒に確認。
```

## Exemplar 3-post (model of the deliverable)

Purpose: show the FORMAT on the trivial warmup. hello-world has no bug (one line), so
the only finding available is cosmetic - the post says so explicitly and points students
to the real bar (bug/edge-case) starting with Lasagna. Verification stays but stays EASY:
the browser "Run Tests" button, not a CLI. Also models honest AI use (translate the prompt
to understand it; code written by the student).

```
【お手本】3点投稿の形（今週の準備運動 Hello World で）

**1. 解答**
Exercism が最初にこのスケルトンをくれる:
​```js
//
// This is only a SKELETON file for the 'Hello World' exercise. It's been provided as a
// convenience to get you started writing code faster.
//

export function hello() {
  return 'Hello, World!';
}
​```
中身はもう正しい。Exercism の「Run Tests」ボタンで緑を確認 → 提出。

**2. メモ**
・AIで問題文を日本語に翻訳して内容を理解した（コードは自分で書いた）。
・先頭の `//` コメントは「これはスケルトンです」という説明で、動作に関係ないノイズ。
　自分のコードじゃないので削除。もう一度 Run Tests → 緑のまま。

**3. レビュー（ペア視点）**
おつかれさま。指摘1つ：スケルトンの説明コメントが残ってる。動作に不要なので消してOK。

（※今週は準備運動なのでバグが無く、指摘がコメント整理だけになる。
本番の Lasagna からは「バグ・抜けてるケース」を1つ挙げるのがレビュー。
見た目だけの指摘は"レビュー"に数えない。）
```

---
Verification note: Exercism slugs pulled from the track's authoritative config.json. School lesson URLs pulled from school.kakkoi.dev/tech-lessons.html. hellointerview deep links NOT verified - link the homepage and navigate.
