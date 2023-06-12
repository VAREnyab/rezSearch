
import pandas as pd


import base64
import io, random
import time
import uuid

from pyresparser import ResumeParser

import streamlit as st
from streamlit_tags import st_tags

import pymysql

from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import TextConverter

import plotly.express as px




# Connection with database
connection = pymysql.connect(user='root', host='127.0.0.1', password='mysql30', db='resume_parse')
cursor = connection.cursor()



# Define Streamlit app
st.set_page_config(page_title="Resume Search Engine", page_icon=":guardsman:", layout="wide")

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

# Clean Data
def clean_resume_data(pdf_files):
    resume_features = pdf_files
    
    # Extract Name
    name = resume_features['name'].lower().split('email')
    resume_features['name'] = name[0].strip()

    # Extract Emails
    email = resume_features.get('email', '').lower()
    modified_email = email.replace("email:", "").strip()
    resume_features['email'] = modified_email

    return resume_features['name'], resume_features['email']

def insert_data(name, email, phone_number, skills):
    db_table_name = 'resume_table'
    insert_sql = "INSERT INTO " + db_table_name + """ 
    (ID, Name, Email_ID, Phone_number, Skills) VALUES (0, %s, %s, %s, %s)"""
    
    rec_values = (name, email, str(phone_number), skills)
    cursor.execute(insert_sql, rec_values)
    connection.commit()

def main():
    st.title("Resume Search Engine")

    # Create the Database
    db_sql = """ CREATE DATABASE IF NOT EXISTS RES_PARS;"""
    cursor.execute(db_sql)
    
    # Create table
    db_table_name = 'resume_table'
    table_sql = "CREATE TABLE IF NOT EXISTS " + db_table_name + """
                (ID INT NOT NULL AUTO_INCREMENT,
                Name varchar(100) NOT NULL,
                Email_ID varchar(50) NOT NULL,
                Phone_number varchar(25) NOT NULL,
                Skills varchar(300) NOT NULL,
                PRIMARY KEY (ID))"""
                
    cursor.execute(table_sql)

    pdf_file = st.file_uploader("Upload your Resume", type=['pdf'])
    if pdf_file is not None:
        save_resume_path = './Sample Resumes/' + pdf_file.name
        with open(save_resume_path, 'wb') as f:
            f.write(pdf_file.getbuffer())
        display_pdf(save_resume_path)
        resume_data = ResumeParser(save_resume_path).get_extracted_data()

        if resume_data:
            # Get the whole text
            whole_text = extract_whole_resume(save_resume_path)
            resume_data['name'], resume_data['email'] = clean_resume_data(resume_data)    
            
            st.header("Resume Explanation")
            try:
                st.text('Name: ' + resume_data['name'])
                st.text('Email: ' + resume_data['email'])
                st.text('Phone Number: ' + resume_data['mobile_number'])
            except:
                pass
        
        # Technical Skills Show
        skill_tags = st_tags(label=f"### Skills that {resume_data['name'].capitalize()} has",
                                value=resume_data['skills'], key='skill_set')


        job_skills = {
            'web_developer': [
                "HTML", "CSS", "JavaScript", "jQuery", "React", "Angular", "Vue.js",
                "PHP", "Python", "Ruby", "Node.js", "Express.js", "Django", "Flask",
                "MySQL", "MongoDB", "Firebase", "RESTful APIs", "Git", "Webpack"
            ],
            'data_scientist': [
                "Python", "R", "NumPy", "Pandas", "Matplotlib", "Seaborn", "Scikit-learn", "Seaborn",
                "TensorFlow", "Keras", "PyTorch", "SQL", "MySQL", "Hadoop", "Spark", "Data Visualization",
                "Machine Learning", "Statistical Analysis", "Deep Learning", "Natural Language Processing"
            ],
            'android': [
                'android', 'android development', 'flutter', 'kotlin', 'xml', 'kivy'
            ],
            'uiux': [
                'ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes',
                'storyframes', 'adobe photoshop', 'photoshop', 'editing', 'adobe illustrator',
                'illustrator', 'adobe after effects', 'after effects', 'adobe premier pro',
                'premier pro', 'adobe indesign', 'indesign', 'wireframe', 'solid', 'grasp',
                'user research', 'user experience'
            ]
        }
        
        # Generate a unique key using UUID
        unique_key = str(uuid.uuid4())

        recommended_skills = []
        reco_field = ''
        for i in resume_data['skills']:
            
            for field, skills in job_skills.items():
                if i.lower() in skills:
                    reco_field = field.replace('_', ' ').title()
                    st.success(f"** Our analysis says you are looking for {reco_field} Jobs **")
                    recommended_skills = job_skills[field]
                    st_tags(label='### Recommended skills for you.',
                            text='Recommended skills generated from System',
                            value=recommended_skills, 
                            key=f'recommended_keywords_{unique_key}')
                    break
                
        #insert_data(resume_data['name'], resume_data['email'], resume_data['mobile_number'],str(resume_data['skills']))
        
        #  Wincel add here   


# Run the Streamlit app
if __name__ == "__main__":
    main()

