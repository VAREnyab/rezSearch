import pandas as pd
import streamlit as st
from fuzzywuzzy import fuzz


# Read in data from Excel file
data = pd.read_excel("resume_extracted.xlsx")
data['Tags'] = data['Tags'].astype(str)

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
        words.append(data.loc[i, "Tags"].split(","))
    
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

# Define Streamlit app
st.set_page_config(page_title="Resume Search Engine", page_icon=":guardsman:", layout="wide")
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
            st.write("Resume text:")
            st.write(data.loc[data["filename"]==selected_resume, "resume text"].values[0])
    else:
        st.write("No matching resumes found.")
else:
    st.write("Please enter a search term.")
