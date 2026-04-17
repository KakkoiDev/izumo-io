# Module 2 - Multiple Tables (L11-L15)

Prereq: Module 1 complete. You're comfortable with SELECT, INSERT, UPDATE, DELETE on one table.

---

## L11 - Why multiple tables? Normalization intuition

### Concept

If you store "book and its author" in one row, you repeat the author's name. Change "Martin Kleppmann" to "Martin A. Kleppmann" and you have to update every row. Miss one, inconsistency.

Normalization: split data so each fact lives in exactly one place.

### Illustration (don't run yet, just read)

Denormalized:
```
books(id, title, author_name, author_email, author_country)
  1, 'Book A', 'Alice', 'a@x.com', 'FR'
  2, 'Book B', 'Alice', 'a@x.com', 'FR'
```

If Alice changes email: 2 rows to update. At 10,000 books: disaster.

Normalized:
```
authors(id, name, email, country)
  1, 'Alice', 'a@x.com', 'FR'

books(id, title, author_id)
  1, 'Book A', 1
  2, 'Book B', 1
```

Alice's email change: one row. Book queries get the author via a JOIN (next lesson).

### Normal forms

- **1NF**: no repeating groups; each cell holds a single atomic value (no CSV strings in a column; use `text[]` if you must have a set)
- **2NF**: every non-key column depends on the whole key
- **3NF**: non-key columns depend only on the key, not on other non-key columns

Rule of thumb: if you see the same value in many rows and it can change, extract it into its own table.

### When NOT to normalize

- Read-heavy analytics. Denormalized rolls are faster.
- Audit / snapshot tables. You want historical values frozen.
- JSONB columns for semi-structured bits that don't warrant a full table.

### No steps, no exercises, no check-in.

Move to L12 when you can explain normalization to a friend in 30 seconds.

---

## L12 - Foreign keys and referential integrity

### Concept

A foreign key is a column that references another table's primary key. Postgres enforces that the referenced row exists.

### Steps

Start clean in `bookshelf`:

```sql
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS authors;

CREATE TABLE authors (
  id    int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name  text NOT NULL,
  email text UNIQUE
);

CREATE TABLE books (
  id         int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  title      text NOT NULL,
  author_id  int NOT NULL REFERENCES authors(id),
  published  date
);
```

The key line: `author_id int NOT NULL REFERENCES authors(id)`.

Insert in order:
```sql
INSERT INTO authors (name, email) VALUES
  ('Martin Kleppmann', 'mk@x.com'),
  ('Dimitri Fontaine', 'df@x.com');

INSERT INTO books (title, author_id, published) VALUES
  ('Designing Data-Intensive Applications', 1, '2017-03-16'),
  ('The Art of PostgreSQL', 2, '2018-06-01');
```

Try a bad insert:
```sql
INSERT INTO books (title, author_id) VALUES ('Ghost Book', 999);
```

Expected: `insert or update on table "books" violates foreign key constraint`. Postgres protected your data.

### ON DELETE behaviors

```sql
DELETE FROM authors WHERE id = 1;
```

Expected: error, because a book still references id=1.

Options when declaring the FK:
- `ON DELETE RESTRICT` (default) - refuse to delete if referenced
- `ON DELETE CASCADE` - delete referencing rows too
- `ON DELETE SET NULL` - set FK column to NULL (must be nullable)
- `ON DELETE SET DEFAULT` - set to column default

Example with cascade:
```sql
ALTER TABLE books DROP CONSTRAINT books_author_id_fkey;
ALTER TABLE books ADD CONSTRAINT books_author_id_fkey
  FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE;

DELETE FROM authors WHERE id = 1;
SELECT * FROM books;  -- the book is gone too
```

### Concept: integrity over convenience

Beginners hate the FK error. Pros love it. The error is the DB keeping your data consistent. You lose silent data corruption in exchange for explicit errors at the boundary.

### Exercises

1. Add a `publishers` table (id PK, name not null). Add `publisher_id` FK to `books` with `ON DELETE SET NULL`. Why set null and not cascade?
2. Re-seed authors and books. Try deleting a referenced author, see the error.
3. Look up "composite foreign keys" and write down when you'd use one.

### Check-in

Show `\d books` - confirm the FK constraint appears at the bottom.

---

## L13 - Your first INNER JOIN

### Concept

A JOIN stitches rows from two tables based on a matching column.

### Steps

```sql
SELECT b.title, a.name AS author
FROM books b
JOIN authors a ON b.author_id = a.id;
```

Read this slowly:
- `FROM books b` - alias `books` as `b`
- `JOIN authors a` - also join `authors`, aliased as `a`
- `ON b.author_id = a.id` - match condition
- SELECT pulls columns from both

Without alias:
```sql
SELECT books.title, authors.name
FROM books
JOIN authors ON books.author_id = authors.id;
```

Works. Aliases just shorten.

### Default JOIN = INNER JOIN

An INNER JOIN returns only rows that match on both sides. If a book had `author_id` pointing to nobody (can't happen here because of the FK, but imagine), it'd be excluded.

### Three-way join (preview)

```sql
ALTER TABLE books ADD COLUMN publisher_id int REFERENCES authors(id);

-- Pretend author 2 is also a publisher for demo
UPDATE books SET publisher_id = 2;

SELECT b.title, a.name AS author, p.name AS publisher
FROM books b
JOIN authors a ON b.author_id = a.id
JOIN authors p ON b.publisher_id = p.id;
```

Two joins on the same table using different aliases. Reusable pattern.

### Exercises

1. Write a query that lists every book with its author's email.
2. Add two more books. Re-run the join. Confirm new books appear.
3. Try `FROM books, authors WHERE books.author_id = authors.id`. That's the old (pre-1992) implicit join syntax. Works, but harder to read and more error-prone. Prefer explicit JOIN.

### Check-in

Paste output of query 1.

---

## L14 - LEFT JOIN and the "missing rows" trap

### Concept

A LEFT JOIN returns all rows from the left table, matching rows from the right, and NULL for missing matches.

### Steps

Insert an author with no books:
```sql
INSERT INTO authors (name, email) VALUES ('Egor Rogov', 'er@x.com');
```

INNER JOIN skips them:
```sql
SELECT a.name, b.title
FROM authors a
JOIN books b ON b.author_id = a.id;
```

LEFT JOIN keeps them:
```sql
SELECT a.name, b.title
FROM authors a
LEFT JOIN books b ON b.author_id = a.id;
```

Egor shows up with `title = NULL`.

### Use case: "authors with no books"

```sql
SELECT a.name
FROM authors a
LEFT JOIN books b ON b.author_id = a.id
WHERE b.id IS NULL;
```

Note: the WHERE must be on the right side's primary key or NOT NULL column to reliably find unmatched rows.

### Anti-join alternative

```sql
SELECT a.name
FROM authors a
WHERE NOT EXISTS (SELECT 1 FROM books b WHERE b.author_id = a.id);
```

Often cleaner. Both work. We'll see `EXISTS` more in Module 4.

### FULL OUTER JOIN (rare)

Returns everything from both sides, NULLs where missing. Rarely needed outside analytics.

### Exercises

1. Count books per author, including authors with 0 books.
   ```sql
   SELECT a.name, count(b.id) AS book_count
   FROM authors a
   LEFT JOIN books b ON b.author_id = a.id
   GROUP BY a.id, a.name
   ORDER BY book_count DESC;
   ```
   Why `count(b.id)` and not `count(*)`?
2. Rewrite "authors with no books" as a NOT EXISTS.

Answer to 1: `count(*)` would be 1 even for authors with no books (the LEFT JOIN produces one row with NULLs). `count(b.id)` counts non-null book ids, so 0 for those.

### Check-in

Paste output of exercise 1.

---

## L15 - Self-joins

### Concept

A self-join is a table joined to itself, usually via an alias. Used for hierarchies and peer comparisons.

### Steps

Make a table that references itself:

```sql
CREATE TABLE employees (
  id        int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name      text NOT NULL,
  manager_id int REFERENCES employees(id)
);

INSERT INTO employees (name, manager_id) VALUES
  ('CEO', NULL),
  ('VP Eng', 1),
  ('VP Sales', 1),
  ('Engineer', 2),
  ('Sales Rep', 3);
```

Employee with their manager's name:
```sql
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON m.id = e.manager_id;
```

LEFT JOIN because the CEO has no manager (`manager_id IS NULL`).

### Finding peers (same manager)

```sql
SELECT a.name AS employee, b.name AS peer
FROM employees a
JOIN employees b ON a.manager_id = b.manager_id AND a.id <> b.id;
```

`<>` (not equal) excludes matching the employee to themselves.

### Recursive query preview

To get a whole org tree you need a recursive CTE. We cover that in Module 4. Don't try to get 5 levels deep with self-joins alone.

### Exercises

1. List all employees whose manager is the CEO.
2. List employees who have no manager (should return 1 row).
3. Predict: what happens if you forget the `LEFT` in the manager query? Which row disappears?

Answer to 3: the CEO disappears, because INNER JOIN requires a match on the manager side.

### Check-in

Paste the output of the "employee with their manager's name" query.

---

## Module 2 completion criteria

- [ ] You can design a 2-3 table schema with FKs and the right ON DELETE behavior
- [ ] You pick LEFT vs INNER based on whether missing matches should appear
- [ ] You use table aliases without thinking
- [ ] You can find "rows in A with no match in B" two ways (LEFT JOIN + IS NULL, or NOT EXISTS)
