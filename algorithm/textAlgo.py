from ._algorithm import *
from utils.Database import Database
import re
import spacy
from sentence_transformers import SentenceTransformer


NLP = spacy.load("en_core_web_lg") 
SEMANTIC= SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


class TextAlgo(AlgorithmBase):

	def __init__(self, links) -> None: 
		super().__init__()
		self.data = Database('Resume.db')
		self.links = links


	def searchDoc(self, listOfSearch:list, listOfParagraph:list, numRows:int):
		headers = []
		index = range(numRows)
		for indexOfPara, p in enumerate(listOfParagraph):
			if p.text == '': 
				continue

			for i in index: 
				# header = list(filter(lambda e: isinstance(e, str) and e in p.text.lower() and len(p.text.split(' ')) < 4, listOfSearch[i]))
				try:
					# header = list(filter(lambda e: isinstance(e, str) and e == p.text.lower(), listOfSearch[i]))[0] 
					# headers.append([header,indexOfPara])
					headers += self.getHeader(listOfSearch[i], p.text, indexOfPara, headers)
				except IndexError:
					continue
		return headers
	
	def getHeader(self,listOfSearch:list, text:str, indexOfText:int, headers:list):
		_headers = []
		colNames = self.data.getColumnsNames("points")
		for i, e in enumerate(listOfSearch):
			if isinstance(e, str) and e in text.lower().strip() and len(text.strip().split(' ')) < 3 and self.isHeaderExist(indexOfText, headers):
				_headers.append([colNames[i].strip(), indexOfText])
		return _headers
	
	def isHeaderExist(self, currentIndex:int, headers:list):
		for e in headers:
			if currentIndex == e[1]:
				return False
		return True
	def cleanText(self, text):
		doc = NLP(text)
		if len(doc.ents) == 0: return True
		geoList = list(filter(lambda ent : ent.label_=='GPE', doc.ents))
		numberList = list(filter(lambda ent : ent.label_=='CARDINAL', doc.ents))
		return True if len(geoList) == len(doc.ents) or len(numberList)==len(doc.ents) else False

	def summ(self, paragraphs,headers):
		data = []
		for i in range(0,len(paragraphs)): 
			txt1= NLP(paragraphs[i].text) 
			if len(txt1.ents)!=0 and txt1.ents[0].label_ == "PERSON" and i != headers[1]-1:
				for e in paragraphs[i+1 : headers[1]]:
					if e.text != "":
						data.append(e.text)
				# return list(filter(lambda e : e != "", paragraphs[i+1:headers[1]]))
		return data


	# def cleanText(self, text):
	# 	return re.sub('[^A-Za-z0-9\@\-\.\,\(\)\[\]\"\'\:\#\*\+\%\ ]+', ' ', text)
	
	def getLink(self):
		# link = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
		l = []
		
		for key in self.links.keys():
			if self.links[key].is_external:
				l.append(self.links[key]._target)
		return l
	
	def getEmail(self, text):
		email = re.compile(r'[a-z0-9\.\-+_\:\/]+@[a-z0-9\.\-+_]+\.[a-z]+')
		return re.findall(email, text)

	def getPhone(self, text):
		phone = re.compile('\+?[0-9\ \-]{12,20}')
		return re.findall(phone, text)

	def getInfo(self, listOfParagraph:list):
		phones = []
		emails = []
		links = []
		for p in listOfParagraph:
			phone = self.getPhone(p.text)
			email = self.getEmail(p.text)
			# link = self.getLink(p.text)
			phones = phones+phone if len(phone)!=0 else phones
			emails = emails+email if len(email)!=0 else emails
			# links = links+link if len(link)!=0 else links
		links = self.getLink()
		return phones, emails, links

	#overriding the algorithmbase
	def apply(self, data):
		'''
			Args:
				data list(Paragraphs): list of paragraphs 
		'''
		sectionOfHeaders = {}
		searches= self.data.read('points')
		headers = self.searchDoc(listOfSearch=searches,listOfParagraph=data, numRows=13)
		for i, header in enumerate(headers):
			sectionOfHeaders[header[0]] = [] if header[0] not in sectionOfHeaders else sectionOfHeaders[header[0]]
			if i == len(headers)-1:
				for index in range(header[1], len(data)): 
					if header[0]!='info' and not self.cleanText(data[index].text): 
						sectionOfHeaders[header[0]].append(data[index].text.strip())
					if header[0]=="info": 
						sectionOfHeaders[header[0]] += [data[index].text.strip()]
				continue
			for index in range(header[1]+1, headers[i+1][1]):
				if header[0]!='info' and not self.cleanText(data[index].text): 
					sectionOfHeaders[header[0]] += [data[index].text.strip()]
				if header[0] == 'info': 
					sectionOfHeaders[header[0]] += [data[index].text.strip()]

		dataFinal, header = sectionOfHeaders, headers[0] if len(headers)>0 else None
		if len(list(dataFinal.keys()))<2 or header == None: 
			# dataFinal, header = self.extractSectionOfHeadersV2()
			return False
		if 'info' not in dataFinal:
			phones, emails, links = self.getInfo(data)
			dataFinal['info'] = emails + links + phones
			dataFinal['info'] = list(filter(lambda x : x.strip()!="", dataFinal['info']))
		if 'summary' not in dataFinal:
			summList = self.summ(data, header)
			dataFinal['summary'] = summList
		return dataFinal