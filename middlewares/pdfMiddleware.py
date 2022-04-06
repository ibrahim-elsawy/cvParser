from typing import Any

# from config.configFile import Config


class PdfMiddleware():
	def __init__(self, filename, config) -> None:
		self.filename = filename
		self.config = config()

	def __call__(self, *args: Any, **kwds: Any) -> Any:
		links = kwds.get('links')
		pdf = self.config.CONFIG["processing"]["pdf"]()
		data = pdf.process(self.filename)
		algo = self.config.CONFIG["algorithm"][0](links)
		res = algo.apply(data)
		return res	