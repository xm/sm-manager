import os
import pathlib
import re
import time

from lib import paths
from lib import sm


PRINT_META_TEMPLATE = '''\
  Artist: {AT} -> {artist}
   Title: {TL} -> {title}
   Genre: {GE} -> {genre}'''


# Main task that attempts to repair and clean up all meta files
def repair():
  song_count = len(sm.get_song_data_files())
  repair_song_metas()
  update_info_head(song_count)
  prune_extra_song_meta_files(song_count)


# Updates info_head.ini with current song count
def update_info_head(song_count):
  prev_song_count = sm.read_info_head_song_count()

  if prev_song_count != song_count:
    sm.write_info_head(song_count)
    print('Updated info_head.ini song count from {} to {}'.format(prev_song_count, song_count))


# Attempts to create or update missing song meta files
def repair_song_metas():
  print('Creating and updating song meta files')

  song_metas = sm.get_song_meta_files()

  for i, song_meta in enumerate(song_metas):
    data_filename = song_meta['data_path'].name
    parsed_meta = parse_song_meta_from_filename(data_filename)

    if parsed_meta is None:
      print('[ID{:04}.ini] {}: could not parse song meta data'.format(i, data_filename))
    elif song_meta['meta'] is None:
      print('[ID{:04}.ini] {}: creating meta data file'.format(i, data_filename))
      sm.write_song_meta_file(i, **parsed_meta)
    elif should_update_meta(song_meta['meta'], parsed_meta):
      print('[ID{:04}.ini] {}: updating meta data'.format(i, data_filename))
      print(PRINT_META_TEMPLATE.format(**song_meta['meta'], **parsed_meta))
      sm.write_song_meta_file(i, **parsed_meta)
    else:
      print('[ID{:04}.ini] {}: OK!'.format(i, data_filename))


def parse_song_meta_from_filename(filename):
  regex = r'^(?P<genre>.+)__(?P<artist>.+)__(?P<title>.+)\.[a-z0-9]+$'  # Genre__Artist__Title.ext
  m = re.match(regex, filename)

  if m is None:
    return None

  return m.groupdict()


def should_update_meta(current, expected):
  return current['TL'] != expected['title'] or \
         current['AT'] != expected['artist'] or \
         current['GE'] != expected['genre']


# Finds extra song meta files and deletes them
def prune_extra_song_meta_files(expected_count):
  meta_files = pathlib.Path(paths.META_ROOT).iterdir()
  files_to_delete = list(filter(lambda p: should_prune(p, expected_count), meta_files))
  delete_count = len(files_to_delete)

  if delete_count == 0:
    return

  file_copy = 'file' if delete_count is 1 else 'files'
  print('Found {} extraneous {} in {}:'.format(delete_count, file_copy, paths.META_ROOT))

  for f in files_to_delete:
    os.remove(f.absolute())
    print(' - Deleted {}'.format(f.absolute()))


def should_prune(p, expected_count):
  m = re.match(r'^ID(?P<meta_count>\d{4})\.ini$', p.name)

  if m is None:
    meta_count = None
  else:
    meta_count = int(m.groupdict()['meta_count'])

  return p.is_file() and meta_count is not None and meta_count >= expected_count
