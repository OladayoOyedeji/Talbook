# File: mysql_user.py
import pymysql

DB_NAME = "Talbook"
USE_DB = "use %s;" % DB_NAME
INIT_SQL_FILE = "app/db/init.sql"  # path to MySQL initialization script

def get_db_connection(db=None):
    """
    Establishes a database connection.
    If `db` is None, connects without specifying a database (for initial setup).
    """
    if db:
        return pymysql.connect(user="root", password="root", database=db)
    else:
        return pymysql.connect(user="root", password="root")
    
def execute_sql(sql, params=(), commit=False, get_lastrowid=False):
    """
    Executes a SQL statement and returns the results.
    - If `commit=True`, commits the transaction.
    - If an error occurs, rolls back the transaction.   
    - If the SQL statement is meant to change the database,
    pass in `commit=True`. `commit=False` is for statements like
    `SELECT` that don't change the database.
    """
    conn = get_db_connection(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute(sql, params)
        if commit:
            conn.commit() # commit changes
        if get_lastrowid:
            return cursor.lastrowid
        return list(cursor.fetchall())
    except Exception as e:
        print("error in execute_sql():", e)
        conn.rollback() # rollback on failure
    finally: # this always executes, even after the return in the try
        cursor.close()
        conn.close()

def execute_many_sql(sql, param_list, commit=False):
    """
    Executes a batch of SQL statements
    """
    conn = get_db_connection(DB_NAME)
    cursor = conn.cursor()

    added = False
    
    try:
        cursor.executemany(sql, param_list)
        if commit:
            conn.commit()

        added = True
    except Exception as e:
        print("error in execute_many_sql():", e)
        conn.rollback()
        
        
    cursor.close()
    conn.close()
    return added

def database_exists(db_name=DB_NAME):
    """
    Checks if the 'talbook' database exists.
    """
    sql = "SHOW DATABASES;"
    databases = execute_sql(sql)
    return db_name in [db[0] for db in databases]

def execute_sql_file(filename):
    """
    Executes an SQL file
    """
    conn = get_db_connection(DB_NAME)
    cursor = conn.cursor()
    with open(filename, "r") as f:
        sql_statements = f.read().split(";")
        for sql in sql_statements:
            if sql.strip():
                cursor.execute(sql)
                conn.commit()
    cursor.close()
    conn.close()

def ensure_database():
    """
    Ensures that the database exists. If not, it creates it and runs init.sql.
    """
    if not database_exists():
        sql = "CREATE DATABASE %s;"
        execute_sql(sql, (DB_NAME,), commit=True)
        execute_sql_file(INIT_SQL_FILE)

def append_sql(filename: str, sql: str) -> None:
    ''' Appends MySQL content to a file'''
    f = open(filename, 'a')
    f.write(sql + '\n')
    f.close()

def write_sql(filename: str, sql: str) -> None:
    '''Writes MySQL content to a file (overwrites)'''
    f = open(filename, 'w')
    f.write(sql + '\n')
    f.close() 
