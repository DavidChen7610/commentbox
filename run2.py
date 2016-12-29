import itertools
from concurrent.futures import ProcessPoolExecutor

from spider.parser import (
    parser_playlist, parser_song_comments)


# SONG_IDS = [29850531, 431357712]
SONG_IDS = [287063, 344384, 31284040, 431357712, 27955653, 29814898, 29567185, 202377]

with ProcessPoolExecutor(max_workers=16) as executor:
    # executor.submit(parser_playlist, PLAYLIST_ID)
    # executor.submit(parser_test, SONG_ID)

    # for playlist_id in unprocess_playlist_list():
    #     executor.submit(parser_playlist, playlist_id)
    #
    for song_id in itertools.product(SONG_IDS):
        executor.submit(parser_song_comments, song_id)
