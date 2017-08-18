# CSR_BB_Europe
Rearrange the CSR reports from Bloomberg on European companies into folders based on the report year.
Rearrange the CSR, ESG and Annual Reports from Bloomberg on (more) UK companies similarly.
Determine the year of the report from its metadata or content, also consider the upload date as a check.

## Pre-requisits
- Written for Python 2.7.6, requires alterations for Python 3 (particularly `dict.keys()`).
- Uses libraries: bs4, langdetect 1.0.7, numpy, operator, os, pandas, PyPDF2 1.26.0, shutil, xlrd, zipfile 
- The CSR, ESG and AR reports are in PDF or HTM format. Other formats are ignored.
- The reports contain the company ticker in the filename, after the upload date.
- The reference worksheet contains the same ticker*, company name, SIC, ISIN and other codes.
  - * The ticker in the filenames will exclude any slash '/' characters.

## Outputs
- The reports are rearranged by country or report type, then by year, into folders.
- The reports are renamed by SIC and ISIN codes, report type, then a counter if there is more than one in that folder. 
- A reference table of all the reports and several identifiers is produced.
- The language detection produces a separate table.
  - Could join this into the previous table.
- Any reports where the year could not be determined get year value -1.
  
## Contents
Run the stages in the order below.
1. Unzip to country folders
2. Find year and rearrange 
3. Rearrange files
4. Detect language
There are utility scripts described at the end of this document.

## Method
There is a script for the Europe dataset 
and a similar script for the extended UK dataset for each step.

To do: merge the Europe and the UK scripts into one process.


### Step 1. Unzip to country folders
- Unzip all reports. One folder per country (index). 
- All years and report types mixed up. 
- Output format:
	- folder per country (2-digit ISO)
	- filename: unchanged. `UPLOADDATE\_TICKER\_OTHER.pdf` where `UPLOADDATE` is `MMDDYY`
- UK: the files were already unzipped to one folder per report type.
- UK: the `reporttype` has values:
  - AR: annual report
  - CR: corporate sustainability report
  - ESG: economic, social and governance report  

### Step 1a. Copy IN
- Copy in any fixed PDF scripts that had been unreadable by Python before.

### Step 2. Mine the year
- Per country, read first page of PDF to determine year. (Takes a few hours.)
- If not found in first page, look in second, then third, then give up.
- Most (98%) are .pdf format for Europe, copy these and .htm. Ignore the few .docx, .txt, .xlsx files.
- UK: Per report type rather than country.
- UK: Greater proportion are .htm than for Europe.

### Step 2a. Fill year gaps
The year identification process is as follows. 
- We consider three kinds of detection of year:
  - `metayear`: the year from the PDF metadata creation date minus 1, or year in the HTML title field.
  - `minedyear`: the most frequent year mined from the first page of the PDF (or second or third page if none found), or from the entire HTML document.
  - `uploadyear`: the year from the filename denoting upload date by Bloomberg.
- We do not trust `uploadyear` as often many years of documents were uploaded around the same date. However it is used as a sanity check when considering the `metayear` or `minedyear` values - the report date cannot be after the document was uploaded.
- We choose the `bestyear` by the following method.
  - If `metayear` is found, and is less than or equal to `uploadyear`, choose `metayear`.
  - Else if `minedyear` is found, and is less than or equal to `uploadyear`, choose `uploadyear`.
  - Else give up (value -1)
The reports are copied into folders by year (or -1).

The `yearsource` field identifies which year detection method was chosen. The values are as follows.
- "10": metayear
- "20": minedyear
- "30": minedyear but human-read
- "-1": none

Note that the "30" category is not used in any code here, it is for any manual additions made later on reports which the computer could not read a year from.
  
### Step 3. Rearrange
- Create new filenames and copy the files. 
- Reads the Bloomberg Excel identifiers workbook to get ISIN, SIC (matching on Ticker).
- Reads a CSV file of country, file, year
- Output format of `stats.csv`:
	- folder per country (2-digit ISO), folder per year (or -1, use `bestyear`)
	- filename: `SIC\_ISIN\_TYPE_n_.pdf` where `TYPE` is CR and `_n_` is number for multiple reports
- UK: use report type instead of country.
- UK: the `TYPE` could be AR, CR or ESG.
	
### Step 4. Detect language
- Read first 5 (or next 5) pages of PDFs to detect most likely/common language.
- If HTM file, read entire plain text contents.
- Add an extra column to the `stats.csv` as `stats_lang.csv`
- Use Google Translate implementation.
- Return two letter language code, or '-1' if failed.
- Only for Europe dataset for now, ignores the 'GB' data within Europe for speed.
  - When trying this out, some GB files need to be skipped, have not yet identified which.
- Extend search to next 5 pages of PDF if language not found. 
- Does not look at metadata!
- UK: not written the equivalent for the UK data.

## Utililities
### utilCSR
Convertions etc., including dictionary of index code to country code.


### utilGetYearFromPDF
Interprets the first page of a PDF (or any text) and finds the most recent most frequent year.
- There is much room for improvement here!
- If the year is given as a range (either 2015-2016 or 2015-2016) this counts as the later year. Only works for ASCII hyphen.
- The any full year in a year range gets counted extra.
- Does not consider whitespace or word boundaries/tokens, ie 120178 would be picked up a year.
- If first page does not return a year, look at second, then third, then quit.

Includes a function to get the year from any CreationDate metadata field.

### utilGetYearFromHTM
Uses the same method as `utilGetYearFromPDF` (calls this script) 
but from the entire text with all HTML stripped out.

Includes a function to get a year from the `<head><title>` field, if present.


### utilReadExcelCSREurope
Reads in from the Excel tables of company indentifiers by country index. 

- Instantiates the Companies class with Company list. 
- This might be better as a DataFrame.

Format of Excel document:

- First sheet: "Summary". Not read by script, but the dictionary of country to index was used in utilCSR.py.
- Next 15 sheets: "1.AT" to "15.GB". Columns A:G contain:
  - BB Code, e.g. ANDR AV Equity
  - Name, e.g. ANDRITZ AG
  - Disclosure, to 4 decimal places
  - Country code for company, e.g. AT
  - ISIN, e.g. AT0000730007
  - SIC code, two digits.
  - SIC name, e.g. Industrials.
  
There were some companies in multiple indices, some companies not included, and one SIC code/name missing (given 99).

Gives special treatment to tickers with a forward slash '/' character, 
as the slash is not present in the report filenames that include company ticker.

### utilReadExcelCSRUK
Similar to `utilReadExcelCSREurope`, but for an extended UK list. If SIC is not available, give 99.
