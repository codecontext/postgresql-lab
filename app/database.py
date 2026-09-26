import os
from typing import TypedDict

import psycopg


class DatabaseNotConfiguredError(Exception):
    pass


class DatabaseConnectionError(Exception):
    pass


class ColumnInfo(TypedDict):
    name: str
    data_type: str
    nullable: bool
    default: str | None
    primary_key: bool
    foreign_key: bool


class TableInfo(TypedDict):
    name: str
    columns: list[ColumnInfo]


def _connect() -> psycopg.Connection:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise DatabaseNotConfiguredError("DATABASE_URL is not configured")

    try:
        return psycopg.connect(database_url, connect_timeout=3)
    except psycopg.Error as error:
        raise DatabaseConnectionError from error


def check_database_connection() -> None:
    try:
        with _connect() as connection:
            connection.execute("SELECT 1").fetchone()
    except psycopg.Error as error:
        raise DatabaseConnectionError from error


def get_learning_schema() -> list[TableInfo]:
    query = """
        SELECT
            columns.table_name,
            columns.column_name,
            columns.data_type,
            columns.is_nullable = 'YES' AS nullable,
            columns.column_default,
            EXISTS (
                SELECT 1
                FROM information_schema.table_constraints AS constraints
                JOIN information_schema.key_column_usage AS keys
                  USING (constraint_catalog, constraint_schema, constraint_name)
                WHERE constraints.constraint_type = 'PRIMARY KEY'
                  AND constraints.table_schema = columns.table_schema
                  AND constraints.table_name = columns.table_name
                  AND keys.column_name = columns.column_name
            ) AS primary_key,
            EXISTS (
                SELECT 1
                FROM information_schema.table_constraints AS constraints
                JOIN information_schema.key_column_usage AS keys
                  USING (constraint_catalog, constraint_schema, constraint_name)
                WHERE constraints.constraint_type = 'FOREIGN KEY'
                  AND constraints.table_schema = columns.table_schema
                  AND constraints.table_name = columns.table_name
                  AND keys.column_name = columns.column_name
            ) AS foreign_key
        FROM information_schema.columns AS columns
        WHERE columns.table_schema = %s
        ORDER BY columns.table_name, columns.ordinal_position
    """

    try:
        with _connect() as connection:
            rows = connection.execute(query, ("learning",)).fetchall()
    except psycopg.Error as error:
        raise DatabaseConnectionError from error

    tables: dict[str, TableInfo] = {}
    for (
        table_name,
        column_name,
        data_type,
        nullable,
        default,
        primary_key,
        foreign_key,
    ) in rows:
        if table_name not in tables:
            tables[table_name] = {"name": table_name, "columns": []}
        tables[table_name]["columns"].append(
            {
                "name": column_name,
                "data_type": data_type,
                "nullable": nullable,
                "default": default,
                "primary_key": primary_key,
                "foreign_key": foreign_key,
            }
        )

    return list(tables.values())