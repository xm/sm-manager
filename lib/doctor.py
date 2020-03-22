import re
import time

from lib.sm import get_song_meta_files, write_song_meta_file


PRINT_META_TEMPLATE = '''\
  Artist: {AT} -> {artist}
   Title: {TL} -> {title}
   Genre: {GE} -> {genre}'''


# Simple job that repairs existing song meta files. The way it does this is it looks at normalized
# song data names that follow the defined pattern, and makes sure its corresponding meta file has
# the correct values
def repair_song_metas():
  song_metas = get_song_meta_files()

  for i, song_meta in enumerate(song_metas):
    data_filename = song_meta['data_path'].name
    parsed_meta = parse_song_meta_from_filename(data_filename)

    if parsed_meta is None:
      print('[ID{:04}.ini] {}: could not parse song meta data'.format(i, data_filename))
    elif song_meta['meta'] is None:
      print('[ID{:04}.ini] {}: creating meta data file'.format(i, data_filename))
      write_song_meta_file(i, **parsed_meta)
    elif should_update_meta(song_meta['meta'], parsed_meta):
      print('[ID{:04}.ini] {}: updating meta data'.format(i, data_filename))
      print(PRINT_META_TEMPLATE.format(**song_meta['meta'], **parsed_meta))
      write_song_meta_file(i, **parsed_meta)
    else:
      print('[ID{:04}.ini] {}: OK!'.format(i, data_filename))


def prune_extraneous_files():
  pass


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
