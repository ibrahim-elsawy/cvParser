import spacy



class TextProcesing():
	def __init__(self) -> None:
		self.nlp = spacy.load("en_core_web_sm")
	
	def cleanText(self, text):
		doc = self.nlp(text)
		if len(doc.ents) == 0: return True
		geoList = list(filter(lambda ent : ent.label_=='GPE', doc.ents))
		numberList = list(filter(lambda ent : ent.label_=='CARDINAL', doc.ents))
		return True if len(geoList) == len(doc.ents) or len(numberList)==len(doc.ents) else False
	
	def summ (self, paragraphs,headers):
		data = []
		for i in range(0,len(paragraphs)): 
			txt1= self.nlp(paragraphs[i].text) 
			if len(txt1.ents)!=0 and txt1.ents[0].label_ == "PERSON" and i != headers[1]-1:
				for e in paragraphs[i+1 : headers[1]]:
					if e.text != "":
						data.append(e.text)
				# return list(filter(lambda e : e != "", paragraphs[i+1:headers[1]]))
		return data


