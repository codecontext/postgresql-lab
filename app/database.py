import os

import psycopg


class DatabaseNotConfiguredError(Exception):
    pass


class DatabaseConnectionError(Exception):
    pass


def check_database_connection() -> None:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise DatabaseNotConfiguredError("DATABASE_URL is not configured")

    try:
        with psycopg.connect(database_url, connect_timeout=3) as connection:
            connection.execute("SELECT 1").fetchone()
    except psycopg.Error as error:
        raise DatabaseConnectionError from error