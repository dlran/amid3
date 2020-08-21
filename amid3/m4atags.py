from mutagen import File, mp4
from .am import loadAMAblum, loadCover
import os
import sys
import re

def setTags(data, path, cpil):
    audio = mp4.MP4(path)
    audio.tags['\xa9ART'] = data['artistName']
    audio.tags['\xa9alb'] = data['albumName']
    audio.tags['\xa9nam'] = data['name']
    audio.tags['\xa9day'] = data['releaseDate']
    audio.tags['\xa9gen'] = data['genreNames']
    audio.tags['\xa9wrt'] = data['composerName']
    audio.tags['trkn'] = [(data['trackNumber'], 0)]
    audio.tags['disk'] = [(data['discNumber'], 0)]
    audio.tags['covr'] = [loadCover(data['artwork'])]
    audio.tags['cpil'] = cpil
    audio.save()
    print('[mutagen] Dest: %s' % path)

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

def m4aTags(id, src='./', cpil=False):
    src = os.path.realpath(src)
    listFiles = listAudio(src) if os.path.isdir(src) else [src]
    tracksAttrs = loadAMAblum(id=id)
    for ls in listFiles:
        # replace youtube vid
        assert_name = re.sub(r'-.{11}$', '', os.path.splitext(os.path.basename(ls))[0])
        def simiTracks(track):
            simi_name = lsc(track['attributes']['name'], assert_name)
            simi_name_artist = lsc(track['attributes']['name'] + ' ' + track['attributes']['artistName'], assert_name)
            simi_artist_title = lsc(track['attributes']['artistName'] + ' ' + track['attributes']['name'], assert_name)
            # print(track['attributes']['name'], simi_name, simi_name_artist, simi_artist_title)
            return max(simi_name, simi_name_artist, simi_artist_title)
        simi_all_tracks = list(map(simiTracks, tracksAttrs))
        max_simi = max(simi_all_tracks)
        max_simi_idx = simi_all_tracks.index(max_simi)

        print('[matching] Title: %s | Assert: %s | Match: %s' % (
            tracksAttrs[max_simi_idx]['attributes']['name'],
            assert_name,
            max_simi))
        if max_simi > 0.6:
            setTags(tracksAttrs[max_simi_idx]['attributes'], ls, cpil)
        else:
            print('[matching] Cannot match')

        print('')

