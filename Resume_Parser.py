import streamlit as st
from call import delete_records_and_files

st.set_page_config(
    page_title="Mulitpage App",
    layout="wide",
    page_icon=""
)

# # Use st.markdown to add custom CSS
# st.markdown(
#     """
#     <style>
#     /* CSS code to move the sidebar to the bottom */
#     .sidebar-content {
#         position: fixed;
#         bottom: 0;
#         left: 0;
#         width: 100%;
#         display: flex;
#         flex-direction: row-reverse;
#         z-index: 1;
#     }
    
#     .sidebar {
#         width: 20%;
#         margin-left: auto;
#         padding: 1rem;
#     }
    
#     .main {
#         width: 80%;
#         padding: 1rem;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )


st.title("RESUME PARSER")
st.sidebar.success("Select a page above")

    
# Add elements to the sidebar and main content area
with st.sidebar:
    if st.sidebar.button('Delete all'):
        delete_records_and_files()

with st.container():
    st.write('''A resume parser is a software tool that automates the extraction and analysis of information from resumes or CVs (Curriculum Vitae). 
It uses natural language processing (NLP) techniques to parse and interpret the textual content of resumes, extracting key details 
such as personal information, contact details, education history, work experience, skills, and other relevant information. Resume parsers 
help streamline the recruitment and hiring process by automatically extracting and structuring resume data, enabling recruiters and HR 
professionals to efficiently review and analyze large volumes of resumes, identify qualified candidates, and make informed decisions. 
These tools save time and effort by eliminating the need for manual data entry and enable recruiters to focus on evaluating candidates 
based on their qualifications and fit for specific roles.''')

'''


'''

