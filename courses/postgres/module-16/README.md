# Module 16 - Operations (L76-L79)

Prereq: Modules 0-10. This module teaches the bare minimum to run Postgres in production without shooting your foot.

---

## L76 - pg_dump backups

### Concept

`pg_dump` writes a logical backup (SQL statements) of a database.

### Steps

From your host:
```bash
docker exec pg pg_dump -U postgres -d bookshelf -Fc -f /tmp/bookshelf.dump
docker cp pg:/tmp/bookshelf.dump ./bookshelf.dump
ls -lh bookshelf.dump
```

- `-Fc` = custom format, compressed, good for `pg_restore`
- `-Fp` = plain SQL (can `psql < file`)
- `-Fd` = directory format (parallel-safe)

### Full-server dump

```bash
docker exec pg pg_dumpall -U postgres -f /tmp/all.sql
```

### What pg_dump does NOT include

- Other databases (use `pg_dumpall`)
- Cluster-level state (roles, tablespaces - need `pg_dumpall --globals-only`)
- Physical replication state
- Large objects (normally included; check flags)

### Exercises

1. Dump `bookshelf`, delete a table, restore from dump.
2. Compare the size of `-Fc` vs `-Fp`.

### Check-in

Show successful pg_dump and dump file size.

---

## L77 - Restore from backup

### Steps

Create a fresh target database:
```sql
CREATE DATABASE bookshelf_restored;
```

Restore:
```bash
docker cp ./bookshelf.dump pg:/tmp/bookshelf.dump
docker exec pg pg_restore -U postgres -d bookshelf_restored /tmp/bookshelf.dump
```

Verify:
```bash
docker exec -it pg psql -U postgres -d bookshelf_restored -c 'SELECT count(*) FROM books;'
```

### Point-in-time recovery (PITR) concept

`pg_dump` is logical, not PITR. Real PITR uses base backups + WAL archiving:
- Use `pg_basebackup` for a physical snapshot
- Archive WAL files continuously
- Restore by replaying WAL to a chosen timestamp

Tools that automate this: pgBackRest, barman, WAL-G. Use one in production.

### Exercises

1. Accidentally (on purpose) DROP TABLE books. Restore just that table from the dump.
2. Read about pgBackRest or WAL-G.

### Check-in

Show count of restored books matching the original.

---

## L78 - pg_stat_statements

### Concept

Tracks execution statistics for every SQL statement. Essential for finding slow queries.

### Steps

```sql
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

(Also needs `shared_preload_libraries = 'pg_stat_statements'` in postgresql.conf for best results; the official Postgres image usually has it enabled.)

Run some queries, then:
```sql
SELECT
  round(total_exec_time::numeric, 2) AS total_ms,
  calls,
  round(mean_exec_time::numeric, 2)  AS mean_ms,
  left(query, 80) AS query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

Shows your worst offenders by total time spent.

### Resetting

```sql
SELECT pg_stat_statements_reset();
```

Before a test to focus only on new activity.

### Exercises

1. Run a few random slow queries. Find them in pg_stat_statements.
2. Identify the query with the highest mean time.

### Check-in

Paste top 3 by total_ms.

---

## L79 - Connection pooling (PgBouncer)

### Concept

Postgres is one process per connection. Opening 10k connections = bad. Pooling multiplexes many client connections onto few DB connections.

Two main modes:
- **Transaction pooling** (most apps): each transaction gets a connection from the pool, returned on commit. Incompatible with prepared statements, LISTEN/NOTIFY.
- **Session pooling**: like having a direct connection; less throughput win.

### Steps

Run PgBouncer in Docker:
```bash
docker run -d \
  --name pgbouncer \
  --link pg:db \
  -e DATABASES_HOST=db \
  -e DATABASES_USER=postgres \
  -e DATABASES_PASSWORD=dev \
  -e DATABASES_DBNAME=bookshelf \
  -e POOL_MODE=transaction \
  -p 6432:6432 \
  edoburu/pgbouncer
```

Connect through it:
```bash
psql postgres://postgres:dev@localhost:6432/bookshelf
```

### When to pool

- You run a backend with >100 concurrent clients
- You run serverless functions (connections cold-start)
- Always in production if scale matters

### Supabase / Neon

Both have built-in pooling. You connect to a pooler URL; they handle the rest.

### Exercises

1. Start PgBouncer, benchmark concurrent connections vs direct Postgres.
2. Try a `LISTEN` through PgBouncer in transaction mode; it'll fail. Why?

### Check-in

Show successful connection through pgbouncer and a simple query.

---

## Module 16 completion criteria

- [ ] You run pg_dump regularly and know how to pg_restore
- [ ] You know pg_dump isn't PITR and what tool to use instead
- [ ] `pg_stat_statements` is enabled in your DBs
- [ ] You pool connections in production (PgBouncer or managed provider)
