from ._processing import *
import pytesseract as pt

class ImageProcessing(ProcessBase):

	#overriding abstract method for image process 
	def process(self, data):
		"""
			Args: 
				data (Image.PIL.object):  image object 
			Outputs: 
				formalRes list(Paragraph): text list for applying algorithm
		"""
		extracted = pt.image_to_string(data)
		sentance = extracted.split('\n')
		cleanedSentance = list(filter( lambda x: x.strip()!='', sentance))
		formalRes = list(map(lambda x : Paragraph(x), cleanedSentance))
		return formalRes


