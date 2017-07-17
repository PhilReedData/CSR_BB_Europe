# CSR_BB_Europe
Analyse the CSR reports from Bloomberg on European companies.

## Contents
Various stages below.
1. Unzip to country folders
2. Find year and rearrange 

Also 0. testing

## Summary
### 1. Unzip to country folders
- Unzip all reports so far. One folder per country (index). 
- All years and report types mixed up. 
- Can't use given year in filenames (this is upload date, not report date).

### 2. Find year and rearrange 
- Per country, read first page of PDF to determine year. 
- Move that file to year folder within country.
- What about .htm files? Or .txt files? Most (98%) are .pdf format.

## Utililities
### utilCSR
Convertions etc.

### utilReadExcelCSREurope
Reads in from the Excel tables of company indentifiers by country index. 
Instantiates the Companies class with Company list.