#!/usr/bin/python    

# convert pdf to txt

import PyPDF2
import codecs

pdf_filenames = [
    "030209_VOD_Corporate_Responsibility1_WD000000001976806596.pdf",
    "031815_GIVN_Corporate_Responsibility_SD000000002200745235.pdf",
    "031815_TIE1V_Corporate_Responsibility_SD000000002200709097.pdf",
    "031816_BAER_Corporate_Responsibility_SD000000002262799802.pdf",
    "031816_SAND_Corporate_Responsibility_WC000000002261108619.pdf",
    "031817_LSE_Corporate_Responsibility_SD000000002337989856.pdf",
    "031912_TW_Corporate_Responsibility_US000000002046000028.pdf",
    "031913_SHP_Corporate_Responsibility_WC000000002082122524.pdf",
    "031914_GSK_Corporate_Responsibility_US000000002131640555.pdf",
    "032009_BTA_Corporate_Responsibility1_SD000000001978367580.pdf"
]

pdf_dir = "U:/Phil_Read/fromIrina/2017-11-08/pdf/"
txt_dir = "U:/Phil_Read/fromIrina/2017-11-08/python_txt/"

def getTextContentOfPdf(path):
    content = ""
    p = file(path, "rb")
    pdf = PyPDF2.PdfFileReader(p)
    for i in range(0, pdf.getNumPages()):
        content += pdf.getPage(i).extractText() + "\n"
    content = " ".join(content.replace(u"\xa0", " ").strip().split())
    return content
	
for filename in pdf_filenames:
    print("Reading " + filename)
    # should use os.join instead of dir+file
    text = getTextContentOfPdf(pdf_dir + filename)
    codecs.open(txt_dir+filename+'.txt', 'w', encoding='utf8', errors='ignore').write(text)
    print("Written " + filename)
    print("")
    
