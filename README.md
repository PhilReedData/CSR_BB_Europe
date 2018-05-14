# CSR Europe and UK method
_The following refers to newer code in directory `v2018`. The earlier code is in `v2017`._

Given a collection of corporate and social reponsibility reports from Bloomberg, organise the files ready to use for text and data mining techniques such as clustering. The filenames for each report contain a company ticker which is mapped to a list of company names and codes. The year for each report must be determined by an algorithm. The language of each report is detected and those in languages other than English are machine translated. 

The study is ran once for the largest c. 600 companies in 15 counties of Europe, and once for the largest companies in the UK. There are flags at the start of each script `isEurope` which must be set to `True` or `False`; sometimes the scripts will run slightly differently for each set.

### Stats and log files
Each step (rather, each sub-step) saves to a CSV file `statsNN.csv` where `NN` is the step number. The next step will read from the CSV file produced by the previous step. Further, the CSV files have `EU` or `UK` in the name to denote which set is being used. Lastly, some steps have an additional `logNN.csv` output file, which is written to throughout the step, whereas the `statsNN.csv` files are only written at the end of the step.

### Requirements
The code was written for Python 2.7.6 (64-bit) and will require altering to run in Python 3. The following packages were used. 

- googletrans 2.1.4
- langdetect 1.0.7
- numpy 1.8.0
- pandas 0.13.1
- PyPDF2 1.26.0
- xlrd 0.9.2

## Overall method
 - Step 10: Unzip reports
   - Step 11: Perform unzip
   - Step 13: Begin table
 - 	Step 20: Identify companies
	- Step 21: Identify companies
 - Step 30: Convert to txt
   - Step 31a: Convert with Acrobat Pro
 - 	Step 40: Mine the year
	- Step 41: Mine (PDF) metadata
	- Step 43: Mine txt content
	- Step 45: Identify best year
 - Step 50: Translate
	- Step 51: Detect language
	- Step 53: Translate non-English

## Sources
- Europe: 15 country indexes including UK, c.600 companies
- UK: 1 larger index

## Step 10: Unzip reports
### Step 11: Perform unzip
#### Types
- Europe: Corporate Responsibility (CR) reports.
- UK: CR, Annual Reports (AR) and ESG reports.
- Mostly: pdf, htm. Outliers: docx, xlsx, txt, xls, ppt.

#### File names
Report file names have standard format:
e.g. `040709_SAND_Corporate_Responsibility_WD000000001979575082.htm`
uploadMMDDYY\_companyTicker\_Report\_Type\_uniqueID.xtn

 - Update date could be several years after the report was written but never before. Sometimes several years' reports for the same company were uploaded in a batch. Year is yet more complicated than that; more later.
 - Company ticker is the alphanumeric characters from its Bloomberg ticker; if there is punctuation (like `BT/` for British Telecom) it is missing.
 - Report type is always `Corporate_Responsibility` for Europe. Various synonyms exist for the others.
 -	Unique ID suggests (ensures?) that the report is unique if there were multiple for that company ticker for that upload date.
 - File extension one of .pdf, .htm, .xls, .txt, .docx (lower case, dot then 3-4 characters).
 
Conversion from ticker to company identifier occurs later.

#### Countries
Europe:
Need to keep track of which country index report came from (could be more than one).
Replace indexname from zip archive name with 2-digit country ISO code:

Country | Index
--------|------
AT | ATX
BE | BEL
CH | SMI
DE | DAX
DK | OMXC
ES | IBEX
FI | OMXH
FR | CAC
GB | UKX
IE | ISEQ
IT | FTSEMIBN
NL | AEX
NO | OBX
PT | PSI
SE | OMX2

UK:
Index for all UK reports is FTSE All Share, so country code is `GB` for all.

#### Output table
On first pass, record each file as being unzipped. But there are duplicates, so need to remove these and replace the country column with countries column (pipe-delimited).
 
First pass, made-up example:

```
filenamefull, filetype, filenameshort, reporttype,uploadyear, ticker, country, unzip
e.g. 040709_SAND_Corp€¦2.htm, htm, 040709_SAND_Corp€¦2, CR, 2009, SAND, GB, 1
e.g. 040709_SAND_Corp€¦2.htm, htm, 040709_SAND_Corp€¦2, CR, 2009, SAND, IE, 0
```
 
### Step 13: Begin output table
Second pass (refine table), made-up example:

```
filenamefull,  filetype, filenameshort, reporttype, uploadyear, ticker, countries
e.g. 040709_SAND_Corp€¦2.htm, htm, 040709_SAND_Corp€¦2, CR, 2009, SAND, GB|IE
```

Integrate Step 13  into Step 11.
Save to `stats13EU.csv`

### Step 15: Copy in unlocked PDFs
Problems with some PDF documents

 - Locked for machine reading/converting/export/printing.
 - Unlocked but image-like content (no machine reading/converting).
 - Some PDFs could not be opened for other reasons, perhaps corrupt files, incorrectly unzipped, or network issues.
 - The usual other PDF layout issues such as columns not being interpreted correctly when machine reading or concerting to txt, page headers and footers getting included. 

#### Unlocking PDFs
An external application was used to unlock the locked PDF reports. Then the files were copied back, overwriting the locked ones.

_Not implememted step 15 yet._

## Step 20: Identify companies
Use reference tables to fill in the details of the companies in the stats table. 
Data sourced from Bloomberg, saved in Excel file.
 
#### Company details file
Uses the Bloomberg filename to create a Company object
 
eg `040709_SAND_Corporate_Responsibility_WD000000001979575082.htm`
Reads data from `20170717c_EuropeCSR.xlsx`
Creates object with fields including company name, ISIN, SIC from the ticker.
 
Sample of the Bloomberg data, the Belgium sheet:

Ticker | Company name | Disclosure | Country | ISIN | SIC Code | SIC Desc
-------|:-------------|-----------:|---------|------|---------:|---------
ACK BB Equity | ACKERMANS & ...| 11.8421| BE |BE0003... | 40 | Financials
AGS BB Equity | AGEAS | 11.8421 | BE | BE0974€¦ | 40 | Financials
ABI BB Equity | ANHEUSER-BU€¦ | 48.3471 | BE |BE0974... |30 | Consum...
 
### Step 21: Identify companies

#### Script
 - Utility that works with UK and Europe details files.
 - Load `stats13.csv` to dataframe `df`
 - Define function to apply to `df` that returns new columns based on filename arg
 - Bottom of Step 21 is a statement to apply that function to `df`
 - Save `df` to new CSV `stats21.csv`

Consider first country. If no company found, use second country (if present). 

Extra output columns: `companyname, tickerfull, isin, sic`.
 
#### Hacks: Fix company tickers not found
Company tickers that end / or /A have special treatment. Some companies still not found. 

## Step 30: Convert to txt
Three choices:

 - Step 31a option: Convert with Acrobat Pro
 - Step 31p option: Convert with Python
 - Step 31r option: Convert with R

Then later _(but not yet implemented)_:

 - Step 35: Convert image-like to txt

### Step 30: Copy in txt
Copy in converted txt files, renaming to remove prefix.
 
### Step 31a  option: Convert with Acrobat Pro
Method pdf ->ACROBAT-> rtf then rtf->WORD-> txt (eventually).  This occurs outside of the Python scripts.
 
#### Script
 - `foundTxts` = Read list of directory of txt files.
 - Load dataframe `df` from `stats21.csv`
 - Function `getFilenameTxt(filenameshort)`
   - Look for `filenameshort + ".txt"` in `foundTxts`.
   - Return this filename, else blank.
 - Apply function `getFilenameTxt` to `df`, new column `filenametxt`.
 - Save `df` to `stats31.csv`.
 

## Step 40: Mine the year
Assume there is a `filenametxt` column to identify which reports have been converted.

### Step 41: Mine (PDF) metadata
Will just do PDF. Skip all others.
 
#### Utility function
 - Function `getPDFMetaCreationYear(filename)`
 - Find `creation` in a metadata key, look for value beginning `20`.
 - If cannot open PDF, `metaYear = -1`
 - If can open PDF but cannot find valid year, `metaYear = -2`
 
#### Main script
 - Load `stats31csv`, to dataframe `df`.
 - Function `getMetaYear(filenamefull, filetype)`
   - Call utility function, depends on filetype (PDF, HTM only)
   - Return `metaYear`.
 - Apply `getMetaYear` function to dataframe, save new column `metayear`.
 - Save `df` to `stats41.csv`.

_Does not get month or day, just year of creation._

### Step 43: Mine txt content
During development, looked at two limits (first 150 then first 2000 characters).
Results fairly close, the second limit helped when no year found in first limit.
Reduced from 696/3416 =20% to 209/3416 = 6%.
There were 108/2416 = 4% where PDF could not be read regardless.
Compare the two limits, for 2612 rows with a year found:
2-tailed Spearman's Rho = 0.982 p < 0.001, so close enough.
Use second limit 2000 characters.

#### Utility utilGetYearFromTXT.py
 - Year can be any of TYPE\_A (2006), TYPE\_B (2006-2007), TYPE\_C (2006-07), from 2000 to 2019.
 - Range year counted as the latter year. Problem if different hyphen or slash used.
 - Count instances of each year occurring in text (in a matrix), return most recent mode.
 - Will mistake a phone number or other string like 320064 as a year.

#### Main script
- Load 'stats41.csv' to dataframe 'df'; fill blanks with `''`.
- Function `getMinedYear(filenametxt)`
  - Call utility file
  - Return `minedyear`
- Apply `getMinedYear` function to dataframe, save new column `minedyear`.
- Save `df` to `stats43.csv`.

### Step 45: Identify best year
We choose the `bestyear` by the following method.

 - If `metayear` is found, and is less than or equal to `uploadyear`, choose `metayear`.
 - Else if `minedyear` is found, and is less than or equal to `uploadyear`, choose `uploadyear`.
 - Else give up (value -1)

The `yearsource` field identifies which year detection method was chosen. The values are as follows.

 - "10": `metayear`
 - "20": `minedyear`
 - "30": `minedyear` but human-read
 - "-1": none

Note that the "30" category is not used in any code here, it is for any manual additions made later on reports which the computer could not read a year from.
 
#### Script
- Load `stats43.csv` to dataframe `df`; fill blanks with `''`.
- Function `getBestYear(metayear, minedyear, uploadyear)`
- Function `getYearSource(metayear, minedyear, uploadyear)`
- Apply `getBestYear` function to dataframe, save new column `bestyear`.
- Apply `getYearSource` function to dataframe, save new column `yearsource`.
- Save `df` to `stats45.csv`.
 

## Step 50: Translate
 
### Step 51: Detect language
- Use entire TXT file to detect most likely/common language.
- Use Google Translate implementation.
- Return two letter language code, or `'-1'` if failed.
- Does not look at metadata.
 
#### Script
- Load `stats45.csv` to dataframe `df`; fill blanks with `''`.
- Function `getLang(filenamefull, filenametxt)`
  - Calls utility
- Apply function `getLang` to `df`, save new column `lang`.
- Save `df` to `stats51.csv`.

### Step 53: Translate non-English
Load txt files, save to new directory.
Files named `xxxxxx.orig.txt` and `xxxxxx.tran.txt`.

Uses Google translate library, force 1 second between calls to prevent lockout.
Break into blocks of up to 5000 characters, join up again after.
 
#### Script
- Load `stats51.csv` to dataframe `df`; fill blanks with `''`.
- Function `callTranslate(filenamefull, filenametxt, lang)`
  - If already translated, skip
  - If `filenametxt` exists and `lang <> en`, Call utility
  - If `lang == en`, copy file
  - (Files of size 64 bytes or under are skipped.)
- Apply function `getLang` to `df`, save new column `filenametxttrans`.
- Function `summarizeTranslate (filenametxttrans)`
  - If copied/translated/error/notxt, return string
- Apply function `summarizeTranslate` to `df`, now col `translated`.
- Save `df` to `stats53.csv`.

## Stats file after all steps
The stats file has the following columns after step 53.

```
filenamefull, filetype, filenameshort, reporttype,u ploadyear, ticker, countries, companyname, tickerfull, isin, sic, filenametxt, metayear, minedyear, bestyear, yearsource, lang, filenametxttrans
```

The text files are available in one directory.


