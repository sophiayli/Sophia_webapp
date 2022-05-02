import sqlite3

DATABASE_FILE = "sophia_webapp.db"

with sqlite3.connect(DATABASE_FILE) as connection:
    cursor = connection.cursor()
    sql = "SELECT * FROM item"
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results) 

