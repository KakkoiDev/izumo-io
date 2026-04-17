# Postgres Mastery Plan: 80/20 Beginner -> Pro

Source: curated from 2026 research + video "I replaced my entire tech stack with Postgres".
Owner: cyril.antoni. Cadence: living doc, update after each tier completion.

## Goal

Compress months of Postgres learning into a Pareto-optimized curriculum. Outcome: ship a production-grade Postgres-only backend. Timeline: 10-14 weeks part-time.

## Tier 0: Environment Setup (Day 0-2)

See `postgres-env-setup.md` for full commands and configs.

- Dockerized Postgres 17 with all extensions preloaded (ivanlonel/postgis-with-extensions)
- psql + `~/.psqlrc` polished
- pgcli as daily driver (autocomplete)
- rainfrog as exploration TUI
- Helix + pgtools LSP for editing
- tmux layout: editor / logs / pgcli / shell
- Atlas or sqitch for migrations

## Tier 1: Foundations (Weeks 1-3) - THE critical 20%

Unlocks ~60% of Postgres value on its own.

1. SQL core: SELECT, JOIN (inner/left/lateral), WHERE, GROUP BY, HAVING, ORDER BY, LIMIT
2. Advanced SQL: CTEs (WITH, recursive), window functions (ROW_NUMBER, RANK, LAG/LEAD, SUM OVER), subqueries, UNION/INTERSECT/EXCEPT
3. Schema design: 1NF-3NF, PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL, generated columns
4. Data types: text, numeric/int/bigint, timestamptz (always tz!), uuid, boolean, interval, array, jsonb
5. Transactions: BEGIN/COMMIT/ROLLBACK, savepoints, isolation levels (READ COMMITTED vs REPEATABLE READ vs SERIALIZABLE)
6. psql mastery: \d family, \timing, \watch, \copy, \gexec, \e
7. EXPLAIN ANALYZE: read plans, identify seq scans, nested loops vs hash joins

Drills:
- Build a library schema (books, authors, loans) from scratch
- Write every query 3 ways (subquery / CTE / window) and compare plans
- Kill a query with a missing index, add it, compare EXPLAIN

## Tier 2: Performance + Indexing (Weeks 4-5)

Separates hobbyist from pro.

1. Index types:
   - B-tree (default, equality/range)
   - GIN (JSONB, full-text, arrays)
   - GiST (geo, range types, exclusion constraints)
   - BRIN (time-series, sequential) - 1000x smaller than B-tree
   - Hash (rarely, equality only)
2. Index strategy: covering (INCLUDE), partial (WHERE), expression (ON (lower(email))), composite column order
3. EXPLAIN (ANALYZE, BUFFERS): cost estimates vs actuals, row misestimates, buffer hits, loop counts
4. VACUUM / ANALYZE: MVCC bloat, dead tuples, autovacuum tuning
5. Connection pooling: PgBouncer (transaction pooling mode)
6. pg_stat_statements: find slow queries

Drills:
- Take a 10M-row table, make a query slow, speed up 1000x with one index
- Create 4 index types on the same column, compare size and query plan

## Tier 3: Swiss Army Extensions (Weeks 6-9)

Replace your entire stack.

1. JSONB deep-dive: `->`, `->>`, `@>`, `?`, `?|`, `?&`, `jsonb_path_query`, GIN indexes, partial GIN with jsonb_path_ops
2. Full-text search: tsvector, tsquery, `@@`, ts_rank_cd, pg_trgm for fuzzy + autocomplete, generated tsvector columns
3. pgvector + pgvectorscale: vector type, HNSW vs IVFFlat, cosine vs L2 vs inner product, hybrid search w/ metadata filters, StreamingDiskANN
4. PostGIS: geography vs geometry, SRID 4326, ST_DWithin, ST_Contains, ST_Intersects, GiST indexes
5. TimescaleDB: hypertables, continuous aggregates, compression policies, retention
6. pgmq: `send/read/archive`, visibility timeout - compare to raw FOR UPDATE SKIP LOCKED
7. Materialized views: CREATE MATERIALIZED VIEW, REFRESH CONCURRENTLY, required unique index
8. Partitioning: declarative RANGE/LIST/HASH, pg_partman automation

Drills:
- Store Stripe webhook payloads as JSONB, index specific paths, query in <1ms
- Build a typo-tolerant search bar with tsvector + pg_trgm rank combo
- Embed 100k docs, find top-5 similar with metadata filter in one query
- Build a job queue with pgmq, run 10 workers concurrently, measure throughput

## Tier 4: Postgres as the Entire Backend (Weeks 10-12)

1. Row-Level Security (RLS): CREATE POLICY, `current_setting('jwt.claims.user_id')`, FORCE ROW LEVEL SECURITY, policy testing
2. PL/pgSQL: functions, triggers, SECURITY DEFINER/INVOKER, NOTIFY/LISTEN for pub/sub
3. PostgREST: auto REST from schema, JWT auth, roles (anon, authenticated), resource embedding, RPC functions
4. pg_graphql: auto GraphQL from schema, FK relationships, Relay-style pagination
5. Realtime: LISTEN/NOTIFY limits, logical replication slots, wal2json, Supabase Realtime
6. Auth: pgcrypto for bcrypt, JWT verification with pgjwt or in PostgREST, magic links patterns
7. Backup + HA: pg_dump basics, WAL archiving, PITR, streaming replication, Patroni for failover
8. Observability: pg_stat_statements, pg_stat_activity, auto_explain, query_id

Drills:
- Build a multi-tenant schema where tenants can't see each other's rows (RLS only)
- Expose a REST API + GraphQL from the same schema with one JWT
- Broadcast row changes to clients via LISTEN/NOTIFY

## Tier 5: Capstone (Weeks 13-14+)

Ship a real backend using only Postgres. Project: "Local-first SaaS tracker" with:
- User accounts (RLS-isolated multi-tenant)
- Full-text search across notes (tsvector + pg_trgm)
- AI semantic search over notes (pgvector)
- Geo-tagged entries (PostGIS)
- Event log (TimescaleDB hypertable)
- Background jobs (pgmq)
- Auto REST API (PostgREST) + GraphQL (pg_graphql)
- Live updates (LISTEN/NOTIFY)
- Deployed on Neon or Supabase

Acceptance: 1000 concurrent requests on a single instance, <100ms p95 for all endpoints.

## Verification Checklist (pro threshold)

- [ ] Read any EXPLAIN ANALYZE plan, identify bottleneck in <60 seconds
- [ ] Pick the right index type for any workload without looking it up
- [ ] Write an RLS policy that survives a red-team review
- [ ] Build a working REST+GraphQL API from a schema in <30 minutes
- [ ] Capstone backend handles 1000+ concurrent requests on a single Neon instance
- [ ] Fluent in JSONB, tsvector, pgvector, and at least one of PostGIS/TimescaleDB

## Progress Log

- 2026-04-17: Plan drafted. Tier 0 environment setup not yet started.
