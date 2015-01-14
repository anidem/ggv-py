# python script to rename (slugify) files in a directory. CD to the directory before running. Note the curr directory path given on line 5

import os
from django.utils.text import slugify

input_dir = os.path.abspath('.')
files = []
for fstr in os.listdir(input_dir):
    if fstr != '.DS_Store':
        files.append(fstr)
        # print fstr

# rename each file by slugifying it.
for i in files:
    # print i
    os.rename(
        os.path.join(input_dir, i),
        os.path.join(input_dir, slugify(unicode(i.replace('(Web)',''), errors='replace')))
    )
 
# files = []
# for fstr in os.listdir(input_dir):
#     if fstr != '.DS_Store':
#         files.append(fstr)
#         # print fstr

# for i in files:
#     # print i
#     os.rename(
#         os.path.join(input_dir, i),
#         os.path.join(input_dir, i.replace('png', '.png'))
#     )
# for fstr in os.listdir(input_dir):
#     if fstr != '.DS_Store':
#         print fstr