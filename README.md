6⃣️6⃣️6⃣️

```
pip3 install git+https://github.com/dlran/amid3.git
```

```
amid3 -h
usage: amid3 [options...] [args] AlbumId

Get Apple Music album data and adds iTunes compatible tags on m4a files.

positional arguments:
  url                   apple music album url or id

optional arguments:
  -h, --help            show this help message and exit
  -s SRC, --src SRC     source directory or single file, default ./
  -c, --cpil            album is a compilation of songs by various artists
  --simi SIMI           value 0-1 similarity of matching file name, default
                        0.6
  --region {us,cn,hk,ca,jp}
                        apple music country or region
  -v, --version         show program's version number and exit

```

```
amid3 "https://music.apple.com/us/album/viva-la-vida-or-death-and-all-his-friends/1122773394" -s Viva\ La\ Vida-zOQ4ld6NsXE.m4a
[apple music] Status: 200
[matching] Title: Viva la Vida | Assert: Viva La Vida | Match: 0.92
[mutagen] Dest: /home/user/Downloads/Viva La Vida-zOQ4ld6NsXE.m4a
```

