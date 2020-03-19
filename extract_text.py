
############# Point 1

# importing libraries 
  
import os
import sys
import os, os.path 
import re
import codecs
import string
import subprocess
import unicodedata
import time
from io import StringIO

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter


## Set important paths
pdf_path = sys.argv[1]
DOCS_PDF = os.path.join(os.getcwd(), pdf_path)
def get_pdf_docs(path=DOCS_PDF):
	"""
	Returns a filtered list of paths to PDF files
	"""
	for name in os.listdir(path):
		if name.endswith('.pdf'):
			yield os.path.join(path, name)
def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text
## Create a path to extract the corpus.
extract = os.path.join(os.getcwd(), "extract")

def extract_pdf_corpus(DOCS_PDF=DOCS_PDF, corpusval=extract):
	"""
	Extracts a text from the PDF documents 
	"""
	# Create corpus directory if it doesn't exist.
	if not os.path.exists(corpusval):
		os.mkdir(corpusval)
	# For each PDF path, use pdf2txt to extract the text file.
	for path in get_pdf_docs(DOCS_PDF):
		# # Write the document out to the  directory extract
		filen = os.path.splitext(os.path.basename(path))[0] + ".txt"
		outp = os.path.join(corpusval, filen)

		document = convert_pdf_to_txt(path)
		document=document.replace('\n',' ')
		document=document.replace('\r',' ')
		document=document.replace(',',' ')
		document=document.replace('-',' ')
		document=document.replace(':',' ')
		document=document.replace('\/',' ')
		with codecs.open(outp, 'w', encoding='utf-8', errors='ignore') as f:
			f.write(document)
# Run the extraction
extract_pdf_corpus()


