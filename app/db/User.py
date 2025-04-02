# File: accounts.py
from app.utils import hash
from app.utils import mysql_util

FILENAME = "app/db/User.sql"

def insert_test_data():
    users = [
        ("bigbrovc@gmail.com", "bigbrovc", "42Farrah$%"),
        ("oroyedeji1@cougars.ccis.edu", "Robiefresh", "24Mutlu^&"),
        ("nalahaideb@cougars.ccis.edu", "nashydog", "i1uv1itt1egir1s!!")
    ]

    sql_statements = []
    for email, username, password in users:
        sql = "INSERT INTO User (email, username, password_hash) VALUES ('%s', '%s', '%s');"
        hashed_password = hash.hash_password(password)
        sql_statements.append(sql % (email, username, hashed_password))

    sql = '\n'.join(sql_statements)
    mysql_util.write_sql(FILENAME, mysql_util.USE_DB)
    mysql_util.append_sql(FILENAME, sql)

if __name__ == '__main__':
    insert_test_data()
