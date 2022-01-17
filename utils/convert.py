from pdf2docx import parse
from typing import Tuple
import aspose.words as aw
import random
import string

# input_file = 'zeinab_CV.pdf'
# output_file = 'cv.docx'
# result = parse(pdf_file=input_file, docx_with_path=output_file)
# summary = { "File": input_file, "Output File": output_file }
# # Printing Summary
# print("## Summary ########################################################")
# print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
# print("###################################################################")

def random_string_generator(): 
    chars = string.ascii_letters + string.punctuation
    size = 12
    return ''.join(random.choice(chars) for x in range(size))



def convert_pdf_to_docx(filename): 
    # load the PDF file 
    doc = aw.Document(filename+".pdf") 
    # convert PDF to Word DOCX format 
    doc.save(filename+".docx")