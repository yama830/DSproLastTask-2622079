import requests
from bs4 import BeautifulSoup

repopo = []
url = 'https://github.com/google'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

repositories = soup.find('span',{'class':'repo'})
a_list = soup.find_all('a')


for a in a_list:
    repo_name = a.find('span', {'class': 'repo'})

