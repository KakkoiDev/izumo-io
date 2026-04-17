# Postgres from Zero

**80 lessons, 18 modules. From your first `docker run postgres:17` to shipping a production-grade Postgres-only backend.**

## Overview

A deep-dive reference course for learners who finished the KakkoiSchool website T-lessons (especially T19 SQLite, T29 Nest.js data) and want to go further. Treats Postgres not just as "a SQL database" but as a full application platform: queries, indexes, transactions, JSONB, full-text search, vectors, row-level security, and Postgres-as-backend via PostgREST / pg_graphql.

**Level**: Beginner-friendly. No prior SQL required.
**Timeline**: 10-14 weeks part-time.
**Format**: Self-contained markdown lessons. Each module includes hands-on steps, "break things on purpose" drills, and a check-in you paste back to your teacher.

## Teaching philosophy

1. **No tool until you need it.** Start with `postgres:17`; add extensions only when a real problem demands one.
2. **You type everything.** Copy-paste builds no muscle memory.
3. **Errors are the curriculum.** Every module has a "break things on purpose" lesson.
4. **One concept per lesson.** Short lessons > long ones.
5. **Check in before moving on.** Paste output; teacher confirms understanding.
6. **Self-contained lessons.** Each module references prereqs so you can resume any time.

## Prerequisites

- Docker installed and running
- A terminal you are comfortable in
- (Optional) Finished [AI Chatbot course](../ai-chatbot/) lesson-07 (SQLite) for context

## Tech stack

- **Postgres 17** (Docker image)
- **psql** (CLI, primary interface while learning)
- **pgcli / rainfrog** (introduced mid-course)
- Extensions introduced just-in-time: `pg_trgm`, `pgvector`, `PostGIS`, `TimescaleDB`, `pg_graphql`, `PostgREST`

See [SETUP.md](./SETUP.md) for the full environment.

## Modules

| Module | Lessons | Topic |
|--------|---------|-------|
| [Module 0](./module-00/) | L01-L05 | First Contact - container, psql, first table, .sql files, persistence |
| [Module 1](./module-01/) | L06-L10 | SQL Fundamentals - data types, NULL, UPDATE/DELETE, ORDER BY, errors |
| [Module 2](./module-02/) | L11-L15 | Multiple Tables - normalization, FKs, INNER/LEFT/self joins |
| [Module 3](./module-03/) | L16-L19 | Aggregation - COUNT/SUM/AVG, GROUP BY, HAVING, DISTINCT |
| [Module 4](./module-04/) | L20-L25 | Advanced Queries - subqueries, CTEs, window functions, LATERAL |
| [Module 5](./module-05/) | L26-L31 | Performance 101 - indexes, EXPLAIN, partial/expression indexes |
| [Module 6](./module-06/) | L32-L35 | Constraints & Integrity - UNIQUE, CHECK, generated columns, upsert |
| [Module 7](./module-07/) | L36-L40 | JSONB - operators, GIN indexes, path queries, trade-offs |
| [Module 8](./module-08/) | L41-L44 | Transactions & Concurrency - isolation, locks, savepoints |
| [Module 9](./module-09/) | L45-L50 | Full-Text Search - tsvector, tsquery, pg_trgm (first extension!) |
| [Module 10](./module-10/) | L51-L54 | Functions & Triggers - SQL/PL-pgSQL, LISTEN/NOTIFY |
| [Module 11](./module-11/) | L55-L58 | Real Tooling - pgcli, rainfrog, .psqlrc, sqitch |
| [Module 12](./module-12/) | L59-L62 | Vectors - pgvector, HNSW indexes, embeddings |
| [Module 13](./module-13/) | L63-L65 | Geo (optional) - PostGIS, geography vs geometry |
| [Module 14](./module-14/) | L66-L68 | Time-series (optional) - partitioning, TimescaleDB hypertables |
| [Module 15](./module-15/) | L69-L75 | Postgres as Backend - RLS, JWT, PostgREST, pg_graphql |
| [Module 16](./module-16/) | L76-L79 | Operations - pg_dump, pg_stat_statements, PgBouncer |
| [Module 17](./module-17/) | L80+ | Capstone - build a full multi-tenant backend end to end |

## Reference docs

- **[SETUP.md](./SETUP.md)** - Docker, psql, pgcli, `.psqlrc`, Helix + pgtools LSP, tmux layout
- **[RESOURCES.md](./RESOURCES.md)** - curated external links (docs, courses, books, tools)
- **[MASTERY-PLAN.md](./MASTERY-PLAN.md)** - 80/20 Pareto-optimized curriculum overview
- **[STACK-2026.md](./STACK-2026.md)** - 2026 Postgres stack reference

## How to use this course

1. Read the module README top-to-bottom.
2. **Type** every command. Don't paste.
3. Do the exercises in order.
4. Hit the check-in, paste the requested output to your teacher (or to Discord).
5. Teacher confirms understanding or re-teaches; tick the lesson in your progress tracker.
6. Move to the next lesson.

Skip lessons only if you can pass the check-in blind.

## Progress tracker

Copy into your personal notes and tick as you go:

```
Module 0:  [ ] L01 [ ] L02 [ ] L03 [ ] L04 [ ] L05
Module 1:  [ ] L06 [ ] L07 [ ] L08 [ ] L09 [ ] L10
Module 2:  [ ] L11 [ ] L12 [ ] L13 [ ] L14 [ ] L15
Module 3:  [ ] L16 [ ] L17 [ ] L18 [ ] L19
Module 4:  [ ] L20 [ ] L21 [ ] L22 [ ] L23 [ ] L24 [ ] L25
Module 5:  [ ] L26 [ ] L27 [ ] L28 [ ] L29 [ ] L30 [ ] L31
Module 6:  [ ] L32 [ ] L33 [ ] L34 [ ] L35
Module 7:  [ ] L36 [ ] L37 [ ] L38 [ ] L39 [ ] L40
Module 8:  [ ] L41 [ ] L42 [ ] L43 [ ] L44
Module 9:  [ ] L45 [ ] L46 [ ] L47 [ ] L48 [ ] L49 [ ] L50
Module 10: [ ] L51 [ ] L52 [ ] L53 [ ] L54
Module 11: [ ] L55 [ ] L56 [ ] L57 [ ] L58
Module 12: [ ] L59 [ ] L60 [ ] L61 [ ] L62
Module 13: [ ] L63 [ ] L64 [ ] L65
Module 14: [ ] L66 [ ] L67 [ ] L68
Module 15: [ ] L69 [ ] L70 [ ] L71 [ ] L72 [ ] L73 [ ] L74 [ ] L75
Module 16: [ ] L76 [ ] L77 [ ] L78 [ ] L79
Module 17: [ ] L80+ (capstone)
```

## Getting started

1. Join Discord: [https://discord.gg/YrtdssGUJa](https://discord.gg/YrtdssGUJa)
2. Read [SETUP.md](./SETUP.md) if you want the full stack up-front (optional - Module 0 gets you running with just Docker).
3. Start with [Module 0](./module-00/).

---

*For general information about Izumo.io, see the [main README](../../README.md). For the self-serve website curriculum, see [kakkoischool.com](https://kakkoischool.com).*
