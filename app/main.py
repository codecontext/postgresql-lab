import os

import psycopg
from fastapi import FastAPI
from fastapi import HTTPException

app = FastAPI(title="PostgreSQL Learning Lab")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/database")
def database_health_check() -> dict[str, str]:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise HTTPException(
            status_code=503,
            detail="DATABASE_URL is not configured",
        )

    try:
        with psycopg.connect(database_url, connect_timeout=3) as connection:
            connection.execute("SELECT 1").fetchone()
    except psycopg.Error as error:
        raise HTTPException(
            status_code=503,
            detail="Unable to connect to PostgreSQL",
        ) from error

    return {"status": "ok", "database": "connected"}