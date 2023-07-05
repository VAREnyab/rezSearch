import streamlit as st
import pandas as pd
import base64
import sys, fitz
import mysql.connector
import openai

# OpeAI API key
key = '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'
openai.api_key = key

# Define Streamlit app
st.set_page_config(page_title="Resume Search Engine", page_icon=":guardsman:", layout="wide")

# Display the pdf
def display_pdf(pdf_file_path):
    with open(pdf_file_path, 'rb') as file:
        base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    resume_pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(resume_pdf_display, unsafe_allow_html=True)

# Initialising the model 
def get_completion(prompt, model="gpt-3.5-turbo",temperature=0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"] 

# Create prompt for NER Extraction
def prompt(text):
    prompt = f"""
    ```{text}```
    From the text extract ner(named entity recognition)

    Things to extract
    1. Name
    2. Email ID
    3. Phone number 
    4. LinkedIn ID
    5. Skills ( eg, programming, marketing)
    6. Tools  ( Linux, ms, python, java)
    7. Experience 
    8. College name
    9. Referrals name,
    10. Referrals phone number
    11. Referrals email
    12. Location
    13. Companies worked at
    14. Designation 
    

    Seperate the details with :
    Skills and Tools details should all be in seperate "" and seperated by a comma
    If any of the details isnt existing on the text return "Nan"
    Put all these details into into a dictionary 

    """
    return get_completion(prompt)


def database():
    # Connect to MySQL database
    db = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='mysql30',
        database='resu'
    )
    return db
       
    
pdf_file = st.file_uploader("Upload your Resume", type=['pdf'])
if pdf_file is not None:
    save_resume_path = './Sample Resumes/' + pdf_file.name
    with open(save_resume_path, 'wb') as f:
        f.write(pdf_file.getbuffer())
    display_pdf(save_resume_path)


   
# Check if a file is uploaded
if pdf_file is not None:
    # Read the PDF file
    pdf_data = pdf_file.read()

    # Load the PDF document
    pdf_document = fitz.open(stream=pdf_data, filetype="pdf")

    # Extract text from each page
    text = ""
    for page in pdf_document:
        text += page.get_text()
    
    # Clean the text
    text = text.strip()
    text = ' '.join(text.split())
    
    # NER Extraction from chatGPT
    response = prompt(text)
    
    df = pd.DataFrame(eval(response), index=[0])
        
    st.dataframe(eval(response))
    
    
    # Database    
    db = database()

    # Create a cursor
    cursor = db.cursor()

    # Insert the extracted text into the database
    # Insert in table name resume_text
    insert_query = "INSERT INTO resume_text (text) VALUES (%s)"
    cursor.execute(insert_query, (text,))
    db.commit()
    
    # Insert in table name resume_details
    for index, row in df.iterrows():
        insert_query = "INSERT INTO resume_detail (name, email, phone_number, linkedin_id, skills, tools, experience, college_name, referrals_name, referrals_phone_number, referrals_email, location, companies_worked_at, designation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (row['Name'], row['Email ID'], row['Phone number'], 
                                      row['LinkedIn ID'], row['Skills'], row['Tools'], 
                                      row['Experience'], row['College name'], row['Referrals name'], 
                                      row['Referrals phone number'], row['Referrals email'], row['Location'], 
                                      row['Companies worked at'], row['Designation']))
        db.commit()

    # Close the cursor and database connection
    cursor.close()
    db.close()
    
    end_resume_upload = st.button("Done Uploading Resumes?")
    
    if end_resume_upload:
        db = database()
        cursor = db.cursor()
        # Execute the SQL query
        cursor.execute("SELECT * FROM resume_detail")
        
        # Fetch the data
        data = cursor.fetchall()
        # Close the cursor and database connection
        cursor.close()
        db.close()
        
        st.table(data)
        
    
    
    
    





