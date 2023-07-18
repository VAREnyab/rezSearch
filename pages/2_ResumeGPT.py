from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import pandas as pd
import streamlit as st
from call import database, uploaded_file_ids


st.set_page_config(page_title="ResumeGPT", page_icon=":guardsman:", layout="wide")
st.title("ResumeGPT")

'''
Welcome to ResumeGPT, your one-stop destination for insightful conversations and 
comprehensive information about your candidates. Engage in real-time chat with our 
intelligent platform to uncover valuable details and gain deeper insights into 
each candidate's qualifications, experience, and skills.
'''

key_pandas = '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'

# Instantiate a LLM
llm = OpenAI(api_token=key_pandas)
pandas_ai = PandasAI(llm)

db = database()
cursor = db.cursor()

if uploaded_file_ids:
    # Construct the SELECT query with the IN operator to match unique IDs in the list
    query = "SELECT * FROM resume_detail WHERE unique_id IN ({})".format(','.join(['%s'] * len(uploaded_file_ids)))

    # Execute the query with the uploaded_file_ids list as parameters
    cursor.execute(query, tuple(uploaded_file_ids))

    # Fetch the column names from the cursor description
    columns = [col[0] for col in cursor.description]

    # Fetch the data
    data = cursor.fetchall()
    
    # Convert data to a dataframe
    df = pd.DataFrame(data, columns=columns)

    # st.dataframe(df)

    # Prompt the user for columns to display
    prompt_from_user = st.text_area("Send a message: ")

    if st.button("Generate:"):
        if prompt_from_user:
            with st.spinner("Generating response..."):
                st.write(pandas_ai(df, prompt=prompt_from_user))
        
        else:
            st.warning("Enter a prompt")
            
else:
    st.write('Upload some resumes')
    
# Close the cursor and database connection
cursor.close()
db.close()


        