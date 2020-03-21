# Path templates which are initialized first thing in main.py
DATA_ROOT = '{root}/karaoke/'                      # MP4 video files
META_ROOT = '{root}/karaokeinfo/'                  # *.ini files 
INFO_HEAD_FILE = '{meta_root}/info_head.ini'       # meta file that keeps track of song counts
SONG_META_FILE = '{meta_root}/ID{{index:04}}.ini'  # song meta file


# Important -- this MUST be called as early as possible
def init_paths():
  global DATA_ROOT, META_ROOT, INFO_HEAD_FILE, SONG_META_FILE

  root = scan_for_root() or prompt_for_root()
  DATA_ROOT = DATA_ROOT.format(root=root)
  META_ROOT = META_ROOT.format(root=root)
  INFO_HEAD_FILE = INFO_HEAD_FILE.format(meta_root=META_ROOT)
  SONG_META_FILE = SONG_META_FILE.format(meta_root=META_ROOT)


# Attempts to find the disk root by looking for ../karaokeinfo/info_head.ini 
def scan_for_root():
  return '/Volumes/Untitled'


# Prompts for manual entry of the disk root
def prompt_for_root():
   return '/Volumes/Untitled'
