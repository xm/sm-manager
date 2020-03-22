import csv


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
