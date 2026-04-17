# Postgres Dev Env Setup (CLI-only, Docker-sandboxed, Helix + tmux)

Target: sandboxed Postgres 17 with all extensions in Docker, Helix editor w/ Postgres LSP, pgcli + rainfrog as TUIs, tmux as workspace.

## 1. Docker sandbox

### docker-compose.yml

```yaml
services:
  db:
    image: ivanlonel/postgis-with-extensions:17
    container_name: pg-sandbox
    environment:
      POSTGRES_PASSWORD: dev
      POSTGRES_DB: sandbox
      POSTGRES_USER: postgres
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./init:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  postgrest:
    image: postgrest/postgrest:latest
    container_name: pg-rest
    depends_on:
      db:
        condition: service_healthy
    environment:
      PGRST_DB_URI: postgres://authenticator:dev@db/sandbox
      PGRST_DB_ANON_ROLE: anon
      PGRST_JWT_SECRET: dev-secret-32-bytes-or-more-change-me
      PGRST_DB_SCHEMA: api
    ports:
      - "3000:3000"

volumes:
  pgdata:
```

### init/01-extensions.sql

```sql
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS unaccent;
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS timescaledb;
CREATE EXTENSION IF NOT EXISTS pgmq CASCADE;
CREATE EXTENSION IF NOT EXISTS pg_partman;
CREATE EXTENSION IF NOT EXISTS pg_graphql;
```

### init/02-roles.sql (for PostgREST)

```sql
CREATE ROLE anon NOLOGIN;
CREATE ROLE authenticated NOLOGIN;
CREATE ROLE authenticator NOINHERIT LOGIN PASSWORD 'dev';
GRANT anon TO authenticator;
GRANT authenticated TO authenticator;

CREATE SCHEMA IF NOT EXISTS api;
GRANT USAGE ON SCHEMA api TO anon, authenticated;
```

### Boot

```bash
docker compose up -d
docker compose logs -f db   # tail until "database system is ready"
```

### Teardown (when you want a clean slate)

```bash
docker compose down -v   # -v drops the named volume = wipes data
```

## 2. psql config (~/.psqlrc)

```psql
\set QUIET 1
\pset null '[null]'
\pset linestyle unicode
\pset border 2
\set COMP_KEYWORD_CASE upper
\set HISTFILE ~/.psql_history- :DBNAME
\set HISTCONTROL ignoredups
\set PROMPT1 '%[%033[1;32m%]%n@%/%[%033[0m%]%R%# '
\set PROMPT2 '  %[%033[1;33m%]>%[%033[0m%] '
\timing
\x auto
\unset QUIET
```

Environment:
```bash
export EDITOR=hx   # so psql's \e opens Helix
export PSQL_PAGER='less -S'
```

## 3. Essential psql meta-commands

| Command | Purpose |
|---------|---------|
| `\l` | List databases |
| `\c dbname` | Connect to db |
| `\dt` | List tables |
| `\d tablename` | Describe table (columns, indexes, FKs) |
| `\d+ tablename` | Describe + storage info |
| `\df` | List functions |
| `\di` | List indexes |
| `\dv` | List views |
| `\dx` | List installed extensions |
| `\du` | List roles |
| `\dn` | List schemas |
| `\timing on/off` | Toggle query timing |
| `\x auto` | Expanded output for wide rows |
| `\e` | Open `$EDITOR` to compose query |
| `\i file.sql` | Execute SQL file |
| `\o file.txt` | Pipe output to file |
| `\watch 2` | Re-run last query every 2s |
| `\copy ... from 'file.csv' csv header` | Client-side CSV import |
| `\gexec` | Execute each row of result as SQL |
| `\set` | List psql variables |
| `\?` | Help on meta-commands |
| `\h SELECT` | Help on SQL command |

## 4. TUI clients

### pgcli - daily driver

```bash
brew install pgcli
# or: pipx install pgcli
```

Connect:
```bash
pgcli postgres://postgres:dev@localhost:5432/sandbox
```

Key features: autocomplete, syntax highlighting, smart completion based on schema. Treat as psql++.

### rainfrog - full TUI explorer

```bash
brew install rainfrog
# or: cargo install rainfrog
```

Key bindings: vim-style navigation, `/` to search, query editor with session history and favorites.

### lazysql - multi-DB TUI

```bash
go install github.com/jorgerojas26/lazysql@latest
```

Use when working across Postgres / MySQL / SQLite / MSSQL.

### harlequin - SQL IDE in terminal

```bash
pipx install 'harlequin[postgres]'
```

Best for exploratory analytics. Textual-based UI, works with DuckDB too.

### usql - universal client (optional)

```bash
brew install xo/xo/usql
```

## 5. Helix editor + Postgres LSP

### Install pgtools

```bash
curl -fsSL https://pgtools.dev/install.sh | sh
# confirms in PATH
command -v postgrestools
```

### ~/.config/helix/languages.toml

```toml
[language-server.pgtools]
command = "postgrestools"
args = ["lsp-proxy"]

[[language]]
name = "sql"
language-servers = ["pgtools"]
formatter = { command = "pg_format", args = ["-"] }
auto-format = true
```

### Fallback: sqls

```bash
go install github.com/sqls-server/sqls@latest
```

```toml
[language-server.sqls]
command = "sqls"

[[language]]
name = "sql"
language-servers = ["sqls"]
```

### Verify

```bash
hx --health sql
```

## 6. tmux workspace

### ~/.tmux.conf additions

```tmux
# Plugins (via TPM)
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'
set -g @continuum-restore 'on'
```

### Session script (~/bin/pg-sandbox.sh)

```bash
#!/usr/bin/env bash
set -euo pipefail
SESSION="pg"
cd ~/Chat/postgres

tmux new-session -d -s "$SESSION" -n editor
tmux send-keys -t "$SESSION:editor" 'hx .' C-m

tmux new-window -t "$SESSION" -n db
tmux split-window -t "$SESSION:db" -h
tmux split-window -t "$SESSION:db.1" -v
tmux send-keys -t "$SESSION:db.0" 'docker compose logs -f db' C-m
tmux send-keys -t "$SESSION:db.1" 'pgcli postgres://postgres:dev@localhost:5432/sandbox' C-m
tmux send-keys -t "$SESSION:db.2" 'clear' C-m

tmux new-window -t "$SESSION" -n tui
tmux send-keys -t "$SESSION:tui" 'rainfrog' C-m

tmux select-window -t "$SESSION:editor"
tmux attach -t "$SESSION"
```

```bash
chmod +x ~/bin/pg-sandbox.sh
```

## 7. Migrations: Atlas

```bash
brew install ariga/tap/atlas
atlas schema inspect -u "postgres://postgres:dev@localhost:5432/sandbox?sslmode=disable" > schema.hcl
```

Workflow: edit `schema.hcl` declaratively, then `atlas schema apply` plans and applies the diff. CI-friendly.

Alternative (pure SQL): **sqitch**
```bash
brew install sqitch
sqitch init mydb --engine pg
sqitch add init -n 'init schema'
# edit deploy/init.sql, verify/init.sql, revert/init.sql
sqitch deploy db:postgres://postgres:dev@localhost/sandbox
```

## 8. Day-0 acceptance

- [ ] `docker compose up -d` succeeds, `docker compose ps` shows db healthy + postgrest up
- [ ] `pgcli postgres://postgres:dev@localhost/sandbox` connects and `\dx` lists pgvector, postgis, timescaledb, pgmq, pg_graphql
- [ ] `hx init/01-extensions.sql` shows LSP diagnostics, autocompletes
- [ ] `rainfrog` opens and can browse tables
- [ ] `curl http://localhost:3000/` returns PostgREST OpenAPI JSON
- [ ] `pg-sandbox.sh` brings up the full tmux layout
- [ ] `atlas schema inspect` or `sqitch` works against the db
