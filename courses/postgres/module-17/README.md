# Module 17 - Capstone

Prereq: Modules 0-16. You know enough to design and build.

Goal: ship one real multi-tenant backend backed only by Postgres.

---

## Project: "Notesy" - multi-tenant notes app

### Spec

- Users sign up with email + password
- Users have one or more workspaces (tenants)
- Each workspace contains notes
- Notes have: title, body, tags, optional location (lat/lng), created_at, updated_at
- Full-text search across user's notes
- AI semantic search (pgvector) across user's notes
- Event log of every action (hypertable)
- Background jobs: re-embed notes when body changes (pgmq or FOR UPDATE SKIP LOCKED)
- REST API (PostgREST) + GraphQL (pg_graphql)
- Live updates via LISTEN/NOTIFY

### Deliverables

- Schema in sqitch (or Atlas)
- Initial seed + demo data
- RLS policies isolating per workspace
- Index strategy documented
- README with run instructions

## Build order

### Phase 1 - Skeleton (1-2 hours)

1. `docker-compose.yml` with:
   - Postgres (timescale-ha image, so you get TimescaleDB + pgvector + PostGIS in one)
   - PostgREST
   - PgBouncer
2. Init script enables extensions
3. Create schema via sqitch:
   - `users(id, email unique, password_hash, created_at)`
   - `workspaces(id, name)`
   - `memberships(user_id, workspace_id, role, PRIMARY KEY (user_id, workspace_id))`
4. Auth: `api.signup(email, password)` RPC that inserts user and returns a JWT
5. Auth: `api.login(email, password)` RPC
6. Verify: sign up, log in, get JWT, ping a protected endpoint

### Phase 2 - Notes core (1-2 hours)

1. `notes(id, workspace_id, author_id, title, body, tags text[], location geography?, search tsvector generated, emb vector(1536)?, created_at, updated_at)`
2. Indexes: GIN on search, GIN on tags, HNSW on emb (cosine), GiST on location, btree on (workspace_id, created_at desc)
3. Trigger: updated_at
4. RLS: user must be a member of the workspace to read/write

### Phase 3 - Search (1-2 hours)

1. FTS endpoint: `api.search_notes(q text)` returns notes in user's workspaces matching FTS + trigram fuzzy
2. Vector endpoint: `api.similar_notes(emb vector, limit int)` returns semantically close notes (user-scoped via RLS)
3. Hybrid endpoint: combines both with a score

### Phase 4 - Events + jobs (1-2 hours)

1. `events` hypertable: `ts, workspace_id, user_id, kind, data jsonb`
2. Trigger on notes INSERT/UPDATE/DELETE -> insert into events + pg_notify
3. `jobs` table (or pgmq queue) for "recompute embedding"
4. Worker loop (bash or Node) that dequeues, calls embedding API, updates note

### Phase 5 - Polish (1-2 hours)

1. Rate limit via a simple check on events table
2. pg_dump cron (you don't schedule it yet, just have the command)
3. README: setup, seed, dev flow

## Acceptance criteria

- [ ] A new user can sign up, log in, create a workspace, create notes
- [ ] Notes are visible only to members of the workspace
- [ ] FTS returns results in <30ms for 100k notes
- [ ] Vector search returns top-5 similar in <100ms
- [ ] PostgREST is the only backend service (plus the worker)
- [ ] All schema changes go through sqitch
- [ ] You can explain every EXPLAIN ANALYZE plan in your app
- [ ] RLS cannot be bypassed (verified with a malicious JWT test)

## Extensions to attempt if you breeze through

- Deploy on Neon (serverless)
- Add real-time subscription endpoint via logical replication
- Add audit log table with retention policy
- Add admin analytics dashboard via materialized view + continuous aggregate

## What success looks like

When you're done, you have a real backend with:
- ~300 lines of SQL
- ~0 lines of CRUD boilerplate (PostgREST handles it)
- <5 running services (db, postgrest, pgbouncer, worker, maybe a static frontend)
- A clear mental model of why each line exists

From this capstone you can iterate into any project. The pattern scales from weekend tools to SOC2 SaaS backends.
