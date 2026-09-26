# PostgreSQL Learning Lab

A small, hands-on environment for learning PostgreSQL. Features are added
incrementally, with SQL kept visible and PostgreSQL as the source of truth.

## Requirements

- Python 3.10 or later
- PostgreSQL

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL='postgresql://USER:PASSWORD@HOST:5432/DATABASE'
python -m uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000/> for the read-only Database Explorer. It displays
the `learning` schema after the setup script has been run and `DATABASE_URL` is
configured. Open <http://127.0.0.1:8000/health> to check the API, or
<http://127.0.0.1:8000/health/database> to check the PostgreSQL connection.

## Create the learning schema

With `DATABASE_URL` set, create the sample schema and data by running:

```bash
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f sql/001_learning_schema.sql
```

The script creates `learning.students`, `learning.courses`, and
`learning.enrollments`, then inserts a small set of sample rows. It can be run
again without duplicating those rows.