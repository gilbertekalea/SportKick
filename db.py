import sqlite3

from sporty.application import createTables


# create connection

def db_connection(db_file):
    "Create a database connection to sqlite"
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
    except KeyError as e:
        print(e)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    db_connection('store.db')


def create_tables(con, sql_tables):
    "Create tables from sql query"


def main():

    pass