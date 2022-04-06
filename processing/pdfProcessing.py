from ._processing import *
import pytesseract as pt
from PIL import Image
import io
import fitz
from pdf2image import convert_from_path


class PdfProcessing(ProcessBase):
	'''
	Args:
                data (str): string name of the file in the data Dir
	Outputs:
                formalRes list(Paragraph): text list for applying algorithm 
        '''

	#overriding abstract method for image process 
	def process(self, data): 
		formalRes = []
		images = self.getImagesFitz(data)
		if len(images) == 0:
			images = self.getImagesScreenshot(data)
		for image in images: 
			extracted = pt.image_to_string(image) 
			sentance = extracted.split('\n') 
			cleanedSentance = list(filter( lambda x: x.strip()!='', sentance)) 
			formalRes = formalRes + list(map(lambda x : Paragraph(x), cleanedSentance))
		return formalRes


	def getImagesFitz(self, filename):
		fitzObject = fitz.open(filename)
		images = []
		for page_index in range(len(fitzObject)): 
			# get the page itself 
			page = fitzObject[page_index] 
			image_list = page.getImageList() 
			# printing number of images found in this page
			images = images + image_list
			for image_index, img in enumerate(page.getImageList(), start=1): 
				# get the XREF of the image
				xref = img[0] 
				# extract the image bytes
				base_image = fitzObject.extractImage(xref) 
				image_bytes = base_image["image"] 
				# img = Image.frombytes("RGB", (128, 128), image_bytes)
				img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
				images.appened(img)
		return images

	def getImagesScreenshot(self, filename):
		images = convert_from_path(filename)
		return images



# if __name__ == '__main__':
# 		print("finished")
