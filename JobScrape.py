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

#Data Libraries
"""Check to remove unused Libraries"""
import pandas as pd
import numpy as np
import time 
import psycopg2




def soup():
    #Indeed uses + for any spacing between words to return results in URL
    s = '+'
    #Job Input Criteria
    job_input = str(input('Enter Job Title Criteria: '))
    job_input = job_input.split(' ')
    job_input = s.join(job_input)

    #City Criteria
    city_input = str(input('Enter City Criteria: '))
    city_input = city_input.split(' ')
    city_input = s.join(city_input)

    #State Criteria
    state_input = str(input('Enter State Criteria: '))
    state_input = state_input.split(' ')
    state_input = s.join(state_input)
    
    if job_input[-1:].endswith('+'):
        job_input = job_input[:-1]
    if city_input[-1:].endswith('+'):
        city_input = city_input[:-1]
    if state_input[-1:].endswith('+'):
        state_input = state_input[:-1]
    
    URL = 'https://www.indeed.com/jobs?q={}&l={}%2C+{}'.format(job_input,city_input,state_input)
    
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")
    
    return soup

def job_title(soup):
    jobs = []
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
            jobs.append(a["title"])
    return jobs

def company_name(soup):
    company_names = []
    for div in soup.find_all(name="div", attrs={"class:row"}):
        company = div.find_all(name="span", attrs={"class":"company"})
        if len(company) > 0:
            for b in company:
                company_names.append(b.text.strip())
        else:
            company_pull_2 = div.find_all(name="span", attrs={"class":"result-link-source"})
            for span in company_pull_2:
                company_names.append(span.text.strip())
    return company_names
    
print(job_title(soup()))
