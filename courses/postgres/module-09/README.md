# Module 9 - Full-Text Search (L45-L50)

Prereq: Module 5 (indexes), Module 7 (GIN exposure).

This module installs our first extension: `pg_trgm`.

---

## L45 - tsvector

### Concept

Full-text search stores documents as a `tsvector`: a bag of normalized, stemmed words (lexemes) plus positions.

### Steps

```sql
SELECT to_tsvector('english', 'The quick brown foxes are running quickly');
-- 'brown':3 'fox':4 'quick':2 'quickli':7 'run':6
```

Stemming folds "foxes" -> "fox", "running" -> "run". "The", "are" are removed as stop words.

Different languages:
```sql
SELECT to_tsvector('french', 'Les renards courent vite');
```

### Add a tsvector column via generated column

```sql
DROP TABLE IF EXISTS articles;
CREATE TABLE articles (
  id      int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  title   text NOT NULL,
  body    text NOT NULL,
  search  tsvector GENERATED ALWAYS AS (
    setweight(to_tsvector('english', coalesce(title,'')), 'A') ||
    setweight(to_tsvector('english', coalesce(body, '')), 'B')
  ) STORED
);

INSERT INTO articles (title, body) VALUES
  ('Postgres is fast', 'Postgres is a battle-tested database.'),
  ('Redis and caching', 'Redis is a fast in-memory store.'),
  ('Kafka at scale', 'Kafka is used for streaming events.');
```

`setweight` marks title as weight 'A' (important), body as 'B' (less). Used later for ranking.

### Exercises

1. Inspect `SELECT search FROM articles;`. Read the output.
2. Add one row with body in French. Notice "english" tsvector won't stem correctly for French text.

### Check-in

Paste the `search` column of your 3 articles.

---

## L46 - tsquery and @@

### Concept

`tsquery` is a search query. `@@` is the match operator.

### Steps

```sql
SELECT title FROM articles WHERE search @@ to_tsquery('english', 'fast');
```

Operators inside tsquery:
- `&` AND, `|` OR, `!` NOT
- `<->` phrase match (followed by)

```sql
SELECT title FROM articles WHERE search @@ to_tsquery('english', 'postgres & fast');
SELECT title FROM articles WHERE search @@ to_tsquery('english', 'redis | kafka');
SELECT title FROM articles WHERE search @@ to_tsquery('english', '!kafka & fast');
```

### User input safety

`to_tsquery` expects properly formatted queries. For raw user input use `websearch_to_tsquery`:

```sql
SELECT title FROM articles
WHERE search @@ websearch_to_tsquery('english', '"fast database" -redis');
```

`websearch_to_tsquery` handles quotes, spaces, minus like Google does. Safer for user strings.

### Exercises

1. Search for "streaming OR in-memory".
2. Search for the phrase "battle tested".

### Check-in

Show results of exercise 2.

---

## L47 - GIN for FTS

### Concept

GIN indexes `tsvector` for fast search.

### Steps

Seed bigger:
```sql
INSERT INTO articles (title, body)
SELECT
  'Article ' || g,
  'Body number ' || g || ' about databases and systems.'
FROM generate_series(1, 100000) g;
```

Time the search:
```sql
\timing
SELECT count(*) FROM articles
WHERE search @@ to_tsquery('english', 'databases');
```

Add the index:
```sql
CREATE INDEX articles_search_gin_idx ON articles USING GIN (search);
```

Retime.

### Exercises

1. Compare EXPLAIN before and after the index.
2. Use ranking: `ts_rank_cd(search, query) AS rank`.

### Check-in

Paste timings before and after.

---

## L48 - Install pg_trgm (first extension!)

### Concept

`pg_trgm` enables trigram matching: fuzzy search, autocomplete, `LIKE '%...%'` acceleration.

### Steps

Inside psql:
```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;
\dx
```

You should see `pg_trgm` in the list. That's all it takes to add an extension when the binaries are installed in the image (the official Postgres image includes pg_trgm by default).

Try:
```sql
SELECT similarity('postgres', 'postgress');
SELECT word_similarity('pgs', 'postgres');
```

Similarity is a 0-1 score. Trigrams of 'postgres': "pos", "ost", "stg"... Two strings share more trigrams = higher score.

### Exercises

1. What's the similarity between 'docker' and 'dokker'?
2. Read the `pg_trgm` docs with `\h CREATE EXTENSION`. Check its functions with `\df *similarity*`.

### Check-in

Paste the output of `\dx`.

---

## L49 - Fuzzy search with similarity()

### Steps

```sql
SELECT name FROM users WHERE similarity(name, 'alise') > 0.3;
-- finds 'Alice' despite typo
```

Index support: trigram GIN:
```sql
CREATE INDEX users_name_trgm_idx ON users USING GIN (name gin_trgm_ops);
```

Now `LIKE '%alice%'` also becomes fast:
```sql
SELECT name FROM users WHERE name ILIKE '%alice%';
```

### Exercises

1. Search for all author names similar to 'Kleppmon'.
2. Time ILIKE before and after creating the trigram GIN index.

### Check-in

Paste the result and timing from exercise 1 post-index.

---

## L50 - Ranking results

### Steps

```sql
SELECT
  title,
  ts_rank_cd(search, query) AS rank
FROM articles,
     websearch_to_tsquery('english', 'postgres fast') AS query
WHERE search @@ query
ORDER BY rank DESC
LIMIT 5;
```

`ts_rank_cd` uses document length and term proximity. Prefer `ts_rank_cd` over `ts_rank`.

### Combine FTS with trigram (hybrid)

```sql
SELECT title, ts_rank_cd(search, query) AS rank, similarity(title, 'postgress') AS sim
FROM articles,
     websearch_to_tsquery('english', 'fast') AS query
WHERE search @@ query OR title % 'postgress'
ORDER BY rank + sim DESC
LIMIT 10;
```

### Headline highlighting

```sql
SELECT ts_headline('english', body, websearch_to_tsquery('english', 'postgres'))
FROM articles WHERE search @@ websearch_to_tsquery('english', 'postgres')
LIMIT 1;
```

Returns text with the match highlighted.

### Exercises

1. Build a search that:
   - matches FTS terms first
   - falls back to trigram similarity for typos
   - returns title + snippet via ts_headline
2. Compare your hand-rolled FTS to the raw ILIKE approach.

### Check-in

Paste the search results with highlighted headlines.

---

## Module 9 completion criteria

- [ ] You add tsvector generated columns with weights
- [ ] You GIN-index them
- [ ] You query with `websearch_to_tsquery`
- [ ] You install `pg_trgm` and use it for fuzzy + LIKE acceleration
- [ ] You rank results with `ts_rank_cd` and highlight with `ts_headline`
