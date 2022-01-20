import spacy



class TextProcesing():
	def __init__(self) -> None:
		self.nlp = spacy.load("en_core_web_lg")
	
	def cleanText(self, text):
		doc = self.nlp(text)
		if len(doc.ents) == 0: return True
		geoList = list(filter(lambda ent : ent.label_=='GPE', doc.ents))
		numberList = list(filter(lambda ent : ent.label_=='CARDINAL', doc.ents))
		return True if len(geoList) == len(doc.ents) or len(numberList)==len(doc.ents) else False
			