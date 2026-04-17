# Postgres Resources (curated, 2026)

Only entries I'd personally trust. Each has a reason.

## Canonical

- https://www.postgresql.org/docs/current/ - the manual. Use the search box first, Google second.
- https://wiki.postgresql.org/ - historical context, gotchas

## Learning (beginner -> intermediate)

- https://www.postgresqltutorial.com/ - free, well-indexed, always up to date
- Coursera "PostgreSQL for Everybody" by Chuck Severance - gentle starter, free audit
- https://pgexercises.com/ - SQL-only drills, fast feedback
- https://roadmap.sh/sql - visual roadmap if you like checklists

## Indexing / performance

- https://use-the-index-luke.com/ - Markus Winand's canonical work. Free. Read cover-to-cover.
- "PostgreSQL 14 Internals" by Egor Rogov - free PDF. The best deep dive on MVCC, planner, vacuum.
- https://pganalyze.com/blog - query plan reasoning, real-world tuning
- https://explain.dalibo.com/ - drop an EXPLAIN plan, get a visual breakdown
- https://pgmustard.com/ - paid, explains EXPLAIN in plain English

## Books

- "The Art of PostgreSQL" by Dimitri Fontaine - best intermediate book. Teaches SQL as a language, not a pile of CRUD.
- "Designing Data-Intensive Applications" by Martin Kleppmann - not Postgres-specific but essential context
- "PostgreSQL 14 Internals" (Rogov, free) - internals bible

## Extensions and deep dives

- https://www.tigerdata.com/blog (formerly Timescale) - best extension deep-dives, vector, time-series
- https://supabase.com/blog - real-world patterns for RLS, pgvector, realtime
- https://www.crunchydata.com/blog - PostGIS, operations
- https://github.com/dhamaniasad/awesome-postgres - extension directory

## API layer

- https://postgrest.org/ - official docs, concise and complete
- https://supabase.com/docs/guides/graphql - pg_graphql usage
- https://postgrest.org/en/stable/references/auth.html - JWT auth patterns
- https://www.youtube.com/@supabase - PostgREST + RLS walk-throughs

## Queues, vectors, geo, time-series

- https://github.com/pgmq/pgmq - queue extension, read the README
- https://github.com/pgvector/pgvector - vector type + HNSW
- https://github.com/timescale/pgvectorscale - StreamingDiskANN for large vector sets
- https://github.com/timescale/pgai - LLM calls from SQL
- https://postgis.net/docs/ - PostGIS reference
- https://docs.tigerdata.com/ - TimescaleDB (hypertables, continuous aggregates)

## Tooling

- https://github.com/dbcli/pgcli - autocomplete CLI
- https://github.com/achristmascarl/rainfrog - full TUI
- https://github.com/jorgerojas26/lazysql - multi-DB TUI
- https://harlequin.sh/ - Textual-based SQL IDE
- https://atlasgo.io/ - declarative migrations
- https://sqitch.org/ - pure SQL migrations
- https://github.com/supabase/pg_graphql - GraphQL extension
- https://pgtools.dev/ - Postgres language server (Helix/VSCode)

## Hosting (2026)

- https://neon.tech/ - serverless, branching, scale-to-zero
- https://supabase.com/ - full BaaS on Postgres
- https://www.tigerdata.com/ - managed TimescaleDB
- https://www.crunchydata.com/products/crunchy-bridge - production Postgres + PostGIS
- Self-hosted on Hetzner - ~10x cheaper than RDS if you can operate it

## Community

- https://news.ycombinator.com/ - search "postgres" weekly
- https://www.reddit.com/r/PostgreSQL/ - Q&A, release discussion
- https://planet.postgresql.org/ - blog aggregator, zero-fluff
- Postgres Slack (community.postgresql.org)
- https://x.com/garrrikkotua, https://x.com/adentaylor, https://x.com/brianlikespg - devs worth following

## Video

- https://www.youtube.com/@hussein-nasser - weekly deep dives
- PGCon / PGConf recordings on YouTube - conference talks
- https://www.youtube.com/@Supabase - practical walk-throughs
