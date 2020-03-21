import json
import os
import pathlib

from lib import paths
from lib import templates


def read_song_count():
  with open(paths.INFO_HEAD_FILE, 'r') as kinfo:
    data = json.loads(kinfo.read())
    return data['total_infok']


def write_info_head(song_count):
  with open(paths.INFO_HEAD_FILE, 'r+') as kinfo:
    # read and parse current file
    data = json.loads(kinfo.read())
    kinfo.seek(0)

    # write to file and truncate
    kinfo.write(templates.INFO_HEAD_TEMPLATE.format(
      fs_hh=data['filesize_HH'], 
      fs_hl=data['filesize_HL'], 
      fs_lh=data['filesize_LH'], 
      fs_ll=data['filesize_LL'], 
      count=song_count, 
      version=data['version'], 
      machine=data['machine_id']
    ))
    kinfo.truncate()

    # read and print out what we just wrote
    kinfo.seek(0)
    print('info_head.ini updated:')
    print(kinfo.read())
 

def get_song_meta_files():
  # get data files sorted by modified time since this is how Singing Machine associates it 
  # to the respective meta file. for example: ID0000.ini will be associated with the oldest
  # modified video in DATA_ROOT, and ID0001.ini will be associated with the second oldest
  # modified video, and so on.
  sorted_data_paths = filter(
    lambda p: p.is_file() and not p.name.startswith('.'),
    sorted(pathlib.Path(paths.DATA_ROOT).iterdir(), key=os.path.getmtime))
  song_meta_files = []
  
  for i, data_path in enumerate(sorted_data_paths):
    song_meta_files.append({
      'data_path': data_path,
      'meta_path': paths.SONG_META_FILE.format(index=i),
      'meta': read_song_meta_file(i)
    })
  
  return song_meta_files


def read_song_meta_file(index):
  path = paths.SONG_META_FILE.format(index=index)

  try:
    with open(path) as file: 
      return json.loads(file.read())
  except FileNotFoundError:
    return None


def write_song_meta_file(index, artist, title, genre):
  path = paths.SONG_META_FILE.format(index=index)

  with open(path, 'w') as file:
    file.write(templates.SONG_META_TEMPLATE.format(
      artist=artist, title=title, genre=genre))
    file.truncate()
