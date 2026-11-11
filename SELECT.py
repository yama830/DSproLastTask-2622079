import sqlite3


con = sqlite3.connect('repo.db')
cur = con.cursor()

print("--- DBに保存されたデータを表示します ---")

cur.execute('SELECT * FROM repo')
rows = cur.fetchall()


for row in rows:
    print(row)

con.close()