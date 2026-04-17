# Module 3 - Aggregation (L16-L19)

Prereq: Module 2. You have `authors`, `books`, `employees` tables.

---

## L16 - COUNT, SUM, AVG, MIN, MAX

### Concepts

Aggregate functions collapse many rows into one value.

### Steps

Seed more books:
```sql
INSERT INTO books (title, author_id, published) VALUES
  ('Book X', 2, '2020-01-01'),
  ('Book Y', 3, '2021-06-15'),
  ('Book Z', 2, '2019-03-01');
```

Basics:
```sql
SELECT count(*) FROM books;                    -- total rows
SELECT count(author_id) FROM books;            -- non-null author_ids
SELECT count(DISTINCT author_id) FROM books;   -- unique authors
SELECT max(published), min(published) FROM books;
```

Aggregates on numerics:
```sql
SELECT avg(page_count), sum(page_count) FROM playground;  -- adapt if you dropped it
```

String aggregation:
```sql
SELECT string_agg(title, ', ' ORDER BY title) FROM books;
```

Array aggregation:
```sql
SELECT array_agg(title ORDER BY published) FROM books;
```

### Exercises

1. Find the earliest and latest book.
2. Find the total number of distinct author names in books.
3. Comma-separate all titles alphabetically.

### Check-in

Paste output of exercise 1.

---

## L17 - GROUP BY

### Concept

GROUP BY collapses rows into groups; aggregates compute per group.

### Steps

```sql
SELECT author_id, count(*) AS book_count
FROM books
GROUP BY author_id
ORDER BY book_count DESC;
```

With join for readable output:
```sql
SELECT a.name, count(b.id) AS book_count
FROM authors a
LEFT JOIN books b ON b.author_id = a.id
GROUP BY a.id, a.name
ORDER BY book_count DESC;
```

### The "must appear in GROUP BY" error

Try:
```sql
SELECT a.name, b.title, count(*)
FROM authors a JOIN books b ON b.author_id = a.id
GROUP BY a.name;
```

Expected: `column "b.title" must appear in the GROUP BY clause or be used in an aggregate function`.

Why: you asked for `b.title`, but grouped only by `a.name`. Each group has many titles. Postgres refuses to silently pick one.

Fix options:
- Add `b.title` to GROUP BY (creates one group per name+title)
- Aggregate `b.title` (e.g., `string_agg(b.title, ', ')`)

### Grouping by expressions

```sql
SELECT extract(year from published) AS year, count(*)
FROM books
WHERE published IS NOT NULL
GROUP BY year
ORDER BY year;
```

### Exercises

1. Books per year of publication.
2. Average number of books per author (advanced: two aggregates combined).
3. Find authors who have written exactly 2 books.

### Check-in

Paste output of exercise 1.

---

## L18 - HAVING vs WHERE

### Concept

- `WHERE` filters rows BEFORE grouping
- `HAVING` filters groups AFTER aggregation

### Steps

Authors with more than 1 book:
```sql
SELECT a.name, count(b.id) AS book_count
FROM authors a
JOIN books b ON b.author_id = a.id
GROUP BY a.id, a.name
HAVING count(b.id) > 1;
```

Can't use `WHERE count(b.id) > 1` - aggregates aren't available at WHERE time.

### Both in one query

Books published after 2018, then authors with more than 1 such book:
```sql
SELECT a.name, count(b.id) AS book_count
FROM authors a
JOIN books b ON b.author_id = a.id
WHERE b.published > '2018-01-01'    -- filter rows first
GROUP BY a.id, a.name
HAVING count(b.id) > 1;             -- then filter groups
```

### Exercises

1. Authors with an average (hypothetical page_count) > 300. Use HAVING.
2. Authors publishing in the last 5 years with >= 2 books in that window.

### Check-in

Paste output of the "authors with more than 1 book" query.

---

## L19 - DISTINCT and its costs

### Concept

`DISTINCT` removes duplicate rows. Cheap to type, often expensive to run.

### Steps

Insert a duplicate-looking row:
```sql
INSERT INTO authors (name, email) VALUES ('Martin Kleppmann', 'different@x.com');
SELECT name FROM authors;            -- Martin appears twice
SELECT DISTINCT name FROM authors;   -- once
```

`DISTINCT` sorts or hashes to find uniques. On large tables this can be slow. Prefer a query that doesn't produce duplicates to begin with.

### DISTINCT ON (Postgres-specific gem)

"For each author, one book with the earliest publication date":
```sql
SELECT DISTINCT ON (b.author_id)
       b.author_id, b.title, b.published
FROM books b
ORDER BY b.author_id, b.published ASC;
```

`DISTINCT ON (expr)` keeps the first row per group. You must sort by the ON columns first, then by the tiebreaker.

### Exercises

1. Run `SELECT name FROM authors;` vs `SELECT DISTINCT name FROM authors;`. Compare row counts.
2. Use `DISTINCT ON` to find the latest book per author.
3. Rewrite exercise 2 with `ROW_NUMBER()` (preview; we do this properly in Module 4). It's OK if you can't yet.

### Check-in

Paste output of exercise 2.

---

## Module 3 completion criteria

- [ ] You know when to use `count(*)` vs `count(col)`
- [ ] You correctly place columns in SELECT vs GROUP BY
- [ ] You use HAVING for post-aggregate filters, WHERE for pre-aggregate
- [ ] You use `DISTINCT ON` instead of DISTINCT when grouping is the real intent
