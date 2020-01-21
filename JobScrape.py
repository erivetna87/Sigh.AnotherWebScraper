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


def url_search():
    #Indeed uses + for any spacing between words to return results in URL
    s = '+'
    #Job Input Criteria
    job_input = str(input('Enter Job Title Criteria: '))
    job_input = job_input.split(' ')
    job_input = s.join(job_input)

    #City Criteria
    city_input = str(input('Enter City Criteria: '))
    job_input = job_input.split(' ')
    job_input = s.join(job_input)



    
    # URL = 'https://www.indeed.com/jobs?q={}&l={}%2C+{}'.format(job_input, )

url_search()