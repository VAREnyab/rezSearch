import mysql.connector
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import pandas as pd
import streamlit as st

key_pandas = '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'

# Instantiate a LLM
llm = OpenAI(api_token=key_pandas)
pandas_ai = PandasAI(llm)

def database():
    # Connect to MySQL database
    db = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='mysql30',
        database='resu'
    )
    return db

db = database()
cursor = db.cursor()
# Execute the SQL query
cursor.execute("SELECT * FROM resume_detail")

# Fetch the column names from the cursor description
columns = [col[0] for col in cursor.description]

# Fetch the data
data = cursor.fetchall()
# Close the cursor and database connection
cursor.close()
db.close()




# Convert data to a dataframe
df = pd.DataFrame(data, columns=columns)




st.dataframe(df)

# Prompt the user for columns to display
prompt_from_user = st.text_area("Enter your prompt: ")

if st.button("Generate:"):
    if prompt_from_user:
        with st.spinner("Generating response..."):
            st.write(pandas_ai(df, prompt=prompt_from_user))
    
    else:
        st.warning("Enter a prompt")
        