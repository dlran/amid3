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
    regions = {'us': 'en-US', 'cn': 'zh-cn', 'hk': 'zh-hk', 'ca': 'en-ca', 'jp': 'ja'}
    ampApi = f'https://amp-api.music.apple.com/v1/catalog/{region}/albums/{url}?art%5Burl%5D=f&extend=editorialArtwork%2CeditorialVideo%2CextendedAssetUrls%2Coffers&fields%5Bartists%5D=name%2Curl&fields%5Bcurators%5D=name&fields%5Brecord-labels%5D=name%2Curl&format%5Bresources%5D=map&include=record-labels%2Cartists&include%5Bmusic-videos%5D=artists&include%5Bplaylists%5D=curator&include%5Bsongs%5D=artists%2Ccomposers%2Calbums&l={regions[region]}&meta%5Balbums%3Atracks%5D=popularity&platform=web&views=appears-on%2Caudio-extras%2Cmore-by-artist%2Cother-versions%2Crelated-videos%2Cvideo-extras%2Cyou-might-also-like'

    with request.urlopen(__request(
            url=ampApi,
            header={
                'authority': 'amp-api.music.apple.com',
                'origin': 'https://music.apple.com',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                'authorization': 'Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldlYlBsYXlLaWQifQ.eyJpc3MiOiJBTVBXZWJQbGF5IiwiaWF0IjoxNjc1MjAxMDY0LCJleHAiOjE2ODI0NTg2NjQsInJvb3RfaHR0cHNfb3JpZ2luIjpbImFwcGxlLmNvbSJdfQ.X6_jxCKuAndOhOL-hWPMPqwMiNJ6dWCau-FTP8AuXeHYCJLPueZDNSus_cdvqkKWPKyUD5FeTJwxwfvxezY0ow'}
            )) as res:
        print('[apple music] Status: %s' % res.status)
        content = json.loads(res.read().decode("UTF-8"))['resources']
        tracks = content['songs']
        albums = content['albums'][url]
        for t in tracks:
            tracks[t]['attributes']['copyright'] = albums['attributes'].get('copyright') or albums['attributes']['recordLabel']
            tracks[t]['attributes']['description'] = albums['id']
        return list(tracks.values())

def loadCover(artwork):
    url = artwork['url'].format(w='1000', h='1000', f='jpg')
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


