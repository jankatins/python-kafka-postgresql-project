"""Easy access to postgres databases via psycopg2"""

# stolen and adapted from https://github.com/mara/mara-db/blob/master/mara_db/postgresql.py
# this implementation always opens a new connection which is not optimized for high volume of events
# but for now ok...

import contextlib
import psycopg2
import psycopg2.extensions

from . import config as c


@contextlib.contextmanager
def postgres_cursor_context(user: str = c.CONSUMER_POSTGRES_USER,
                            password: str = c.CONSUMER_POSTGRES_PASSWORD,
                            host: str = c.CONSUMER_POSTGRES_HOST,
                            port: int = c.CONSUMER_POSTGRES_PORT,
                            database: str = c.CONSUMER_POSTGRES_DB) -> 'psycopg2.extensions.cursor':
    """Creates a context with a psycopg2 cursor for a database alias"""

    connection = psycopg2.connect(dbname=database, user=user, password=password,
                                  host=host, port=port)  # type: psycopg2.extensions.connection
    cursor = connection.cursor()  # type: psycopg2.extensions.cursor
    try:
        yield cursor
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()
