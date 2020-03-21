from os import path


# Path templates which are initialized first thing in main.py
# NOTE: Do not prefix these with '/'!
DATA_ROOT = 'karaoke/'               # MP4 video files
META_ROOT = 'karaokeinfo/'           # *.ini files 
INFO_HEAD_FILE = 'info_head.ini'     # meta file that keeps track of song counts
SONG_META_FILE = 'ID{index:04}.ini'  # song meta file


# Important -- this MUST be called as early as possible
def init_paths(disk_root=None):
  global DATA_ROOT, META_ROOT, INFO_HEAD_FILE, SONG_META_FILE

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
  SONG_META_FILE = path.join(META_ROOT, SONG_META_FILE)


# Attempts to find the disk root by looking for ../karaokeinfo/info_head.ini 
def scan_for_disk_root():
  return '/Volumes/Untitled'


# Prompts for manual entry of the disk root
def prompt_for_disk_root():
   return '/Volumes/Untitled'
