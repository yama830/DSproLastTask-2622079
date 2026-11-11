import time
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

current_url = 'https://github.com/orgs/google/repositories'

while True:

    res = requests.get(current_url)

    soup = BeautifulSoup(res.content, 'html.parser')

    all_li = soup.find_all('li',{'class':'listItem__X41oTe'})

    for li in all_li:
        time.sleep(1)
        repo = li.find('span')
        repo_name = repo.text
        print(repo_name)

    next_page = soup.find('a',{'class':'prc-Pagination-Page-Etgqf'})

    if not next_page:
        print('終了')
        break

    href = next_page.get('href')

    if href:
        current_url = urljoin(current_url,href)
    else:
        break

    time.sleep(1)

