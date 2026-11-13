import time
import requests
import sqlite3
from bs4 import BeautifulSoup

db_path = 'repo.db'
con = sqlite3.connect(db_path)
cur = con.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS repo (
        repo_name TEXT PRIMARY KEY,
        language TEXT,
        star_count TEXT
    )
''')
con.commit()

base_url = 'https://github.com/orgs/google/repositories'
headers = {'User-Agent': 'Mozilla/5.0 (scraping-practice)'}
START_PAGE = 1  


def fetch(page, max_retry=5):
    """429や5xxのときは待って再試行する"""
    for attempt in range(max_retry):
        res = requests.get(f"{base_url}?page={page}", headers=headers, timeout=30)
        if res.status_code == 200:
            return res
        if res.status_code in (429, 502, 503, 504):
            wait = int(res.headers.get('Retry-After', 0)) or 10 * (attempt + 1)
            print(f"  ステータス {res.status_code}。{wait}秒待って再試行します")
            time.sleep(wait)
            continue
        return res  # 404など、リトライしても無駄なもの
    return res


page = START_PAGE
prev_names = None
total_new = 0

while True:
    print(f"--- {page}ページ目をスクレイピング中 ---")
    res = fetch(page)

    if res.status_code != 200:
        print(f"ステータスコード {res.status_code} のため終了")
        break

    soup = BeautifulSoup(res.content, 'html.parser')
    all_li = soup.find_all('li', {'class': 'listItem__X41oTe'})

    if not all_li:
        print("リポジトリが見つからないため終了")
        break

    rows = []
    for li in all_li:
        repo = li.find('span')
        language = li.find('span', {'class': 'PrimaryLanguageName__94OAQO'})
        star = li.find('a', {'class': 'IconLabel__xAiop0 prc-Link-Link-9ZwDx'})

        repo_name = repo.text.strip() if repo else "なし"
        language_name = language.text.strip() if language else "なし"
        star_count = star.text.strip() if star else "0"
        rows.append((repo_name, language_name, star_count))

    # 前のページと全く同じ内容なら、最終ページを超えたとみなして終了
    names = [r[0] for r in rows]
    if names == prev_names:
        print("前ページと同じ内容のため終了")
        break
    prev_names = names

    for row in rows:
        cur.execute(
            'INSERT OR IGNORE INTO repo (repo_name, language, star_count) VALUES (?, ?, ?)',
            row
        )
        total_new += cur.rowcount
    con.commit()

    page += 1
    time.sleep(1)


print("\n--- DBに保存されたデータをSELECT文で表示します ---")
cur.execute('SELECT * FROM repo')
rows = cur.fetchall()
for row in rows:
    print(row)

print(f"\n完了: 今回 {total_new} 件を新規保存（DB内合計 {len(rows)} 件）")
con.close()