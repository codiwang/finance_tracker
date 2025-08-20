from adb import DB
from tkinter import *
from tkinter import ttk
import matplotlib as plt
plt.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
import numpy as np
from tkcalendar import DateEntry


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title('Finance Tracker')
        self.width = 800
        self.height = 600
        self.master.resizable(False, False)
        self.x = (self.master.winfo_screenwidth() // 2) - (self.width // 2)
        self.y = (self.master.winfo_screenheight() // 2) - (self.height // 2)
        self.master.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x, self.y))
        self.enhead = ('DefaultFont', 16)
        self.enbody = ('DefaultFont', 14)
        self.zhfont = ('微軟正黑體', 12)
        self.create_widgets()
    
    def refresh_clicked(self):
        self.tree.delete(*self.tree.get_children())
        with DB() as db:
            mlist = db.get_data()
        for i in range(len(mlist)):
            m = list(mlist[i])
            self.tree.insert('','end',values=m)
        print('refreshed!')

    def clear_entry(self):
        self.e2.delete(0,10)
        self.e3.delete(0,10)
        self.e4.delete(0,100)
        print('cleared!')

    def create_widgets(self):
        mainw = self.master
        enhead = self.enhead
        enbody = self.enbody
        zhfont = self.zhfont
        # 建立各個分頁
        self.tabs = ttk.Notebook(mainw)
        self.tab1 = Frame(self.tabs, width=self.width, height=self.height)
        self.tab2 = Frame(self.tabs, width=self.width, height=self.height)
        self.tab3 = Frame(self.tabs, width=self.width, height=self.height)
        self.tabs.add(self.tab1, text='Dashboard')
        self.tabs.add(self.tab2, text='Records')
        
        mainw.grid_rowconfigure(0, weight=1)
        mainw.grid_columnconfigure(0, weight=2)
        self.tabs.grid(row=0, column=0, sticky=NSEW, padx=4, pady=4)

    
        # 城市的格子
        '''
        self.frame1 = []
        N = 5
        for i in range(N):
            self.frame = Frame(self.tab1)
            self.frame.pack()
            self.frame1.append(self.frame)
        self.all_btns = []
        for i in range(N*N):
            fi = i // N
            # bd = border
            self.btn = Button(self.frame1[fi], font=enhead, width=6, height=3,
            relief=GROOVE, bd=1,
            bg='white', fg='black')
            self.btn.pack(side=LEFT)
            self.all_btns.append(self.btn)    
        '''
        
        with DB() as db:
            # Tab 1: Overview
            self.frame1 = Frame(self.tab1, height=200)
            self.frame1.pack(pady=10)
            self.r1 = Label(self.frame1, text='Total Income', font=enhead).grid(row=0,column=0,padx=20,pady=5)
            self.r2 = Label(self.frame1, text='Total Expenses', font=enhead).grid(row=0,column=1,padx=20,pady=5)
            self.r3 = Label(self.frame1, text='Total Balance', font=enhead).grid(row=0,column=2,padx=20,pady=5)
            self.r4 = Label(self.frame1, text=f'{db.get_total()[0]}',font=enhead,fg='green').grid(row=1,column=0,padx=20,pady=5)
            self.r5 = Label(self.frame1, text=f'{db.get_total()[1]}',font=enhead,fg='red').grid(row=1,column=1,padx=20,pady=5)
            self.r6 = Label(self.frame1, text=f'{db.get_total()[2]}',font=enhead).grid(row=1,column=2,padx=20,pady=5)
            
            self.frame1b = Frame(self.tab1, height=300)
            self.frame1b.pack(pady=30)
            
            # Category review
            self.r7 = Label(self.frame1b, text='Category Review', font=enhead).grid(row=0,column=0)
            tdict = db.get_data_by_category()
            tlist = np.array(list(tdict.values()))
            fig = Figure(figsize=(4,4), dpi=80)
            if sum(tlist) == 0:
                print("No data to plot!")
            else:
                ax = fig.add_subplot(111)
                ax.pie(tlist, labels=list(tdict.keys()), shadow=True)
                ax.legend()
            chart1 = FigureCanvasTkAgg(fig, self.frame1b)
            chart1.get_tk_widget().grid(row=1,column=0,padx=10,pady=5)
            
            # Monthly Review (6 months)
            self.r8 = Label(self.frame1b, text='Monthly Review (6 months)', font=enhead).grid(row=0,column=1)
            rlist = db.get_data_by_month()
            xpoints = np.array([r[0] for r in rlist])
            ypoints1 = np.array([r[1] for r in rlist])
            ypoints2 = np.array([r[2] for r in rlist])
            fig2 = Figure(figsize=(4,4), dpi=80)
            ax2 = fig2.add_subplot(111)
            ax2.plot(xpoints, ypoints1, marker = 'o', markersize=5, label='Income')
            ax2.plot(xpoints, ypoints2, marker = 'o', markersize=5, label='Expense')
            ax2.set_xlabel("Month")
            ax2.set_ylabel("NTD")
            ax2.grid()
            ax2.legend()
            chart2 = FigureCanvasTkAgg(fig2, self.frame1b)
            chart2.get_tk_widget().grid(row=1,column=1,padx=10,pady=5)

            # Tab 2: add, delete, edit + list
            # 1. All Records list
            self.tree = ttk.Treeview(self.tab2, column=('1','2','3','4','5','6'), show='headings')
            style = ttk.Style()
            style.configure('Treeview.Heading', font=enhead)
            style.configure('Treeview', font=enbody, rowheight=30)
            style.map('Treeview', background=[('selected', 'grey')])
            self.tree.heading('1', text='ID')
            self.tree.heading('2', text='Date')
            self.tree.heading('3', text='Category')
            self.tree.heading('4', text='Income')
            self.tree.heading('5', text='Expense')
            self.tree.heading('6', text='Memo')
            self.tree.column('1', width=120, anchor='center')
            self.tree.column('2', width=120, anchor='center')
            self.tree.column('3', width=120, anchor='center')
            self.tree.column('4', width=120, anchor='center')
            self.tree.column('5', width=120, anchor='center')
            self.tree.column('6', width=120, anchor='center')
            mlist = db.get_data()
            for i in range(len(mlist)):
                m = list(mlist[i])
                self.tree.insert('','end',values=m)
            self.tree.pack()
            
            # 2. Database functions
            self.frame2 = Frame(self.tab2, height=200)
            self.frame2.pack()
            self.frame2['borderwidth'] = 3
            self.frame2['relief'] = 'flat'
            self.frame2.columnconfigure(0, weight=3)
            self.frame2.columnconfigure(1, weight=2)
            
            # Input labels and entries
            # Date
            self.l0 = Label(self.frame2, text='Date', font=enhead).grid(row=0,column=0,padx=10,pady=2,sticky=W)
            self.date_entry = DateEntry(self.frame2, width=12, background='darkblue', foreground='white', borderwidth=2, year=2025)
            self.date_entry.grid(row=0, column=1)
            # Category
            self.l1 = Label(self.frame2, text='Category', font=enhead).grid(row=1,column=0,padx=10,pady=2,sticky=W)
            options = ['Food','Clothes','Transportation','Entertainment','Income']
            self.variable = StringVar()
            self.variable.set('Food')
            self.drop = OptionMenu(self.frame2, self.variable, *options)
            self.drop.grid(row=1,column=1,padx=10,pady=2,ipadx=5,sticky=W)
            self.drop.config(font=enbody)
            # Income
            self.l2 = Label(self.frame2, text='Income', font=enhead).grid(row=2,column=0,padx=10,pady=2,sticky=W)
            self.e2 = Entry(self.frame2, font=enbody)
            self.e2.insert(-1, '0')
            self.e2.grid(row=2,column=1,padx=10,pady=2)
            # Expense
            self.l3 = Label(self.frame2, text='Expense', font=enhead).grid(row=3,column=0,padx=10,pady=2,sticky=W)
            self.e3 = Entry(self.frame2, font=enbody)
            self.e3.insert(-1, '0')
            self.e3.grid(row=3,column=1,padx=10,pady=2)
            # Memo
            self.l4 = Label(self.frame2, text='Memo', font=enhead).grid(row=4,column=0,padx=10,pady=2,sticky=W)
            self.e4 = Entry(self.frame2, font=enbody)
            self.e4.grid(row=4,column=1,padx=10,pady=2)
            
            # Buttons
            # Add
            self.b1 = Button(self.frame2, text='Add', font=enhead, fg='black', bg='#a9d5ee', 
                             command=lambda: [db.add(self.date_entry.get_date(), self.variable.get(),self.e2.get(),self.e3.get(),self.e4.get()), 
                                              self.clear_entry(), self.e2.insert(-1, '0'), self.e3.insert(-1, '0'), self.refresh_clicked()])
            self.b1.grid(row=0,column=2,padx=10,pady=2,sticky=W)
            # Edit
            self.b2 = Button(self.frame2, text='Edit', font=enhead, fg='black', bg='#a9d5ee', command=db.get_data)
            self.b2.grid(row=1,column=2,padx=10,pady=2,sticky=W)
            # Delete
            self.b3 = Button(self.frame2, text='Delete', font=enhead, fg='black', bg='#a9d5ee', 
                             command=lambda: [db.delete(self.tree.item(self.tree.focus(),'values')[0]), self.refresh_clicked()])
            self.b3.grid(row=2,column=2,padx=10,pady=2,sticky=W)
            # Print
            self.b4 = Button(self.frame2, text='Print', font=enhead, fg='black', bg='#a9d5ee', command=db.get_data)
            self.b4.grid(row=3,column=2,padx=10,pady=2,sticky=W)
            # Refresh
            self.b5 = Button(self.frame2, text='Refresh', font=enhead, fg='black', bg='#a9d5ee', command=self.refresh_clicked)
            self.b5.grid(row=4,column=2,padx=10,pady=2,sticky=W)
            
            self.master.mainloop()

            
            
twin = Tk()
app = Application(master=twin)
#app.mainloop()

#choose date
#edit
#monthly/weekly review
#dropdown, radio
#treeview 要有 rowid 每次顯示時重新計算，要update,delete時要回傳rowid, 資料庫裡面不用


    