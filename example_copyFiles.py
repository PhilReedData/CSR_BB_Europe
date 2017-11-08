#!/usr/bin/python    

from os import makedirs
from os.path import exists, join
from shutil import copy2

# Directory where all the files to copy are found.
fromDir = "C:/path/with/forward/slashes/"

# Directory to copy these files to.
toDir = "C:/other/path/with/forward/slashes/"

# One filename per line, list of files to copy.
listPath = "C:/path/with/forward/slashes/list.txt"

# create toDir if it does not exist
if not exists(toDir):
    makedirs(toDir)
    
# Python list of files to copy
filesToCopy = open(listPath,'r').read().strip().split('\n')

numfiles = len(filesToCopy)
print ("Copying " + str(numfiles) + " from " + fromDir + " to " + toDir)

for filename in filesToCopy: 
    # Copy. Join each directory path to the filename.
    copy2(join(fromDir,filename), join(toDir,filename))
    print ("Copied " + filename)
    