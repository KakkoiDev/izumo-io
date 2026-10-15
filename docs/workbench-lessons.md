# The Workbench

## Part 1: Working with Pi

What the workbench is, how to ask, and how to read what Pi did

> Meeting your new apprentice before you hand over the keys

- [W01: What the Workbench Is (and the Three AI Risks)](lessons/w01.md) - Pi Workbench is a local workshop where an AI agent builds your app and a checker watches every move. What it does, what it does not do, and the three rules that keep you safe.
- [W02: Asking Well: Requests, Context, Pi's Memory](lessons/w02.md) - A request is a work order. Say what you want and how you will know it works, point Pi at the right files, and keep standing instructions in AGENTS.md.
- [W03: Reading What Pi Did](lessons/w03.md) - The foreman's notebook: the task file, a test that fails then passes, what 'verified' means, the commit the harness makes, and how to go back.

## Part 2: Your First App

The server stack, one piece at a time: pages, looks, htmx, data, rules, two languages

> Learning each room of the house you are building

- [W04: Your First App from the Starter](lessons/w04.md) - Pi never starts from nothing: the starter is a small, working notes app with tests. Make your copy, run it, and learn what each folder is for.
- [W05: Pages: HTML in Templates](lessons/w05.md) - A template is a form letter with blanks. Jinja fills the blanks, base.html is the shared frame, pages are whole pages and fragments are pieces. Add your first page.
- [W06: Looking Good: Basecoat and Tailwind](lessons/w06.md) - Furniture and floor plan: Basecoat gives ready-made components as class names, Tailwind arranges them. The classes that are almost always right, and the build step behind them.
- [W07: HTML over the Wire: htmx](lessons/w07.md) - The kitchen sends finished plates: the server returns HTML fragments and htmx 4 puts them in place. Read the starter's add, delete and error flows, and the htmx 4 rules Pi must follow.
- [W08: Data That Stays: SQLite and Migrations](lessons/w08.md) - One file holds all your app's data. Migrations are the numbered renovation plans that change its shape safely, and db.py is the only door in.
- [W09: Rules as Small Typed, Tested Functions](lessons/w09.md) - Keep the app's rules in pure functions: data in, data out, no surprises. Types let pyright catch mistakes before anything runs, and small tests check every rule completely.
- [W10: Two Languages: English and Japanese](lessons/w10.md) - Every word on the page goes through t("key"), with one dictionary per language. How the language is chosen, how to add a word, and why the starter's test keeps both dictionaries in step.

## Part 3: Sharing It

History, GitHub, the phone, apps with no server, and putting it online

> Opening the door so other people can come in

- [W11: Git, the Time Machine the Harness Drives](lessons/w11.md) - Git records every verified change as a snapshot. Set it up once, read the history, see exactly what changed, go back, and try ideas on a branch.
- [W12: GitHub: Account, Connect, First Repository](lessons/w12.md) - Put a copy of your project's history on GitHub: a free account, your computer connected with gh, one command to publish, and the push you do after Pi's commits.
- [W13: On the Phone: an Installable App (PWA)](lessons/w13.md) - Your app is already a PWA: a manifest, a service worker, an icon. Open it on your phone over HTTPS, add it to the home screen, and know what works offline.
- [W14: An App with No Server at All](lessons/w14.md) - One question decides whether your app needs a server. If not, it runs entirely in the browser: free on GitHub Pages, works offline, nothing to keep on. What you gain, what you lose, and how people can still share live.
- [W15: Native Phone Apps without a Store](lessons/w15.md) - When a PWA is not enough: Capacitor wraps the same app in a native shell. Installing it on Android (an APK, GitHub releases, Google's new verification) and on iPhone (what Apple allows, stated plainly).
- [W16: Putting It Online](lessons/w16.md) - Three ways, one for each kind of app: GitHub Pages for apps with no server, Tailscale Funnel as the free default for server apps, Fly.io when it must be always on.

## Part 4: Growing It

Accounts, AI inside the app, finding bugs, and shipping for real

> The house stands. Now you live in it, fix it, and add rooms

- [W17: Logins and Accounts](lessons/w17.md) - Who are you, and what may you do? When an app needs accounts, the safest login you already have, and the rules for building one: hashed passwords, sessions, CSRF, HTTPS.
- [W18: An App That Uses AI](lessons/w18.md) - Your computer already runs a model for Pi. Your app can ask it too: one typed function in the shell, pure logic around it, a test that never calls the real model, and the AI risks, now for your users.
- [W19: Finding Bugs with Pi: Reproduce First](lessons/w19.md) - A doctor examines before prescribing. Report a bug with its conditions, have Pi see it fail before fixing it, and let a failing test prove the cause. A true story from the harness itself.
- [W20: Shipping, and What Comes Next](lessons/w20.md) - Finishing is a skill: a shipping checklist for your app, keeping it simple so it still runs in two years, and where to go from here.
