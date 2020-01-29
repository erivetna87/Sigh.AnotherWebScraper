"""
!Python3 
Eric Rivetna - Data Scientist 
Lambda School Project: QuikHire.io

Initial WebScraper for QuikHire.io - Indeed
"""

#Webscraping Libraries
import requests
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#Data Libraries
"""Check to remove unused Libraries"""
import pandas as pd
import numpy as np
import time 
import psycopg2


# def user_input():
#     #Indeed uses + for any spacing between words to return results in URL
#     s = '+'
#     #Job Input Criteria
#     job_input = str(input('Enter Job Title Criteria: '))
#     job_input = job_input.split(' ')
#     job_input = s.join(job_input)

#     #City Criteria
#     city_input = str(input('Enter City Criteria: '))
#     city_input = city_input.split(' ')
#     city_input = s.join(city_input)

#     #State Criteria
#     state_input = str(input('Enter State Criteria: '))
#     state_input = state_input.split(' ')
#     state_input = s.join(state_input)
    
#     if job_input[-1:].endswith('+'):
#         job_input = job_input[:-1]
#     if city_input[-1:].endswith('+'):
#         city_input = city_input[:-1]
#     if state_input[-1:].endswith('+'):
#         state_input = state_input[:-1]
    
#     URL = 'https://www.indeed.com/jobs?q={}&l={}%2C+{}'.format(job_input,city_input,state_input)

#     return job_input, city_input, state_input, URL

# job_input, city_input, state_input, URL = user_input()



def url_list():
    tech_cities = {'Austin':'Texas','Raleigh':'North Carolina','San Jose':'California',
    'Seattle':'Washington','San Francisco':'California','Charlotte':'North Carolina',
    'Dallas':'Texas','Atlanta':'Georgia','Denver':'Colorado','Huntsville':'Alabama','Washington':'DC',
    'Columbus':'Ohio','Durham-Chapel Hill':'North Carolina','Boulder':'Colorado','Boston':'MA','Colorado Springs':'Colorado',
    'San Diego':'California','Jacksonville':'Florida','Tampa':'Florida','Baltimore':'Maryland',}
            
    data_set = {'Data Science', 'Business Intelligence', 'Data Analyst', 'Data Engineer','Machine Learning'}
    software_web_set = {'Software Engineer', 'Front-End Developer', 'Back-End Developer'}
    design_set = {'UX Designer', 'Product Designer'}
    
    data_url = []
    sw_url = []
    ux_url = []
    
    for i in data_set:
        for k,v in tech_cities.items():
            data_url.append('https://www.indeed.com/jobs?q={}&l={}%2C+{}'.format(i,k,v))

    for s in software_web_set:
        for k,v in tech_cities.items():
            sw_url.append('https://www.indeed.com/jobs?q={}&l={}%2C+{}'.format(s,k,v))

    for p in design_set:
        for k,v in tech_cities.items():
            ux_url.append('https://www.indeed.com/jobs?q={}&l={}%2C+{}'.format(p,k,v))
    
    return data_url, sw_url, ux_url

def url_test():

    data_url, sw_url, ux_url = url_list()

    for url in data_url:
        for i in range(0,10,10):
            print(url+'&start='+str(i))
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            soup.prettify()

    


url_test()




def job_summary_sel(url_list):
    
    df = pd.DataFrame(columns=["Title","Location","Company","Salary","Sponsored","Description","Days Posted"])
    
    data_url, sw_url, ux_url = url_list()
    
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome('./chromedriver')  
    
    for url in url_list:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        for i in range(0,500,10):
            driver.get(url+'&start='+str(i))
            driver.implicitly_wait(8)
            all_jobs = driver.find_elements_by_class_name('result')
            for job in all_jobs:
                result_html = job.get_attribute('innerHTML')
                soup_func = BeautifulSoup(result_html, 'html.parser')
                
                try:
                    title = soup_func.find("a", class_="jobtitle").text.replace('\n','')
                except:
                    title = 'None'
                    
                try:
                    location = soup_func.find(class_="location").text.replace('\n','')
                except:
                    location = 'None'
                    
                try:
                    company = soup_func.find(class_="company").text.replace('\n','')
                except:
                    company = 'None'
                    
                try:
                    salary = soup_func.find(class_="salaryText").text.replace('\n','')
                except:
                    salary = 'None'
                    
                try: 
                    sponsored = soup.find(class_="sponsoredGray").text
                except:
                    sponsored = "Organic"
                        
                sum_div = job.find_elements_by_class_name("summary")[0]

                try: 
                    days = soup_func.find(class_="date").text.replace('\n','')
                except:
                    days = 'None'
                    
                try:
                    sum_div.click()
                except:
                     close_popup = driver.find_element_by_class_name('popover-x-button-close')
                     close_popup.click()
                     sum_div.click()

                try:
                    job_desc = driver.find_element_by_id('vjs-desc').text
                except:
                    job_desc = 'None'
                    
                df = df.append({'Title':title,'Location':location,"Company":company,"Salary":salary,
                "Sponsored":sponsored,"Description":job_desc, "Days Posted":days}, ignore_index=True)

                df.to_csv('DB_Check.csv', index=False)

                driver.close()




        
# job_summary_sel()



# def job_title(soup):
#     print(soup.prettify())
#     jobs = []
#     for div in soup.find_all(name="div", attrs={"class":"row"}):
#         for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
#             jobs.append(a["title"])
#     return jobs

# def company_name(soup):
#     companies = []
#     for i in soup.find_all(name="div", attrs={"class":"row"}):
#         company = i.find_all(name="span", attrs={"class":"company"})
#         for a in company:
#             companies.append(a.text.strip())
    
#     return companies

# def location_name(soup):
#     locations = []
#     spans = soup.find_all(name="div", attrs={"class":"location"})
#     for g in spans:
#         locations.append(g.text.strip())
    
#     return locations

# def summary(soup):
#     summaries = []
#     div = soup.find_all(name="div", attrs={"class":"summary"})
#     for li in div:
#         summaries.append(li.text.strip())
    
#     return summaries



