# Module 4 - Advanced Queries (L20-L25)

Prereq: Module 3. You are comfortable with aggregations and GROUP BY.

---

## L20 - Subqueries

### Concept

A subquery is a SELECT nested inside another query. Three kinds: scalar, correlated, EXISTS.

### Scalar subquery

Returns one row with one column. Use in SELECT or WHERE:

```sql
SELECT title,
       (SELECT name FROM authors WHERE id = books.author_id) AS author
FROM books;
```

Works but almost always better rewritten as a JOIN.

### IN subquery

```sql
SELECT title FROM books
WHERE author_id IN (SELECT id FROM authors WHERE email LIKE '%@x.com');
```

### EXISTS (correlated)

```sql
SELECT a.name FROM authors a
WHERE EXISTS (SELECT 1 FROM books b WHERE b.author_id = a.id);
```

Postgres stops reading books once it finds one match - cheaper than IN for many cases.

### NOT EXISTS

"Authors with no books":
```sql
SELECT a.name FROM authors a
WHERE NOT EXISTS (SELECT 1 FROM books b WHERE b.author_id = a.id);
```

### The golden rule

- **EXISTS / NOT EXISTS** is usually the cleanest for "does related data exist"
- **JOIN** is cleanest for "I need columns from both"
- **IN** is fine for short static lists; prefer EXISTS for subqueries

### Exercises

1. Find books whose author has no email (`email IS NULL`). Write two ways: subquery and JOIN.
2. Find authors with at least one book published after 2019.
3. Find authors with zero books (use NOT EXISTS).

### Check-in

Paste the EXISTS version of exercise 2.

---

## L21 - Common Table Expressions (CTEs, WITH)

### Concept

A CTE is a named subquery. Makes complex queries readable.

### Steps

```sql
WITH recent_books AS (
  SELECT * FROM books WHERE published > '2018-01-01'
)
SELECT a.name, count(rb.id)
FROM authors a
LEFT JOIN recent_books rb ON rb.author_id = a.id
GROUP BY a.id, a.name;
```

Read top-down:
1. Define `recent_books` as a virtual table.
2. Use it in the outer query.

### Multi-CTE

```sql
WITH
  recent_books AS (SELECT * FROM books WHERE published > '2018-01-01'),
  author_counts AS (
    SELECT author_id, count(*) AS n
    FROM recent_books
    GROUP BY author_id
  )
SELECT a.name, ac.n
FROM author_counts ac
JOIN authors a ON a.id = ac.author_id
ORDER BY ac.n DESC;
```

### CTE optimization note

Pre-PG12 CTEs were always materialized (forced the planner's hand). PG12+ inlines them by default. So they're purely a readability tool now. Use them freely.

### Exercises

1. Rewrite any 2-step query you've done using a CTE.
2. Write a CTE that counts books per author, then another CTE that keeps only authors with >= 2 books, then select both.

### Check-in

Paste output of exercise 2.

---

## L22 - Recursive CTEs

### Concept

`WITH RECURSIVE` lets you walk hierarchies, graphs, series.

### Steps

Remember `employees` from L15? Build the full org tree with levels:

```sql
WITH RECURSIVE org AS (
  -- base case: CEO
  SELECT id, name, manager_id, 0 AS level
  FROM employees
  WHERE manager_id IS NULL

  UNION ALL

  -- recursive case: direct reports
  SELECT e.id, e.name, e.manager_id, org.level + 1
  FROM employees e
  JOIN org ON e.manager_id = org.id
)
SELECT level, name FROM org ORDER BY level, name;
```

Anatomy:
- Base case: start point (non-recursive)
- `UNION ALL`: combines base + recursive results
- Recursive case: refers to the CTE name itself

### Generate series

Non-table recursion for a sequence:
```sql
WITH RECURSIVE n(i) AS (
  SELECT 1
  UNION ALL
  SELECT i + 1 FROM n WHERE i < 10
)
SELECT i FROM n;
```

But `generate_series(1, 10)` is simpler. Recursion shines for actual graphs.

### Exercises

1. Show every employee with their chain of managers as a comma-separated string (advanced).
2. Use `generate_series` to list every Monday in 2026.
3. Build a Fibonacci generator with `WITH RECURSIVE`. Cap at 20 terms.

### Check-in

Paste output of the org tree query.

---

## L23 - Window functions, part 1

### Concept

Windows let you compute across a set of rows while returning one row per input row. Unlike GROUP BY, no collapse.

### Steps

```sql
SELECT
  title,
  author_id,
  count(*) OVER (PARTITION BY author_id) AS books_by_this_author
FROM books;
```

Each row keeps its own data AND sees its author's total.

### ROW_NUMBER and RANK

```sql
SELECT
  title,
  author_id,
  row_number() OVER (PARTITION BY author_id ORDER BY published) AS rn,
  rank()       OVER (PARTITION BY author_id ORDER BY published) AS rnk,
  dense_rank() OVER (PARTITION BY author_id ORDER BY published) AS dr
FROM books;
```

- `row_number`: 1, 2, 3 strict (ties broken arbitrarily)
- `rank`: 1, 2, 2, 4 (gaps on ties)
- `dense_rank`: 1, 2, 2, 3 (no gaps)

### Top N per group

"Latest book per author":
```sql
SELECT * FROM (
  SELECT
    *,
    row_number() OVER (PARTITION BY author_id ORDER BY published DESC) AS rn
  FROM books
) t
WHERE rn = 1;
```

Same as `DISTINCT ON` from L19. Windows are more flexible when you need top-N not just top-1.

### Exercises

1. Add a column `rank_within_author` numbered by publication date.
2. Find the 2 most recent books per author.
3. Compare `row_number` vs `rank` vs `dense_rank` on a tied dataset.

### Check-in

Paste output of exercise 2.

---

## L24 - Window functions, part 2: LAG, LEAD, running totals

### Concept

`LAG` and `LEAD` look at neighboring rows. `SUM OVER` computes running totals.

### Steps

```sql
SELECT
  title, published,
  lag(published)  OVER (ORDER BY published) AS prev_published,
  lead(published) OVER (ORDER BY published) AS next_published,
  published - lag(published) OVER (ORDER BY published) AS gap_since_last
FROM books;
```

Running total of pages per author (assuming a page_count column):
```sql
-- Add page_count first
ALTER TABLE books ADD COLUMN IF NOT EXISTS page_count int;
UPDATE books SET page_count = 400 WHERE page_count IS NULL;

SELECT
  author_id, title,
  sum(page_count) OVER (PARTITION BY author_id ORDER BY published) AS running_total
FROM books
ORDER BY author_id, published;
```

`ORDER BY` in the window makes it cumulative. Without it, SUM would be total-per-partition on every row.

### Frame clause (preview)

```sql
sum(x) OVER (
  PARTITION BY group
  ORDER BY ts
  ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
)
```

Moving sums. Advanced, used in analytics.

### Exercises

1. Find the gap in days between each author's consecutive books.
2. Cumulative count of books published each year (running count).
3. Read the docs section on frame clauses, write down what `RANGE` vs `ROWS` does differently.

### Check-in

Paste output of exercise 1.

---

## L25 - LATERAL joins

### Concept

A LATERAL subquery can reference columns from tables listed before it in the FROM clause. Think: "for each row from A, run this subquery".

### Steps

"Top 2 most recent books per author, one row each":
```sql
SELECT a.name, b.title, b.published
FROM authors a
JOIN LATERAL (
  SELECT title, published
  FROM books
  WHERE author_id = a.id
  ORDER BY published DESC
  LIMIT 2
) b ON true;
```

Without LATERAL you can't reference `a.id` inside the subquery.

### Use cases

- Top N per group (more flexible than window + filter)
- Calling a set-returning function per row: `CROSS JOIN LATERAL generate_series(...)`
- Per-row derived columns that need expensive computation

### Example with generate_series

"One row per day for each book's lifetime":
```sql
SELECT b.title, d::date AS day
FROM books b
CROSS JOIN LATERAL generate_series(b.published, b.published + interval '7 days', interval '1 day') d;
```

### Exercises

1. For each author, get their 3 most recent books.
2. For each book, expand out a row for each weekday in the publication week.

### Check-in

Paste output of exercise 1.

---

## Module 4 completion criteria

- [ ] You choose JOIN vs EXISTS vs IN based on intent, not habit
- [ ] You reach for CTEs when a query has more than 2 clauses
- [ ] You know when a recursive CTE is needed
- [ ] You can write a top-N-per-group query two ways (window + filter, or LATERAL)
