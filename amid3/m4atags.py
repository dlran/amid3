from mutagen import File, mp4
from .am import loadAMAblum, loadCover
import os
import sys
import re

def setTags(data, path):
    audio = mp4.MP4(os.path.realpath(path))
    audio.tags['\xa9ART'] = data['artistName']
    audio.tags['\xa9alb'] = data['albumName']
    audio.tags['\xa9nam'] = data['name']
    audio.tags['\xa9day'] = data['releaseDate']
    audio.tags['\xa9gen'] = data['genreNames']
    audio.tags['\xa9wrt'] = data['composerName']
    audio.tags['trkn'] = [(data['trackNumber'], 0)]
    audio.tags['disk'] = [(data['discNumber'], 0)]
    audio.tags['covr'] = [loadCover(data['artwork'])]
    audio.save()
    # print(audio.pprint())

def listAudio(inputPath):
    fl = filter(lambda x: os.path.splitext(x)[-1] == '.m4a', os.listdir(inputPath))
    return [os.path.join(inputPath, f) for f in fl]

def lsc(tg, t):
    tg_ls = list(tg)
    t_ls = list(t)
    o = list(map(lambda x: [0] * (len(tg_ls) + 1), [[], *t_ls]))
    for k, v in enumerate(t_ls):
        for f, c in enumerate(tg_ls):
            if c == v:
                o[k+1][f+1] = o[k][f]+1
            else:
                o[k+1][f+1] = max(o[k][f+1], o[k+1][f])
    return round(o[len(t_ls)][len(tg_ls)] / max(len(t_ls), len(tg_ls)), 2)

def m4aTags(id, src='./'):
    src = os.path.realpath(src)
    listFiles = listAudio(src) if os.path.isdir(src) else [src]
    for ls in listFiles:
        for track in loadAMAblum(id=id):
            # replace youtube vid
            assert_name = re.sub(r'-.{11}$', '', os.path.splitext(os.path.basename(ls))[0])
            simi_name = lsc(track['attributes']['name'], assert_name)
            simi_artist = lsc(track['attributes']['name'] + ' ' + track['attributes']['artistName'], assert_name)
            simi = max(simi_name, simi_artist)
            if simi > 0.6:
                print('Name: %s | File: %s | Match: %s' % (track['attributes']['name'], ls, simi))
                setTags(track['attributes'], ls)
                break

