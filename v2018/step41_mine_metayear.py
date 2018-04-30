#!/usr/bin/python    

# get creation year metadata, add column to stats table, matching filename
# Could extend it to not perform mining on a report that has already been mined.

### Change this True/False to run Europe or UK version of code. ###
isEurope = True

statsPathIn  = 'stats31EU.csv' if isEurope else 'stats31UK.csv'
statsPathOut = 'stats41EU.csv' if isEurope else 'stats41UK.csv'
logPath = 'log41EU.csv' if isEurope else 'log41UK.csv' # in case of crash

unzipPathEU = "U:/Phil_Read/CSR_Europe/unzipped_allinone/"
unzipPathUK = "U:/Phil_Read/CSR_UK/unzipped_allinone/"
unzipPath = unzipPathEU if isEurope else unzipPathUK

# Get creation year from given PDF document
import PyPDF2

# Get the entire metadata dictionary for given PDF.
def getPDFMetadata(path):
    p = file(path, "rb")
    try:
        pdf = PyPDF2.PdfFileReader(p)
        pdf_info = pdf.getDocumentInfo()
        return pdf_info
    except ValueError:
        print ('Error reading: ' + path)
        return []
    except Exception:
        print ('Exception reading: ' + path)
        return []
        
    
# Get the year of creation from metadata, or whole date string (YMD).
# Returns year as int, or -1 if file not read, or -2 if valid date not found.
def getPDFMetaCreationYear(path, getWholeDate=False):
    meta = getPDFMetadata(path)
    if meta == None or len(meta) == 0:
        # Could not read file
        return -1
    keys = meta.keys()
    creationDateRaw = ""
    creationYear = -2
    for key in keys:
    #for item in meta:
        #print (item[0])
        if "creationdate" in key.lower():
            creationDateRaw = meta[key]
            if getWholeDate:
                return creationDateRaw
            break
    if len(creationDateRaw)>0:
        # Assume year is first instance of "20xx"
        try:
            start = creationDateRaw.index('20')
            creationYearString = creationDateRaw[start:start+4]
            creationYear = int (creationYearString)
        except ValueError:
            pass
        except Exception:
            pass
    return creationYear

# Main logic
#Load stats31csv, to dataframe df.
import pandas as pd
df = pd.read_csv(statsPathIn)
log = open(logPath,'w')
log.write('filenamefull,metayear\n')

#Function getMetaYear(filenamefull, filetype)
#	Call utility file, depends on filetype (PDF only)
#	Return metaYear.
def getMetaYear(filenamefull, filetype):
    year = ''
    if filetype == 'pdf':
        year = getPDFMetaCreationYear(unzipPath + filenamefull)
    log.write(filenamefull + ',' + str(year) + '\n') 
    return year

#Apply getMetaYear function to dataframe, save new column metayear.
df['metayear'] = df.apply(lambda x: getMetaYear(x['filenamefull'], x['filetype']), axis=1)

#Save df to stats41.csv
df.to_csv(statsPathOut, index=False, encoding='utf-8')
log.close()

# Testing
if __name__ == "__main__":
    path = "U:/Phil_Read/CSR_Europe/unzipped_raw/AT/060910_TKA_Corporate_Responsibility_SD000000002004960095.pdf"
    y = getPDFMetaCreationYear(path)
    print ('meta creation year',y)