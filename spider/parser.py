import time

from mongoengine.connection import disconnect

from models import Artist, Song, Comment, User, Process
from app import create_app

from spider.utils import get_tree, post

DISCOVER_URL = 'http://music.163.com/discover/artist/cat?id={}&initial={}'
ARTIST_URL = 'http://music.163.com/artist?id={}'
SONG_URL = 'http://music.163.com/song?id={}'
COMMENTS_URL = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}'  # noqa


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
    process = Process.get_or_create(id=artist_id)  # Process以歌手为单位
    if process.is_success:
        return

    print('Starting fetch artist: {}'.format(artist_id))
    start = time.time()
    process = Process.get_or_create(id=artist_id)

    tree = get_tree(ARTIST_URL.format(artist_id))  # 使用requests获取页面文本，转化为lxml对象

    artist = Artist.objects.filter(id=artist_id)
    if not artist:  # 如果之前没抓过
        artist_name = tree.xpath('//h2[@id="artist-name"]/text()')[0]
        picture = tree.xpath(
            '//div[contains(@class, "n-artist")]//img/@src')[0]
        artist = Artist(id=artist_id, name=artist_name, picture=picture)
        artist.save()
    else:  # 如果之前抓过，但是该歌手的歌曲没抓完
        artist = artist[0]
    song_items = tree.xpath('//div[@id="artist-top50"]//ul/li/a/@href')
    songs = []
    for item in song_items:
        song_id = item.split('=')[1]
        song = parser_song(song_id, artist)  # 进入抓取和解析歌手模式
        if song is not None:
            songs.append(song)
    artist.songs = songs
    artist.save()
    process.make_succeed()  # 标记歌手下的热门歌曲的热门评论抓完
    print('Finished fetch artist: {} Cost: {}'.format(
        artist_id, time.time() - start))


def parser_song(song_id, artist):
    tree = get_tree(SONG_URL.format(song_id))
    song = Song.objects.filter(id=song_id)
    r = post(COMMENTS_URL.format(song_id))  # 必须post一些东西才能获取评论信息
    if r.status_code != 200:
        print('API Error: Song {}'.format(song_id))
        return
    data = r.json()
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
                print('Fetch limit!')
                time.sleep(10)
                return parser_song(song_id, artist)
        song = Song(id=song_id, name=song_name, artist=artist,
                    comment_count=data['total'])
        song.save()
    else:
        song = song[0]
    comments = []
    for comment_ in data['hotComments']:
        comment_id = comment_['commentId']
        content = comment_['content']
        like_count = comment_['likedCount']
        user = comment_['user']
        if not user:
            continue
        user = User.get_or_create(id=user['userId'], name=user['nickname'],
                                  picture=user['avatarUrl'])
        comment = Comment.get_or_create(id=comment_id, content=content,
                                        like_count=like_count, user=user,
                                        song=song)
        comment.save()
        comments.append(comment)
    song.comments = comments
    song.save()
    time.sleep(1)
    return song
