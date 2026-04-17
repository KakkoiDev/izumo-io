# Module 8 - Transactions & Concurrency (L41-L44)

Prereq: Module 2+. You'll need two psql sessions for some demos.

---

## L41 - BEGIN / COMMIT / ROLLBACK

### Concept

A transaction groups statements. Either all commit together, or all roll back.

### Steps

```sql
BEGIN;
INSERT INTO users (email, name) VALUES ('c@x.com', 'Carol');
INSERT INTO users (email, name) VALUES ('d@x.com', 'Dave');
SELECT count(*) FROM users;  -- see both
ROLLBACK;
SELECT count(*) FROM users;  -- neither persisted
```

Real commit:
```sql
BEGIN;
INSERT INTO users (email, name) VALUES ('e@x.com', 'Eve');
COMMIT;
```

### Autocommit

psql runs each statement in its own transaction by default. `BEGIN` opens a multi-statement transaction.

### Savepoints

```sql
BEGIN;
INSERT INTO users (email, name) VALUES ('f@x.com', 'Frank');
SAVEPOINT s1;
INSERT INTO users (email, name) VALUES ('f@x.com', 'Dup');  -- fails!
ROLLBACK TO SAVEPOINT s1;
INSERT INTO users (email, name) VALUES ('g@x.com', 'Grace');
COMMIT;
```

Frank and Grace commit; the duplicate attempt was cleanly abandoned.

### Exercises

1. Inside BEGIN, delete all users. Rollback. Verify.
2. Use SAVEPOINT to do partial work with one possible failure.

### Check-in

Show before/after counts around a ROLLBACK.

---

## L42 - Isolation levels

### Concept

Isolation controls what one transaction sees of another's in-flight work.

Levels (Postgres supports three, defaults to the middle one):
- **READ COMMITTED** (default): each statement sees committed data as of its start
- **REPEATABLE READ**: all statements in the txn see a consistent snapshot from the txn start
- **SERIALIZABLE**: like REPEATABLE READ but also detects serialization anomalies and aborts

### Demo (two sessions)

Session A:
```sql
BEGIN;
SELECT count(*) FROM users;
```

Session B (without BEGIN):
```sql
INSERT INTO users (email, name) VALUES ('h@x.com', 'Henry');
```

Back in A:
```sql
SELECT count(*) FROM users;  -- sees Henry! (READ COMMITTED)
COMMIT;
```

Retry with REPEATABLE READ:
Session A:
```sql
BEGIN ISOLATION LEVEL REPEATABLE READ;
SELECT count(*) FROM users;
```

Session B: insert another row.

Session A:
```sql
SELECT count(*) FROM users;  -- same count as before (snapshot)
COMMIT;
```

### When to use which

- READ COMMITTED: default, 99% of queries
- REPEATABLE READ: long-running reports that need a consistent view
- SERIALIZABLE: the strictest. Use for financial ops where you can't risk write skew. Be prepared to retry on serialization failures.

### Exercises

1. Reproduce the phantom read demo above.
2. Try SERIALIZABLE with a write skew scenario: two sessions both read then write based on the other's data.

### Check-in

Show two screenshots/paste of the counts diverging between sessions under REPEATABLE READ.

---

## L43 - Row locks and deadlocks

### Concept

`SELECT ... FOR UPDATE` locks rows against concurrent updates. Useful for coordinated state changes.

### Steps

Session A:
```sql
BEGIN;
SELECT * FROM users WHERE id = 1 FOR UPDATE;
```

Session B:
```sql
BEGIN;
UPDATE users SET name = 'New' WHERE id = 1;  -- blocks!
```

A:
```sql
COMMIT;  -- B now proceeds
```

### `FOR UPDATE SKIP LOCKED`

The queue-friendly variant. Worker A locks a row; Worker B, looking at the same candidate, just skips it and moves on. Used for "pull one job off the queue":

```sql
SELECT id FROM jobs
WHERE status = 'pending'
ORDER BY id
FOR UPDATE SKIP LOCKED
LIMIT 1;
```

Two workers running this concurrently each get a different row. Foundation of DIY queues (and later, pgmq).

### Deadlocks

If A locks row 1 then waits on row 2, while B locks row 2 then waits on row 1: deadlock. Postgres detects and aborts one with an error.

Avoid: lock rows in a consistent order across transactions.

### Exercises

1. Build a mini queue with a `jobs(id, status, payload)` table and use SKIP LOCKED from two sessions.
2. Force a deadlock on purpose and read the error.

### Check-in

Paste the SKIP LOCKED demo output from two sessions.

---

## L44 - Savepoints (revisit) and advisory locks

### Savepoints recap

Already in L41. Use them for partial rollback within a longer transaction, especially when calling code that might throw.

### Advisory locks

Application-level locks managed by Postgres. No tables needed.

```sql
-- session A
SELECT pg_advisory_lock(42);

-- session B: blocks until A unlocks or its session ends
SELECT pg_advisory_lock(42);

-- A
SELECT pg_advisory_unlock(42);
```

Use cases: coordinate cron jobs, singleton workers, external resource locking.

Non-blocking variant: `pg_try_advisory_lock(id)` returns false immediately if locked.

### Exercises

1. Use `pg_try_advisory_lock` to ensure only one process runs a cleanup job.

### Check-in

Demo of `pg_try_advisory_lock` returning false in a second session.

---

## Module 8 completion criteria

- [ ] You run risky work inside BEGIN/ROLLBACK without thinking
- [ ] You know what isolation level you're on and when to raise it
- [ ] You've seen `FOR UPDATE` and `FOR UPDATE SKIP LOCKED`
- [ ] You understand that advisory locks exist for app-level coordination
