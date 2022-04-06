from ._processing import *
from docx import Document


class DocxProcessing(ProcessBase):
	'''
	Args:
                data (str): string name of the file in the data Dir
	Outputs:
                formalRes list(Paragraph): text list for applying algorithm 
        '''

	#overriding abstract method for image process 
	def process(self, data):
		self.doc = Document(data.replace('pdf','docx'))
		return self.doc.paragraphs, self._getRels()


	def _getRels(self):
		return self.doc.part.rels