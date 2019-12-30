# from gevent import monkey
# monkey.patch_all()
# import gevent

import csv
import time
import types
import random
# import schedule
import tkinter as tk
import webbrowser

import requests
from PIL import Image, ImageTk
from io import BytesIO

from film_func import film_spider

size_film = F_HEIGHT, F_WIDTH = 540, 760
kind_list = ['Comedy', 'Act', 'Love', 'Sci', 'Cartoon', 'Detect', 'Thriller']
kind_dict = {'Hot': '热映', 'Upto': '即将', 'Want': '想看', 'Comedy': '喜剧', 'Act': '动作', 'Love': '爱情',
             'Sci': '科幻', 'Cartoon': '动画', 'Detect': '悬疑', 'Thriller': '惊悚'}


def resize(image_url):
    # Box Size
    w_box = 120
    h_box = 330

    try:
        url = image_url
        res = requests.get(url)
        pil_image = Image.open(BytesIO(res.content))
        # get the size of the image
        # 获取图像的原始大小
        w, h = pil_image.size

        f1 = 1.0 * w_box / w  # 1.0 forces float division in Python2
        f2 = 1.0 * h_box / h
        factor = min([f1, f2])
        # print(f1, f2, factor) # test
        # use best down-sizing filter
        width = int(w * factor)
        height = int(h * factor)
        return pil_image.resize((width, height), Image.ANTIALIAS)

    except OSError:
        pass
    except KeyError:
        pass
    except AttributeError:
        pass
    except requests.exceptions.ConnectionError:
        pass


class Btn:
    def __init__(self, my_frame, my_x, my_y, row):
        self.row = row

        self.sub_frame = tk.Frame(my_frame, bg='#e6e6ff')
        self.sub_frame.place(relx=my_x, rely=my_y, relwidth=0.176, relheight=0.46)

        try:
            self.tk_image = ImageTk.PhotoImage(resize(row[1]))
            head_label = tk.Label(self.sub_frame, image=self.tk_image)
            head_label.place(relx=0, rely=0, relwidth=1, relheight=0.8)
        except AttributeError:
            pass
        except KeyError:
            pass

        film_info = tk.Label(self.sub_frame, text=row[0], bg='#c2d6d6')
        film_info.place(relx=0, rely=0.8, relwidth=1, relheight=0.1)

        '''if strategy:
            self.like_btn = types.MethodType(strategy, self)'''

    def no_watch(self):
        no_label = tk.Label(self.sub_frame, text='None', bg='#c2c2d6')
        no_label.place(relx=0.5, rely=0.9, relwidth=0.5, relheight=0.1)

    def watch_btn(self):
        open_button = tk.Button(self.sub_frame, text='Watch', bg='#c2d6d6',
                                command=lambda: self.open_watch())
        open_button.place(relx=0.5, rely=0.9, relwidth=0.5, relheight=0.1)

    def open_watch(self):
        webbrowser.open(self.row[3])

    def dou_btn(self):
        open_button = tk.Button(self.sub_frame, text='Dou', bg='#c2d6d6',
                                command=lambda: self.open_web())
        open_button.place(relx=0.5, rely=0.9, relwidth=0.5, relheight=0.1)

    def open_web(self):
        webbrowser.open(self.row[2])

    def like_btn(self):
        like_button = tk.Button(self.sub_frame, text='Like', bg='#c2d6d6',
                                command=lambda: self.like())
        like_button.place(relx=0, rely=0.9, relwidth=0.5, relheight=0.1)

    def unlike_btn(self):
        unlike_button = tk.Button(self.sub_frame, text='Unlike', bg='#c2d6d6',
                                  command=lambda: self.unlike())
        unlike_button.place(relx=0, rely=0.9, relwidth=0.5, relheight=0.1)

    def like(self):
        watch_link = film_spider.get_watch(self.row[0])
        # print(watch_link)
        if watch_link is not None:
            new_row = [self.row[0], self.row[1], self.row[2], watch_link]
            # print(new_row)
        else:
            new_row = self.row

        with open('/Users/soul/PycharmProjects/Chat/tk_chatool/film_func/film_files/%s.csv' % '想看',
                  'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(new_row)

        self.unlike_btn()

    def unlike(self):
        list_mine = []
        with open('/Users/soul/PycharmProjects/Chat/tk_chatool/film_func/film_files/%s.csv' % '想看',
                  'r') as my_file:
            reader = csv.reader(my_file)
            for my_row in reader:
                list_mine.append(my_row)

        if self.row in list_mine:
            list_mine.remove(self.row)
            with open('/Users/soul/PycharmProjects/Chat/tk_chatool/film_func/film_files/%s.csv' % '想看',
                      'w', newline='') as new_file:
                writer = csv.writer(new_file)
                for row in list_mine:
                    writer.writerow(row)
        else:
            pass

        self.like_btn()
        self.dou_btn()


class Label:
    def __init__(self, color, my_x, my_text):
        self.no = 0
        self.color = color
        self.text = my_text
        label = tk.Frame(film_window, bg=self.color)
        label.place(relx=my_x, rely=0.05, relwidth=0.15, relheight=0.05)

        my_button = tk.Button(label, text=self.text, bg=color, command=lambda: self.act())
        my_button.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.7)

    def act(self):
        list_mine = []
        # print(self.text)
        if self.text in kind_list and self.no == 0:
            # print('spider')
            # get different kinds of films
            try:
                film_spider.run_spider(kind_dict[self.text])
            except OSError:
                pass

        self.no += 1

        list_read = []
        my_x = 0.02
        my_y = 0.026
        my_frame = tk.Frame(film_window, bg=self.color)
        my_frame.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.85)
        with open('/Users/soul/PycharmProjects/Chat/tk_chatool/film_func/film_files/%s.csv' % kind_dict[self.text],
                  'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if not row:
                    self.no = 0
                film_name = row[0]
                film_cover = row[1]
                film_url = row[2]
                list_read.append(row)

        if len(list_read) > 10:
            list_read = random.sample(list_read, 10)

        for read in list_read:
            with open('/Users/soul/PycharmProjects/Chat/tk_chatool/film_func/film_files/%s.csv' % '想看',
                      'r') as my_file:
                reader = csv.reader(my_file)
                for my_row in reader:
                    list_mine.append(my_row)

            if read in list_mine:
                btn = Btn(my_frame, my_x, my_y, read)
                btn.unlike_btn()
                if len(read) == 4:
                    btn.watch_btn()
                else:
                    btn.no_watch()
            else:
                btn = Btn(my_frame, my_x, my_y, read)
                btn.like_btn()
                btn.dou_btn()

            if my_x < 0.8:
                my_x += 0.196
            else:
                my_x = 0.02
                my_y = 0.513


def routine():
    # print('routine')
    try:
        film_spider.new_film()

    except OSError:
        pass


def my_film():
    global film_window
    film_window = tk.Toplevel()
    film_window.title('Film Function')

    # initial size
    film_canvas = tk.Canvas(film_window, height=F_HEIGHT, width=F_WIDTH)
    film_canvas.pack()

    with open('today.csv', 'r') as today:
        reader = csv.reader(today)
        for row in reader:
            my_time = row[0]

    time_str = time.strftime('%Y-%m-%d', time.localtime())
    if my_time != time_str:
        try:
            film_spider.new_film()

        except OSError:
            pass

        with open('today.csv', 'w', newline='') as today:
            writer = csv.writer(today)
            writer.writerow([time_str])

    # schedule.every().day.do(routine)  # ?? Is this ever Run
    # schedule.run_pending()

    # ----------- Labels ------------
    three = random.sample(kind_list, 3)
    hot = Label(color='#ff9999', my_x=0.05, my_text='Hot')
    hot.act()
    upcoming = Label(color='#ffcc99', my_x=0.2, my_text='Upto')
    want = Label(color='#99ffe6', my_x=0.35, my_text='Want')

    kind_1 = Label(color='#99e6ff', my_x=0.5, my_text=three[0])
    kind_2 = Label(color='#99bbff', my_x=0.65, my_text=three[1])
    kind_3 = Label(color='#b399ff', my_x=0.8, my_text=three[2])

    # ----------- Run ------------
    film_window.mainloop()
