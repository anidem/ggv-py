# python script to rename (slugify) files in a directory. CD to the directory before running. Note the curr directory path given on line 5
import os
from django.utils.text import slugify

input_dir = os.path.abspath('.')


def slugify_file(directory, fstr):
    froot = fstr[:-4]
    fext = fstr[-4:] # get the three letter extension with the '.'
    j = slugify(unicode(froot, errors='replace'))
    j = j + fext
    # print '\t\tRENAMED', j

    os.rename(
        os.path.join(directory, fstr),
        os.path.join(directory, j)
    )    

def slugify_dir(directory):
    # loop through files in dir -- rename each file by slugifying it. 
    for i in os.listdir(directory):
        # print '\t',i
        slugify_file(directory, i)




for j in filter(os.path.isdir, os.listdir(input_dir)):
    subdir = os.path.abspath(os.path.join(input_dir, j))
    # print subdir
    slugify_dir(subdir)





        