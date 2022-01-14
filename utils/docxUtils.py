from functools import reduce
from docx import Document
from docx.enum.style import WD_STYLE_TYPE, WD_STYLE




class DocxUtils():
	def __init__(self, filename) -> None: 
		self.filename = filename
		self.doc = Document(self.filename)

	def getFonts(self):
		fonts = set()
		for p in self.doc.paragraphs:
			fonts.add(p.style.font.size)
		return fonts
	
	def getFontOfEducation(self):
		for p in self.doc.paragraphs:
			if p.text.lower() == "education":
				return p.style.font.size
		return None

	def getHeaderFont(self):
		fonts = self.getFonts()
		educationFont = self.getFontOfEducation()
		for font in fonts:
			if font == educationFont:
				return font
		return None
	def getCapitalWords(self):
		headers = []
		for p in self.doc.paragraphs:
			if p.text.isupper():
				headers.append(p.text)
		return headers

	def searchDoc(self, listOfSearch:list, listOfParagraph:list, numRows:int):
		headers = []
		index = range(numRows)
		for indexOfPara, p in enumerate(listOfParagraph):
			if p.text == '':
				continue
			for i in index: 
				# header = list(filter(lambda e: isinstance(e, str) and e in p.text.lower() and len(p.text.split(' ')) < 3, listOfSearch[i]))
				try:
					header = list(filter(lambda e: isinstance(e, str) and e == p.text.lower(), listOfSearch[i]))[0] 
					headers.append([header,indexOfPara])
				except IndexError:
					continue
		return headers
