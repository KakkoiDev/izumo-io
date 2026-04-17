# Module 6 - Constraints & Integrity (L32-L35)

Prereq: Module 2 (FKs). Module 5 (indexes) helpful.

---

## L32 - UNIQUE constraints

### Concept

`UNIQUE` guarantees no two rows have the same value in a column (or combo).
Under the hood: Postgres creates a unique B-tree index.

### Steps

```sql
CREATE TABLE users (
  id    int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email text NOT NULL UNIQUE,
  name  text
);

INSERT INTO users (email, name) VALUES ('a@x.com', 'Alice');
INSERT INTO users (email, name) VALUES ('a@x.com', 'Alice v2');
```

Expected error on the second:
```
duplicate key value violates unique constraint "users_email_key"
```

### NULL and UNIQUE

`NULL` is special: by default, Postgres treats NULLs as distinct, so multiple NULL emails are allowed.

Change with:
```sql
CREATE TABLE t (email text UNIQUE NULLS NOT DISTINCT);
```

Then only one NULL row is allowed. PG15+.

### Composite UNIQUE

```sql
CREATE TABLE memberships (
  user_id int NOT NULL,
  org_id  int NOT NULL,
  role    text NOT NULL,
  UNIQUE (user_id, org_id)
);
```

One membership per (user, org) pair.

### Exercises

1. Try inserting duplicate emails.
2. Add `UNIQUE (title, author_id)` to books. Try to insert the same book twice for one author.

### Check-in

Show the error message from exercise 1.

---

## L33 - CHECK constraints

### Concept

`CHECK (expr)` refuses rows where `expr` is false.

### Steps

```sql
CREATE TABLE products (
  id    int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name  text NOT NULL,
  price numeric(10,2) NOT NULL CHECK (price >= 0),
  stock int NOT NULL CHECK (stock >= 0)
);

INSERT INTO products (name, price, stock) VALUES ('Widget', -1, 5);
```

Expected: `new row for relation "products" violates check constraint`.

### Table-level CHECK (multi-column)

```sql
CREATE TABLE events (
  id         int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  start_at   timestamptz NOT NULL,
  end_at     timestamptz NOT NULL,
  CHECK (end_at > start_at)
);
```

### Don't push too much logic into CHECK

CHECK must be immutable. No lookups to other tables, no `now()`, no functions that aren't marked `IMMUTABLE`. For cross-row or cross-table rules, use triggers (Module 10).

### Exercises

1. Add a CHECK to books that `page_count > 0`.
2. Try inserting a 0-page book.
3. Think: why can't CHECK use `(SELECT ...)`?

### Check-in

Show constraint listed in `\d products`.

---

## L34 - Generated columns

### Concept

A column computed from other columns. Stored or virtual.

### Steps

```sql
CREATE TABLE orders (
  id         int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  quantity   int NOT NULL,
  unit_price numeric(10,2) NOT NULL,
  total      numeric(12,2) GENERATED ALWAYS AS (quantity * unit_price) STORED
);

INSERT INTO orders (quantity, unit_price) VALUES (3, 9.99);
SELECT * FROM orders;
```

`total` filled itself in.

Attempting to write to it:
```sql
INSERT INTO orders (quantity, unit_price, total) VALUES (1, 10, 999);
```
Expected error.

### STORED vs VIRTUAL

Postgres (as of PG17) only supports `STORED` (physically stored). VIRTUAL is planned. For most cases stored is fine.

### Use cases

- Full-text search columns (tsvector)
- Normalized search strings (`lower(email)`)
- Computed metrics

### Exercises

1. Add a generated column `email_lower text GENERATED ALWAYS AS (lower(email)) STORED` to `users`. Create an index on it.
2. Rewrite the "case-insensitive search" from L31 without lower() in the WHERE.

### Check-in

Show `\d users` with the new generated column.

---

## L35 - ON CONFLICT (upsert)

### Concept

Postgres's powerful upsert: insert, but on collision with a UNIQUE constraint, update instead (or do nothing).

### Steps

```sql
-- Ignore the insert if duplicate
INSERT INTO users (email, name) VALUES ('a@x.com', 'New Name')
ON CONFLICT (email) DO NOTHING;

-- Update on collision
INSERT INTO users (email, name) VALUES ('a@x.com', 'Updated Name')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name;

SELECT * FROM users WHERE email = 'a@x.com';
```

`EXCLUDED` refers to the row you tried to insert.

### Partial upsert

Only update if the incoming value is non-null:
```sql
ON CONFLICT (email) DO UPDATE
SET name = COALESCE(EXCLUDED.name, users.name);
```

### Upsert with composite key

```sql
INSERT INTO memberships (user_id, org_id, role) VALUES (1, 1, 'admin')
ON CONFLICT (user_id, org_id) DO UPDATE SET role = EXCLUDED.role;
```

### Exercises

1. Insert 3 products. Run the same INSERT again with ON CONFLICT DO NOTHING (you'll need a UNIQUE constraint on name first).
2. Write an upsert that bumps `stock` on conflict.

### Check-in

Show the SELECT after a DO UPDATE upsert.

---

## Module 6 completion criteria

- [ ] You declare UNIQUE constraints to prevent duplicates
- [ ] You use CHECK for column-level and row-level invariants
- [ ] You use generated columns for derived data you want to index
- [ ] You use ON CONFLICT for upserts rather than SELECT-then-INSERT (race-prone)
