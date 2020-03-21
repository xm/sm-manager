#!/usr/bin/env python3

from lib.sm import get_song_meta_files

song_metas = get_song_meta_files()

for song_meta in song_metas:
  print(song_meta['data_path'])
  print(song_meta['meta_path'])
  print(song_meta['meta'])
  print()
