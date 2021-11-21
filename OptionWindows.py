import time
from tkinter import *
from tkinter import messagebox, ttk
from tkinter.ttk import *

import PIL
import requests

import Dropbox
import funtzioak
import Dropbox as dBox
import helper

selected_items =[]
def downloadw(lista):
    window = Tk()
    window.title("Download")
    window.geometry('550x400')

    lbl = Label(window, text="Path", font=(14))
    lbl.place(x=50, y=100)

    path = Entry(window, width=30)
    path.place(x=90, y=100)

    for l in lista:
        funtzioak.download(l)


def error(root):
    window = Toplevel(root)
    window.title("Error")
    window.geometry('300x200')
    lbl = Label(window, text="Invalid url",font=("Arial Bold", 16))
    lbl.pack()

def DropBox(filepath,url):
    root = Toplevel()
    root.geometry('250x100')
    # root.iconbitmap('./favicon.ico')
    root.title('Login Dropbox')
    helper.center(root)

    login_frame = Frame(root, padx=10, pady=10)
    login_frame.pack(fill=BOTH, expand=True)
    # Login and Authorize in Drobpox
    dropbox = Dropbox.Dropbox(root)

    label = Label(login_frame, text="Login and Authorize\nin Drobpox")
    label.pack(side=TOP)
    button = Button(login_frame, borderwidth=4, text="Login", width=10, pady=8, command=dropbox.do_oauth)
    button.pack(side=BOTTOM)
    erantzuna = requests.get(url, allow_redirects=False)
    pdf_file = erantzuna.content
    dropbox.transfer_file(filepath,pdf_file)
'''
def dropBoxLista(lista):
    root = Toplevel()
    root.geometry('0x0')
    dropbox = Dropbox.Dropbox(root)
    dropbox.do_oauth()
    for f in lista():
        pdfname = f.replace('http:://', '')
        pdfname = pdfname.replace('https://', '')
        pdfname = pdfname.replace('/', '-')
        filepath='/'+pdfname
        erantzuna = requests.get(f, allow_redirects=False)
        pdf_file = erantzuna.content
        dropbox.transfer_file(filepath, pdf_file)'''

def html2pdfW(root):
    window = Toplevel(root)
    window.title("HTML TO PDF")
    window.geometry('550x400')
    lbl = Label(window, text="URL",font=(14))

    lbl.place(x=50,y=100)
    url= Entry(window, width=30)
    url.place(x=90,y=100)


    path = Entry(window, width=20,state='disabled')
    path.place(x=120, y=200)

    lpath = Label(window, text="Path:", font=(14))
    lpath.place(x=50, y=200)

    def callbackFunc(event):
        if combo.get()=='Local':
            path["state"] = "normal"
        else:
            path["state"] = "disabled"
            #combo.config(state='normal')


    combo=Combobox(window,values=['Local', 'DropBox'],width=10)
    combo['state'] = 'readonly'
    combo.place(x=340,y=100)

    combo.bind("<<ComboboxSelected>>", callbackFunc)

    def clicked():
        if combo.get()=='DropBox':
            gorde=''
        else:
            gorde=path.get()


        funtzioak.html2pdf(url.get(),gorde,combo.get())



    btn = Button(window, text="Download", command=clicked)
    btn.place(x=450,y=100)

def on_selecting(event):
    global selected_items
    widget = event.widget
    selected_items = widget.curselection()
    print(selected_items)

def allFiles(root):
    window = Toplevel()
    window.title("Get files")
    window.geometry('800x700')
    lbl = Label(window, text="URL")
    lbl.place(x=20,y=100)
    url = Entry(window, width=50)
    url.place(x=50, y=100)

    lb = Listbox(window, width=50, height=30, selectmode=EXTENDED)
    lb.place(x=50, y=150)

    def clicked():
        lista=funtzioak.get_url_paths(url,'pdf')
        print(lista)
        #lista = funtzioak.getAllLinks(url.get())
        if len(lista)==0:
            lb.insert(0,'No files to download')
        else:
            for file in lista:
                lb.insert(END,file)
                lb.bind('<<ListboxSelect>>', on_selecting())




    btn = Button(window, text="Search", command=clicked)
    btn.place(x=500, y=100)

    def download(lista,path):
        for i in lista:
            funtzioak.download(i,path)


    path = Entry(window, width=20)
    path.place(x=460, y=200)

    lpath = Label(window, text="Path:", font=(14))
    lpath.place(x=515, y=160)

    btnDownload = Button(window, text="Download", command=download(selected_items,path))
    btnDownload.place(x=500, y=250)


   # window.mainloop()

