import pandas as pd
from bs4 import BeautifulSoup
import streamlit as st
import time
from call import database
import openai

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

st.set_page_config(page_title="LinkedInGPT", page_icon=":guardsman:", layout="wide")
st.title("LinkedInGPT")

'''
Welcome to our LinkedInGPT, a powerful tool designed to enhance your 
recruitment process by providing deeper insights into potential candidates. 
With our platform, you can now effortlessly access comprehensive information 
about your recruitees, from their professional backgrounds and skills to their 
career achievements and endorsements.
'''

key = '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'
openai.api_key = key

def get_completion(prompt, model="gpt-3.5-turbo",temperature=0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

db = database()
cursor = db.cursor()

# Execute the SQL query
cursor.execute("SELECT linkedin_id FROM resume_detail WHERE linkedin_id != 'Nan'")

# Fetch the data
data = cursor.fetchall()
# Close the cursor and database connection
cursor.close()
db.close()

# Convert data to a dataframe
df = pd.DataFrame(data, columns=['Linkedin_profiles'])

# paste the URL 
selected_profile = st.selectbox("Select a profile to view:", [""] + df['Linkedin_profiles'].tolist(), key="profile_select")
st.text("OR")
profile_url = st.text_input("Enter the profile URL", "")

# Creating a webdriver instance
chrome_options = Options()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
# driver = webdriver.Chrome()

# Opening linkedIn's login page
driver.get("https://linkedin.com/uas/login")

# waiting for the page to load
time.sleep(5)

# entering username
username = driver.find_element(By.ID, "username")

# Enter Your Email Address
username.send_keys("212029wincel@staloysius.ac.in")
time.sleep(0.5)

# entering password
pword = driver.find_element(By.ID, "password")

# Enter Your Password
pword.send_keys("Pass@2thisacc")
time.sleep(0.5)

# Clicking on the log in button
driver.find_element(By.XPATH, "//button[@type='submit']").click()


if selected_profile != "":
    driver.get("https://www."+selected_profile)
    time.sleep(3)
else:
    driver.get(profile_url)
    time.sleep(3)


start = time.time()

# will be used in the while loop
initialScroll = 0
finalScroll = 1000

while True:
    driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
    
    # scrolls the window starting from
    initialScroll = finalScroll
    finalScroll += 1000

    time.sleep(3)
   
    end = time.time()
    
    if round(end - start) > 20:
        break
    
src = driver.page_source
 
# Now using beautiful soup
soup = BeautifulSoup(src, 'lxml')

text = soup.find_all('div',class_='display-flex align-items-center mr1 hoverable-link-text t-bold')
text1 = soup.find('div', {'class': 'pv-text-details__left-panel'})

def prompt(text):
    prompt = f"""
     ```{text1}```
     ```{text}```

    From the texts given extract ner(named entity recognition)

    Things to extract
    Name: 
    About:
    Education:
    Projects:
    Skills:
    Tools:
    Experience:

    Only give the keywords
    All details that are in the form of a list should all be in seperate "" and seperated by a comma
    For name only give the first one only
    Put all these details into a dictionary 

    """
    return get_completion(prompt)

response = prompt(text)
st.write(response)

# df = pd.DataFrame(eval(response), index=[0])
        
# st.dataframe(eval(response))
driver.close()