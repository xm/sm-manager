#!/usr/bin/env python3

import json
import os


DISK_ROOT = '/Volumes/Untitled/'         # USB root location
INFO_ROOT = DISK_ROOT + 'karaokeinfo/'   # *.ini files 
INFO_HEAD = INFO_ROOT + 'info_head.ini'  # meta file that keeps track of song counts
DATA_ROOT = DISK_ROOT + 'karaoke/'       # MP4 video files
INFO_HEAD_TEMPLATE = '''\
{{
	"filesize_HH":	{fs_hh},
	"filesize_HL":	{fs_hl},
	"filesize_LH":	{fs_lh},
	"filesize_LL":	{fs_ll},
	"total_infok":	{count},
	"version":	"{version}",
	"machine_id":	"{machine}"
}}'''


def read_total_song_count():
  with open(INFO_ROOT + 'test_info_head.ini', 'r') as kinfo:
    data = json.loads(kinfo.read())
    return data['total_infok']


def write_info_head(count):
  with open(INFO_ROOT + 'test_info_head.ini', 'r+') as kinfo:
    # read and parse current file
    data = json.loads(kinfo.read())
    kinfo.seek(0)

    # write to file and truncate
    kinfo.write(INFO_HEAD_TEMPLATE.format(
      fs_hh=data['filesize_HH'], 
      fs_hl=data['filesize_HL'], 
      fs_lh=data['filesize_LH'], 
      fs_ll=data['filesize_LL'], 
      count=count, 
      version=data['version'], 
      machine=data['machine_id']
    ))
    kinfo.truncate()

    # read and print out what we just wrote
    kinfo.seek(0)
    print('info_head.ini updated:')
    print(kinfo.read())


count = read_total_song_count()
write_info_head(count)
