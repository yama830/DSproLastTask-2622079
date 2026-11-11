import time
import requests
from bs4 import BeautifulSoup

url = 'https://github.com/orgs/google/repositories'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

all_li = soup.find_all('li',{'class':'listItem__X41oTe'})

for li in all_li:
    time.sleep(1)
    repo = li.find('span')
    repo_name = repo.text
    print(repo_name)




