import csv
import sys

from os import path
from pytube import YouTube as yt

from lib import doctor
from lib import paths


def import_songs(songs_file):
    songs_to_download = parse_songs_file(songs_file)
    total = len(songs_to_download)

    for i, song in enumerate(songs_to_download):
        print('[{}/{}] Downloading {} - {} from {}'.format(
            i + 1, total, song['Artist'], song['Title'], song['Source']
        ))
        download_song(song)

    print('\nVideos have finished downloading -- updating song meta files\n')

    doctor.repair_song_metas()


def parse_songs_file(songs_file):
    print('Parsing {} for songs to download'.format(songs_file.name))

    songs = list(csv.DictReader(songs_file, delimiter="\t", quotechar='"'))
    total = len(songs)

    if total == 0:
        print('Could not parse songs from {}, exiting'.format(songs_file.name))
        exit(1)

    print('Found {} song{} to download'.format(total, '' if total == 1 else 's'))

    return songs


def download_song(song):
    streams = yt(song['Source']).streams
    streams = streams.filter(subtype='mp4', progressive=True)
    streams = streams.order_by('resolution').desc()

    if streams is None or len(streams) == 0:
        print('\tFailed -- could not find a suitable stream')

    try:
        filename = paths.get_song_filename(song['Genre'], song['Artist'], song['Title'])
        saved_file_path = streams[0].download(output_path=paths.DATA_ROOT, filename=filename)
        print('\tSaved video to {}'.format(saved_file_path))
    except:
        print('\tFailed -- download from source failed ({})'.format(sys.exc_info()[0]))
