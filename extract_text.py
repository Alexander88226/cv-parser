
############# Point 1

# importing libraries 
import os, os.path 
  
import os
import re
import codecs
import string
import subprocess
import unicodedata
import time
## Set important paths
DOCS_PDF = os.path.join(os.getcwd(), "cv documents")
print(os.getcwd())
def get_pdf_docs(path=DOCS_PDF):
	"""
	Returns a filtered list of paths to PDF files
	"""
	print(path)
	for name in os.listdir(path):
		if name.endswith('.pdf'):
			yield os.path.join(path, name)
#total number documents
print(len(list(get_pdf_docs())))

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
		# Call the subprocess command (must be on your path)
		tp=os.path.join(os.getcwd(), 'my_pdf2txt.py')
		document = subprocess.check_output(
			['python',tp, path]
		)
		time.sleep(1)


		# Write the document out to the  directory extract
		filen = os.path.splitext(os.path.basename(path))[0] + ".txt"
		outp = os.path.join(corpusval, filen)
		# print(document)
		############# Point 3

		document=document.decode("utf-8") 
		document=document.replace('\n',' ')
		document=document.replace('\r',' ')
		document=document.replace(',',' ')
		document=document.replace('-',' ')
		document=document.replace(':',' ')
		
		document=str(document)

		############# Point 4

		# document=document.encode("utf-8") 
		document=str(document)

		with codecs.open(outp, 'w', encoding='utf-8', errors='ignore') as f:
			f.write(document)
# Run the extraction
extract_pdf_corpus()
