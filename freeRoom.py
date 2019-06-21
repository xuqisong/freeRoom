#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:xxx time:2019/6/18
import os
import re
import time

import requests
from bs4 import BeautifulSoup



head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'
}

def get_page(url):
    req = requests.get(url=url,headers=head)
    if req.status_code == 200:
        res = req.text
        return res
    else:
        return None


def parser_page():
    num = 1
    base_url = "https://findlifee.com/page_{}.html"

    flag = True
    while flag:
        url1 = base_url.format(str(num))
        print('第一层：',url1)
        html = get_page(url1)
        num += 1
        soup1 = BeautifulSoup(html, 'lxml')
        fr = soup1.findAll(class_="list-tu")
        for child in fr:
            href = child['href']
            title = child['title']
            print('第二层：',href)
            html = get_page(href)
            soup = BeautifulSoup(html,'lxml')
            img_list = soup.findAll(class_="info-zi")
            # print(img_list)
            for img in img_list:
                child_img = img.contents
                child2 = child_img[1].contents
                if len(child2) > 3:
                    for a in child2:
                        get_three(a,title)

                else:
                    for a in child_img:
                        get_three(a,title)



        next_page_list = soup1.findAll(class_="page")
        flag = re.search('›',str(next_page_list))
        print(flag)


def get_three(a,title):
    pattern = re.compile('<img\salt=\".*?\".*?src=\"(.*?)\"/>')
    result = re.search(pattern, str(a))
    if result is not None:
        img_url = result.groups(1)[0]
        print('第三层: ', img_url)
        save_img(img_url, title)
    else:
        print('--- --- ')

        # print(items)


def save_img(url,title):
    req = requests.get(url=url,headers= head).content
    path = 'img/{}'.format(title)
    setup_download_dir(path)
    with open(os.path.join(path,title+str(time.time())+'.jpg'),'wb')as fw:
        fw.write(req)

def setup_download_dir(directory):
    """ 设置文件夹，文件夹名为传入的 directory 参数，若不存在会自动创建 """
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as e:
            pass
    return True


if __name__ == '__main__':
    items = parser_page()


