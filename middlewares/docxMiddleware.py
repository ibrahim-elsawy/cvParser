from typing import Any

from middlewares.pdfMiddleware import PdfMiddleware

# from config.configFile import Config


class DocxMiddleware():
	def __init__(self, filename, config) -> None:
		self.filename = filename
		self._config = config
		self.config = config()

	def __call__(self, *args: Any, **kwds: Any) -> Any:
		doc = self.config.CONFIG["processing"]["docx"]()
		data, links = doc.process(self.filename)
		algo = self.config.CONFIG["algorithm"][0](links)
		res = algo.apply(data)
		if res:
			return res


		#call pdfMiddleware to apply token algo on the pdf as docx algo failed
		pdfMiddleware = PdfMiddleware(self.filename, self._config)
		res = pdfMiddleware(links=links)
		return res
