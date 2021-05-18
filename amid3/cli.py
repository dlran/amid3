import sys
import os
import argparse
from .__init__ import m4aTags
from .__version__ import __version__

def main():
    parser = argparse.ArgumentParser(description = '666', usage="amid3 [options...] [args] AlbumId")
    parser.add_argument('url', type=str, help='apple music album url or id')
    parser.add_argument('-s', '--src', type=str, help='source directory or single file, default ./', default='./')
    parser.add_argument('-c', '--cpil', action='store_true', help="album is a compilation of songs by various artists")
    parser.add_argument('--simi', type=float, help="value 0-1 similarity of matching file name, default 0.6")
    parser.add_argument('--region', choices=['us', 'cn', 'hk', 'ca', 'jp'], type=str, help="apple music country or region", default='us')
    parser.add_argument('-v', '--version', action='version', version=__version__)
    argv = sys.argv
    args = parser.parse_args()
    if len(argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    m4aTags(url=args.url, src=args.src, cpil=args.cpil, simi=args.simi, region=args.region)


if __name__ == '__main__':
    main()
