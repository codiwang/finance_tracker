import os
import sqlite3

if os.path.exists('datas.db'):
    os.unlink('datas.db')

conn = sqlite3.connect('datas.db')
cur = conn.cursor()

cur.execute("CREATE TABLE MONEY (ID integer, DATE text, CATEGORY text, INCOME integer, EXPENSE integer, MEMO text)")
cur.execute("CREATE TABLE MAP (RINDEX integer, CINDEX integer, TYPE text, LEVEL integer)")
conn.commit()

conn.close()