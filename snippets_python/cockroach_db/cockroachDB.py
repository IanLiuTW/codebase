import psycopg2
from loguru import logger as lo

COCKROACHDB_CONFIG = {
    "sample": {
        "host": "localhost",
        "port": 26257,
        "user": "root",
        "dbname": "sample",
    }
}


async def execute_query(db_name, query):
    try:
        conn = psycopg2.connect(**COCKROACHDB_CONFIG[db_name])
    except Exception:
        lo.error("database connection failed")
        raise
    try:
        with conn:
            with conn.cursor() as curs:
                curs.execute(query)
    except Exception:
        lo.error("database query failed")
        raise
    finally:
        conn.close()


def get_db_info(db_name):
    db = COCKROACHDB_CONFIG[db_name]
    return f"{db['host']}:{db['port']}/{db['dbname']}"