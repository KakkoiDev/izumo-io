# Module 5 - Performance 101 (L26-L31)

Prereq: comfortable with JOINs and aggregation.

---

## L26 - What is an index? (no SQL)

### Concept

A table is stored as rows on disk. Without an index, finding one row means reading every row (sequential scan).

An index is a separate data structure sorted by one or more columns. Postgres looks up in the index (log N, very fast), gets a pointer to the row, fetches just that row.

### Analogy

A book without an index: to find "Postgres" you flip every page.
A book with an index at the back: you look up "Postgres", find "page 213", jump there.

### Trade-offs

- Reads: much faster for matching queries
- Writes: slower (index must be updated on every insert/update/delete)
- Storage: indexes take disk space (sometimes as big as the table)

Rule: index what you query on, not "everything".

### Index types (preview)

- B-tree: default, equality and range
- GIN: full-text, arrays, JSONB
- GiST: geo, range types
- BRIN: huge, sorted-by-insertion data (time-series)
- Hash: equality-only, rarely used

### No steps. No check-in. Read again if unclear.

---

## L27 - Your first index

### Steps

Make a big enough table to see the difference. Inside `bookshelf`:

```sql
DROP TABLE IF EXISTS events;
CREATE TABLE events (
  id         bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id    int NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  payload    text
);

INSERT INTO events (user_id, payload)
SELECT (random() * 10000)::int, 'event ' || g
FROM generate_series(1, 1000000) g;
```

(Takes ~10 seconds.)

Query without index, timed:
```sql
\timing
SELECT count(*) FROM events WHERE user_id = 42;
```

Likely 50-200 ms depending on hardware.

Add an index:
```sql
CREATE INDEX events_user_id_idx ON events(user_id);
```

Rerun:
```sql
SELECT count(*) FROM events WHERE user_id = 42;
```

Should be under 1 ms.

### Anatomy of the CREATE INDEX line

- `events_user_id_idx` - name. Convention: `<table>_<column>_<type>_idx`.
- `ON events(user_id)` - what to index.

Multi-column:
```sql
CREATE INDEX events_user_time_idx ON events(user_id, created_at);
```

Column order matters: index is useful when your WHERE filters on the first column (and optionally the next).

### Exercises

1. Drop the index, rerun the query, confirm slowdown.
2. Recreate it. Try `WHERE created_at > now() - interval '1 day'` - why doesn't the `user_id` index help here?
3. Create an index on `created_at`. Rerun the time query.

### Check-in

Paste the 3 timings: no index, user_id index, created_at index.

---

## L28 - EXPLAIN

### Concept

`EXPLAIN <query>` shows the planned execution without running.

### Steps

```sql
EXPLAIN SELECT * FROM events WHERE user_id = 42;
```

Look for nodes:
- `Seq Scan on events` - no index used. Expensive if big table.
- `Index Scan using events_user_id_idx on events` - uses the index.
- `Bitmap Heap Scan` / `Bitmap Index Scan` - combines multiple indexes or many matching rows.

Estimated cost:
```
Index Scan using events_user_id_idx on events  (cost=0.43..8.45 rows=1 width=...)
```

- `cost=0.43..8.45`: startup cost .. total cost. Postgres units, not ms.
- `rows=1`: estimated row count.

### When Postgres chooses Seq Scan on purpose

If you're asking for "most rows", sequential is faster than bouncing around via index. Postgres picks based on estimated cost.

### Exercises

1. `EXPLAIN SELECT * FROM events;` - always a Seq Scan.
2. `EXPLAIN SELECT * FROM events WHERE user_id > 5000;` - large predicate, likely Seq Scan.
3. `EXPLAIN SELECT * FROM events ORDER BY created_at LIMIT 10;` - hopefully uses the `created_at` index.

### Check-in

Paste the output of exercise 3.

---

## L29 - EXPLAIN ANALYZE

### Concept

`EXPLAIN ANALYZE` actually runs the query and reports real times + rows.

Warning: `ANALYZE` executes the query. For `DELETE`/`UPDATE`, use a transaction to rollback, or just use `EXPLAIN` without `ANALYZE`.

### Steps

```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM events WHERE user_id = 42;
```

Key fields:
- `actual time=X..Y` - real timing
- `rows=N` - real rows
- `Buffers: shared hit=X read=Y` - pages from cache (hit) vs disk (read)
- Total `Planning Time` and `Execution Time` at the bottom

### Spotting misestimates

If estimated `rows=1` but actual `rows=500000`, the planner's stats are stale. Run:
```sql
ANALYZE events;
```

(That's the maintenance command, not the query hint. Confusingly same word.)

### Exercises

1. Run the query twice. First run reads from disk (`read=`), second from cache (`hit=`). Observe.
2. Add 100 more events with `user_id = 42`. Rerun. Stats may be stale. ANALYZE and retry.

### Check-in

Paste output including both `Planning Time` and `Execution Time`.

---

## L30 - When an index hurts

### Concept

Every index adds write cost. 10 indexes on a table means 10 structures to update per insert.

### Steps

Benchmark insert with and without indexes:

```sql
-- Without extra indexes (you have pk + user_id + created_at already)
\timing
INSERT INTO events (user_id, payload)
SELECT (random() * 10000)::int, 'b ' || g
FROM generate_series(1, 100000) g;
```

Note the time. Add more indexes:
```sql
CREATE INDEX events_payload_idx ON events(payload);
```

Re-run the insert. Slower.

### Rule

Add indexes for read paths that matter. Drop unused ones:
```sql
SELECT indexrelname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0;
```

Indexes with `idx_scan = 0` are candidates to drop.

### Exercises

1. Drop `events_payload_idx`, rerun inserts.
2. Find all unused indexes in your DB.

### Check-in

Paste insert timings before and after the extra index.

---

## L31 - Partial and expression indexes

### Concept

- **Partial index**: index only rows matching a predicate. Smaller, faster.
- **Expression index**: index the result of an expression (e.g., lower(email)).

### Partial index

```sql
CREATE INDEX events_recent_idx ON events(created_at)
WHERE created_at > '2026-04-01';
```

Useful when queries only ever look at recent rows.

### Expression index

```sql
CREATE TABLE users (
  id    bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email text NOT NULL
);

INSERT INTO users (email) VALUES ('Alice@X.com'), ('bob@X.COM');

-- Without expression index, case-insensitive search won't use an index:
EXPLAIN SELECT * FROM users WHERE lower(email) = 'alice@x.com';

CREATE INDEX users_email_lower_idx ON users(lower(email));

EXPLAIN SELECT * FROM users WHERE lower(email) = 'alice@x.com';
-- Now uses the index.
```

### Exercises

1. Build a partial index on `events` where `user_id < 100` (VIPs). Query with and without.
2. Build an expression index on `substr(payload, 1, 10)`.

### Check-in

Paste EXPLAIN output showing the partial index being used.

---

## Module 5 completion criteria

- [ ] You know that indexes speed reads but slow writes
- [ ] You read an EXPLAIN plan and spot Seq Scan vs Index Scan
- [ ] You spot misestimates and know to `ANALYZE`
- [ ] You create partial and expression indexes when they fit
