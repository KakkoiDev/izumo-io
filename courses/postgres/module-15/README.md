# Module 15 - Postgres as the Entire Backend (L69-L75)

Prereq: Modules 0-10 at minimum. This is where "replace your stack with Postgres" happens.

---

## L69 - Row-level security (RLS) concept

### Concept

RLS filters which rows each user sees/writes. A per-row ACL enforced by the DB, no app code.

Use cases:
- Multi-tenant SaaS: tenant A can't see tenant B's data
- Per-user data: users see only their own rows

### The mental model

1. You create roles and grant table access.
2. You enable RLS on the table.
3. You write `POLICY` expressions that evaluate per query.
4. The running session's identity (via `current_user` or JWT claims) filters rows.

### No steps yet. Read again if fuzzy.

---

## L70 - JWT claims in Postgres

### Concept

PostgREST (and Supabase) decode JWT tokens and inject claims into Postgres settings. RLS policies can read these.

### Steps

Simulate a JWT claim:
```sql
SET request.jwt.claims TO '{"role":"authenticated","user_id":"42"}';
SELECT current_setting('request.jwt.claims', true);
SELECT (current_setting('request.jwt.claims', true)::json ->> 'user_id');
```

In production, PostgREST sets this automatically when a valid JWT arrives.

### Exercises

1. Play with SET to different JWTs. Extract claims.

### Check-in

Show a SELECT extracting `user_id` from a JWT setting.

---

## L71 - Your first RLS policy

### Steps

```sql
DROP TABLE IF EXISTS notes;
CREATE TABLE notes (
  id      int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id int NOT NULL,
  body    text NOT NULL
);

INSERT INTO notes (user_id, body) VALUES
  (1, 'Alice note 1'), (1, 'Alice note 2'),
  (2, 'Bob note 1');
```

Enable RLS:
```sql
ALTER TABLE notes ENABLE ROW LEVEL SECURITY;
ALTER TABLE notes FORCE ROW LEVEL SECURITY;
```

`FORCE` applies RLS even to the table owner. Without it, superusers bypass.

Policy:
```sql
CREATE POLICY notes_user_isolation ON notes
  USING (user_id = (current_setting('request.jwt.claims', true)::json ->> 'user_id')::int);
```

`USING` filters SELECT/UPDATE/DELETE; `WITH CHECK` filters INSERT/UPDATE.

Simulate Alice:
```sql
SET request.jwt.claims TO '{"user_id":"1"}';
SELECT * FROM notes;   -- only Alice's
```

Switch to Bob:
```sql
SET request.jwt.claims TO '{"user_id":"2"}';
SELECT * FROM notes;   -- only Bob's
```

### Adding INSERT rule

```sql
CREATE POLICY notes_insert ON notes
  FOR INSERT
  WITH CHECK (user_id = (current_setting('request.jwt.claims', true)::json ->> 'user_id')::int);
```

Bob can insert Bob-owned rows, not Alice-owned ones.

### Exercises

1. Write an RLS policy for a `projects(id, owner_id, name)` table.
2. Try to insert a row where `user_id` doesn't match the JWT.

### Check-in

Show SELECT returning different rows for different JWT settings.

---

## L72 - Install PostgREST

### Concept

PostgREST is a standalone Haskell binary. Point it at Postgres, expose a REST API.

### Steps

Extend the docker-compose style; easiest:

```bash
docker run -d \
  --name pgrest \
  --link pg:db \
  -e PGRST_DB_URI=postgres://authenticator:dev@db/bookshelf \
  -e PGRST_DB_ANON_ROLE=anon \
  -e PGRST_JWT_SECRET="dev-secret-change-me-32-bytes-plz" \
  -e PGRST_DB_SCHEMA=api \
  -p 3000:3000 \
  postgrest/postgrest:latest
```

Prepare Postgres:
```sql
-- Run as superuser
CREATE ROLE anon NOLOGIN;
CREATE ROLE authenticated NOLOGIN;
CREATE ROLE authenticator NOINHERIT LOGIN PASSWORD 'dev';
GRANT anon TO authenticator;
GRANT authenticated TO authenticator;

CREATE SCHEMA IF NOT EXISTS api;
GRANT USAGE ON SCHEMA api TO anon, authenticated;
```

Expose a view:
```sql
CREATE OR REPLACE VIEW api.books AS SELECT * FROM books;
GRANT SELECT ON api.books TO anon, authenticated;
```

Hit it:
```bash
curl http://localhost:3000/books
```

JSON array of books.

### Exercises

1. Expose `api.authors` as well.
2. Try `curl 'http://localhost:3000/books?author_id=eq.1'`. PostgREST translates that to WHERE.

### Check-in

Paste curl output of one endpoint.

---

## L73 - REST from your schema

### Concept

Every table/view you expose in the `api` schema becomes an endpoint. PostgREST supports filtering, ordering, pagination, joins via query params.

### Steps

Filtering:
```
GET /books?author_id=eq.1
GET /books?title=like.*postgres*
GET /books?published=gte.2018-01-01
```

Ordering:
```
GET /books?order=published.desc.nullslast
```

Pagination:
```
GET /books?limit=10&offset=20
```

Embedded resources (via FK):
```
GET /books?select=title,authors(name)
```

Column selection:
```
GET /books?select=title,author_id
```

### Inserts

```
POST /books
Body: {"title":"New Book","author_id":1}
```

Only works if the underlying table/view is writable to your role.

### Exercises

1. Expose `api.authors`, fetch all, filter by name ILIKE.
2. Use `select=*,books(*)` to fetch authors with their books embedded.

### Check-in

Show a curl that filters + embeds.

---

## L74 - Auth with roles

### Concept

PostgREST's JWT flow:
1. Client sends `Authorization: Bearer <jwt>`
2. PostgREST validates JWT with `PGRST_JWT_SECRET`
3. PostgREST switches the Postgres session to the role in the JWT's `role` claim
4. RLS policies filter rows based on claims

### Steps

Sign a JWT (use jwt.io for quick testing):

Header:
```json
{"alg":"HS256","typ":"JWT"}
```

Payload:
```json
{"role":"authenticated","user_id":"1"}
```

Use your `PGRST_JWT_SECRET` to sign.

Call with token:
```bash
curl -H "Authorization: Bearer <token>" http://localhost:3000/notes
```

RLS filters to user 1's notes only.

Without token, you're `anon`. If `anon` lacks SELECT on `api.notes`, you get 401.

### Stored procedures as RPC

```sql
CREATE OR REPLACE FUNCTION api.login(email text, password text)
RETURNS text
LANGUAGE plpgsql
AS $$
DECLARE token text;
BEGIN
  -- verify password (use pgcrypto), if ok:
  token := 'signed-jwt-here';
  RETURN token;
END;
$$;
```

Called via:
```
POST /rpc/login
{"email":"a@x.com","password":"..."}
```

### Exercises

1. Set up RLS on `notes` (from L71), expose via PostgREST. Test with two different JWTs.
2. Write an RPC function that creates an account.

### Check-in

Show `notes` returning different rows for different JWTs via curl.

---

## L75 - Install pg_graphql

### Concept

Auto-generate a GraphQL API from your schema. FKs become relations, tables become types.

### Steps

Timescale-HA image includes pg_graphql. If not, use Supabase's image or install from source.

```sql
CREATE EXTENSION IF NOT EXISTS pg_graphql;
```

Query via the built-in `graphql.resolve` function:
```sql
SELECT graphql.resolve($$
  query {
    booksCollection {
      edges {
        node {
          id
          title
          authors { name }
        }
      }
    }
  }
$$);
```

### Expose over HTTP via PostgREST

```sql
CREATE OR REPLACE FUNCTION api.graphql(query text, operationName text default null, variables jsonb default '{}'::jsonb)
RETURNS jsonb
LANGUAGE sql
AS $$
  SELECT graphql.resolve(query, variables, operationName);
$$;

GRANT EXECUTE ON FUNCTION api.graphql TO anon, authenticated;
```

Then:
```bash
curl -X POST http://localhost:3000/rpc/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ booksCollection { edges { node { title } } } }"}'
```

### Exercises

1. Explore the generated schema (there's introspection).
2. Write a GraphQL mutation to insert a book.

### Check-in

Paste a GraphQL query response.

---

## Module 15 completion criteria

- [ ] RLS isolates rows by JWT claim
- [ ] PostgREST serves REST from your schema
- [ ] You can write and use RPC functions
- [ ] GraphQL is available via pg_graphql
- [ ] You've stopped writing Node/Python CRUD for simple APIs
