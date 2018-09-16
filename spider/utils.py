import random

import requests
from lxml import etree
from fake_useragent import UserAgent

from spider.encrypt import gen_data
from config import PROXIES


TIMEOUT = 5


def choice_proxy():
    if PROXIES:
        return random.choice(PROXIES + [''])
    return ''


def get_user_agent():
    ua = UserAgent()
    return ua.random


def fetch(url, retry=0):
    s = requests.Session()
    proxies = {
        'http': choice_proxy()
    }
    s.headers.update({'user-agent': get_user_agent(),
                      'referer': 'http://music.163.com/'})
    try:
        return s.get(url, timeout=TIMEOUT, proxies=proxies)
    except requests.exceptions.RequestException:
        if retry < 3:
            return fetch(url, retry=retry + 1)
        raise


def post(url):
    # headers = {
    #     'Cookie': 'appver=1.5.0.75771;',
    #     'Referer': 'http://music.163.com/'
    # }

    headers = {
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'  # noqa
    }

    return requests.post(url, headers=headers, data=gen_data())


def get_tree(url):
    # import re
    # import os

    r = fetch(url)
    # pat = re.compile('com/([a-z]+)\W')
    # fileName = os.path.join(os.getcwd(), 'html', pat.findall(url)[0] + ".html")
    # with open(fileName, 'w') as f:
    #     f.write(r.text)

    return etree.HTML(r.text)
