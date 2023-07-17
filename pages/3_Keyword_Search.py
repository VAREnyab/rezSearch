import pandas as pd
import streamlit as st

from fuzzywuzzy import fuzz
import base64
from call import database, uploaded_file_ids


# Display the pdf
def display_pdf(pdf_file_path):
    with open(pdf_file_path, 'rb') as file:
        base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    resume_pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(resume_pdf_display, unsafe_allow_html=True)
    

db = database()
cursor = db.cursor()
# Execute the SQL query
if uploaded_file_ids:
    
    query = "SELECT * FROM resume_keyword WHERE unique_id IN ({})".format(','.join(['%s'] * len(uploaded_file_ids)))
    cursor.execute(query, tuple(uploaded_file_ids))

    # Fetch the column names from the cursor description
    columns = [col[0] for col in cursor.description]

    # Fetch the data
    db_data = cursor.fetchall()
    # Close the cursor and database connection
    cursor.close()
    db.close()

    # Convert data to a dataframe
    data = pd.DataFrame(db_data, columns=columns)

    data['keyword'] = data['keyword'].astype(str)

    # Define function for fuzzy string matching
    def similarity_fuzzy(word1, word2):
        score = fuzz.ratio(word1, word2)
        d = score/100
        return d

    # Define function to get top resume matches
    def get_top_resumes(search_word, threshold):
        name = []
        words = []
        for i in range(len(data)):
            name.append(data.loc[i, "filename"])
            words.append(data.loc[i, "keyword"].split(","))
        
        i = 0
        score_dict = dict()
        for each_resume_words in words:
            fuzz_score = 0
            for word in each_resume_words: 
                if similarity_fuzzy(word.lower(), search_word.lower()) > threshold:
                    fuzz_score += 1
            score_dict[name[i]] = fuzz_score
            i += 1
        ranked_dict = dict(sorted(score_dict.items(), key=lambda item: item[1], reverse=True))
        
        return ranked_dict

    st.title("Resume Search Engine")

    # Create search box and button
    search_word = st.text_input("Enter search term:", "")
    threshold = st.slider("Select similarity threshold:", 0, 100, 70)
    #search_word = 'NLP'
    threshold = threshold/100


    submit_button = st.button("Search")

    if search_word != "":
        # Get top resume matches and display in a table
        top_resumes = get_top_resumes(search_word, threshold)
        if len(top_resumes) > 0:
            st.write("Top resume matches:")
            df = pd.DataFrame(list(top_resumes.items()), columns=['filename', 'Score'])
            st.table(df)

            # Create dropdown to view selected resume
            selected_resume = st.selectbox("Select a resume to view:", df['filename'], key="resume_select")

            if selected_resume:
                st.write("Resume:")
                # st.write(data.loc[data["filename"]==selected_resume, "text"].values[0])
                display_pdf(selected_resume)
        else:
            st.write("No matching resumes found.")
    else:
        st.write("Please enter a search term.")
else:
    st.write('No Resumes Found')
