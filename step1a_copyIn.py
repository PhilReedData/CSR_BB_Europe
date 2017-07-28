#!/usr/bin/python    
# Copy unlocked PDF files in

# fixed PDF directory
fromPath = "U:/Ser-Huang_Poon/PhilMinus1"

# copy into the rest of the unzipped PDFs, and overwrite
toPath = "U:/Phil_Read/CSR_Europe/unzipped_raw"

from os import listdir
from os.path import isfile, join
from shutil import copyfile, copy2
# One directory per country code
countries = [f for f in listdir(fromPath) if (not isfile(join(fromPath, f)) )]

COUNTRIES_TO_EXCLUDE = []
CORRUPT_FILES = []

print ('Copying from: ' + fromPath)
print ('Copying to: ' + toPath)
print (str(len(countries)) + ' countries')

for country in countries:
    if not country in COUNTRIES_TO_EXCLUDE:
        print ('Country: ' + country)
        # Get list of files
        files = [f for f in listdir(join(fromPath, country)) if (isfile(join(fromPath, country ,f)) )]
        print (len(files), 'files')
        for file in files:
            if file.endswith('.pdf') and (not file in CORRUPT_FILES):
                fromPathFull = join(fromPath, country, file)
                toPathFull = join(toPath, country)
                copy2(fromPathFull, toPathFull)
                print ('Copied ' + file)
  