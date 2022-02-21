from tkinter import *
from tkinter import ttk
import pandas as pd
import random, string

fnt_2 = 'Consolas'  #text1

def TableDel(tr):
    for x in tr.get_children():
        tr.delete(x)
def TableFetch(tr, clm):
    lst = []
    for x in tr.get_children():
        lst.append(tr.item(x)['values'])
    return pd.DataFrame(lst, columns=clm)
def TableApp(dt, tr, uniq):   #data, tree, unique append (True/ False)
    lst = []
    lst1 = []
    dtc = dt
    if uniq:
        for x in tr.get_children():
            lst.append(list(tr.item(x)['values']))

        for x in range(dt.shape[0]):
            if list(dt.iloc[x]) not in lst:
                lst1.append(list(dt.iloc[x]))
        dtc = pd.DataFrame(lst1)
        

    for x in range(dtc.shape[0]):
        # generating random strings 

        res = ''.join(random.choices(string.ascii_uppercase +string.digits, k = 10))
        tr.insert(parent='',index='end', iid=str(res), values=tuple(dtc.iloc[x]), text='')
        break           
def TableDis(dt, column_name, max_ht, rt, app, wid):    #Tree view creater
    w = ttk.Scrollbar(rt)
    w.pack(side=RIGHT, fill = 'y')
    tr = ttk.Treeview(rt, yscrollcommand=w.set)
    tr['columns'] = column_name
    tr.column('#0', minwidth=0, width=0)
    for x in range(len(column_name)):
        id = '#'+str(x+1)
        tr.column(id, anchor=W, width=wid)
    for x in column_name:
        tr.heading(x, text = x, anchor=W)
    tr['height'] = max_ht
    if app:
        for x in range(dt.shape[0]):
            # generating random strings 
            while(True):
                try:
                    res = ''.join(random.choices(string.ascii_uppercase +string.digits, k = 10))
                    tr.insert(parent='',index='end', iid=str(res), values=tuple(dt.iloc[x]), text='')
                    break
                except:
                    pass
    tr.pack()
    w.config(command=tr.yview)
    return tr
def ListCre(rt):
    scr = Scrollbar(rt)
    scr.pack(side=RIGHT, fill=Y)
    lst_bx = Listbox(rt, yscrollcommand=scr.set, font=(fnt_2, 15))
    lst_bx.pack(side = LEFT, fill = BOTH)
    scr.config(command=lst_bx.yview)
    return lst_bx
def ListIns(lst_bx, lst):
    for x in lst:
        lst_bx.insert(END, str(x))
#pd
def read(loc, colm_Name = None): #reader
    try:
        return pd.read_csv(loc)
    except:
        df = pd.DataFrame([], columns=colm_Name)
        df.to_csv(loc, index=False, mode = 'w', columns = list(df.columns), header = True)
        return pd.read_csv(loc)
def write(dt, loc, indx = False, mod = 'a', colus=None, hdr = False):  #default append (can be a writer and creater)
    dt.to_csv(loc, index=indx, mode = mod, columns = colus, header = hdr)