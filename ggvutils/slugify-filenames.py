# python script to rename (slugify) ispring folder names in a directory. 

import os
from django.utils.text import slugify


""" Usage:
1. cd to directory containing files/folders that need to be renamed (slugified)
2. run python slugify-filenames.py within above directory

"""

def slugify_file(directory, fstr):
    ftrim = fstr[:-4] # remove (Web) from filename.
    ftrim = slugify(unicode(ftrim, errors='replace'))
    os.rename(
        os.path.join(directory, fstr),
        os.path.join(directory, ftrim)
    )


def slugify_dir(directory):
    # loop through files in dir -- rename each file by slugifying it.
    files = [i for i in os.listdir(directory) if i[0] != '.']
    for i in files:
        slugify_file(directory, i)

if __name__ == '__main__':
    input_dir = os.path.abspath('.')
    slugify_dir(input_dir)

