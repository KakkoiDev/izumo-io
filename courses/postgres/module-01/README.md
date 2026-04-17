# Module 1 - SQL Fundamentals (L06-L10)

Prereq: Module 0 complete. You have `pg` running with `pgdata` volume, and the `bookshelf` database.

---

## L06 - Core data types

### Concepts

- The types you'll use 95% of the time
- Why `timestamptz` over `timestamp`
- Why `text` over `varchar`
- `numeric` for money, never `float`

### The short list

| Type | Use for | Notes |
|------|---------|-------|
| `int` (int4) | Regular integers | -2B to +2B |
| `bigint` (int8) | Big ids, counters | -9 quintillion to +9 quintillion |
| `smallint` | Small ints (rarely) | -32k to +32k |
| `numeric(p,s)` | Money, exact decimals | Arbitrary precision. Slow but correct. |
| `real` / `double precision` | Floats for science | Never for money. |
| `text` | Strings of any length | Preferred in Postgres |
| `varchar(n)` | String with hard limit | No perf benefit in PG. Use only if business rule says so. |
| `boolean` | true/false | Also accepts 'yes'/'no'/'1'/'0' |
| `date` | Calendar date | No time |
| `timestamptz` | Date + time + timezone | **Always prefer this** |
| `timestamp` | Date + time, no tz | Avoid. Silent timezone bugs. |
| `interval` | A duration (3 days, 2 hours) | `now() - interval '7 days'` |
| `uuid` | Global unique ids | With `pgcrypto.gen_random_uuid()` |
| `jsonb` | Flexible documents | Binary JSON, indexable. More in Module 7. |
| `bytea` | Raw bytes | Avoid storing blobs in DB when possible |

### Steps

Make a playground table:

```sql
DROP TABLE IF EXISTS playground;
CREATE TABLE playground (
  id          int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name        text NOT NULL,
  age         int,
  salary      numeric(12,2),
  is_active   boolean DEFAULT true,
  birthday    date,
  created_at  timestamptz DEFAULT now(),
  tags        text[]
);
```

Insert with a mix:
```sql
INSERT INTO playground (name, age, salary, birthday, tags) VALUES
  ('Alice', 30, 50000.00, '1995-06-12', ARRAY['admin','eng']),
  ('Bob', 25, 42000.50, '2000-01-01', ARRAY['eng']);
```

Read back:
```sql
SELECT * FROM playground;
```

Notice `created_at` filled itself in, `is_active` defaulted to true.

### The timezone trap

Try:
```sql
SELECT now();                     -- current time
SELECT now() AT TIME ZONE 'UTC';  -- explicit UTC
SELECT now() AT TIME ZONE 'Asia/Tokyo';
```

All represent the same instant, displayed in different zones. Because we stored `created_at timestamptz`, the actual byte representation is always UTC. Display happens at query time.

If we'd used `timestamp` (no tz), you'd be storing "whatever my session said the time was", which is a bug generator.

### Rule: always `timestamptz` for real-world times.

### Exercises

1. Add a `last_login timestamptz` column with `ALTER TABLE`. Look up the syntax.
2. Try inserting `age = 'thirty'`. Read the error.
3. Try `SELECT 1/0;`. Read the error.
4. Predict: what does `SELECT 1.0/3.0;` return? What about `SELECT 1/3;`? Try both.

Answer to 4: `1.0/3.0` returns a numeric ~0.33333. `1/3` returns int 0 (integer division).

### Check-in

Paste output of `\d playground` and `SELECT now() AT TIME ZONE 'Asia/Tokyo';`.

---

## L07 - NULL and 3-valued logic

### Concept

NULL is not a value. It's "unknown". That changes everything.

### Steps

```sql
-- NULL is not equal to anything, not even itself
SELECT NULL = NULL;         -- returns NULL, not true
SELECT NULL = 1;            -- NULL
SELECT NULL + 1;            -- NULL
SELECT 'hello' || NULL;     -- NULL

-- The correct operators
SELECT NULL IS NULL;        -- true
SELECT 1 IS NOT NULL;       -- true
SELECT NULL IS DISTINCT FROM NULL;  -- false (treats NULL=NULL)
```

Insert a row with NULLs:
```sql
INSERT INTO playground (name) VALUES ('Charlie');
SELECT id, name, age FROM playground WHERE age IS NULL;
SELECT id, name, age FROM playground WHERE age = NULL;  -- returns 0 rows, common bug!
```

### The three-valued truth table

| a | b | a AND b | a OR b |
|---|---|---------|--------|
| true | true | true | true |
| true | false | false | true |
| true | NULL | NULL | true |
| false | NULL | false | NULL |
| NULL | NULL | NULL | NULL |

### Useful functions

```sql
SELECT COALESCE(NULL, NULL, 'fallback');  -- 'fallback', first non-null
SELECT NULLIF('', '');                    -- NULL, convert empty to NULL
SELECT name, age, COALESCE(age, 0) AS age_or_zero FROM playground;
```

### Exercises

1. Count rows where age is unknown vs known:
   ```sql
   SELECT
     count(*) FILTER (WHERE age IS NULL)     AS unknown,
     count(*) FILTER (WHERE age IS NOT NULL) AS known
   FROM playground;
   ```
2. Explain why `SELECT count(age) FROM playground;` may differ from `SELECT count(*) FROM playground;`.
3. Try `SELECT NULL::text || '!';`. Then `SELECT concat(NULL::text, '!');`. Explain the difference.

Answer to 2: `count(*)` counts rows. `count(col)` counts non-null values of `col`.

Answer to 3: `||` propagates NULL. `concat()` skips NULLs.

### Check-in

Paste the output of exercise 1.

---

## L08 - UPDATE and DELETE (and the WHERE that saves your career)

### Concept

`UPDATE` and `DELETE` without a `WHERE` affect EVERY row. You will do it once. The panic is educational.

### Steps

First, make a safe sandbox in a transaction:

```sql
BEGIN;
SELECT count(*) FROM playground;  -- baseline

-- The dangerous one
DELETE FROM playground;
SELECT count(*) FROM playground;  -- 0

ROLLBACK;
SELECT count(*) FROM playground;  -- restored
```

`ROLLBACK` undoes everything since `BEGIN`. This is the real safety net in Postgres. `BEGIN` before risky work, verify, then `COMMIT` or `ROLLBACK`.

### UPDATE

```sql
BEGIN;
UPDATE playground SET is_active = false WHERE name = 'Alice';
SELECT * FROM playground WHERE name = 'Alice';
COMMIT;
```

You can update multiple columns:
```sql
UPDATE playground SET age = 31, salary = 55000 WHERE name = 'Alice';
```

### DELETE

```sql
DELETE FROM playground WHERE name = 'Charlie';
```

Always check before committing a destructive action:
```sql
BEGIN;
DELETE FROM playground WHERE name LIKE 'A%';
SELECT * FROM playground;  -- verify
-- If happy: COMMIT; If not: ROLLBACK;
```

### Three habits

1. **BEGIN first** for anything destructive on data you care about.
2. **Run the SELECT before the DELETE** with the same WHERE, see what you'd affect.
3. **LIMIT in safe mode**. Some clients (pgcli) have a "safe update mode" that refuses DELETE/UPDATE without WHERE.

### Exercises

1. Inside a `BEGIN/ROLLBACK` pair, delete all rows. Confirm count 0. Rollback. Confirm restored.
2. Update Bob's age to 26 and salary to 45000 in one statement.
3. Try this: `DELETE FROM playground;` without BEGIN. On the second thought, don't. But understand what'd happen.

### Check-in

Paste a screenshot (or text) showing a BEGIN / DELETE / count / ROLLBACK / count cycle.

---

## L09 - ORDER BY, LIMIT, OFFSET

### Concepts

- Sorting results: ASC (default) vs DESC
- NULLs in sorting (NULLS FIRST / NULLS LAST)
- Paging with LIMIT and OFFSET (and its cost)
- Better paging: keyset pagination (preview only)

### Steps

Seed more data:
```sql
INSERT INTO playground (name, age) VALUES
  ('Dave', 40), ('Eve', 35), ('Frank', NULL), ('Grace', 28);
```

Sort:
```sql
SELECT name, age FROM playground ORDER BY age;           -- asc, NULL last by default
SELECT name, age FROM playground ORDER BY age DESC;      -- desc, NULL first by default
SELECT name, age FROM playground ORDER BY age NULLS FIRST;
SELECT name, age FROM playground ORDER BY age DESC NULLS LAST;
```

Multiple sort keys:
```sql
SELECT name, age FROM playground ORDER BY age DESC, name ASC;
```

Paging:
```sql
SELECT name FROM playground ORDER BY id LIMIT 3;           -- first page
SELECT name FROM playground ORDER BY id LIMIT 3 OFFSET 3;  -- second page
```

### The OFFSET trap

OFFSET 100000 makes Postgres compute and discard 100k rows. Slow at scale. Real apps use "keyset pagination":

```sql
-- Page 1
SELECT id, name FROM playground ORDER BY id LIMIT 3;
-- Suppose last row had id = 3. Page 2:
SELECT id, name FROM playground WHERE id > 3 ORDER BY id LIMIT 3;
```

This uses the index, stays fast even past millions of rows. We'll revisit in Module 5.

### Exercises

1. Get the 2 oldest users.
2. Get users sorted by name alphabetically.
3. Get users 3-4 (rows 3 and 4) with OFFSET.
4. Predict: without ORDER BY, does `LIMIT 1` return the same row every time? Try by running 3-4 times.

Answer: no. Without ORDER BY, order is undefined. Engine may return in insertion order, physical order, index order. Never rely on it.

### Check-in

Paste the output of `SELECT name, age FROM playground ORDER BY age DESC NULLS LAST;`.

---

## L10 - Break things on purpose

### Concept

Reading error messages is 40% of being good at databases. Today you deliberately break five things and read each error carefully.

### Break 1 - Type mismatch

```sql
INSERT INTO playground (name, age) VALUES ('Bad', 'not a number');
```

Expected: `invalid input syntax for type integer: "not a number"`. Postgres is strict about types on insert.

### Break 2 - NOT NULL violation

```sql
INSERT INTO playground (age) VALUES (99);
```

Expected: `null value in column "name" of relation "playground" violates not-null constraint`. You didn't provide `name`.

### Break 3 - Syntax error

```sql
SELECT * FORM playground;
```

Expected: `syntax error at or near "FORM"`. Typo. Postgres tells you the line/position.

### Break 4 - Unknown column

```sql
SELECT email FROM playground;
```

Expected: `column "email" does not exist`. Sometimes it suggests "Perhaps you meant to reference the column 'name'".

### Break 5 - Dividing by zero

```sql
SELECT 10 / 0;
```

Expected: `division by zero`. Same outside SQL, this is a real error, not silent NaN.

### Meta-concept

Error messages contain:
1. The error class (e.g., `ERROR`, `NOTICE`, `WARNING`)
2. The cause
3. Sometimes the line/position
4. Sometimes a hint

Train yourself to read the full text before panicking. 90% of them tell you exactly what's wrong.

### Exercises

1. Drop the `playground` table. Try to insert into it. Read the error.
2. Create a table without `NOT NULL`, insert a NULL, then add `NOT NULL` with `ALTER TABLE`. Predict what happens.
3. Create a table with a `CHECK (age >= 0)`. Insert -5. Read the error.

### Check-in

No check-in. This lesson is purely about seeing errors.

---

## Module 1 completion criteria

- [ ] You can list Postgres core types from memory
- [ ] You understand why `timestamptz` beats `timestamp`
- [ ] NULL = NULL returns NULL, you use `IS NULL`
- [ ] You always `BEGIN` before a risky DELETE
- [ ] You can read an error message and fix the cause in one shot
