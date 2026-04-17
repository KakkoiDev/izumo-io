# Module 14 - Time-series (L66-L68) [optional track]

Prereq: Module 5 (indexes).

Two approaches: native partitioning + BRIN (built in), or TimescaleDB (extension).

---

## L66 - Partitioning by hand

### Concept

Split a giant table into physical chunks based on a column. Queries hit only relevant chunks.

### Steps

```sql
CREATE TABLE metrics (
  ts     timestamptz NOT NULL,
  name   text NOT NULL,
  value  double precision NOT NULL
) PARTITION BY RANGE (ts);

CREATE TABLE metrics_2026_04 PARTITION OF metrics
  FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');
CREATE TABLE metrics_2026_05 PARTITION OF metrics
  FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');
```

Insert normally:
```sql
INSERT INTO metrics VALUES ('2026-04-15 10:00+00', 'cpu', 0.4);
```

Postgres routes to the right partition.

### BRIN index

For sorted-by-insertion data, BRIN is ~1000x smaller than B-tree:
```sql
CREATE INDEX metrics_ts_brin_idx ON metrics USING BRIN (ts);
```

BRIN stores min/max per block range. Queries skip whole ranges.

### Automating partitions: pg_partman

Most people don't create partitions by hand monthly. `pg_partman` does it.

### Exercises

1. Create a monthly-partitioned `events_ts` table.
2. Insert data spanning two months; verify each row lands in its partition (check `pg_class`).
3. Add a BRIN index on ts.

### Check-in

Show the partition assignment.

---

## L67 - Install TimescaleDB

### Concept

TimescaleDB automates partitioning, adds compression, continuous aggregates, retention policies. Much smoother than hand-rolling.

### Steps

Switch image:
```bash
docker stop pg && docker rm pg
docker run -d \
  --name pg \
  -e POSTGRES_PASSWORD=dev \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  timescale/timescaledb-ha:pg17
```

(`-ha` bundles TimescaleDB + pgvector + PostGIS.)

Enable:
```sql
CREATE EXTENSION IF NOT EXISTS timescaledb;
```

### Exercises

1. `\dx` to confirm.
2. `SELECT timescaledb_experimental.version();` or `SELECT default_version FROM pg_available_extensions WHERE name='timescaledb';`

### Check-in

Paste `\dx` showing timescaledb enabled.

---

## L68 - Hypertables

### Concept

A hypertable transparently partitions by time. You query it as one table; Timescale handles chunking.

### Steps

```sql
CREATE TABLE readings (
  ts     timestamptz NOT NULL,
  sensor text NOT NULL,
  value  double precision NOT NULL
);

SELECT create_hypertable('readings', 'ts', chunk_time_interval => interval '7 days');
```

Insert:
```sql
INSERT INTO readings
SELECT now() - (g * interval '1 hour'), 'sensor_' || (g % 5), random()
FROM generate_series(1, 10000) g;
```

Query:
```sql
SELECT time_bucket('1 day', ts) AS day, sensor, avg(value)
FROM readings
GROUP BY day, sensor
ORDER BY day, sensor;
```

### Continuous aggregates

Pre-compute rollups that refresh in the background:
```sql
CREATE MATERIALIZED VIEW readings_daily
WITH (timescaledb.continuous) AS
SELECT time_bucket('1 day', ts) AS day, sensor, avg(value) AS avg_val
FROM readings
GROUP BY day, sensor;

-- Set refresh policy
SELECT add_continuous_aggregate_policy('readings_daily',
  start_offset => INTERVAL '1 month',
  end_offset   => INTERVAL '1 hour',
  schedule_interval => INTERVAL '1 hour');
```

### Compression

```sql
ALTER TABLE readings SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'sensor'
);

SELECT add_compression_policy('readings', INTERVAL '7 days');
```

Chunks older than 7 days get compressed automatically.

### Retention

```sql
SELECT add_retention_policy('readings', INTERVAL '1 year');
```

### Exercises

1. Create a hypertable, insert 1M rows, build a continuous aggregate, query it.
2. Compare query speed on raw vs aggregate.

### Check-in

Paste timings from exercise 2.

---

## Module 14 completion criteria

- [ ] You understand native partitioning + BRIN as the no-extension path
- [ ] You install TimescaleDB when the workload justifies it
- [ ] You create hypertables, continuous aggregates, compression policies
