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
REPORT_TYPES = {
    'CR'    :'Corporate_Responsibility'
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
    if "_Corporate_Responsibility_" in rawFilename:
        return "CR"
    return "UNKNOWN"

if __name__ == "__main__":
    #test_getIsoFromString()
    #test_rawFilename2Ticker()
    
    zipPath = "U:/Ser-Huang_Poon/CSR_Europe/"
    unzipPath = "U:/Phil_Read/CSR_Europe/unzipped_raw/"
    
    from os import listdir
    from os.path import isfile, join
    zipfiles = [f for f in listdir(zipPath) if (isfile(join(zipPath, f)) )]
    print(len(zipfiles))
    
