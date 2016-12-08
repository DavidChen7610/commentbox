from concurrent.futures import ProcessPoolExecutor

from spider.parser import (
    parser_playlist_list, parser_playlist, unprocess_playlist_list)

# USER_ID = [97348077, 58350079]
# USER_ID = 97348077
PLAYLIST_ID = 114973874

# parser_playlist_list(USER_ID)
# parser_playlist(PLAYLIST_ID)

with ProcessPoolExecutor(max_workers=16) as executor:
    executor.submit(parser_playlist, PLAYLIST_ID)

    # for playlist_id in unprocess_playlist_list():
    #     executor.submit(parser_playlist, playlist_id)
    #
    # for playlist_id in parser_playlist_list(USER_ID):
    #     executor.submit(parser_playlist, playlist_id)
