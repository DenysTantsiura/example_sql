


import pathlib


sql_request = './sql_request/sqlr.sql'
request_counter = 1


def sql_requests():
    """Cyclically perform requests."""
    while pathlib.Path(sql_request).exist():
        ...
        sql_request = 


if __name__ == "__main__":
    sql_requests()