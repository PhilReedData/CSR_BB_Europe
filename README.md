# CSR_BB_Europe
Rearrange the CSR reports from Bloomberg on European companies.

## Contents
Run the stages in the order below.
1. Unzip to country folders
2. Find year and rearrange 
3. Rearrange files
4. Detect language

Also 0. testing

## Summary
There is a script for the Europe dataset 
and a similar script for the extended UK dataset for each step.

### Step 1. Unzip to country folders
- Unzip all reports so far. One folder per country (index). 
- All years and report types mixed up. 
- Can't use given year in filenames (this is upload date, not report date).
- Output format:
	- folder per country (2-digit ISO)
	- filename: unchanged. UPLOADDATE\_TICKER\_OTHER.pdf where UPLOADDATE is MMDDYY

### Step 2. Mine the year
- Per country, read first page of PDF to determine year. (Takes a few hours.)
- If not found in first page, look in second, then third, then give up.
- What about .htm files? Or .txt files? Most (98%) are .pdf format for Europe.
  - Also copy the .htm files for UK script (will add this feature to Europe).

### Step 2a. Fill year gaps
- As well as mined year (above), get year from metadata in report, and from date of upload in filename.
- (For UK for now, will implement for Europe soon...)
- Choose the best year based on:
  - Use metadata year, if found
  - Else use mined year, if found
  - Else report -1
- Keep bestyear, minedyear, metadatayear and upload year, plus yearsource...
  - yearsource explains which year was chosen for bestyear
  - 10 for metadatayear, 20 for minedyear, -1 for no year.

### Step 3. Rearrange
- Create new filenames and copy the files. 
- Reads the Bloomberg Excel identifiers workbook to get ISIN, SIC (matching on Ticker).
- Reads a CSV file of country, file, year
- Output format:
	- folder per country (2-digit ISO), folder per year (or -2 unfound, -1 encrypted)
	- filename: SIC\_ISIN\_TYPEn.pdf where TYPE is CR and _n_ is number for multiple reports
	
### Step 4. Detect language
- Read first 5 pages of PDFs to detect most likely/common language.
- Add an extra column to the stats.csv as stats_lang.csv
- Use Google Translate implementation.
- Return two letter language code, or '-1' if failed.
- Only for Europe dataset for now, ignores the 'GB' data for speed.
  - Some GB files need to be skipped, have not yet identified which.


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
Uses the same method as utilGetYearFromPDF (calls this script) 
but from the entire text with all HTML stripped out.

Includes a function to get a year from the <head><title> field, if present.


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
Similar to utilReadExcelCSREurope, but for an extended UK list. If SIC is not available, give 99.
