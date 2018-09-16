"""
功能：抓取每首歌的精彩(热点)评论
demo url: https://music.163.com/#/song?id=188175
demo params: 在网页中直接拿下来用
demo encSecKey: 在网页中直接拿下来用
"""

import requests
import json


def get_url(url):

    name_id = url.split('=')[1]
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'
        # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'  # noqa
    }

    params = 'uxgiEGvWsslBNX4izrGy9247Sshe4KvMhc2abtTjSE+9A2p/GgZM1gv0LPMWnwH1EntQlLUHa+UFxjRyc0DsGSVsMzmY07pHMIMvxnPojCU8f1IokaYb8I8+TtE4sIB7DK+/iXo2QuheOph791SYiYwb+UkvJmJctiYB2TD7cFpDVHsZY2OMQzYnAfjgZpCm'  # noqa
    encSecKey = '00b33844f56ba0c7db395b74e6c945a0155a9e88b6ec55a1c80d00ae7b201d3d02b7511e8a3172f56b0d70d7bd9514690782834423d91638e1096741f9f83dbdda47eec8740df95a915e5d424efab65bb89731e36f23ac2e892b3ce04864802ecb097ea9d3ac26540b2ba19882272878a537f70a2f42bae9952bdfa47dd2e1d6'  # noqa
    data = {'params': params, 'encSecKey': encSecKey}

    target_url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token='.format(name_id)
    response = requests.post(target_url, headers=headers, data=data)

    return response


def get_comment(response):
    comment_json = json.loads(response.text)
    hot_comment = comment_json['hotComments']

    with open('music_hot_comment.txt', 'w', encoding='utf-8') as f:
        for each in hot_comment:
            f.write(each['user']['nickname'] + ':\n\n')
            f.write(each['content'] + '\n')
            f.write('==================' + '\n')


def main():
    url = input('请输入音乐的链接: ')
    response = get_url(url)
    get_comment(response)


if __name__ == '__main__':
    main()
