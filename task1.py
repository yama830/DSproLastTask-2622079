import time
import requests
import sqlite3
from urllib.parse import urljoin
from bs4 import BeautifulSoup

path = './db/'
db_name = 'github.sqlite'
con = sqlite3.connect(path + db_name)
cur = con.cursor()
sql_create_table_git = 'CREATE TABLE git(repo_name text , language text,  star_count int);'
cur.execute(sql_create_table_git)
con.close()

current_url = 'https://github.com/orgs/google/repositories'

#スクレイピング
while True:

    res = requests.get(current_url)

    soup = BeautifulSoup(res.content, 'html.parser')

    all_li = soup.find_all('li',{'class':'listItem__X41oTe'})

    for li in all_li:
        time.sleep(1)
        repo = li.find('span')
        language = li.find('span',{'class':'PrimaryLanguageName__94OAQO'})
        star = li.find('a',{'class':'IconLabel__xAiop0 prc-Link-Link-9ZwDx'})

        repo_name = repo.text if repo else "なし"
        language_name = language.text if language else "なし"
        star_count = star.text if star else "0"

        print(repo_name)
        print(language_name)
        print(star_count)

    next_page = soup.find('a',rel = 'next')

    if not next_page:
        print('終了')
        break

    href = next_page.get('href')

    if href:
        current_url = urljoin(current_url,href)
    else:
        break

    time.sleep(1)

