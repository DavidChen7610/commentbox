import itertools

# 多进程多线程统一接口，选择多线程方便调试
# concurrent的executor会catch到线程里的错误，对调试不方便
# from concurrent.futures import ProcessPoolExecutor
# from concurrent.futures import ThreadPoolExecutor as ProcessPoolExecutor

from spider.parser import (parser_artist_list, parser_artist, unprocess_artist_list)

# CAT_IDS = [1001, 1002, 1003, 2001, 2002, 2003, 4001, 4002, 4003, 6001, 6002, 6003, 7001, 7002, 7003]  # 歌手地区分类
# INITIAL_IDS = [0, -1] + list(range(65, 91))  # 歌手姓名按字母分类

# with ProcessPoolExecutor(max_workers=1) as executor:
#     for artist_id in unprocess_artist_list():
#         print(artist_id)
#         executor.submit(parser_artist, artist_id)

#     for product in itertools.product(CAT_IDS, INITIAL_IDS):
#         for artist_id in parser_artist_list(*product):
#             executor.submit(parser_artist, artist_id)

# 下面是单线程选取2个歌手进行调试
CAT_IDS = [1001]
INITIAL_IDS = [0]

for product in itertools.product(CAT_IDS, INITIAL_IDS):
    for i, artist_id in enumerate(parser_artist_list(*product)):
        if i > 1:
            break

        print(artist_id)
        parser_artist(artist_id)
