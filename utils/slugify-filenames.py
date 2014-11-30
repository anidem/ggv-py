# python script to rename (slugify) files in a directory.
import os
from django.utils.text import slugify

input_dir = '/Library/WebServer/Documents/stacks'
files = []
for fstr in os.listdir(input_dir):
    if fstr != '.DS_Store':
        files.append(fstr)

# rename each file by slugifying it.
for i in files:
    print i
    s = i.replace('-web', '')
    os.rename(
        os.path.join(input_dir, i),
        os.path.join(input_dir, s)

        # os.path.join(input_dir, slugify(unicode(i, errors='replace')))
    )

