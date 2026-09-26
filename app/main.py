from pathlib import Path

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import FileResponse

from app.database import DatabaseConnectionError
from app.database import DatabaseNotConfiguredError
from app.database import check_database_connection
from app.database import get_learning_schema
from app.database import TableInfo

app = FastAPI(title="PostgreSQL Learning Lab")


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(Path(__file__).parent / "static" / "index.html")


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


@app.get("/api/explorer/learning-schema")
def learning_schema() -> list[TableInfo]:
    try:
        return get_learning_schema()
    except DatabaseNotConfiguredError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        ) from error
    except DatabaseConnectionError as error:
        raise HTTPException(
            status_code=503,
            detail="Unable to read PostgreSQL schema",
        ) from error