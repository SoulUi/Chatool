import csv
import tkinter as tk

import login_win


# ----------- Save User Info ------------
def save_info(nick, email, password):
    with open('user_info.csv', 'a', newline='') as ui_file:
        writer = csv.writer(ui_file)
        writer.writerow([nick, email, password])

    su_window.destroy()
    login_win.login()


def signup():
    global su_window
    # ----------- Create Sign Up Window ------------
    size_su = HEIGHT, WIDTH = 600, 320

    su_window = tk.Tk()
    su_window.title('Chatool SignUp')

    # initial size
    canvas = tk.Canvas(su_window, height=HEIGHT, width=WIDTH)
    canvas.pack()

    truck_image = tk.PhotoImage(file='/Users/soul/PycharmProjects/Chat/tk_chatool/truck.png')
    truck_label = tk.Label(su_window, image=truck_image)
    truck_label.place(x=0, y=0, relwidth=1, relheight=0.47)

    # ----------- Nick Name Area ------------
    nick_frame = tk.Frame(su_window, bg='#c2d6d6')
    nick_frame.place(relx=0.1, rely=0.42, relwidth=0.8, relheight=0.07)
    label_nick = tk.Label(nick_frame, text='Nick:', bg='#c2d6d6')
    label_nick.place(relx=0, rely=0.12, relwidth=0.18, relheight=0.8)
    entry_nick = tk.Entry(nick_frame)
    entry_nick.place(relx=0.18, rely=0.1, relwidth=0.8, relheight=0.8)

    # ----------- User Email Area ------------
    user_frame = tk.Frame(su_window, bg='#c2d6d6')
    user_frame.place(relx=0.1, rely=0.54, relwidth=0.8, relheight=0.07)
    label_user = tk.Label(user_frame, text='Mail:', bg='#c2d6d6')
    label_user.place(relx=0, rely=0.12, relwidth=0.18, relheight=0.8)
    entry_user = tk.Entry(user_frame)
    entry_user.place(relx=0.18, rely=0.1, relwidth=0.8, relheight=0.8)

    # ----------- Password Area ------------
    pass_frame = tk.Frame(su_window, bg='#c2d6d6')
    pass_frame.place(relx=0.1, rely=0.66, relwidth=0.8, relheight=0.07)
    label_pass = tk.Label(pass_frame, text='Pass:', bg='#c2d6d6')
    label_pass.place(relx=0, rely=0.12, relwidth=0.18, relheight=0.8)
    entry_pass = tk.Entry(pass_frame)
    entry_pass.place(relx=0.18, rely=0.1, relwidth=0.8, relheight=0.8)

    # ----------- Sign Up Button ------------
    su_button = tk.Button(
        su_window, text='Sign Up', bg='#c2d6d6',
        command=lambda: save_info(entry_nick.get(), entry_user.get(), entry_pass.get()))
    su_button.place(relx=0.3, rely=0.8, relwidth=0.4, relheight=0.07)

    # ----------- Run ------------
    su_window.mainloop()
