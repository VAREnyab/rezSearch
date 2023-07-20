import mysql.connector

def database():
    # Connect to MySQL database
    db = mysql.connector.connect(
        host='aws.connect.psdb.cloud',
        user='2navrj03w1pymyqaxr3u',
        password='pscale_pw_Y2Ibnd175OXmR9FHvc9SJUNHY8NMA7JDd7I3IFH0rC9',
        database='resume_parser'
    )
    return db