import pandas as pd
from bs4 import BeautifulSoup
import streamlit as st
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import openai

key = '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'
openai.api_key = key

def get_completion(prompt, model="gpt-3.5-turbo",temperature=0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

# Creating a webdriver instance
# Options = Options()
# Options.add_argument('--headless=new')
# driver = webdriver.Chrome(options=Options)
driver = webdriver.Chrome()


# Opening linkedIn's login page
driver.get("https://linkedin.com/uas/login")

# waiting for the page to load
time.sleep(5)

# entering username
username = driver.find_element(By.ID, "username")

# Enter Your Email Address
username.send_keys("email")

# entering password
pword = driver.find_element(By.ID, "password")

# Enter Your Password
pword.send_keys("password")

# Clicking on the log in button
driver.find_element(By.XPATH, "//button[@type='submit']").click()

# paste the URL 
profile_url = st.text_input("Enter the profile URL", "")

if profile_url:
    driver.get(profile_url)

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

def prompt(text):
    prompt = f"""
     ```{text}```

    From the text extract ner(named entity recognition)

    Things to extract
    Name: 
    About:
    Education:
    Projects:
    Skills:
    Tools:
    Experience:

    Only give the keywords
    For name only give the which has repeated many times
    Put all these details into a dictionary 

    """
    return get_completion(prompt)

response = prompt(text)
st.write(response)

# df = pd.DataFrame(eval(response), index=[0])
    
# st.dataframe(eval(response))
driver.close()