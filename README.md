# CSR_BB_Europe
Rearrange the CSR reports from Bloomberg on European companies.

## Contents
Various stages below.
1. Unzip to country folders
2. Find year and rearrange 
3. Rearrange files

Also 0. testing

## Summary
### 1. Unzip to country folders
- Unzip all reports so far. One folder per country (index). 
- All years and report types mixed up. 
- Can't use given year in filenames (this is upload date, not report date).
- Output format:
	- folder per country (2-digit ISO)
	- filename: unchanged. UPLOADDATE\_TICKER\_OTHER.pdf where UPLOADDATE is YYMMDD

### 2. Find year
- Per country, read first page of PDF to determine year. (Takes a few hours.)
- What about .htm files? Or .txt files? Most (98%) are .pdf format, so ignore.

### 3. Rearrange
- Create new filenames and copy the files. 
- Reads the Bloomberg Excel identifiers workbook to get ISIN, SIC (matching on Ticker).
- Reads a CSV file of country, file, year
- Output format:
	- folder per country (2-digit ISO), folder per year (or -2 unfound, -1 encrypted)
	- filename: SIC\_ISIN\_TYPEn.pdf where TYPE is CR and _n_ is number for multiple reports
	
## Utililities
### utilCSR
Convertions etc., including dictionary of index code to country code.


### utilGetYearFromPDF
Interprets the first page of a PDF (or any text) and finds the most recent most frequent year.
- There is much room for improvement here!
- If the year is given as a range (either 2015-2016 or 2015-2016) this counts as the later year. Only works for ASCII hyphen.
- The any full year in a year range gets counted extra.
- Does not consider whitespace or word boundaries/tokens, ie 120178 would be picked up a year.


### utilReadExcelCSREurope
Reads in from the Excel tables of company indentifiers by country index. 

- Instantiates the Companies class with Company list. 
- This might be better as a DataFrame.
