from algorithm.textAlgo import TextAlgo
from algorithm.tokenAlgo import TokenAlgo
from processing.docxProcessing import DocxProcessing
from processing.imageProcessing import ImageProcessing
from processing.pdfProcessing import PdfProcessing


class Config():
	def __init__(self) -> None:
		self.CONFIG = {
			"processing" : {
				"image" : ImageProcessing,
				"docx": DocxProcessing,
				"pdf": PdfProcessing,
			},
			"algorithm" : [TextAlgo, TokenAlgo],
		}

	def __call__(self, type:str):
		if type == 'image':
			return self.CONFIG["processing"]["image"], self.CONFIG["algorithm"]
		return self.CONFIG["processing"]["docx"], self.CONFIG["algorithm"]