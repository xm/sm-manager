import csv
import sys

from os import path
from pytube import YouTube as yt

from lib import paths

def import_songs(songs_file):
    songs_to_download = parse_songs_file(songs_file)
    total = len(songs_to_download)

    for i, song in enumerate(songs_to_download):
        download_song(i + 1, total, song)

    print


def parse_songs_file(songs_file):
    print('Parsing {} for songs to download'.format(songs_file.name))

    songs = list(csv.DictReader(songs_file, delimiter="\t", quotechar='"'))
    total = len(songs)

    if total == 0:
        print('Could not parse songs from {}, exiting'.format(songs_file.name))
        exit(1)

    print('Found {} song{} to download'.format(total, '' if total == 1 else 's'))

    return songs


def download_song(i, total, song):
    print('[{}/{}] Downloading {} - {} from {}'.format(
        i, total, song['Artist'], song['Title'], song['Source']
    ))

    streams = yt(song['Source']).streams
    streams = streams.filter(subtype='mp4', progressive=True)
    streams = streams.order_by('resolution').desc()

    if streams is None or len(streams) == 0:
        print('[{}/{}] Failed -- could not find a suitable stream'.format(i, total))
        return

    try:
        filename = paths.get_song_filename(song['Genre'], song['Artist'], song['Title'])
        saved_file_path = streams[0].download(output_path=paths.DATA_ROOT, filename=filename)
        print('[{}/{}] Saved to {}'.format(i, total, saved_file_path))
    except:
        print('[{}/{}] Failed -- download from source failed'.format(i, total))
        print('Error', sys.exc_info()[0])
