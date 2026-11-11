import time
import requests
import sqlite3
from urllib.parse import urljoin
from bs4 import BeautifulSoup

db_path ='repo.db'
con = sqlite3.connect(db_path)
cur = con.cursor()
cur.execute('CREATE TABLE repo(repo_name text, language text, star_count);')
con.commit()

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

        cur.execute('''
    CREATE TABLE IF NOT EXISTS repositories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        repo_name TEXT NOT NULL UNIQUE,
        language TEXT,
        star_count TEXT,
        scraped_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    con.commit()
 
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

