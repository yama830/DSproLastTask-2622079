import requests
from bs4 import BeautifulSoup

url = 'https://github.com/orgs/google/repositories'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

all_ul = soup.find_all('ul',{'class':'ul__5IxUHb withMetadata__klorrw'})



