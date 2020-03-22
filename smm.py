#!/usr/bin/env python3

import argparse

from lib.paths import init_paths
from lib.doctor import repair
from lib.importer import import_songs


def main():
  parser = argparse.ArgumentParser('Manage your Singing Machine karaoke songs.')
  parser.add_argument('--doctor', action='store_true', help='Attempt to repair and normalize the song meta data')
  parser.add_argument('--import', type=argparse.FileType('r'), help='Download and import songs from a .tsv file', metavar='<file>')
  parser.add_argument('--disk-root', help='Manually set the disk root path', metavar='<path>')
  args = vars(parser.parse_args())

  if not args['doctor'] and not args['import']:
    parser.print_usage()
    exit(1)

  # required for subsequent commands to work
  init_paths(args['disk_root'])

  if args['doctor']:
    repair()

  if args['import']:
    import_songs(args['import'])


if __name__ == "__main__":
  main()
