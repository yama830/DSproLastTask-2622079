import time
import requests
import sqlite3
from urllib.parse import urljoin
from bs4 import BeautifulSoup

db_path = 'repo.db'
con = sqlite3.connect(db_path)
cur = con.cursor()

# IF NOT EXISTS を付けると、2回目以降の実行でもエラーにならない
cur.execute('''
    CREATE TABLE IF NOT EXISTS repo (
        repo_name TEXT,
        language TEXT,
        star_count TEXT
    )
''')
con.commit()

current_url = 'https://github.com/orgs/google/repositories'

# スクレイピング
while True:

    res = requests.get(current_url)

    soup = BeautifulSoup(res.content, 'html.parser')

    all_li = soup.find_all('li', {'class': 'listItem__X41oTe'})

    for li in all_li:
        repo = li.find('span')
        language = li.find('span', {'class': 'PrimaryLanguageName__94OAQO'})
        star = li.find('a', {'class': 'IconLabel__xAiop0 prc-Link-Link-9ZwDx'})

        repo_name = repo.text if repo else "なし"
        language_name = language.text if language else "なし"
        star_count = star.text.strip() if star else "0"

        print(repo_name)
        print(language_name)
        print(star_count)

        # ここでデータを挿入する(forループの中)
        cur.execute(
            'INSERT INTO repo (repo_name, language, star_count) VALUES (?, ?, ?)',
            (repo_name, language_name, star_count)
        )

    # 1ページ分が終わったらコミット
    con.commit()

    next_page = soup.find('a', rel='next')

    if not next_page:
        print('終了')
        break

    href = next_page.get('href')

    if href:
        current_url = urljoin(current_url, href)
    else:
        break

    time.sleep(1)

con.close()