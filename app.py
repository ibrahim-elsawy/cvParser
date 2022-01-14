from pdf2docx import parse
from typing import Tuple
import aspose.words as aw
from docx import Document
from docx.enum.style import WD_STYLE_TYPE, WD_STYLE

from utils.DataExtract import Extraction
from utils.Database import Database
from utils.docxUtils import DocxUtils

document = Document("r.docx")
e = Extraction('./rdx.docx')
dx = DocxUtils('./rdx.docx')
d = Database("Resume.db")
# d.createTable('points')
# d.insert(table_name='points',skill='skis', charac='soft skills', experience='expence')

# print(e.extractHeaders())
l = d.read('points')
rows = d.getNumRows("points")
print(dx.searchDoc(l,document.paragraphs, rows))
print(e.extractSectionOfHeader())
# print(dx.getCapitalWords())
print("finished!!!!!!!!!!!!!!!!!!")
