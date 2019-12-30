import csv
import time
import socket
import schedule
# import threading
import tkinter as tk
from tkinter import *
# from tkinter.scrolledtext import ScrolledText

import my_smtp
import my_pop
from film_func import film_win

list_time = []


def add_group(nick, email, state):
    with open('group.csv', 'a', newline='') as ag_f:
        writer = csv.writer(ag_f)
        writer.writerow([nick, email, state])
        listbox.insert(END, '  ' + nick, '⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯%s⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯' % state)

    entry_add.delete(0, END)
    entry_nick.delete(0, END)


def read_group():
    with open('group.csv', 'r') as rg_f:
        reader = csv.reader(rg_f)
        for row in reader:
            listbox.insert(END, '  ' + row[0], '⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯%s⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯' % row[2])


def show_msg(update_time):
    # Receive MSG........................
    try:
        my_pop.receive_msg(update_time)
        with open('msg.csv', 'r') as rmsg:
            reader = csv.reader(rmsg)
            for row in reader:
                msg_from = '   ' + row[1] + '：'
                msg_text = row[4]
                for ms in msg_text:
                    msg_from += ms
                    if len(msg_from) == 18:
                        sh_listbox.insert(END, msg_from)
                        msg_from = '   '
                sh_listbox.insert(END, msg_from, '')
                sh_listbox.yview_moveto(1)

    except socket.gaierror:
        sh_listbox.insert(END, '%s----No Internet----' % (' ' * 45), '')
        sh_listbox.yview_moveto(1)

    new_time = time.time()
    list_time.append(new_time)


def sent_typing(*args):
    mine = '%s子闲：' % (' ' * 66)
    my_text = typing.get()
    typing.delete(0, END)

    # Sent MSG........................
    try:
        my_smtp.sent_mail(my_text, '子闲')
        for m in my_text:
            mine += m
            if len(mine) == 81:
                sh_listbox.insert(END, mine)
                mine = ' ' * 66

        sh_listbox.insert(END, mine, '')
        sh_listbox.yview_moveto(1)

    except socket.gaierror:
        sh_listbox.insert(END, '%s----No Internet----' % (' ' * 45), '')
        sh_listbox.yview_moveto(1)


def chatting():
    global entry_add
    global entry_nick
    global listbox
    global sh_listbox
    global typing

    size_ch = HEIGHT, WIDTH = 460, 810

    ch_window = tk.Tk()
    ch_window.title('Chatooling')

    # initial size
    canvas = tk.Canvas(ch_window, height=HEIGHT, width=WIDTH)
    canvas.pack()

    # ----------- Function Area ------------
    func_frame = tk.Frame(ch_window, bg='#1a1a1a')
    func_frame.place(relx=0, rely=0, relwidth=0.09, relheight=1)
    cat_image = tk.PhotoImage(file='/Users/soul/Desktop/2.png')
    head_label = tk.Label(func_frame, image=cat_image)
    head_label.place(relx=0.15, rely=0.03, relwidth=0.7, relheight=0.11)

    zone_frame = tk.Frame(func_frame, bg='#404040')
    zone_frame.place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.33)

    film_button = tk.Button(
        zone_frame, text='_Film', bg='#1a1a1a', command=lambda: film_win.my_film())
    film_button.place(relx=0.1, rely=0.08, relwidth=0.8, relheight=0.18)

    arch_button = tk.Button(
        zone_frame, text='_Arch', bg='#1a1a1a', command=lambda: print('arch'))
    arch_button.place(relx=0.1, rely=0.34, relwidth=0.8, relheight=0.18)

    Hip_Dict_button = tk.Button(
        zone_frame, text='_Dict', bg='#1a1a1a', command=lambda: print('Hip_Dict'))
    Hip_Dict_button.place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.18)

    # ----------- Group Area ------------
    gp_frame = tk.Frame(ch_window, bg='#f2f2f2')
    gp_frame.place(relx=0.09, rely=0, relwidth=0.3, relheight=1)

    # Add Member Email
    add_frame = tk.Frame(gp_frame, bg='#c2d6d6')
    add_frame.place(relx=0.05, rely=0.03, relwidth=0.9, relheight=0.07)
    label_add = tk.Label(add_frame, text='+Mail:', bg='#c2d6d6')
    label_add.place(relx=0.01, rely=0.12, relwidth=0.2, relheight=0.8)
    entry_add = tk.Entry(add_frame)
    entry_add.place(relx=0.21, rely=0.1, relwidth=0.78, relheight=0.8)

    # Add Member Nick Name
    nick_frame = tk.Frame(gp_frame, bg='#c2d6d6')
    nick_frame.place(relx=0.05, rely=0.14, relwidth=0.9, relheight=0.07)
    label_nick = tk.Label(nick_frame, text='+Nick:', bg='#c2d6d6')
    label_nick.place(relx=0.01, rely=0.12, relwidth=0.2, relheight=0.8)
    entry_nick = tk.Entry(nick_frame)
    entry_nick.place(relx=0.21, rely=0.1, relwidth=0.45, relheight=0.8)
    add_button = tk.Button(
        nick_frame, text='>_ Add', bg='#c2d6d6', command=lambda: add_group(entry_nick.get(), entry_add.get(), 0))
    add_button.place(relx=0.68, rely=0.1, relwidth=0.3, relheight=0.8)

    # Show Group Member
    group_frame = tk.Frame(gp_frame, bg='#c2d6d6', bd=10)
    group_frame.place(relx=0.05, rely=0.26, relwidth=0.9, relheight=0.69)

    scroll = Scrollbar(group_frame)
    scroll.place(relx=0, rely=0, relwidth=0.04, relheight=1)

    listbox = tk.Listbox(group_frame, yscrollcommand=scroll.set)
    listbox.place(relx=0.04, rely=0, relwidth=0.96, relheight=1)
    read_group()

    scroll.config(command=listbox.yview)

    # ----------- Chatting Area ------------
    # Showing Frame............
    start_time = time.time()
    list_time.append(start_time)

    sh_frame = tk.Frame(ch_window, bg='#e6e6e6')
    sh_frame.place(relx=0.39, rely=0, relwidth=0.61, relheight=0.65)

    sh_scroll = Scrollbar(sh_frame)
    sh_scroll.place(relx=0.97, rely=0.02, relwidth=0.02, relheight=0.98)

    sh_listbox = tk.Listbox(sh_frame, yscrollcommand=sh_scroll.set)
    sh_listbox.place(relx=0.01, rely=0.02, relwidth=0.96, relheight=0.98)
    sh_scroll.config(command=sh_listbox.yview)

    # Typing Frame.............
    typing_frame = tk.Frame(ch_window, bg='#e6e6e6')
    typing_frame.place(relx=0.39, rely=0.65, relwidth=0.61, relheight=0.35)
    typing = Entry(typing_frame, font=('宋体', 16))
    typing.bind('<Return>', sent_typing)
    typing.place(relx=0.01, rely=0.23, relwidth=0.98, relheight=0.7)
    sent_button = tk.Button(
        typing_frame, text='@_Sent', bg='#c2d6d6', command=lambda: sent_typing())
    sent_button.place(relx=0.85, rely=0.03, relwidth=0.14, relheight=0.17)

    receive_button = tk.Button(
        typing_frame, text='Receive', bg='#c2d6d6', command=lambda: show_msg(list_time[-1]))
    receive_button.place(relx=0.01, rely=0.03, relwidth=0.14, relheight=0.17)

    # ----------- Run ------------
    ch_window.mainloop()
