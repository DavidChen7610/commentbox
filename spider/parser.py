# coding=utf-8
from datetime import datetime
import time

from mongoengine.connection import disconnect

from models import Artist, Song, Comment, User, Process, BeReplied
from app import create_app

from spider.utils import get_user_agent, get_tree, post

DISCOVER_URL = 'http://music.163.com/discover/artist/cat?id={}&initial={}'
ARTIST_URL = 'http://music.163.com/artist?id={}'
SONG_URL = 'http://music.163.com/song?id={}'
COMMENTS_URL = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}'  # noqa

# =========================
HOME_URL = 'http://music.163.com/#/user/home?id={}'
PLAYLIST_URL = 'http://music.163.com/playlist?id={}'


# 评论完整API before_time=0 获取最新时间 limit=100 返回100条 默认时间降序(从新到旧)
# COMMENTS_URL_ = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?limit=100&before_time={}' \
#                 '&compareUserLocation=true&commentId=0&composeConcert=true'


def parser_artist_list(cat_id, initial_id):
    tree = get_tree(DISCOVER_URL.format(cat_id, initial_id))
    artist_items = tree.xpath('//a[contains(@class, "nm-icn")]/@href')

    return [item.split('=')[1] for item in artist_items]


def unprocess_artist_list():
    create_app()
    unprocess = Process.objects.filter(status=Process.PENDING)
    return [p.id for p in unprocess]


def parser_artist(artist_id):
    create_app()
    process = Process.get_or_create(id=artist_id)
    if process.is_success:
        return

    print 'Starting fetch artist: {}'.format(artist_id)
    start = time.time()
    process = Process.get_or_create(id=artist_id)

    tree = get_tree(ARTIST_URL.format(artist_id))

    artist = Artist.objects.filter(id=artist_id)
    if not artist:
        artist_name = tree.xpath('//h2[@id="artist-name"]/text()')[0]
        picture = tree.xpath(
            '//div[contains(@class, "n-artist")]//img/@src')[0]
        artist = Artist(id=artist_id, name=artist_name, picture=picture)
        artist.save()
    else:
        artist = artist[0]
    song_items = tree.xpath('//div[@id="artist-top50"]//ul/li/a/@href')
    songs = []
    for item in song_items:
        song_id = item.split('=')[1]
        song = parser_song(song_id, artist)
        if song is not None:
            songs.append(song)
    artist.songs = songs
    artist.save()
    process.make_succeed()
    print 'Finished fetch artist: {} Cost: {}'.format(
        artist_id, time.time() - start)


def parser_song(song_id, artist):
    tree = get_tree(SONG_URL.format(song_id))
    song = Song.objects.filter(id=song_id)
    # r = post(COMMENTS_URL.format(song_id), "")
    # if r.status_code != 200:
    #     print 'API Error: Song {}'.format(song_id)
    #     return
    # data = r.json()
    if not song:
        for404 = tree.xpath('//div[@class="n-for404"]')
        if for404:
            return

        try:
            song_name = tree.xpath('//em[@class="f-ff2"]/text()')[0].strip()
        except IndexError:
            try:
                song_name = tree.xpath(
                    '//meta[@name="keywords"]/@content')[0].strip()
            except IndexError:
                print 'Fetch limit!'
                time.sleep(10)
                return parser_song(song_id, artist)
        song = Song(id=song_id, name=song_name, artist=artist)  # comment_count=data['total']
        song.save()
    else:
        song = song[0]
    # comments = []
    # for comment_ in data['hotComments']:
    #     comment_id = comment_['commentId']
    #     content = comment_['content']
    #     like_count = comment_['likedCount']
    #     user = comment_['user']
    #     if not user:
    #         continue
    #     user = User.get_or_create(id=user['userId'], name=user['nickname'],
    #                               picture=user['avatarUrl'])
    #     comment = Comment.get_or_create(id=comment_id, content=content,
    #                                     like_count=like_count, user=user,
    #                                     song=song)
    #     comment.save()
    #     comments.append(comment)
    # song.comments = comments
    # song.save()
    # time.sleep(1)
    return song


# =========================
# 用户主页暂时不能爬取(主要歌单部分是iframe name="contentFrame"动态请求API加载的[因API-post参数是Token暂无法获取])
def parser_playlist_list(user_id):
    tree = get_tree(HOME_URL.format(user_id))
    artist_items = tree.xpath('//a[contains(@class, "msk")]/@href')

    return [item.split('=')[1] for item in artist_items]


def unprocess_playlist_list():
    create_app()
    unprocess = Process.objects.filter(status=Process.PENDING)
    return [p.id for p in unprocess]


# 爬取歌单数据
def parser_playlist(playlist_id):
    create_app()
    # process = Process.get_or_create(id=playlist_id)
    # if process.is_success:
    #     return

    print 'Starting parser_playlist playlist_id: {}'.format(playlist_id)
    start = time.time()
    process = Process.get_or_create(id=playlist_id)

    tree = get_tree(PLAYLIST_URL.format(playlist_id))

    artist = Artist.objects.filter(id=playlist_id)
    if not artist:
        playlist_name = tree.xpath('//h2[@class="f-ff2 f-brk"]/text()')[0]
        print 'playlist_name: ' + playlist_name
        picture = tree.xpath(
            '//div[contains(@class, "cover u-cover u-cover-dj")]//img/@src')[0]
        artist = Artist(id=playlist_id, name=playlist_name, picture=picture)
        artist.save()
    else:
        artist = artist[0]
    song_items = tree.xpath('//div[@id="song-list-pre-cache"]//a/@href')
    songs = []
    for item in song_items:
        song_id = item.split('=')[1]
        song = parser_song(song_id, artist)
        parser_comments(song, 0)
        if song is not None:
            songs.append(song)
    artist.songs = songs
    artist.save()
    process.make_succeed()
    print 'Finished parser_playlist playlist_id: {} Cost: {}'.format(
        playlist_id, time.time() - start)


# 爬取指定song的所有评论
def parser_comments(song, before_time):
    print 'Starting parser_comments song_id: {}'.format(song.id)
    print 'song_name: ' + song.name
    start = time.time()

    params = {"limit": "30", "compareUserLocation": "true", "beforeTime": before_time, "composeConcert": "true",
              "commentId": "0"}
    r = post(COMMENTS_URL.format(song.id), params)
    if r.status_code != 200:
        print 'API Error: Song {}'.format(song.id)
        return
    data = r.json()

    comments = []
    for comment_ in data['comments']:
        comment_id = comment_['commentId']
        # 检测数据库中是否已存在当前获取的最新评论
        comment = Comment.objects.filter(id=comment_id)
        if comment:
            return
        content = comment_['content']
        like_count = comment_['likedCount']
        user = comment_['user']
        timestamp = comment_['time']

        be_replied = comment_['beReplied']  # 当前评论所回复的评论
        if be_replied:
            for replied in be_replied:
                content_ = replied['content']
                user_ = replied['user']
                if not user_:
                    continue
                user_ = User.get_or_create(id=user_['userId'], name=user_['nickname'],
                                           picture=user_['avatarUrl'])
                be_replied_db = BeReplied.get_or_create(id=comment_id, content=content_, user=user_)
                be_replied_db.save()

        if not user:
            continue
        user = User.get_or_create(id=user['userId'], name=user['nickname'],
                                  picture=user['avatarUrl'])
        date_time = datetime.fromtimestamp(timestamp / 1000)  # 去除时间戳后三位(可能是时区)
        comment = Comment.get_or_create(id=comment_id, content=content, timestamp=timestamp,
                                        time=date_time, like_count=like_count, user=user, be_replied=len(be_replied))
        comment.save()
        comments.append(comment)
    song.comments = comments
    song.save()

    if data['more']:
        time.sleep(1)  # 休息休息
        parser_comments(song, comments.__getitem__(len(comments) - 1).timestamp)
    else:
        print 'Finished parser_comments song_id: {} Cost: {}'.format(song.id, time.time() - start)


def parser_test(song_id):
    create_app()

    song = Song.objects.filter(id=song_id)
    song = Song(id=song_id, name='test')
    parser_comments(song_id, 0, song)
