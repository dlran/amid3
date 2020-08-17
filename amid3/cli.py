import sys
import os
import argparse
from .__init__ import m4aTags
from .__version__ import __version__

def main():
    parser = argparse.ArgumentParser(description = '666', usage="amid3 [options...] [args] AlbumId")
    parser.add_argument('id', type=str, help='apple music album id')
    parser.add_argument('-s', '--src', type=str, help='source directory or single file, default ./', default='./')
    parser.add_argument('-v', '--version', action='version', version=__version__)
    argv = sys.argv
    args = parser.parse_args()
    if len(argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    m4aTags(id=args.id, src=args.src)


if __name__ == '__main__':
    main()
