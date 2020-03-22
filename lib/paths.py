from os import mkdir, path, walk
from platform import system

from lib.templates import NEW_INFO_HEAD_FILE, NEW_PLAYLISTS_FILE, \
  NEW_FAVORITES_FILE

# Path templates which are initialized first thing in main.py
# NOTE: Do not prefix these with '/'!
DATA_ROOT = 'karaoke'                # directory of MP4 video files
META_ROOT = 'karaokeinfo'            # directory *.ini files
INFO_HEAD_FILE = 'info_head.ini'     # meta file that keeps track of song counts
PLAYLISTS_FILE = 'playlist.ini'      # meta file that keeps track of playlists
FAVORITES_FILE = 'favorite.ini'      # meta file that keeps track of favorite songs
SONG_META_FILE = 'ID{index:04}.ini'  # song meta file


# Important -- this MUST be called as early as possible
def init_paths(disk_root=None):
  global DATA_ROOT, META_ROOT, INFO_HEAD_FILE, PLAYLISTS_FILE, \
    FAVORITES_FILE, SONG_META_FILE

  if disk_root is not None:
    if not path.exists(disk_root):
      print('Passed in root path \'{}\' does not exist, exiting'.format(disk_root))
      exit(1)
    elif not path.isdir(disk_root):
      print('Passed in root path \'{}\' is not a directory, exiting'.format(disk_root))
      exit(1)
    else:
      disk_root = path.abspath(disk_root)

  disk_root = disk_root or scan_for_disk_root() or prompt_for_disk_root()
  DATA_ROOT = path.join(disk_root, DATA_ROOT)
  META_ROOT = path.join(disk_root, META_ROOT)
  INFO_HEAD_FILE = path.join(META_ROOT, INFO_HEAD_FILE)
  PLAYLISTS_FILE = path.join(META_ROOT, PLAYLISTS_FILE)
  FAVORITES_FILE = path.join(META_ROOT, FAVORITES_FILE)
  SONG_META_FILE = path.join(META_ROOT, SONG_META_FILE)

  bootstrap_disk()


# Attempts to find the disk root by looking for ../karaokeinfo/info_head.ini
def scan_for_disk_root():
  os_name = system()

  if os_name == 'Darwin':  # Mac
    root_disk = scan_for_disk_root_mac()
  elif os_name == 'Windows':
    root_disk = scan_for_disk_root_win()

  if root_disk is not None:
    print('Found Singing Machine disk: {}'.format(root_disk))

  return root_disk


has_info_head = lambda root: path.exists(path.join(root, META_ROOT, INFO_HEAD_FILE))


# Mac implementation of scan_for_disk
def scan_for_disk_root_mac():
  search_dir = '/Volumes'
  sub_dirs = next(walk(search_dir))[1]
  candidates = map(lambda d: path.join(search_dir, d), sub_dirs)
  disk_root = next(iter(filter(has_info_head, candidates)), None)

  return disk_root


# Windows implementation of scan_for_disk
def scan_for_disk_root_win():
  from win32api import GetLogicalDriveStrings
  from win32file import GetDriveType, DRIVE_FIXED, DRIVE_REMOVABLE

  drives = GetLogicalDriveStrings()
  drives = drives.split('\000')[:-1]
  drives = list(filter(lambda d: GetDriveType(d) == DRIVE_FIXED or GetDriveType(d) == DRIVE_REMOVABLE, drives))
  disk_root = next(iter(filter(has_info_head, drives)), None)

  return disk_root


# Prompts for manual entry of the disk root
def prompt_for_disk_root(show_header=True):
  if show_header:
    print('Unable to find your root disk')

  disk_root = input('Disk Root Path: ')

  if not path.exists(disk_root):
    print('{} does not exists, try again'.format(disk_root))
    return prompt_for_disk_root(False)
  elif not path.isdir(disk_root):
    print('{} is not a directory, try again'.format(disk_root))
    return prompt_for_disk_root(False)

  return disk_root


# Bootstraps a path with missing files
def bootstrap_disk():
  paths_to_create = list(filter(lambda d: not path.exists(d), [DATA_ROOT, META_ROOT]))
  files_to_create = list(filter(lambda f: not path.exists(f[0]), [
    (INFO_HEAD_FILE, NEW_INFO_HEAD_FILE),
    (PLAYLISTS_FILE, NEW_PLAYLISTS_FILE),
    (FAVORITES_FILE, NEW_FAVORITES_FILE)
  ]))

  if len(paths_to_create) == 0 and len(files_to_create) == 0:
    return

  print('Some files appear to missing from your disk.')
  prompt = input('Would you like to create them (y)? ')

  if prompt != 'y':
    print('Aborting due to missing files on your disk')
    exit(1)


  for p in paths_to_create:
    print('Creating directory {}'.format(p))
    mkdir(p)

  for p, template in files_to_create:
    print('Creating file {}'.format(p))

    with open(p, 'w+') as f:
      f.write(template)
      f.truncate()
      f.seek(0)
      print(f.read())
