import streamlit as st
import pandas as pd
import bs4
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

st.set_page_config(page_title="Job Search", page_icon=":guardsman:", layout="wide")
st.title("Job Search")

'''
Welcome to our job search platform, where finding your dream job is made simple and efficient. 
Our website offers a vast and diverse range of job opportunities from leading companies across 
various industries. With our user-friendly interface and powerful search tools, you can easily 
browse through job listings, filter results based on your preferences, and apply with just a 
few clicks.
'''


# Creating a webdriver instance
chrome_options = Options()
chrome_options.add_argument('--headless=new')

browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

#query search on google jobs site with location mentioned
query = st.text_input("What jobs are you looking for: ")
query = '+'.join(query.lower().split())
url = f"https://www.google.com/search?q={query}&oq=/&aqs=chrome..69i57j69i59j0i512j0i22i30i625l4j69i60.4543j0j7&sourceid=chrome&ie=UTF-8&ibp=htl;jobs&sa=X&ved=2ahUKEwjXsv-_iZP9AhVPRmwGHX5xDEsQutcGKAF6BAgPEAU&sxsrf=AJOqlzWGHNISzgpAUCZBmQA1mWXXt3I7gA:1676311105893#htivrt=jobs&htidocid=GS94rKdYQqQAAAAAAAAAAA%3D%3D&fpstate=tldetail"
browser.get(url)
page=bs4.BeautifulSoup(browser.page_source)

if query != "":
    #job filter
    jobs_filter = page.find_all('div', {"data-facet": "job_family_1", "class": "eNr05b GbaVB ZkkK1e yUTMj k1U36b"})
    job_filter_list = [i['data-value'] for i in jobs_filter if not i['data-value'] == '__placeholder__']
    # Select job filter if needed
    words_jobs = set(job_filter_list)
    descriptions_jobs = words_jobs

    selected_options_jobs = st.multiselect('Select Job Options', descriptions_jobs)

    #location filter
    location_filter=page.find_all('div',{"data-facet":"city","class":"eNr05b GbaVB ZkkK1e yUTMj k1U36b"})
    location_filter_list=[i['data-value'] for i in location_filter if not i['data-value']=='__placeholder__']
    location_filter_name=[i['data-name'] for i in location_filter if not i['data-value']=='__placeholder__']
    location_dict={location_filter_name[i]:location_filter_list[i] for i in range(len(location_filter_list))}
    #Select location filter if needed
    words_loc = location_filter_name
    descriptions_loc = words_loc
    
    selected_options_loc = st.multiselect('Select Location', descriptions_loc)
    
    #employment type filter
    type_filter=page.find_all('div',{'data-facet':"employment_type","class":"eNr05b GbaVB ZkkK1e yUTMj k1U36b"})
    type_filter_list=[i['data-value'] for i in type_filter if not i['data-value']=='__placeholder__']
    #Select location filter if needed
    words_type = set(type_filter_list)
    descriptions_type = words_type
    
    selected_options_type = st.multiselect('Select the type of the job', descriptions_type)

    # Find all date posted
    job_dates = page.find_all("div", {"data-facet":"date_posted","class":"eNr05b GbaVB ZkkK1e yUTMj k1U36b"})

    # Extract dates posted
    job_date_list = [job_date['data-name'] for job_date in job_dates if not job_date['data-value']=="__placeholder__"]
    
    selected_options_date = st.radio('Select a date', job_date_list)

    #org filter
    org_filter=page.find_all('div',{'data-facet':"organization_mid","class":"eNr05b GbaVB ZkkK1e yUTMj k1U36b"})
    org_filter_name=[i['data-name'] for i in org_filter if not i['data-value']=='__placeholder__']
    #Select Organization filter if needed
    words_org = set(org_filter_name)
    descriptions_org = words_org
    
    selected_options_org = st.multiselect('Select the organisation', descriptions_org)

    #Industry filter
    ind_filter=page.find_all('div',{'data-facet':"industry.id","class":"eNr05b GbaVB ZkkK1e yUTMj k1U36b"})
    ind_filter_name=[i['data-name'] for i in ind_filter if not i['data-value']=='__placeholder__']
    #Select Organization filter if needed
    words_ind = set(ind_filter_name)
    descriptions_ind = words_ind
    
    selected_options_ind = st.multiselect('Select the organisation', descriptions_ind)

    filters='htichips='
    for i in selected_options_jobs:
        filters+=f'job_family_1:{i},'
    for i in selected_options_loc:
        filters+=f'city:{i},'
    for i in selected_options_type:
        filters+=f'employment_type:{i},'
    for i in selected_options_org:
        filters+=f'organization_mid:{i},'
    for i in selected_options_ind:
        filters+=f'industry.id:{i},'
    filters=filters[:-1]
        
    jobs_to_do = 1000
    jobs_done = 0
    l_prev=0
    
    browser.get(url)
    while jobs_done < jobs_to_do:
        lis = browser.find_elements(By.XPATH, "//li[@data-ved]//div[@role='treeitem']/div/div")
        l = len(lis)
        if l==0 or l==l_prev:
            break
        li = lis[-1]
        browser.execute_script('arguments[0].scrollIntoView({block: "center", behavior: "smooth"});', li)        
        jobs_done = l
        print(f'{jobs_done=}', end='\r')
        time.sleep(2)
        l_prev = l
        
    page = bs4.BeautifulSoup(browser.page_source)
    list_of_jobs = page.find_all("div", {"class": "PwjeAc"})
    role = []
    company = []
    location = []
    description = []
    for i in list_of_jobs:
        role.append(i.select('div.BjJfJf.PUpOsf')[0].text)
        company.append(i.select('div.vNEEBe')[0].text)
        location.append(i.select('div.Qk80Jf')[0].text)
        elements = i.select('span.HBvzbc')
        if elements:
            description.append(elements[0].text)
        else:
            pass
    df=pd.DataFrame(zip(role,company,location,description),columns=['Role','Company','Location','Description'])
    st.dataframe(df)