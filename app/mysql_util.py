# File: mysql_user.py
import pymysql

def execute_sql(sql, params=(), commit=False):
    """
    Executes a SQL statement and returns the results.
    - If `commit=True`, commits the transaction.
    - If an error occurs, rolls back the transaction.   
    - If the SQL statement is meant to change the database,
    pass in `commit=True`. `commit=False` is for statements like
    `SELECT` that don't change the database.
    """
    conn = pymysql.connect(user='root', passwd='root', db='talbook')
    cursor = conn.cursor()

    try:
        cursor.execute(sql, params)
        if commit:
            conn.commit() # commit changes
        return list(cursor.fetchall())
    except Exception as e:
        print("error in execute_sql():", e)
        conn.rollback() # rollback on failure
    finally: # this always executes, even after the return in the try
        cursor.close()
        conn.close() 
