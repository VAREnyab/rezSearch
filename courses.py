
def Technical_skills(resume_data):
    
    web_developer_skills = [
        "HTML", "CSS", "JavaScript", "jQuery", "React", "Angular", "Vue.js",
        "PHP", "Python", "Ruby", "Node.js", "Express.js", "Django", "Flask",
        "MySQL", "MongoDB", "Firebase", "RESTful APIs", "Git", "Webpack"
    ]

    data_scientist_skills = [
        "Python", "R", "NumPy", "Pandas", "Matplotlib", "Seaborn", "Scikit-learn",
        "TensorFlow", "Keras", "PyTorch", "SQL", "Hadoop", "Spark", "Data Visualization",
        "Machine Learning", "Statistical Analysis", "Deep Learning", "Natural Language Processing"
    ]

    android_skills = [
        'android', 'android development', 'flutter', 'kotlin', 'xml', 'kivy'
    ]
                
    uiux_skills = [
        'ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes',
        'storyframes', 'adobe photoshop', 'photoshop', 'editing', 'adobe illustrator',
        'illustrator', 'adobe after effects', 'after effects', 'adobe premier pro',
        'premier pro', 'adobe indesign', 'indesign', 'wireframe', 'solid', 'grasp',
        'user research', 'user experience'
    ]


    recommended_skills = []
    reco_field = ''
    rec_course = ''
    ## Courses recommendation
    for i in resume_data['skills']:

        ## Web development recommendation
        if i.lower() in web_developer_skills:
            print(i.lower())
            reco_field = 'Web Development'
            #st.success("** Our analysis says you are looking for Web Development Jobs **")
            recommended_skills = ['React', 'Django', 'Node JS', 'React JS', 'php', 'laravel', 'Magento',
                                    'wordpress', 'Javascript', 'Angular JS', 'c#', 'Flask', 'SDK']
            recommended_keywords = st_tags(label='### Recommended skills for you.',
                                            text='Recommended skills generated from System',
                                            value=recommended_skills, key='3')
            st.markdown(
                '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                unsafe_allow_html=True)
            rec_course = course_recommender(web_course)
            break
        
        ## Data science recommendation
        elif i.lower() in data_scientist_skills:
            print(i.lower())
            reco_field = 'Data Science'
            #st.success("** Our analysis says you are looking for Data Science Jobs.**")
            recommended_skills = ['Data Visualization', 'Predictive Analysis', 'Statistical Modeling',
                                    'Data Mining', 'Clustering & Classification', 'Data Analytics',
                                    'Quantitative Analysis', 'Web Scraping', 'ML Algorithms', 'Keras',
                                    'Pytorch', 'Probability', 'Scikit-learn', 'Tensorflow', "Flask",
                                    'Streamlit']
            recommended_keywords = st_tags(label='### Recommended skills for you.',
                                            text='Recommended skills generated from System',
                                            value=recommended_skills, key='2')
            st.markdown(
                '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                unsafe_allow_html=True)
            rec_course = course_recommender(ds_course)
            break

        ## Android App Development
        elif i.lower() in android_skills:
            print(i.lower())
            reco_field = 'Android Development'
            #st.success("** Our analysis says you are looking for Android App Development Jobs **")
            recommended_skills = ['Android', 'Android development', 'Flutter', 'Kotlin', 'XML', 'Java',
                                    'Kivy', 'GIT', 'SDK', 'SQLite']
            recommended_keywords = st_tags(label='### Recommended skills for you.',
                                            text='Recommended skills generated from System',
                                            value=recommended_skills, key='4')
            st.markdown(
                '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                unsafe_allow_html=True)
            rec_course = course_recommender(android_course)
            break


        ## Ui-UX Recommendation
        elif i.lower() in uiux_skills:
            print(i.lower())
            reco_field = 'UI-UX Development'
            #st.success("** Our analysis says you are looking for UI-UX Development Jobs **")
            recommended_skills = ['UI', 'User Experience', 'Adobe XD', 'Figma', 'Zeplin', 'Balsamiq',
                                    'Prototyping', 'Wireframes', 'Storyframes', 'Adobe Photoshop', 'Editing',
                                    'Illustrator', 'After Effects', 'Premier Pro', 'Indesign', 'Wireframe',
                                    'Solid', 'Grasp', 'User Research']
            recommended_keywords = st_tags(label='### Recommended skills for you.',
                                            text='Recommended skills generated from System',
                                            value=recommended_skills, key='6')
            st.markdown(
                '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                unsafe_allow_html=True)
            rec_course = course_recommender(uiux_course)
            break
        
        
def course_recommender(course_list):
    st.subheader("**Courses & Certificates🎓 Recommendations**")
    c = 0
    rec_course = []
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 4)
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course


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

# Course Recommendation
def course_recommender(course_list):
    st.subheader("**Courses & Certificates🎓 Recommendations**")
    c = 0
    rec_course = []
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 4)
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course