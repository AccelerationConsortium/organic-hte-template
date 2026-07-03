# analysis/

Code that turns measurements into derived results — each run of it should
create an `Analysis` record in AnaliticaDB (linked to the measurements it
consumed, with `method`/`parameters` and this repo's commit hash as
`source_commit`), never edit measurement rows.

Keep the code parameterized and re-runnable: a re-analysis inserts a new
`Analysis` that supersedes the old one; both remain queryable.
