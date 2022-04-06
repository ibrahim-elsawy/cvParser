import fitz
from PIL import Image
import io


class test():
	def __init__(self, filename):
		self.fitzObject = fitz.open(filename)	
	def getTextFromImage(self):
		# iterate over PDF pages 
		for page_index in range(len(self.fitzObject)): 
			# get the page itself 
			page = self.fitzObject[page_index] 
			image_list = page.getImageList() 
			# printing number of images found in this page
			if image_list: 
				print(f"[+] Found a total of {len(image_list)} images in page {page_index}") 
			else: 
				print("[!] No images found on page", page_index) 
			for image_index, img in enumerate(page.getImageList(), start=1): 
				# get the XREF of the image
				xref = img[0] 
				# extract the image bytes
				base_image = self.fitzObject.extractImage(xref) 
				image_bytes = base_image["image"] 
				# img = Image.frombytes("RGB", (128, 128), image_bytes)
				img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
				img.save("im.jpeg")
t = test("test2.pdf")
t.getTextFromImage()
