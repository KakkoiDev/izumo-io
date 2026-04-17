# Postgres Stack Reference (2026)

Validation of the "replace your stack with Postgres" pattern against 2026 state of art, plus the recommended extension set.

## Video-stack validation

| Capability | Video says | 2026 reality | Better alternative |
|-----------|-----------|--------------|--------------------|
| NoSQL documents | JSONB + GIN | Still optimal | None |
| Message queue | `FOR UPDATE SKIP LOCKED` | Works but DIY | **pgmq** extension (SQS-like, production-ready) |
| Search engine | tsvector/tsquery + pg_trgm | Strong for most apps | **paradedb/pg_search** (BM25, closer to Elasticsearch) when you need ES-grade |
| Vector DB | pgvector + HNSW | Excellent <=10M rows | **pgvectorscale** (StreamingDiskANN) for >10M; **pgai** for in-SQL LLM calls |
| Geo | PostGIS + GiST | Industry gold standard | None |
| Time-series | Partitioning + BRIN | Works manually | **TimescaleDB** hypertables (auto chunking / compression / retention) |
| Cached aggregates | Materialized views + CONCURRENTLY | Still the pattern | Add **continuous aggregates** from Timescale if time-series |
| Backend layer | PostgREST / pg_graphql + RLS | Production-proven | **Supabase** bundles both + auth + storage + realtime |

Bottom line: video is directionally correct. The modern default stack is Postgres core + pgmq + pgvector(+scale) + PostGIS + TimescaleDB + PostgREST/pg_graphql + RLS, optionally wrapped in Supabase.

## Recommended extension set (copy-paste into init.sql)

```sql
-- Core utilities
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Search
CREATE EXTENSION IF NOT EXISTS pg_trgm;        -- fuzzy + autocomplete
CREATE EXTENSION IF NOT EXISTS unaccent;       -- accent-insensitive search

-- Vectors / AI
CREATE EXTENSION IF NOT EXISTS vector;         -- pgvector
CREATE EXTENSION IF NOT EXISTS vectorscale;    -- pgvectorscale (StreamingDiskANN)
CREATE EXTENSION IF NOT EXISTS ai CASCADE;     -- pgai (call LLMs from SQL)

-- Geo
CREATE EXTENSION IF NOT EXISTS postgis;

-- Time-series
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Queues
CREATE EXTENSION IF NOT EXISTS pgmq CASCADE;

-- Partitioning automation
CREATE EXTENSION IF NOT EXISTS pg_partman;

-- API layer
CREATE EXTENSION IF NOT EXISTS pg_graphql;
-- PostgREST runs as a separate process, not an extension
```

## Decision matrix: which extension for which problem

| Problem | Use | Avoid |
|---------|-----|-------|
| Flexible schema for semi-structured data | JSONB + GIN | Separate MongoDB |
| Background jobs, retries, visibility timeout | pgmq | Separate Redis/RabbitMQ until >10k jobs/s |
| Small vector search (<10M rows) | pgvector HNSW | Pinecone, Weaviate |
| Large vector search (>10M rows) | pgvectorscale StreamingDiskANN | Pinecone |
| In-SQL embeddings / LLM calls | pgai | Python glue code |
| Full-text search | tsvector + pg_trgm | Elasticsearch until ES-specific features needed |
| Elasticsearch-grade search | paradedb/pg_search (BM25) | Self-hosted ES cluster |
| Geo queries (contains, within, nearest) | PostGIS + GiST | Separate GIS system |
| Append-only time-series | TimescaleDB hypertables | InfluxDB / separate TSDB |
| Billions of events, hot/warm/cold | TimescaleDB + compression + retention | DIY partitioning |
| REST API from schema | PostgREST | Hand-written Node/Python CRUD |
| GraphQL API from schema | pg_graphql | Hasura for more features |
| Multi-tenant auth | RLS + JWT | Middleware auth |
| Dashboards | Materialized views (CONCURRENTLY refresh) | Snowflake for <100GB |

## When NOT to use Postgres-only

- Millions of telemetry events/sec requiring horizontal sharding
- Sub-millisecond in-memory caching for millions of concurrent websocket connections
- Global edge replication with <50ms reads from any region
- Cross-region multi-master writes

Below those thresholds, Postgres-only is the smartest cost-effective bet.

## Hosting options (2026)

| Provider | Best for | Key feature |
|----------|---------|-------------|
| **Neon** | Serverless, dev/staging branching | Git-like branches, scale-to-zero |
| **Supabase** | Fast backend with auth/realtime/storage | Full BaaS, SOC2+HIPAA |
| **Tiger Data** (ex-Timescale) | Time-series-heavy workloads | TimescaleDB managed |
| **Crunchy Bridge** | Production Postgres + PostGIS | Tight Postgres focus |
| **RDS / Cloud SQL / Azure** | Enterprise compliance | Battle-tested, expensive |
| **Self-hosted on Hetzner** | Cost-optimized, full control | ~10x cheaper than RDS |
