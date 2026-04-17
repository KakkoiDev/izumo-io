# Module 7 - JSONB (L36-L40)

Prereq: Module 5 (indexes) and Module 6 (constraints).

No extension needed. JSONB is built into Postgres.

---

## L36 - When to reach for JSONB

### Concepts

- `json` (text-based) vs `jsonb` (binary, indexable). Always use `jsonb`.
- JSONB is for **semi-structured data**: optional fields, variable shape, things that would make a relational schema awkward.

### When to use JSONB

- Event payloads from many sources (Stripe webhooks, analytics events)
- User preferences / settings with a long tail of optional keys
- Denormalized copies of external API responses

### When NOT to use JSONB

- Data with fixed, known shape: use columns
- Data you join on often: columns and FKs are cleaner
- Data where types and constraints matter: JSONB is schemaless

### No steps, no check-in.

---

## L37 - JSONB operators

### Steps

```sql
DROP TABLE IF EXISTS logs;
CREATE TABLE logs (
  id        bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  ts        timestamptz NOT NULL DEFAULT now(),
  payload   jsonb NOT NULL
);

INSERT INTO logs (payload) VALUES
  ('{"user": "alice", "event": "login", "ip": "1.1.1.1", "country": "FR"}'),
  ('{"user": "bob", "event": "purchase", "amount": 9.99, "items": [{"sku":"a"},{"sku":"b"}]}'),
  ('{"user": "alice", "event": "logout"}');
```

Key operators:

```sql
SELECT payload -> 'user' FROM logs;            -- jsonb value
SELECT payload ->> 'user' FROM logs;           -- text value (unquoted)
SELECT payload -> 'items' -> 0 ->> 'sku' FROM logs;  -- chain into nested
SELECT payload #> '{items, 0, sku}' FROM logs;       -- path variant
SELECT payload #>> '{items, 0, sku}' FROM logs;      -- path, as text
```

`->` returns `jsonb`. `->>` returns `text` (unquoted string).

### Containment

```sql
SELECT * FROM logs WHERE payload @> '{"event":"login"}';  -- contains
SELECT * FROM logs WHERE payload ? 'amount';              -- has key at top level
SELECT * FROM logs WHERE payload ?| ARRAY['amount','ip']; -- has any key
SELECT * FROM logs WHERE payload ?& ARRAY['user','event']; -- has all keys
```

### Type coercion for numeric filters

```sql
SELECT * FROM logs WHERE (payload->>'amount')::numeric > 5;
```

JSONB stores numbers, but the `->>` returns text. Cast for arithmetic comparisons.

### Exercises

1. Find all events by user 'alice'.
2. Find all purchases with amount > 5.
3. Extract the country of each event.

### Check-in

Paste output of exercise 1.

---

## L38 - GIN index for JSONB

### Concept

A GIN (Generalized Inverted iNdex) indexes the contents of JSONB, not the raw bytes. Makes `@>` and `?` fast.

### Steps

Seed more data first (so timing matters):
```sql
INSERT INTO logs (payload)
SELECT jsonb_build_object(
  'user', 'user' || (g % 1000),
  'event', (ARRAY['login','logout','purchase'])[(g % 3) + 1],
  'country', (ARRAY['FR','JP','US'])[(g % 3) + 1]
)
FROM generate_series(1, 1000000) g;
```

(Takes a moment.)

Baseline:
```sql
\timing
SELECT count(*) FROM logs WHERE payload @> '{"event":"login"}';
```

Add GIN:
```sql
CREATE INDEX logs_payload_gin_idx ON logs USING GIN (payload);
```

Rerun:
```sql
SELECT count(*) FROM logs WHERE payload @> '{"event":"login"}';
```

Should be dramatically faster.

### Operator class: jsonb_path_ops

Smaller, faster for `@>` only (drops `?` support):
```sql
CREATE INDEX logs_payload_gin_pathops_idx ON logs USING GIN (payload jsonb_path_ops);
```

### Exercises

1. Run EXPLAIN on `WHERE payload @> '{"event":"login"}'` before and after the index.
2. Create a BTREE expression index on `((payload->>'user'))` and try `WHERE payload->>'user' = 'user5'`. Compare.

### Check-in

Paste EXPLAIN output post-index showing `Bitmap Index Scan on logs_payload_gin_idx`.

---

## L39 - jsonb_path_query and path expressions

### Concept

SQL/JSON path expressions to filter inside JSONB. More powerful than `->` chains.

### Steps

```sql
SELECT jsonb_path_query(payload, '$.items[*].sku') FROM logs WHERE id = 2;
-- returns each sku separately
```

Filter with predicates:
```sql
SELECT payload FROM logs
WHERE payload @? '$.items[*] ? (@.sku == "a")';
```

`@?` = "does this path exist?"; `@@` = "does this path match this boolean expression?".

### Extract all amounts > 5

```sql
SELECT jsonb_path_query(payload, '$.amount ? (@ > 5)')
FROM logs;
```

### Exercises

1. Find logs where any item has sku starting with 'a'.
2. Extract the `ip` field for all login events.

### Check-in

Paste output of exercise 2.

---

## L40 - Trade-offs: normalize vs JSONB

### When each wins

| Need | Use columns | Use JSONB |
|------|-------------|-----------|
| Type safety | Yes | No |
| Constraints (CHECK, FK) | Yes | Limited |
| Joins on field | Yes | Painful |
| Sparse / optional fields | Bloats | Natural |
| Schema stability | Changes cost migrations | Zero-schema-migration writes |
| Indexing | Many types | GIN, expression indexes |

### Hybrid pattern

Most real apps: "well-known fields as columns, tail as JSONB":

```sql
CREATE TABLE events_hybrid (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  ts timestamptz NOT NULL DEFAULT now(),
  user_id int NOT NULL,
  event_type text NOT NULL,
  extra jsonb NOT NULL DEFAULT '{}'::jsonb
);
```

Indexes on the columns you always query, GIN on `extra` for the rest.

### Exercises

1. Take the `logs` table and rewrite as the hybrid pattern.
2. Migrate data with an UPDATE using `payload->>'event'` etc.

### Check-in

Show the hybrid schema and a successful insert.

---

## Module 7 completion criteria

- [ ] You choose JSONB vs columns deliberately
- [ ] You use `->`, `->>`, `@>`, `?` fluently
- [ ] You GIN-index JSONB columns that are queried by containment
- [ ] You prefer the hybrid pattern over pure-JSONB tables
