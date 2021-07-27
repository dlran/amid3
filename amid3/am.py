from urllib import request
import json
import re
import time

def __request(url, method='GET', header={}):
    return request.Request(
        url = url,
        headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            **header},
        method = method)

def appleMusic(url, region='us'):
    try:
        int(url)
    except ValueError:
        url = re.sub(r'\/$', '', url).rsplit('/', 1)[-1]
    regions = {'us': 'en-us', 'cn': 'zh-cn', 'hk': 'zh-hk', 'ca': 'en-ca', 'jp': 'ja'}
    ampApi = f'https://amp-api.music.apple.com/v1/catalog/{region}/albums/{url}?omit%5Bresource%5D=autos&include=tracks%2Cartists&include%5Bsongs%5D=composers&extend=offers%2Cpopularity&views=appears-on%2Cmore-by-artist%2Crelated-videos%2Cother-versions%2Cyou-might-also-like&fields%5Bartists%5D=name%2Curl&l={regions[region]}'

    with request.urlopen(__request(
            url=ampApi,
            header={'authorization': 'Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldlYlBsYXlLaWQifQ.eyJpc3MiOiJBTVBXZWJQbGF5IiwiaWF0IjoxNjI2OTg0ODk4LCJleHAiOjE2NDI1MzY4OTh9.Ftw-IRCBuL9EWw7N8yqsnvsmZc5DI_aqG7ic0eZXOfZMAB7lrVij7HGihIo6Jf9C3ZHw5RfZsd2ZDdYn_ncD9A'}
            )) as res:
        print('[apple music] Status: %s' % res.status)
        content = json.loads(res.read().decode("UTF-8"))['data'][0]
        tracks = content['relationships']['tracks']['data']
        for t in tracks:
            t['attributes']['copyright'] = content['attributes'].get('copyright') or content['attributes']['recordLabel']
            t['attributes']['description'] = content['id']
        return tracks

def loadCover(artwork):
    url = artwork['url'].format(w='1000', h='1000')
    with request.urlopen(__request(url)) as res:
        return res.read()

def iHeartRadio(url):
    with request.urlopen(__request(url)) as res:
        print('[iHeartRadio] Status: %s' % res.status)
        content = re.findall(
            r'<script data-name="initial-state" id="initialState" type="application/json">(.+?)</script>',
            res.read().decode('utf-8'))
        if content:
            content = content[0]
        else:
            print('[iHeartRadio] Error: script json data not found')
        albums = json.loads(content)['albums']['albums']
        albums = albums[list(albums.keys())[0]]
        def mapTracks(track):
            return {
              'attributes': {
                'albumName': albums['title'],
                'artistName': track['artistName'],
                'name': track['title'],
                'releaseDate': time.strftime('%Y-%m-%d %H%M%S', time.localtime(albums['releaseDate'] / 1000)),
                'genreNames': '', # ['Pop']
                'composerName': '',
                'trackNumber': track['trackNumber'],
                'discNumber': track['volume'],
                'artwork': {'url': albums['image']},
                'contentRating': 'explicit' if track['explicitLyrics'] else '',
                'copyright': albums['copyright'],
                'description': url
              }
            }
        return map(mapTracks, albums['tracks'])


