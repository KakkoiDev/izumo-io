# Module 12 - Vectors (L59-L62)

Prereq: Modules 0-7 at minimum. This introduces our second extension, `pgvector`.

---

## L59 - What is a vector? (no ML required)

### Concept

A vector is an ordered list of numbers: `[0.12, -0.43, 0.87, ...]`.

In AI apps, an "embedding" is a vector that represents the meaning of a piece of text (or image). Two similar texts have vectors that are geometrically close.

Typical embedding dimensions:
- OpenAI text-embedding-3-small: 1536
- Cohere embed-v3: 1024
- Many open-source models: 384 / 768

### Distance metrics

- **Cosine distance**: angle between vectors (usually best for text embeddings)
- **L2 (Euclidean)**: straight-line distance
- **Inner product**: dot product

### Why in Postgres?

You can JOIN vectors with your relational data. Example: "find the 5 most similar articles to this query, authored by users in France". Impossible cleanly with a separate vector DB.

### No steps, no check-in.

---

## L60 - Install pgvector

### Concept

Our base image `postgres:17` doesn't include pgvector. Switch to `pgvector/pgvector:pg17` which does.

### Steps

Stop current container:
```bash
docker stop pg
docker rm pg
```

Recreate pointing to the same volume:
```bash
docker run -d \
  --name pg \
  -e POSTGRES_PASSWORD=dev \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  pgvector/pgvector:pg17
```

Connect and enable:
```bash
docker exec -it pg psql -U postgres -d bookshelf
```

```sql
CREATE EXTENSION IF NOT EXISTS vector;
\dx
```

You should see `vector` listed.

### Exercises

1. `\dx+ vector` - list the functions and types it adds.
2. Read about installation alternatives if you're on another setup.

### Check-in

Paste output of `\dx`.

---

## L61 - Store and query embeddings

### Concept

Define a column of type `vector(N)` where N is dim. Insert arrays of floats. Query with distance operators.

### Steps

```sql
CREATE TABLE docs (
  id     int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  title  text NOT NULL,
  body   text,
  emb    vector(3)  -- tiny for demo; use 1536 etc in real apps
);

INSERT INTO docs (title, emb) VALUES
  ('cat',   '[0.9, 0.1, 0.0]'),
  ('kitten','[0.85, 0.15, 0.0]'),
  ('dog',   '[0.1, 0.9, 0.0]'),
  ('car',   '[0.0, 0.0, 0.9]');
```

Distance operators:
- `<=>` - cosine distance
- `<->` - L2 distance
- `<#>` - negative inner product

Find closest to `[0.9, 0.1, 0.0]`:
```sql
SELECT title, emb <=> '[0.9, 0.1, 0.0]' AS dist
FROM docs
ORDER BY dist
LIMIT 3;
```

`kitten` should be very close; `dog` far; `car` farthest.

### Getting real embeddings

Usually from an API:
- OpenAI: `text-embedding-3-small`
- Cohere, Voyage, local Ollama, etc.

You call the API from your app, get back a vector, insert it. Or use the `pgai` extension (optional upgrade) to call LLMs inline from SQL.

### Exercises

1. Insert 10 more 3-dim vectors, some close to existing ones, some far. Run similarity queries.
2. Add a WHERE clause to the similarity search.

### Check-in

Paste the top-3 result for a given query vector.

---

## L62 - HNSW index

### Concept

Brute-force vector search is O(N). Not OK past 100k rows. We use approximate nearest neighbor indexes.

pgvector offers:
- **HNSW** (Hierarchical Navigable Small World): slower to build, higher recall, better for dynamic data
- **IVFFlat**: faster to build, lower recall, good for static data

Default choice: HNSW.

### Steps

Big seed:
```sql
INSERT INTO docs (title, emb)
SELECT 'doc_' || g, ARRAY[random(), random(), random()]::vector
FROM generate_series(1, 100000) g;
```

Time without index:
```sql
\timing
SELECT title FROM docs ORDER BY emb <=> '[0.5,0.5,0.5]' LIMIT 5;
```

Create HNSW:
```sql
CREATE INDEX docs_emb_hnsw_idx ON docs USING hnsw (emb vector_cosine_ops);
```

(Index build takes a bit. Tunable params: `m` and `ef_construction`.)

Retime.

### Operator classes

Match the class to your distance:
- `vector_cosine_ops` for `<=>`
- `vector_l2_ops` for `<->`
- `vector_ip_ops` for `<#>`

Using the wrong class means the index won't be used.

### Hybrid queries

Filter AND search:
```sql
SELECT title, emb <=> '[0.5,0.5,0.5]' AS d
FROM docs
WHERE title LIKE 'doc_1%'
ORDER BY d
LIMIT 5;
```

Works, but the filter reduces the planner's ability to use the index optimally. For large-scale hybrid search, see pgvectorscale's StreamingDiskANN.

### Exercises

1. Build an HNSW index. EXPLAIN the same query before and after.
2. Change to IVFFlat (drop and recreate). Compare recall and build time (run the same query, compare top-k).

### Check-in

Paste the EXPLAIN output showing `Index Scan using docs_emb_hnsw_idx`.

---

## Module 12 completion criteria

- [ ] You understand embeddings as vectors of numbers
- [ ] You use the right distance operator for your model
- [ ] You index with HNSW using the matching operator class
- [ ] You can write a hybrid (filter + vector search) query
