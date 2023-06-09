import PyPDF2
import pandas as pd
import glob
import streamlit as st
import base64
import io
from pyresparser import ResumeParser
from streamlit_tags import st_tags
import pymysql
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import TextConverter
import plotly.express as px



# Connection with database
connection = pymysql.connect(user='root', host='127.0.0.1', password='mysql30', db='res_pars')
cursor = connection.cursor()



# Define Streamlit app
st.set_page_config(page_title="Resume Search Engine", page_icon=":guardsman:", layout="wide")


def run():
    st.title("Resume Search Engine")
    activities = ['Normal User', 'Admin']
    
    choice = st.sidebar.selectbox("Choose any of the following: ", activities)

    # Create the Database
    db_sql = """ CREATE DATABASE IF NOT EXISTS RES_PARS;"""
    cursor.execute(db_sql)
    
    # Create table
    db_table_name = 'resume_table'
    table_sql = "CREATE TABLE IF NOT EXISTS " + db_table_name + """
                (ID INT NOT NULL AUTO_INCREMENT,
                Name varchar(100) NOT NULL,
                Email_ID varchar(50) NOT NULL,
                Phone_number int NOT NULL,
                Resume_score varchar(8) NOT NULL,
                Skills varchar(300) NOT NULL,
                Recommended_courses varchar(600) NOT NULL,
                PRIMARY KEY (ID))"""
                
    cursor.execute(table_sql)

    if choice == 'Normal User':
        pdf_file = st.file_uploader("Upload your Resume", type=['pdf'])
        if pdf_file is not None:
            save_resume_path = "r'D:\2. Resume Parser\'"+pdf_file.name
            with open(save_resume_path, 'wb') as f:
                f.write(pdf_file.getbuffer())
            display_pdf(save_resume_path)
            resume_data = ResumeParser(save_resume_path).get_extracted_data()

            if resume_data:
                # Get the whole text
                whole_text = extract_whole_resume(save_resume_path)
                
                
                st.header("Resume Explanation")
                try:
                    st.text('Name: ' + resume_data['name'])
                    st.text('Email: ' + resume_data['email'])
                    st.text('Phone Number: ' + resume_data['mobile_number'])
                except:
                    pass
            
            # Skills Show
            skill_tags = st_tags(label=f"### Skills that {resume_data['name'].capitalize()} has",
                                 value=resume_data['skills'], key='skill_set')



# Display the pdf
def display_pdf(pdf_file_path):
    with open(pdf_file_path, 'rb') as file:
        base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    resume_pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(resume_pdf_display, unsafe_allow_html=True)

# Extract the whole text
def extract_whole_resume(pdf_files):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    convertor = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, convertor)
    with open(pdf_files, 'rb') as file:
            pages = PDFPage.get_pages(file, caching=True, check_extractable=True)
            for page in pages:
                page_interpreter.process_page(page)
            text = fake_file_handle.getvalue()
            
    convertor.close()
    fake_file_handle.close()
    return text



run()

# Resume Parser
def resume_features_extraction(pdf_files):
    parsed_data = []
    for pdf_file in pdf_files:
        data = ResumeParser(pdf_file, custom_regex=r'\+?\d[\d -]{8,12}\d').get_extracted_data() 
        parsed_data.append(data)
        
    return parsed_data


# Define the folder path containing the PDFs
folder_path = r'D:\2. Resume Parser\search_engine'

# Provide a list of PDF files to parse and specify the output CSV file
pdf_files = glob.glob(folder_path + '/*.pdf')




def clean_data(pdf_files):
    resume_features = resume_features_extraction(pdf_files)
    resume_texts = extract_whole_resume(pdf_files)
    columns = []

    for resume, pdf_file, resume_text in zip(resume_features, pdf_files, resume_texts):
        if resume.get('name') and resume.get('email'):
            # Extract Name
            name = resume['name'].lower().split('email')
            resume['name'] = name[0].strip()

            # Extract Emails
            email = resume.get('email', '').lower()
            modified_email = email.replace("email:", "").strip()
            resume['email'] = modified_email

            # Extract name of the file
            filename = pdf_file.split('\\')[-1]
            resume_text = resume_text.split(",:")
            

            columns.append({
                'File Name': filename,
                'Resume Text': resume_text[1],
                'Name': resume['name'],
                'Email': resume['email'],
                'Phone Number': resume['mobile_number'],
                'Skills': ', '.join(resume['skills'])
            })

    return columns


# def extract_whole_resume(pdf_files):
#     resume_texts = []
#     for pdf_file in pdf_files:
#         with open(pdf_file, 'rb') as file:
#             reader = PyPDF2.PdfReader(file)
#             whole_text = ',:'
#             for page in reader.pages:
#                 whole_text += page.extract_text().replace('\t', ' ').replace('\n', ' ')
#             resume_texts.append(whole_text)
#     return resume_texts