import mysql.connector
import streamlit as st
import os

def database():
    # Connect to MySQL database
    db = mysql.connector.connect(
        host='aws.connect.psdb.cloud',
        user='2navrj03w1pymyqaxr3u',
        password='pscale_pw_Y2Ibnd175OXmR9FHvc9SJUNHY8NMA7JDd7I3IFH0rC9',
        database='resume_parser'
    )
    return db
















def delete_files():
    if st.button("Are you sure? All resumes will be removed"):
        folder_path = './Resumes'

        # Get file names in the folder
        file_names = os.listdir(folder_path)

        # Iterate over the file names and delete each file
        for file_name in file_names:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
                
        db = database()
        cursor = db.cursor()

        cursor.execute("DELETE FROM resume_text")
        cursor.execute("DELETE FROM resume_detail")
        cursor.execute("DELETE FROM resume_keyword")

        cursor.execute("ALTER TABLE resume_text AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE resume_detail AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE resume_keyword AUTO_INCREMENT = 1")

        cursor.close()
        db.close()