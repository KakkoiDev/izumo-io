# Module 10 - Functions & Triggers (L51-L54)

Prereq: Module 2+. Comfortable with SQL basics.

---

## L51 - Simple SQL functions

### Concept

Functions are reusable SQL/procedural code stored in the DB.

### Steps

```sql
CREATE OR REPLACE FUNCTION full_name(first text, last text)
RETURNS text
LANGUAGE sql
IMMUTABLE
AS $$
  SELECT first || ' ' || last;
$$;

SELECT full_name('Alice', 'Smith');
```

Key parts:
- `LANGUAGE sql` - plain SQL (vs `plpgsql` for procedural)
- `IMMUTABLE` - same input always gives same output, no side effects. Lets the planner cache.
- `$$` - dollar-quoted string, avoids quote hell

### Volatility categories

- `IMMUTABLE` - pure
- `STABLE` - same within a single query (e.g., reads from DB)
- `VOLATILE` (default) - can differ each call (`now()`, `random()`)

Use the strictest category that's still truthful. Helps the planner.

### Exercises

1. Write `discount_price(price numeric, pct numeric)` returns numeric.
2. Write `is_weekday(d date)` returns boolean.

### Check-in

Show `SELECT full_name('Claude', 'Bot');` and the definition.

---

## L52 - PL/pgSQL basics

### Concept

`LANGUAGE plpgsql` gives you variables, loops, control flow.

### Steps

```sql
CREATE OR REPLACE FUNCTION greet_or_bye(user_name text, intent text)
RETURNS text
LANGUAGE plpgsql
AS $$
BEGIN
  IF intent = 'hi' THEN
    RETURN 'Hello, ' || user_name;
  ELSIF intent = 'bye' THEN
    RETURN 'Goodbye, ' || user_name;
  ELSE
    RAISE EXCEPTION 'Unknown intent: %', intent;
  END IF;
END;
$$;

SELECT greet_or_bye('Alice', 'hi');
SELECT greet_or_bye('Alice', 'shrug');
```

### Looping / variables

```sql
CREATE OR REPLACE FUNCTION sum_to(n int)
RETURNS int
LANGUAGE plpgsql
AS $$
DECLARE
  total int := 0;
  i int;
BEGIN
  FOR i IN 1..n LOOP
    total := total + i;
  END LOOP;
  RETURN total;
END;
$$;
```

(SQL's `SELECT sum(i) FROM generate_series(1,n) i` is simpler. Use plpgsql when you need logic.)

### Exceptions

```sql
BEGIN
  PERFORM 1/0;
EXCEPTION
  WHEN division_by_zero THEN
    RAISE NOTICE 'Caught the divide by zero';
END;
```

### Exercises

1. Write a plpgsql function `safe_divide(a numeric, b numeric)` returning NULL on divide-by-zero.
2. Write one that takes a text and returns lowercased, trimmed, no special chars.

### Check-in

Show `safe_divide(10, 0)` returning NULL cleanly.

---

## L53 - Triggers (auto-updated_at)

### Concept

Triggers run functions on INSERT/UPDATE/DELETE events.

### Steps

```sql
ALTER TABLE users ADD COLUMN IF NOT EXISTS updated_at timestamptz NOT NULL DEFAULT now();

CREATE OR REPLACE FUNCTION touch_updated_at()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  NEW.updated_at := now();
  RETURN NEW;
END;
$$;

CREATE TRIGGER users_touch_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION touch_updated_at();
```

Test:
```sql
UPDATE users SET name = 'changed' WHERE id = 1;
SELECT id, name, updated_at FROM users WHERE id = 1;
```

`updated_at` is fresh.

### BEFORE vs AFTER

- `BEFORE` lets you modify the row about to be written (or block it with RAISE)
- `AFTER` runs post-write, good for audit logs

### Trigger variables

- `NEW` - the row being written (INSERT / UPDATE)
- `OLD` - the row before (UPDATE / DELETE)
- `TG_OP` - 'INSERT' / 'UPDATE' / 'DELETE'

### Audit log example

```sql
CREATE TABLE audit (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  ts timestamptz NOT NULL DEFAULT now(),
  action text,
  row_data jsonb
);

CREATE OR REPLACE FUNCTION audit_users()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  INSERT INTO audit (action, row_data)
  VALUES (TG_OP, to_jsonb(NEW));
  RETURN NEW;
END;
$$;

CREATE TRIGGER users_audit AFTER INSERT OR UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION audit_users();
```

### Exercises

1. Implement updated_at for the `books` table.
2. Implement an audit log for `products` that captures OLD and NEW on UPDATE.

### Check-in

Show an UPDATE causing `updated_at` to move forward.

---

## L54 - LISTEN / NOTIFY

### Concept

Postgres pub/sub without an extra broker. Good for sending change events to clients.

### Steps

Session A (subscriber):
```sql
LISTEN user_changes;
```

Session B (publisher):
```sql
NOTIFY user_changes, 'id=1';
```

Session A sees: `Asynchronous notification "user_changes" with payload "id=1"`.

Use a trigger to auto-notify:
```sql
CREATE OR REPLACE FUNCTION notify_user_change()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  PERFORM pg_notify('user_changes', json_build_object('op', TG_OP, 'id', NEW.id)::text);
  RETURN NEW;
END;
$$;

CREATE TRIGGER users_notify AFTER INSERT OR UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION notify_user_change();
```

### Limitations

- Max payload 8 KB
- Delivery within a single server (not cross-node without replication)
- For high throughput, use pgmq (Module 15) or a real broker

### Exercises

1. Add LISTEN in one psql session, do INSERTs in another, watch notifications stream.
2. Read about `LISTEN` from a Node/Python client (the `pg` / `psycopg` lib both support it).

### Check-in

Show LISTEN + NOTIFY roundtrip.

---

## Module 10 completion criteria

- [ ] You write SQL and PL/pgSQL functions with the right volatility
- [ ] You add triggers for updated_at and audit logs
- [ ] You understand NEW/OLD/TG_OP in trigger bodies
- [ ] You know LISTEN/NOTIFY exists and when to use it
