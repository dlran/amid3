from urllib import request
import json

def __request(url, method='GET', header={}):
    return request.Request(
        url = url,
        headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'authorization': 'Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldlYlBsYXlLaWQifQ.eyJpc3MiOiJBTVBXZWJQbGF5IiwiaWF0IjoxNTk2NzQ4MjU1LCJleHAiOjE2MTIzMDAyNTV9.0RaBH15qTCKAhV3toQzZfxjNkYg6cqNagNUPQMkpUE3Ox6O-EV-3G42hOJprkv-b8tLBUG6lxa94W7BORdYluw',
            **header},
        method = method)

def loadAMAblum(id):
    with request.urlopen(__request(f'https://amp-api.music.apple.com/v1/catalog/us/albums/{id}?omit%5Bresource%5D=autos&include=tracks%2Cartists&include%5Bsongs%5D=composers&extend=offers%2Cpopularity&views=appears-on%2Cmore-by-artist%2Crelated-videos%2Cother-versions%2Cyou-might-also-like&fields%5Bartists%5D=name%2Curl&l=en-us')) as res:
        content = json.loads(res.read().decode("UTF-8"))
        return content['data'][0]['relationships']['tracks']['data']
        # for track in content['data'][0]['relationships']['tracks']['data']:
        #     print(track['attributes']['name'])
        #     print(track['attributes']['albumName'])
        #     print(track['attributes']['artistName'])

def loadCover(artwork):
    url = artwork['url'].format(w='1000', h='1000')
    with request.urlopen(__request(url)) as res:
        return res.read()
