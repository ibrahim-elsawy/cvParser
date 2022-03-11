import spacy
from sentence_transformers import SentenceTransformer
from scipy import spatial 


NLP = spacy.load("en_core_web_lg") 
SEMANTIC= SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

class TextProcesing():
	def __init__(self) -> None:
		pass

	
	def cleanText(self, text):
		doc = NLP(text)
		if len(doc.ents) == 0: return True
		geoList = list(filter(lambda ent : ent.label_=='GPE', doc.ents))
		numberList = list(filter(lambda ent : ent.label_=='CARDINAL', doc.ents))
		return True if len(geoList) == len(doc.ents) or len(numberList)==len(doc.ents) else False

	def sentence_similarity(self, w1, w2):
		embeddings = SEMANTIC.encode([w1, w2])
		res = 1 - spatial.distance.cosine(embeddings[0], embeddings[1])
		return True if res > 0.5 else False


	# def getScore(self, query, docs): 
	# 	# Encode query and documents 
	# 	query_emb = model.encode(query) 
	# 	doc_emb = model.encode(docs) 
	# 	# Compute dot score between query and all document embeddings 
	# 	scores = util.dot_score(query_emb, doc_emb)[0].cpu().tolist() 
	# 	# Combine docs & scores 
	# 	doc_score_pairs = list(zip(docs, scores)) 
	# 	# Sort by decreasing score 
	# 	doc_score_pairs = sorted(doc_score_pairs, key=lambda x: x[1], reverse=True) 
	# 	# Output passages & scores 
	# 	for doc, score in doc_score_pairs: 
	# 		print(score, doc)

	
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


