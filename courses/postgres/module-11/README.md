# Module 11 - Your First Real Tooling (L55-L58)

Prereq: comfortable with psql. Modules 0-10 complete.

We've been using raw `psql` to internalize fundamentals. Now we upgrade.

---

## L55 - Install pgcli

### Concept

`pgcli` is psql with superpowers: autocomplete, syntax highlighting, smart table suggestions.

### Steps

Install on macOS:
```bash
brew install pgcli
```

Connect:
```bash
pgcli postgres://postgres:dev@localhost:5432/bookshelf
```

Features to try:
- Start typing `SELEC`, press TAB
- Start typing `SELECT * FROM bo`, press TAB, get `books`
- Type `SELECT * FROM books WHERE `, pgcli suggests column names
- `F2` toggles named queries
- `F3` toggles multiline mode
- Up arrow for history

### Safe update mode

```
\config
```

Edit the file at `~/.config/pgcli/config` and set `destructive_warning = True`. Forces confirmation before DELETE/UPDATE without WHERE.

### When to use pgcli vs psql

- Daily work: pgcli
- Scripts / CI: psql (simpler, no deps)
- Container: psql is already inside

### Exercises

1. Connect with pgcli, run a joined query with column autocomplete.
2. Compare pgcli vs psql for speed of writing.

### Check-in

Paste a screenshot description: which columns did pgcli suggest when you typed `SELECT ` for a table?

---

## L56 - Install rainfrog

### Concept

`rainfrog` is a TUI database explorer. Vim-like nav, query editor, browse tables, inspect schema.

### Steps

```bash
brew install rainfrog
# or: cargo install rainfrog
```

Launch:
```bash
rainfrog --url postgres://postgres:dev@localhost:5432/bookshelf
```

Key bindings (vim-style):
- `h j k l` - navigate
- `/` - search
- `i` - insert mode in the query editor
- `:w` to execute query
- `?` - help screen

### When to use

- Exploring unfamiliar schemas
- Reviewing table data in a spreadsheet-like view
- Running ad-hoc queries with a better editor than psql's default

### Not a replacement for pgcli; complement.

### Exercises

1. Browse the `books` table, sort by published date.
2. Run a JOIN query in the editor.

### Check-in

Describe which panes rainfrog shows.

---

## L57 - Polish ~/.psqlrc

### Steps

Create or edit `~/.psqlrc`:

```psql
\set QUIET 1
\pset null '[null]'
\pset linestyle unicode
\pset border 2
\set COMP_KEYWORD_CASE upper
\set HISTFILE ~/.psql_history- :DBNAME
\set HISTCONTROL ignoredups
\set PROMPT1 '%[%033[1;32m%]%n@%/%[%033[0m%]%R%# '
\timing
\x auto
\unset QUIET
```

What each does:
- `\set QUIET 1` - suppress startup messages (restored at end)
- `\pset null '[null]'` - display NULL as `[null]` instead of empty
- `\pset linestyle unicode` - nicer borders
- `\pset border 2` - full borders
- `\set COMP_KEYWORD_CASE upper` - tab completion yields UPPERCASE keywords
- `\set HISTFILE ...` - history per database
- `\set PROMPT1` - colored, informative prompt (user, db, privilege)
- `\timing` - always show query time
- `\x auto` - auto-expanded for wide rows

### The file is for interactive psql only. Pipes (`psql < file.sql`) skip it.

### Exercises

1. Apply the config, reconnect, observe color and NULL display.
2. Tweak PROMPT1 to add the hostname.

### Check-in

Paste the first 4 lines of a psql session showing the new prompt.

---

## L58 - Migrations with sqitch

### Concept

Until now we've hand-created tables in psql. Real projects use a migration tool: versioned, reversible, in git.

sqitch is pure-SQL (no DSL). Each change has deploy/revert/verify scripts.

### Install

```bash
brew install sqitch --with-postgres-support
# or follow docs
```

### Steps

Init a project:
```bash
cd ~/pg-work
sqitch init bookshelf --engine pg
```

Creates `sqitch.conf`, `sqitch.plan`, `deploy/`, `revert/`, `verify/`.

Add a change:
```bash
sqitch add schema -n 'initial schema'
```

Edit `deploy/schema.sql`:
```sql
-- Deploy bookshelf:schema to pg
BEGIN;
CREATE TABLE authors (id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY, name text NOT NULL);
CREATE TABLE books (id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY, title text NOT NULL, author_id int REFERENCES authors(id));
COMMIT;
```

Edit `revert/schema.sql`:
```sql
BEGIN;
DROP TABLE books;
DROP TABLE authors;
COMMIT;
```

Edit `verify/schema.sql`:
```sql
SELECT 1 FROM authors LIMIT 0;
SELECT 1 FROM books LIMIT 0;
```

Deploy to a test db:
```bash
createdb bookshelf2
sqitch deploy db:pg://postgres:dev@localhost/bookshelf2
sqitch verify db:pg://postgres:dev@localhost/bookshelf2
```

Revert if needed:
```bash
sqitch revert db:pg://postgres:dev@localhost/bookshelf2 --to @ROOT
```

### Alternative: Atlas (declarative)

If you prefer "write the target schema, tool plans the migration":
```bash
brew install ariga/tap/atlas
```

Atlas compares schema.hcl to live DB, generates a plan. Different mental model; try both and pick.

### Exercises

1. Initialize sqitch, create an `init` migration with authors+books.
2. Add a second migration that adds `email UNIQUE` to authors. Deploy, verify, revert, redeploy.
3. Commit `deploy/`, `revert/`, `verify/`, `sqitch.conf`, `sqitch.plan` to git.

### Check-in

Show `sqitch log` against `bookshelf2`.

---

## Module 11 completion criteria

- [ ] pgcli is your daily driver
- [ ] You know rainfrog for exploration
- [ ] `~/.psqlrc` is set up
- [ ] You use sqitch (or Atlas) for every schema change; no more raw CREATE TABLE in psql
