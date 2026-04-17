# Module 0 - First Contact

Lessons L01-L05. From zero to a persistent Postgres container you can talk to, with a `books` table, your first `.sql` files, and surviving restarts.

---

## L01 - First Container, First Query

### Prereqs

- Docker installed and running
- A terminal

### Concepts introduced

- Container vs image
- `docker run` flags (-d, --name, -e, -p)
- psql prompt anatomy
- Semicolons as query terminators
- `\q` as a psql meta-command

### Step 1 - Start Postgres

```bash
docker run -d \
  --name pg \
  -e POSTGRES_PASSWORD=dev \
  -p 5432:5432 \
  postgres:17
```

Flag meanings:

- `docker run` - create and start a container
- `-d` - detached (runs in background)
- `--name pg` - so we can refer to it later as "pg"
- `-e POSTGRES_PASSWORD=dev` - env var; the official image refuses to boot without one on first run
- `-p 5432:5432` - host port : container port. 5432 is Postgres' default.
- `postgres:17` - image name : tag

### Step 2 - Verify

```bash
docker ps
```

Expect one row with `pg` in NAMES, `postgres:17` in IMAGE, STATUS showing "Up".

### Step 3 - Connect

```bash
docker exec -it pg psql -U postgres
```

- `docker exec` - run a command inside a running container
- `-it` - interactive + TTY attached
- `pg` - container name
- `psql -U postgres` - launch psql as user `postgres` (the superuser)

You should see:

```
postgres=#
```

That prompt means:
- `postgres` - you are connected to the database named `postgres`
- `=#` - you are a superuser waiting for input. `=>` would mean a regular user.

### Step 4 - Two queries

Type (don't paste). Semicolon required.

```sql
SELECT 1 + 1;
```

Expected:
```
 ?column?
----------
        2
(1 row)
```

Then:
```sql
SELECT version();
```

Expected: one row with a long string starting with `PostgreSQL 17...`.

### Step 5 - Quit

```
\q
```

That's a psql meta-command. They all start with `\` and don't need a semicolon.

### Expected errors (if you stumble here)

| Error | Cause | Fix |
|-------|-------|-----|
| `Cannot connect to the Docker daemon` | Docker not running | Start Docker Desktop / `systemctl start docker` |
| `bind for 0.0.0.0:5432 failed: port is already allocated` | Another Postgres on 5432 | `docker stop $(docker ps -q)` or change `-p 5433:5432` |
| `Error: database "postgres" does not exist` | Wrong `-U` flag | Use `-U postgres` |
| No output after typing | Forgot the `;` | Type `;` and press enter |

### Check-in

Paste the output of:

```sql
SELECT version();
```

If you got that, you're done with L01. Tick it in the outline and move to L02.

---

## L02 - Your Own Database, First Table, INSERT + SELECT

### Prereqs

- L01 complete: container `pg` is running, you can connect with psql

### Concepts introduced

- Why a dedicated database per project
- `CREATE DATABASE` / `\c` (connect)
- `CREATE TABLE`
- Primary keys (`bigserial`, the old way; `identity`, the modern way)
- `INSERT INTO ... VALUES ...`
- `SELECT * FROM ...`
- The difference between `text` and `varchar`

### Step 1 - Connect

```bash
docker exec -it pg psql -U postgres
```

Prompt:
```
postgres=#
```

### Step 2 - Create a database

A database is a logical container for tables. You typically create one per project.

```sql
CREATE DATABASE bookshelf;
```

Output:
```
CREATE DATABASE
```

List all databases:

```
\l
```

You should see `bookshelf` in the list, plus the built-in ones (`postgres`, `template0`, `template1`).

### Step 3 - Connect to the new database

```
\c bookshelf
```

Prompt changes to:
```
bookshelf=#
```

The database name in the prompt always shows where you are. Always glance at it before running anything.

### Step 4 - Your first table

```sql
CREATE TABLE books (
  id     int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  title  text NOT NULL,
  author text NOT NULL
);
```

Read this slowly:

- `CREATE TABLE books` - make a table called `books`
- `id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY` - auto-incrementing integer id, Postgres assigns the next one for you on insert. Modern idiom (replaces old `serial`).
- `title text NOT NULL` - text column, can never be null
- `text` vs `varchar(n)` - in Postgres there is no performance difference. Prefer `text`. Only use `varchar(n)` if the business rule truly needs a hard length limit.
- `PRIMARY KEY` - this column uniquely identifies each row, and cannot be null

### Step 5 - Describe the table

```
\d books
```

You'll see the columns, types, and the index Postgres auto-created for the primary key (called `books_pkey`).

### Step 6 - Insert rows

```sql
INSERT INTO books (title, author) VALUES
  ('The Art of PostgreSQL', 'Dimitri Fontaine'),
  ('Database Internals', 'Alex Petrov'),
  ('Designing Data-Intensive Applications', 'Martin Kleppmann');
```

Output:
```
INSERT 0 3
```

The `3` means 3 rows inserted. The `0` is legacy and ignored today.

Notice we didn't pass `id`. Postgres assigned 1, 2, 3 because of `GENERATED ALWAYS AS IDENTITY`.

### Step 7 - Read everything back

```sql
SELECT * FROM books;
```

Output should look like:
```
 id |                 title                 |      author
----+---------------------------------------+------------------
  1 | The Art of PostgreSQL                 | Dimitri Fontaine
  2 | Database Internals                    | Alex Petrov
  3 | Designing Data-Intensive Applications | Martin Kleppmann
(3 rows)
```

`*` means "all columns". Prefer named columns in real code; `*` is for exploration.

### Step 8 - Break it on purpose

This is how you learn errors. Try:

```sql
INSERT INTO books (id, title, author) VALUES (1, 'Duplicate', 'Someone');
```

Expected error:
```
ERROR:  duplicate key value violates unique constraint "books_pkey"
DETAIL:  Key (id)=(1) already exists.
```

Read it:
- `books_pkey` - the primary key index
- `Key (id)=(1) already exists` - row with id 1 is already there

The PK protects you from accidentally inserting the same identity twice.

Try:

```sql
INSERT INTO books (title) VALUES ('No Author');
```

Expected:
```
ERROR:  null value in column "author" of relation "books" violates not-null constraint
```

The `NOT NULL` constraint blocked you. These errors are good. The DB is defending your data.

### Step 9 - Targeted SELECT

Don't use `*` forever. Try:

```sql
SELECT title FROM books;
```

```sql
SELECT title, author FROM books;
```

```sql
SELECT title AS book_name FROM books;
```

`AS` renames a column in the output. Useful when joining later.

### Exercises (do these before L03)

1. Create a second table called `authors` with columns `id` (identity PK) and `name` (text not null).
2. Insert 3 authors.
3. Select only the names, ordered alphabetically (you'll need `ORDER BY name`; peek at the docs or guess).
4. Try to insert two authors with the same `id`. Confirm it errors.
5. Describe the `authors` table with `\d authors`.

### Expected errors table

| Error | Cause | Fix |
|-------|-------|-----|
| `relation "books" does not exist` | You're in the wrong database | `\c bookshelf` |
| `duplicate key ...` | Tried to reuse a PK | Let identity assign it, or insert a new value |
| `null value in column ... violates not-null` | Left a NOT NULL column out | Pass a value |
| `syntax error at or near ")"` | Missing comma between columns | Reread; commas separate columns, no comma after the last |

### Check-in

Paste the output of:

```sql
SELECT * FROM books;
\d books
\d authors
```

Once you pass L02, tick it and move to L03 (psql survival kit).

---

## L03 - psql survival kit

### Concepts

- Meta-commands (start with `\`, no semicolon)
- `\?` and `\h` help system
- `\timing` for measuring query time
- `\x` for expanded output (wide rows)
- History and tab completion

### Steps

Reconnect:
```bash
docker exec -it pg psql -U postgres -d bookshelf
```

Try each:

```
\?          -- list of all meta-commands
\h SELECT   -- SQL help for SELECT syntax
\h          -- list all SQL commands psql knows help for
```

Turn on timing:
```
\timing
```

Run a query:
```sql
SELECT * FROM books;
```

You'll see `Time: 1.234 ms` under the result. Always leave timing on while learning.

Expanded output for tables with many columns:
```
\x
SELECT * FROM books;
\x
```

`\x` toggles. `\x auto` (run once) switches automatically based on terminal width.

Tab completion: type `SELECT * FROM bo` and press TAB. Should autocomplete to `books`.

History: press Up arrow to get previous commands. History survives psql restarts (stored in `~/.psql_history` by default, or wherever `HISTFILE` points).

### Exercises

1. Use `\h CREATE TABLE` - read the syntax diagram.
2. Run `SELECT * FROM books;` three times and note the timing values.
3. Use `\df` - list all functions. A LOT. Postgres ships with hundreds.
4. Use `\di` - list all indexes. You should see `books_pkey`.

### Check-in

Paste output of `\di`.

---

## L04 - Save your work in .sql files

### Concepts

- SQL as source code, not throwaway
- `\i` to run a file
- Keeping migration-like files under version control later

### Steps

Open a new terminal (leave psql open in the other). Create a file:

```bash
mkdir -p ~/pg-work && cd ~/pg-work
cat > seed_books.sql <<'EOF'
INSERT INTO books (title, author) VALUES
  ('The Art of PostgreSQL', 'Dimitri Fontaine'),
  ('Database Internals', 'Alex Petrov'),
  ('Designing Data-Intensive Applications', 'Martin Kleppmann');

SELECT count(*) AS total_books FROM books;
EOF
```

Now you have a file but your `books` table is inside the container. Two options:

**Option A: copy the file in, then \i it**
```bash
docker cp seed_books.sql pg:/tmp/seed_books.sql
```

Back in psql:
```
\i /tmp/seed_books.sql
```

**Option B: pipe it directly**
```bash
docker exec -i pg psql -U postgres -d bookshelf < seed_books.sql
```

(`-i` not `-it` when piping.)

### Exercises

1. Write a `schema.sql` file that creates a second table `authors (id identity PK, name text not null)`. Run it via either method.
2. Write a `cleanup.sql` that drops both tables. Don't run it yet.
3. What happens if you run `\i seed_books.sql` twice? Predict before trying.

Prediction answer: the second run duplicates the rows (because `title`/`author` aren't unique). The PK id keeps incrementing; no error.

### Check-in

Show your `seed_books.sql` content and the output of running `SELECT count(*) FROM books;`.

---

## L05 - Data persistence (volumes)

### Concepts

- Container storage is ephemeral by default
- Docker named volumes for persistence
- Migrating the existing container to a volume (or recreating with one)

### Step 1 - Prove the problem

If you `docker rm pg`, all your data dies. Let's not do that yet. Instead, imagine it happens.

### Step 2 - Stop and remove current container

```bash
docker stop pg
docker rm pg
```

Gone. Now recreate it with a volume:

```bash
docker run -d \
  --name pg \
  -e POSTGRES_PASSWORD=dev \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:17
```

New flag:
- `-v pgdata:/var/lib/postgresql/data` - mount a Docker-managed named volume `pgdata` at the Postgres data directory inside the container.

Docker creates the volume if it doesn't exist. Verify:

```bash
docker volume ls
```

You should see a `pgdata` volume.

### Step 3 - Re-seed

The database is fresh. Recreate:

```bash
docker exec -it pg psql -U postgres <<'EOF'
CREATE DATABASE bookshelf;
\c bookshelf
CREATE TABLE books (
  id     int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  title  text NOT NULL,
  author text NOT NULL
);
INSERT INTO books (title, author) VALUES
  ('The Art of PostgreSQL', 'Dimitri Fontaine'),
  ('Database Internals', 'Alex Petrov');
EOF
```

### Step 4 - Prove persistence works

```bash
docker stop pg
docker rm pg
docker run -d --name pg -e POSTGRES_PASSWORD=dev -p 5432:5432 -v pgdata:/var/lib/postgresql/data postgres:17
docker exec -it pg psql -U postgres -d bookshelf -c 'SELECT * FROM books;'
```

Your books should still be there. The container was destroyed; the volume survived.

### Concepts to take forward

- **Data lives in the volume, not the container.** Containers are disposable.
- **Named volumes** live under Docker's management. You can inspect them (`docker volume inspect pgdata`).
- **Bind mounts** (like `-v $(pwd)/data:/var/lib/postgresql/data`) put data in a host folder. Useful if you want to see / back up the files directly. Slower on Mac/Windows due to filesystem translation. Use named volumes for Postgres on Mac.
- To fully wipe data: `docker volume rm pgdata` (only when the container using it is stopped).

### Exercises

1. Run `docker volume inspect pgdata`. Note the `Mountpoint` path (on Mac this is inside a VM).
2. Stop and start `pg` three times. Confirm data survives.
3. Predict: if you `docker rm pg` but NOT `docker volume rm pgdata`, then recreate a new container with a different name pointing to `pgdata`, what happens? Try it.

Prediction: the new container sees the existing data. Volumes are the real home of data.

### Check-in

Paste output of `docker volume ls` and `SELECT * FROM books;` after a stop/start cycle.

---

## Module 0 completion criteria

- [ ] Container survives restarts, data in named volume
- [ ] You can enter psql, switch DBs, describe tables without looking up syntax
- [ ] You can run `.sql` files via `\i` or pipe
- [ ] You can read meta-command help (`\?`) and SQL help (`\h CREATE TABLE`) yourself

When all four are true, you've earned Module 1.
