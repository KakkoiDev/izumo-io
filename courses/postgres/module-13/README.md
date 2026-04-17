# Module 13 - Geo (L63-L65) [optional track]

Prereq: basic SQL. Enables spatial queries via PostGIS.

This module is optional. Skip if you don't need geo.

---

## L63 - Install PostGIS

### Concept

PostGIS adds geography and geometry types, spatial indexes (GiST), hundreds of `ST_*` functions. Industry standard.

### Steps

Easiest path: switch to the PostGIS-enabled image.

```bash
docker stop pg
docker rm pg
docker run -d \
  --name pg \
  -e POSTGRES_PASSWORD=dev \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgis/postgis:17-3.5
```

Connect:
```bash
docker exec -it pg psql -U postgres -d bookshelf
```

Enable:
```sql
CREATE EXTENSION IF NOT EXISTS postgis;
\dx
SELECT PostGIS_Version();
```

### Note on image switching

Your existing data (in volume `pgdata`) is preserved. The image brings new binaries. If you see version mismatch errors, you may need to run `SELECT pg_upgrade` or recreate the volume.

### Exercises

1. Enable, check version, list some functions with `\df ST_*`.

### Check-in

Paste `SELECT PostGIS_Version();` output.

---

## L64 - geography vs geometry

### Concept

- **geometry**: 2D planar. Fast. Assumes your data is on a flat map.
- **geography**: spherical earth. Slower. Correct for Earth-scale distances.

Rule of thumb: for "real world lat/lng" use `geography`. For local CAD / small-area work use `geometry`.

### Steps

```sql
CREATE TABLE places (
  id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name text NOT NULL,
  loc geography(Point, 4326) NOT NULL
);

INSERT INTO places (name, loc) VALUES
  ('Tokyo Tower', ST_MakePoint(139.7454, 35.6586)::geography),
  ('Shibuya',     ST_MakePoint(139.7004, 35.6591)::geography),
  ('Osaka',       ST_MakePoint(135.5023, 34.6937)::geography);
```

SRID 4326 = WGS84 = what GPS and Google Maps use.

Distance (meters):
```sql
SELECT a.name, b.name, ST_Distance(a.loc, b.loc) AS meters
FROM places a, places b
WHERE a.id < b.id;
```

### Within / Nearest

```sql
SELECT name FROM places
WHERE ST_DWithin(loc, ST_MakePoint(139.7, 35.7)::geography, 5000);
-- within 5 km
```

### Exercises

1. Insert 5 more places, find all within 10 km of Shibuya.
2. Find the closest place to Kyoto.

### Check-in

Paste the within-10-km query result.

---

## L65 - GiST indexes for geo

### Concept

GiST (Generalized Search Tree) indexes 2D shapes. PostGIS uses it by default.

### Steps

```sql
CREATE INDEX places_loc_gix ON places USING GIST (loc);
```

Now `ST_DWithin` queries are fast.

### Polygon containment

```sql
-- A bounding box
SELECT name FROM places
WHERE ST_Within(loc::geometry,
                ST_MakeEnvelope(139.6, 35.5, 139.8, 35.7, 4326));
```

### Exercises

1. Create a `regions` table with a polygon column. Insert a polygon around central Tokyo. Find all places within it.
2. Read about `ST_Buffer` - create buffers around points.

### Check-in

Paste EXPLAIN showing the GiST index being used.

---

## Module 13 completion criteria

- [ ] You enable PostGIS
- [ ] You choose `geography` for planet-scale, `geometry` for local work
- [ ] You use GiST indexes with `ST_DWithin` / `ST_Contains`
