import csv
# import time
import random

import re
import json
from requests_html import HTMLSession
from pprint import pprint


session = HTMLSession()


def get_film(kind):
    global list_films

    list_films = []
    my_max = 128
    my_start = (random.randint(0, my_max)) * 20
    # print(my_start)
    # print(kind)

    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'
    data = {'sort': 'U',
            'range': '0,10',
            'tags': '电影',
            'start': my_start,
            'genres': kind}
    r = session.get('https://movie.douban.com/j/new_search_subjects?', headers={'user-agent': ua}, params=data)
    result = json.loads(r.html.html)

    for i in list(range(0, 20)):
        star = result['data'][i]['star']

        if int(star) >= 20:
            # pprint(result['data'][i])
            film = result['data'][i]['title']
            cover = result['data'][i]['cover']
            f_url = result['data'][i]['url']

            list_films.append([film, cover, f_url])


def run_spider(my_kind):
    # print(my_kind)
    try:
        get_film(my_kind)

    except IndexError:
        pass
    except KeyError:
        pass

    if list_films:
        with open('/Users/soul/PycharmProjects/Chat/tk_chatool/film_func/film_files/%s.csv' % my_kind,
                  'w', newline='') as file:
            writer = csv.writer(file)
            for f in list_films:
                writer.writerow(f)


def new_film():
    list_np = []
    list_uc = []
    list_hot = []
    p = 0
    u = 0

    r_new = session.get('https://movie.douban.com/cinema/nowplaying/beijing/')
    new_result = r_new.html

    comp = re.compile(r'[\u4E00-\u9FA5]+')
    patt = re.compile(r'https://movie.douban.com/subject.*?poster')
    pat = re.compile(r'https.*?jpg')

    # ----------- Now Playing ------------
    now_playing = new_result.find('div#nowplaying img')
    now_playing_u = new_result.find('div#nowplaying a.ticket-btn')

    for np in patt.findall(str(now_playing_u)):
        if p == 0:
            list_np.append(np)
            p = 1
        elif p == 1:
            p = 0

    for np_img, np_url in zip(now_playing, list_np):
        now_playing_text = comp.findall(str(np_img))[0]
        now_playing_img = pat.findall(str(np_img))[0]

        list_hot.append([now_playing_text, now_playing_img, np_url])

    with open('/Users/soul/PycharmProjects/Chat/tk_chatool/film_func/film_files/%s.csv' % '热映',
              'w', newline='') as file:
        writer = csv.writer(file)
        for row in list_hot:
            writer.writerow(row)

    # ----------- Upcoming ------------
    upcoming = new_result.find('div#upcoming img')
    upcoming_u = new_result.find('div#upcoming a')

    for uc in patt.findall(str(upcoming_u)):
        if u == 0:
            list_uc.append(uc)
            u = 1
        elif u == 1:
            u = 0

    with open('/Users/soul/PycharmProjects/Chat/tk_chatool/film_func/film_files/%s.csv' % '即将',
              'w', newline='') as file:
        writer = csv.writer(file)
        for uc_img, uc_url in zip(upcoming, list_uc):
            upcoming_text = comp.findall(str(uc_img))[0]
            upcoming_img = pat.findall(str(uc_img))[0]

            writer.writerow([upcoming_text, upcoming_img, uc_url])


'''def all_video(that_name, that_link):
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'
    data = {'wd': that_name}
    patall = re.compile(r'/show-.*?html')
    patsecond = re.compile(r'/play/.*?html')
    r_all = session.post('https://www.qsptv.com/search/', headers={'user-agent': ua}, params=data)
    all_result = r_all.html.html
    # pprint(all_result)
    link_list = patall.findall(all_result)
    if link_list:
        second_link = 'https://www.qsptv.com'+link_list[0]
        r_watch_2 = session.get(second_link)
        watch_result_2 = r_watch_2.html
        # pprint(watch_result_2)
        watching_2 = watch_result_2.find('div.playlist a')
        # print(watching_2)
        watching_link_2 = patsecond.findall(str(watching_2[0]))
        # print(watching_link_2)
        if watching_link_2:
            that_link.append('https://www.qsptv.com' + watching_link_2[0])'''


def get_watch(the_name):
    the_link = []
    bili = 0
    r_watch = session.get('https://so.iqiyi.com/so/q_%s?' % the_name)
    watch_result = r_watch.html

    pattt = re.compile(r'http://www.iqiyi.com/v_19rr.*?html')
    patttt = re.compile(r'https://www.bilibili.com/bangumi/play.*?from=search')
    patyk = re.compile(r'http://v.youku.com/v_show/id_.*?html')

    # ----------- Watching Link ------------
    watching = watch_result.find('div.result-right')
    result_btn = watching[0].find('a.qy-search-result-btn')
    if result_btn:
        link = result_btn[0].links
        watching_link = pattt.findall(str(link))
        if watching_link:
            the_link.append(watching_link[0])

    '''if not the_link:
        all_video(the_name, the_link)'''

    '''if not the_link:
        r_watch_1 = session.get('https://search.bilibili.com/all?keyword=%s' % the_name)
        watch_result_1 = r_watch_1.html
        # pprint(watch_result_1)
        watching_1 = watch_result_1.find('div.right-info')
        for wa in watching_1:
            wat = wa.find('span.pgc-label')
            if wat:
                wat_n = watch_result_1.find('em.keyword')[bili].text
                # print(bili)
                # print(wat_n)
                if wat_n == the_name:
                    watching_link_1 = patttt.findall(str(wa.find('a')[bili]))
                    # print(watching_link_1)
                    if watching_link_1:
                        the_link.append(watching_link_1[0])

            bili += 1'''

    if not the_link:
        left = watch_result.find('a.qy-mod-link')
        for nine, le in zip(range(9), left):
            lab = le.find('span.qy-mod-label')
            if lab:
                # print(lab[0].text)
                if len(lab[0].text) > 5:
                    the_link.append(str(le.links)[2:-2])
                    # print(str(le.links)[2:-2])
                    break
        '''for you in watching:
            youku = patyk.findall(str(you.find('a.main-tit')))
            if youku:
                the_link.append(youku[0])
                break'''

    if the_link:
        # print(the_link[0])
        return the_link[0]


# get_watch('军火贩')
