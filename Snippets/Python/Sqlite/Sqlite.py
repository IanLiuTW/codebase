import sqlite3
from dataclasses import dataclass

from loguru import logger as lo

SQLITE_CONFIG = {
    "SAMPLE": {
        "path": "./sample.db",
        "tables": ["sample1",]
    }
}

SAMPLE_SCHEMA = {
    "sample1":
    """ 
    CREATE TABLE IF NOT EXISTS sample1 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        type TEXT,
        date TEXT DEFAULT CURRENT_DATE,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """,
}


@dataclass
class Sqlite:
    name: str

    def execute(self, sql_query, values=()):
        try:
            conn = sqlite3.connect(SQLITE_CONFIG[self.name]["path"])
        except Exception as e:
            lo.error(f"Sqlite {self.name} connection failed with error: {e}")
            return
        try:
            cur = conn.cursor()
            results = cur.execute(sql_query, values).fetchall()
            conn.commit()
            return results
        except Exception as e:
            lo.error(f"Sqlite {self.name} operation failed with error: {e}")
        finally:
            conn.close()

    def create_tables(self):
        for table_name in SQLITE_CONFIG[self.name]["tables"]:
            self.execute(TABLES_SCHEMA[table_name])
        lo.debug(f"Sqlite {self.name} tables created")