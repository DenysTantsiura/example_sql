import logging
import pathlib
from sqlite3 import Error
from typing import Optional

from connect_to_db_sqlite import create_connection, DATABASE


sql_script = pathlib.Path('./sql_requests_sqlite/query_1.sql')
logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')


def perform_select(conn, query: str) -> Optional[str]:
    """
    Execute Query(SELECT) in the task.
    """
    rows = None
    cur = conn.cursor()
    try:
        cur.execute(query)
        rows = cur.fetchall() # отримати всі (решту) рядки результату запиту, повертаючи їх у вигляді послідовності послідовностей

    except Error as error:
        logging.error(f'Error when execute scripts:\n{query}\n\terror:\n{error}')

    finally:
        cur.close()

    return rows


def read_file(file: pathlib.Path) -> str:
    """Read file and return contents."""
    with open(file, 'r', encoding='utf-8') as fh:  # try/except?
        script = fh.read()

    return script


def show_results(results: list) -> None:
    """Display the result line by line."""
    [logging.info(f'{line}') for line in results]


def sql_requests(file: pathlib.Path) -> None:
    """Cyclically perform requests."""
    rc = request_counter = 1
    
    while pathlib.Path(file).is_file():
        logging.info(f'======> {file}:')
        script = read_file(file)
        with create_connection(DATABASE) as conn:
            if conn is not None:
                # execute query
                select_result = perform_select(conn, script)
                show_results(select_result)

            else:
                logging.error(f'Error! cannot create the database ({DATABASE}) connection.')

        rc += 1
        prefix = len(file.stem.split('_')[0])  # prefix length 
        file = file.parent.joinpath(f'{file.name[:prefix]}_{rc}{file.suffix}')


if __name__ == "__main__":
    sql_requests(sql_script)
