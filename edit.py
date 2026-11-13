import sqlite3

con = sqlite3.connect('repo.db')
cur = con.cursor()

# 同じrepo_nameのうち、最初の1件（最小のrowid）だけを残して重複を削除
cur.execute('''
    DELETE FROM repo
    WHERE rowid NOT IN (
        SELECT MIN(rowid)
        FROM repo
        GROUP BY repo_name
    )
''')

con.commit()
con.close()