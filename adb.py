import datetime

class DB():
    def __init__(self):
        self.conn = None
        self.cur = None 

    def __enter__(self):
        self.open()
        return self
 
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False

    def open(self):
        if self.conn is None:
            import sqlite3
            self.conn = sqlite3.connect('datas.db')
            self.cur = self.conn.cursor()
        return True
    
    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
        return True

    def add(self, date, etype, income, expense, memo):
        #date = datetime.date.today()
        self.cur.execute("SELECT MAX(ID) FROM MONEY")
        row = self.cur.fetchone()
        next_id = (row[0] or 0) + 1 
        self.cur.execute("INSERT INTO MONEY VALUES (?, ?, ?, ?, ?, ?)", (next_id, date, etype, income, expense, memo))
        return self.conn.commit()
    
    def update(self, i, col, new):
        self.cur.execute("UPDATE MONEY SET {col}=? WHERE ID=?",(new,i))
        return self.conn.commit()

    def delete(self, i):
        self.cur.execute("DELETE FROM MONEY WHERE ID=?", (i,))
        self.cur.execute("UPDATE MONEY SET ID=ID-1 WHERE ID>?",(i,))
        return self.conn.commit()

    def get_total(self):
        self.cur.execute("SELECT SUM(INCOME) FROM MONEY")
        ti = self.cur.fetchone()[0]
        self.cur.execute("SELECT SUM(EXPENSE) FROM MONEY")
        te = self.cur.fetchone()[0]
        if ti==None or te==None:
            return list([0,0,0])
        else:  
            tb = ti-te
            return list([ti, te, tb])

    def get_data(self):
        self.cur.execute("SELECT * FROM MONEY")
        mlist = self.cur.fetchall()
        print('-'*40)
        for m in mlist:
            print(m)
        print()
        return mlist

    def get_data_by_category(self):
        options = ['Food','Clothes','Transportation','Entertainment']
        tdict = {}
        for i in options:
            self.cur.execute("SELECT SUM(EXPENSE) FROM MONEY WHERE CATEGORY=?", (i,))
            t = self.cur.fetchone()[0]
            if t==None:
                tdict[i] = 0
            else:
                tdict[i] = t
        return tdict
    
    def get_data_by_month(self):
        import datetime
        
        month = str(datetime.date.today())[0:7]
        self.cur.execute("""
        SELECT
            STRFTIME("%m-%Y", DATE) AS Month,
            SUM(INCOME) AS Income,
            SUM(EXPENSE) AS Expense
        FROM MONEY
        WHERE DATE BETWEEN DATE('now','-6 month','start of month') AND DATE('now')
        GROUP BY
            STRFTIME("%m-%Y", DATE);""")
        rlist = self.cur.fetchall()
        return rlist





