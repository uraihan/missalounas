from collections.abc import Iterator

import psycopg
from litestar.datastructures import State
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from src.shared.config import get_db_string


def create_pool() -> ConnectionPool:
    db_string = get_db_string()

    return ConnectionPool(
        conninfo=db_string, open=False, kwargs={"row_factory": dict_row}
    )


def provide_db(state: State) -> Iterator[psycopg.Connection]:
    with state.pool.connection() as conn:
        yield conn
