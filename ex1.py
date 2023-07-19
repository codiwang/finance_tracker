"""
A(4)   90 ~ 100
B(3)   80 ~  89
C(2)   70 ~  79
D(1)   60 ~  69
F(0)    0 ~  59
"""

from tkinter import *
from tkinter import messagebox, filedialog, ttk
from tkinter.font import Font, families
from functools import partial
from random import choice, randint
from datetime import date

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title('學生成績')
        self.width = 640
        self.height = 480
        self.year = date.today().year-1911
        self.master.resizable(True, True)
        self.x = (self.master.winfo_screenwidth() // 2) - (self.width // 2)
        self.y = (self.master.winfo_screenheight() // 2) - (self.height // 2)
        self.master.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x, self.y))
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.appfont = Font(family='Consolas', size=12)
        self.create_widgets()
        self.bind_functions()

    def fixed_map(self, style, option):
        # https://core.tcl-lang.org/tk/info/509cafafae
        return [elm for elm in style.map('Treeview', query_opt=option)
            if elm[:2] != ('!disabled', '!selected')]

    def create_widgets(self):
        myfont = self.appfont
        mainw = self.master
        self.tabs = ttk.Notebook(mainw)
        self.tab1 = Frame(self.tabs)
        self.tab2 = Frame(self.tabs)
        self.tabs.add(self.tab1, text='列表')
        self.tabs.add(self.tab2, text='報告')
        self.tabs.grid(row=0, column=0, sticky=NSEW, padx=4, pady=4)
        # for tab1
        self.tab1.grid_rowconfigure(0, weight=1)
        self.tab1.grid_columnconfigure(0, weight=1)
        self.sbr1 = Scrollbar(self.tab1)
        self.tree = ttk.Treeview(self.tab1, columns=('1','2','3','4'),
            show='headings', yscrollcommand=self.sbr1.set)
        style = ttk.Style()
        style.configure('Treeview.Heading', font=('微軟正黑體', 11))
        style.map('Treeview',
            foreground=self.fixed_map(style, 'foreground'),
            background=self.fixed_map(style, 'background'))
        self.tree.column('1', width=100, anchor='center')
        self.tree.column('2', width=100, anchor='center')
        self.tree.column('3', width=100, anchor='center')
        self.tree.column('4', width=100, anchor='center')
        self.tree.heading('1', text='學號')
        self.tree.heading('2', text='性別')
        self.tree.heading('3', text='國文')
        self.tree.heading('4', text='英文')
        classes = (('apple', '蘋果班', 10), ('banana', '香蕉班', 16), ('cherry', '櫻桃班', 12))
        self.tree.tag_configure('oddrow', background='#d5d5d5')
        self.tree.tag_configure('evenrow', background='#dceff8')
        for i, cla in enumerate(classes):
            cla_row = self.tree.insert('', i, cla[0], text=cla[1], open=1, values=(cla[1], '*收合*'))
            cla_num = cla[2]
            for j in range(1, cla_num+1):
                zh = randint(10, 100)
                en = randint(10, 100)
                stuid = f'{self.year}{cla[0][0].upper()}{j:02d}'
                row = (stuid, choice(('F', 'M')), zh, en)
                tag = 'oddrow' if j % 2 == 1 else 'evenrow'
                self.tree.insert(cla_row, 'end', text=stuid, values=row, tags=(tag,))

        self.tree.grid(row=0, column=0, sticky=NSEW, ipadx=2, ipady=2)
        self.sbr1.grid(row=0, column=1, sticky=NSEW)
        self.sbr1.config(command=self.tree.yview)
        # for tab2
        self.txt1 = Text(self.tab2, font=('Consolas', 12))
        self.txt1.grid(row=0, sticky=NSEW, ipadx=2, ipady=2)
        self.txt1.focus()

    def select_item(self, event=None):
        current_item = self.tree.focus()
        item = self.tree.item(current_item)
        self.txt1.delete(1.0, END)
        if len(item['values']) == 2:
            if item['open']:
                item['values'][1] = '*收合*'
            else:
                item['values'][1] = '*展開*'
            self.tree.item(current_item, values=item['values'])
        else:
            for i in self.tree.selection():
                item = self.tree.item(i)
                item['values'].append('\n')
                line = ' '.join(list(map(str, item['values'])))
                self.txt1.insert(INSERT, line)

    def bind_functions(self):
        self.master.bind('<Escape>', self.quit_app)
        self.tree.bind('<ButtonRelease-1>', self.select_item)
        self.tree.bind('<KeyRelease>', self.select_item)
        self.tree.bind('<<TreeviewSelect>>', self.select_item)

    def quit_app(self, event=None):
        if messagebox.askokcancel('關閉', '確定離開？'):
            self.master.destroy()


twin = Tk()
app = Application(master=twin)
app.mainloop()

