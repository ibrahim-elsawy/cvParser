from typing import Any
import base64
from PIL import Image
import io


# from config.configFile import Config


class ImageMiddleware():
	def __init__(self, imagesEnc, config) -> None:
		self.imagesEnc = imagesEnc
		self.config = config()


	def __call__(self, *args: Any, **kwds: Any) -> Any:

		data = []
		pdfProcessing = self.config.CONFIG["processing"]["image"]()
		for i, imgEnc in enumerate(self.imagesEnc):
			image_bytes = base64.decodestring(imgEnc)
			img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
			data = data + pdfProcessing.process(img)



		# algo = self.config.CONFIG["algorithm"][1]()
		# res = algo.apply(data)
		# algo = self.config.CONFIG["algorithm"][0](links)
		# res = algo.apply(data)
		# if res:
		# 	return res


		#call pdfMiddleware to apply token algo on the pdf as docx algo failed 
		algo = self.config.CONFIG["algorithm"][1]()
		res = algo.apply(data) 
		return res	