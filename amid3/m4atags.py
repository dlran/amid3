from mutagen import File, mp4
from .am import appleMusic, loadCover, iHeartRadio
import os
import sys
import re
import logging


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

def setTags(data, path, cpil):
    audio = mp4.MP4(path)
    audio.tags['\xa9ART'] = data['artistName']
    audio.tags['\xa9alb'] = data['albumName']
    audio.tags['\xa9nam'] = data['name']
    audio.tags['\xa9day'] = data['releaseDate']
    audio.tags['\xa9gen'] = data['genreNames']
    audio.tags['\xa9wrt'] = data.get('composerName', '')
    audio.tags['trkn'] = [(data['trackNumber'], 0)]
    audio.tags['disk'] = [(data['discNumber'], 0)]
    audio.tags['covr'] = [loadCover(data['artwork'])]
    audio.tags['cpil'] = cpil

    audio.tags['cprt'] = data.get('copyright', '')
    yt_vid = re.findall(r'-.{11}$', os.path.splitext(os.path.basename(path))[0])
    if data.get('description') and yt_vid:
        keep_id = data['description'] + yt_vid[0]
    else:
        keep_id = data.get('description', '')
    audio.tags['desc'] = keep_id

    if data.get('contentRating') == 'explicit':
        audio.tags['rtng'] = [4]
    elif data.get('contentRating') == 'clean':
        audio.tags['rtng'] = [2]

    audio.save()
    logger.info('[mutagen] Dest: %s' % path)

def listAudio(inputPath):
    fl = filter(lambda x: os.path.splitext(x)[-1] == '.m4a', os.listdir(inputPath))
    return [os.path.join(inputPath, f) for f in fl]

def lcs(tg, t):
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

def m4aTags(url, src='./', cpil=False, simi=None, region='us', logger_name=''):
    if logger_name:
        global logger
        logger = logging.getLogger(logger_name)
    src = os.path.realpath(src)
    listFiles = listAudio(src) if os.path.isdir(src) else [src]
    if 'iheart.com' in url:
        tracksAttrs = list(iHeartRadio(url=url))
    else:
        tracksAttrs = appleMusic(url, region)
    result = []
    for ls in listFiles:
        # replace youtube vid
        assert_name = re.sub(r'-.{11}$', '', os.path.splitext(os.path.basename(ls))[0])
        def simiTracks(track):
            simi_name = lcs(track['attributes']['name'], assert_name)
            simi_name_artist = lcs(track['attributes']['name'] + ' ' + track['attributes']['artistName'], assert_name)
            simi_artist_title = lcs(track['attributes']['artistName'] + ' ' + track['attributes']['name'], assert_name)
            # logger.info(track['attributes']['name'], simi_name, simi_name_artist, simi_artist_title)
            return max(simi_name, simi_name_artist, simi_artist_title)
        simi_all_tracks = list(map(simiTracks, tracksAttrs))
        max_simi = max(simi_all_tracks)
        max_simi_idx = simi_all_tracks.index(max_simi)

        logger.info('[matching] Title: %s | Assert: %s | Match: %s' % (
            tracksAttrs[max_simi_idx]['attributes']['name'],
            assert_name,
            max_simi))
        if max_simi > (simi or 0.6):
            setTags(tracksAttrs[max_simi_idx]['attributes'], ls, cpil)
            result.append(ls)
        else:
            logger.info('[matching] Cannot match')

        logger.info('')
    return result

