import mysql.connector

def database():
    # Connect to MySQL database
    db = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='mysql30',
        database='resu'
    )
    return db