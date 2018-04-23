#!/usr/bin/python 

# Utils

# Dict of Bloomberg index code to ISO country code.
INDEX2ISO = {
    'ATX'       :'AT', 
    'BEL'       :'BE', 
    'OMXC'      :'DK', 
    'OMXH'      :'FI', 
    'CAC'       :'FR', 
    'DAX'       :'DE', 
    'ISEQ'      :'IE', 
    'FTSEMIBN'  :'IT', 
    'AEX'       :'NL', 
    'OBX'       :'NO', 
    'PSI'       :'PT', 
    'IBEX'      :'ES', 
    'OMX2'      :'SE', 
    'SMI'       :'CH', 
    'UKX'       :'GB' 
}

# Dict of codes for the known report types.
# Note: there are other AR strings: Preliminary_Annual, 20-F
# Note: other CR strings: PrelimDigest_CSR_Report, Corporate_Responsiblity0
# where 0 is a number of 1-2 digits
REPORT_TYPES = {
    'CR'    :'Corporate_Responsibility',
    'AR'    :'Annual_Report',
    'ESG'   :'ESG_Releases'
}

# Given a zip filename that begins with a Bloomberg index code,
# return ISO country code.
def getIsoFromString(instring):
    if instring in INDEX2ISO:
        return INDEX2ISO[instring]
    for index in INDEX2ISO.keys():
        # if instring begins with this index, return its iso
        if instring[:len(index)] == index:
            return INDEX2ISO[index]
    print(instring)
    return 'ZZ_OTHER/' + instring[:-4]
    
def test_getIsoFromString():
    test1 = getIsoFromString("OMXH25")
    print(test1, " (should be FI)")
    test2 = getIsoFromString("IBEX2012_BB_Docs_071417_110458.zip")
    print(test2, " (should be ES)")
    
# Given a raw Bloomberg report filename, return the company ticker
# Ticker is between first and second underscore. 
def rawFilename2Ticker(rawFilename):
    firstU = rawFilename.index('_')
    secondU = rawFilename.index('_', firstU + 1)
    return rawFilename[firstU+1:secondU]

def test_rawFilename2Ticker():
    ticker = rawFilename2Ticker("012011_MRK_Corporate_Responsibility_US000000002016945409.pdf")
    print(ticker, 'MRK')
    
# Given a raw Bloomberg report filename,
# return a code for the report type.
def rawFilename2ReportType(rawFilename):
    if "_Corporate_Responsibility" in rawFilename or "_PrelimDigest_CSR_Report" in rawFilename:
        return "CR"
    elif "_Annual_Report" in rawFilename or "_Preliminary_Annual" in rawFilename or "_20-F" in rawFilename:
        return "AR"
    elif "_ESG_Releases" in rawFilename:
        return "ESG"
    return "UNKNOWN"

# Given a raw Bloomberg report filename,
# return a 4-digit year the report was uploaded
def rawFilename2UploadYear(rawFilename):
    # Filename begins MMDDYY.
    try: 
        uploadYear = int("20" + rawFilename[4:6])
    except ValueError:
        uploadYear = -1
    return uploadYear

# Given a raw Bloomberg report filename,
# return the file extension, or blank if none
def rawFilename2Ext(rawFilename):
    # Get characters after dot
    try:
        dot = rawFilename.rindex('.')
    except ValueError:
        return ''
    return rawFilename[dot+1:]
    
# Given a raw Bloomberg report filename,
# return the filename without extension, or whole if no extension
def rawFilename2Short(rawFilename):
    # Get characters after dot
    try:
        dot = rawFilename.rindex('.')
    except ValueError:
        return rawFilename
    return rawFilename[:dot]
    
if __name__ == "__main__":
    #test_getIsoFromString()
    #test_rawFilename2Ticker()
    
    zipPath = "U:/Ser-Huang_Poon/CSR_Europe/"
    unzipPath = "U:/Phil_Read/CSR_Europe/unzipped_raw/"
    
    from os import listdir
    from os.path import isfile, join
    zipfiles = [f for f in listdir(zipPath) if (isfile(join(zipPath, f)) )]
    print(len(zipfiles))
    