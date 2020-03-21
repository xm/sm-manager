#!/usr/bin/env python3

import argparse
import sys

from lib.paths import init_paths
from lib.doctor import repair_song_metas


def main():
  parser = argparse.ArgumentParser('Manage your Singing Machine karaoke songs.')
  parser.add_argument('--doctor', action='store_true', help='Attempt to repair and normalize the song meta data')
  parser.add_argument('--import', type=argparse.FileType('r'), help='Import ', metavar='<file>')
  args = vars(parser.parse_args())

  if len(sys.argv) == 1:
    parser.print_usage()
    exit(1)

  # required for subsequent commands to work
  init_paths()

  if args['doctor']:
    repair_song_metas()

  if args['import']:
    print(args['import'])  


if __name__ == "__main__":
  main()
