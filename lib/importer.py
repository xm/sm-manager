import csv


def import_songs(songs_file):
    # parse songs_file as tsv
    parsed = list(csv.DictReader(songs_file, delimiter="\t", quotechar='"'))

    if len(parsed) == 0:
        print('Could not parse songs from {}.'.format(songs_file.name))
        print('Check that it is formatted correctly and try again.')
        exit(1)

    for row in parsed:
        print(row)
