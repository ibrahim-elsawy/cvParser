from re import search
from docx import Document
from docx.enum.style import WD_STYLE_TYPE, WD_STYLE

from utils.Database import Database
from utils.brain import TextProcesing

from .docxUtils import DocxUtils


class Extraction():
	def __init__(self, filename:str) -> None:
		self.filename = filename
		self.doc = Document(self.filename)
		self.dx = DocxUtils(self.filename)
		self.data = Database('Resume.db')
		self.process = TextProcesing()
		pass

	def extractHeaders(self):
		fontHeader = self.dx.getHeaderFont()
		headers = []
		for p in self.doc.paragraphs:
			if p.style.font.size == fontHeader:
				headers.append(p.text)
		return headers
	def extractSectionOfHeader(self):
		sectionOfHeaders = {}
		searches= self.data.read('points')
		headers = self.dx.searchDoc(listOfSearch=searches,listOfParagraph=self.doc.paragraphs, numRows=13)
		for i, header in enumerate(headers):
			sectionOfHeaders[header[0]] = [] if header[0] not in sectionOfHeaders else sectionOfHeaders[header[0]]
			if i == len(headers)-1:
				for index in range(header[1], len(self.doc.paragraphs)): 
					if header[0]!='info' and not self.process.cleanText(self.doc.paragraphs[index].text): 
						sectionOfHeaders[header[0]].append(self.doc.paragraphs[index].text)
				continue
			for index in range(header[1]+1, headers[i+1][1]):
				if header[0]!='info' and not self.process.cleanText(self.doc.paragraphs[index].text): 
					sectionOfHeaders[header[0]] += [self.doc.paragraphs[index].text]
		return sectionOfHeaders
	
	def parseResume(self):

		#FIXME summary is hardcoded !!!!!!!!!!!!
		
		data = self.extractSectionOfHeader()
		if 'info' not in data:
			phones, emails, links = self.dx.getInfo(self.doc.paragraphs)
			data['info'] = emails + links + phones
			return data
		return data