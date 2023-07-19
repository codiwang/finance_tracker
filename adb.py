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

    def add(self, etype, income, expense, memo):
        import datetime
        date = datetime.date.today()
        self.cur.execute("INSERT INTO MONEY VALUES (?, ?, ?, ?, ?)", (date, etype, income, expense, memo))
        return self.conn.commit()
    
    def update(i,col,new):
        self.cur.execute("UPDATE MONEY SET {col}=? WHERE ID=?",(new,i))
        return self.conn.commit()

    def delete(self, i):
        print(i)
        self.cur.execute("DELETE FROM MONEY WHERE rowid=?", (i,))
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





