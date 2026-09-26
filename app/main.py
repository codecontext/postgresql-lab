from fastapi import FastAPI
from fastapi import HTTPException

from app.database import DatabaseConnectionError
from app.database import DatabaseNotConfiguredError
from app.database import check_database_connection

app = FastAPI(title="PostgreSQL Learning Lab")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/database")
def database_health_check() -> dict[str, str]:
    try:
        check_database_connection()
    except DatabaseNotConfiguredError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        ) from error
    except DatabaseConnectionError as error:
        raise HTTPException(
            status_code=503,
            detail="Unable to connect to PostgreSQL",
        ) from error

    return {"status": "ok", "database": "connected"}