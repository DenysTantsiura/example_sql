import sqlite3
from contextlib import contextmanager

DATABASE = './assessments.db'


@contextmanager
def create_connection(db_file):
    """Create a database connection to a SQLite database."""
    conn = sqlite3.connect(db_file)
    yield conn
    conn.rollback()
    conn.close()
