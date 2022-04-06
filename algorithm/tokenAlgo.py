from ._algorithm import *
from utils.Database import Database
import re
import spacy
from sentence_transformers import SentenceTransformer
from scipy import spatial 


NLP = spacy.load("en_core_web_lg") 
SEMANTIC= SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')



class TokenAlgo(AlgorithmBase): 

	def __init__(self) -> None: 
		super().__init__()
		self.data = Database('Resume.db') 
		self.TABLENAME = "points"


	def sentence_similarity(self, w1, w2):
		embeddings = SEMANTIC.encode([w1, w2])
		res = 1 - spatial.distance.cosine(embeddings[0], embeddings[1])
		return True if res > 0.5 else False

	def getQueries(self):
		query = []
		colNames = self.data.getColumnsNames(self.TABLENAME)
		colNames.pop(0)
		# for col in colNames: 
		# 	values = self.data.readColumn(self.TABLENAME, col)
		# 	q = ", ".join(values)
		# 	query.append(q)
		query = [
			"skills: Html, css",
			"experience, work history",
			"characteristics: team worker, Time management",
			"summary, objective, overview",
			"education: graduated college",
			"hobbies",
			"info, contact"
		]
		return colNames, query

	#overriding the algorithmbase
	def apply(self, data):
		words = []
		for p in data:
			words += p.text.strip().split(' ')
		colNames, queries = self.getQueries()
		# words = self.dx.getWords()
		sectionOfHeader = {}
		isHeader = False
		for word in words: 
			for index, q in enumerate(queries): 
				isHeader = self.sentence_similarity(word,q) 
				if isHeader: break
			if isHeader:
				sectionOfHeader[colNames[index]] = sectionOfHeader[colNames[index]]+" " + word if colNames[index] in sectionOfHeader else ""
			elif len(list(sectionOfHeader.keys())) > 0: 
				header = list(sectionOfHeader.keys())[-1] 
				sectionOfHeader[header] += " " + word
		# return sectionOfHeader, sectionOfHeader[list(sectionOfHeader.keys())[0]] if len(sectionOfHeader.keys())>0 else None
		return sectionOfHeader, sectionOfHeader[list(sectionOfHeader.keys())[0]] 
