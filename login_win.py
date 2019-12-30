import csv
import tkinter as tk
from tkinter import ttk
import _tkinter

import signup_win
import chat_win


# ----------- Choose a Account to Login ------------
def go_login(account_info):
    for info in list_info:
        if account_info in info:
            with open("temporary.csv", 'w') as temp_f:
                writer = csv.writer(temp_f)
                writer.writerow(info)
            try:
                li_window.destroy()
            except _tkinter.TclError:
                pass

    chat_win.chatting()


def go_signup():
    # li_window.quit()  # Bugggggggggg!!!!!!!!
    li_window.destroy()
    signup_win.signup()


# ----------- Read User Info ------------
def read_info():
    global list_info
    list_info = []

    with open('user_info.csv', 'r') as ui_file:
        reader = csv.reader(ui_file)
        for row in reader:
            if row:
                list_info.append(row)

    if list_info:
        for info in list_info:
            list_value.append(info[0])
    else:
        list_value.append('None')

    return list_value


def login():
    global li_window
    global list_value
    # ----------- Window Set ------------
    list_value = []
    size_li = HEIGHT, WIDTH = 320, 320

    li_window = tk.Tk()
    li_window.title('Chatool Login')

    canvas = tk.Canvas(li_window, height=HEIGHT, width=WIDTH)
    canvas.pack()

    # ----------- Top Frame ------------
    cat_frame = tk.Frame(li_window, bg='#c2d6d6')
    cat_frame.place(relx=0.2, rely=0.12, relwidth=0.6, relheight=0.72)

    cat_image = tk.PhotoImage(file='/Users/soul/PycharmProjects/Chat/tk_chatool/2.png')
    cat_label = tk.Label(cat_frame, image=cat_image)
    cat_label.place(relx=0.1, rely=0.08, relwidth=0.8, relheight=0.6)

    # ----------- Down Frame ------------
    li_frame = tk.Frame(li_window, bg='#c2d6d6')
    li_frame.place(relx=0.25, rely=0.58, relwidth=0.5, relheight=0.24)

    # Account Menu ..............
    comvalue = tk.StringVar()
    comboxlist = ttk.Combobox(li_frame, textvariable=comvalue)
    comboxlist['value'] = read_info()
    comboxlist.current(0)
    comboxlist.place(relx=0.01, rely=0.12, relwidth=0.52, relheigh=0.35)

    # Click ...............
    li_button = tk.Button(li_frame, text='Login', bg='#c2d6d6', command=lambda: go_login(comboxlist.get()))
    li_button.place(relx=0.58, rely=0.12, relwidth=0.4, relheight=0.35)

    go_button = tk.Button(li_frame, text='Go >>  Sign Up', bg='#c2d6d6', command=lambda: go_signup())
    go_button.place(relx=0.01, rely=0.57, relwidth=0.98, relheight=0.35)

    # ----------- Run ------------
    li_window.mainloop()
