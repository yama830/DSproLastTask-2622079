import requests
from bs4 import BeautifulSoup

url = 'https://github.com/orgs/google/repositories'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

all_li = soup.find_all('li',{'class':'listItem__X41oTe'})

for li in all_li:
    repo_name = li.get('aria-label')

print(repo_name)




