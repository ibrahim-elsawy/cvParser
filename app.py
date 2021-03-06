from flask import Flask, request, Response, make_response, jsonify
import os
from waitress import serve
from config.configFile import Config
from middlewares.docxMiddleware import DocxMiddleware
from middlewares.imageMiddleware import ImageMiddleware

import threading

from utils.DataExtract import Extraction
from utils.convert import convert_pdf_to_docx, random_string_generator

ALLOWED_EXTENSIONS = {'docx', 'pdf'}
os.environ['ENV']= 'production'
app = Flask(__name__)
app.config['data_dir'] = os.environ.get("DATADIR")
# app.config['data_dir'] = "./data"

def delFile(filename):
	if os.path.exists(filename): 
		print(f'{filename} is deleted successfully.........')
		os.remove(filename) # one file at a time

def allowed_file(filename):
	extention = filename.rsplit('.', 1)[1].lower()
	return {
		"valid":'.' in filename and  extention in ALLOWED_EXTENSIONS,
		"type": extention
		}

@app.route('/image', methods=['POST'])
def imageSummary():
	if request.method == 'POST':
		try:
			req = request.get_json() 
			middleWare = ImageMiddleware(list(req['images']), Config) 
			res = middleWare() 
			return jsonify(res)
		except Exception as e:
			return Response(status=400)


@app.route('/file', methods=['POST'])
def fileSummary():
	if request.method == 'POST':
		try:
			# req = request.get_json()
			if 'file' not in request.files: 
				return Response(status = 400) 
			file = request.files['file'] 
			fileInfo = allowed_file(file.filename)
			if file and fileInfo['valid']: 
				fitzObject = None
				name = app.config["data_dir"] + "/" + random_string_generator()
				if fileInfo['type'] == 'pdf':
					filename = name + '.pdf'
					file.save(filename)
					convert_pdf_to_docx(name)
				else:
					filename = name + ".docx"
					file.save(filename)
				docxMiddleware = DocxMiddleware(filename, Config)
				res = docxMiddleware()
				# e = Extraction(name+".docx", fitzObject)
				# res = e.parseResume()
				# creating thread 
				t1 = threading.Thread(target=delFile, args=(name+".docx",)) 
				t2 = threading.Thread(target=delFile, args=(name+".pdf",)) 
				# starting thread 1 
				t1.start() 
				# starting thread 2 
				t2.start()
				return jsonify(res)
		except Exception as e:
			return Response(status=400)


@app.route('/test', methods=['GET'])
def text():
	if request.method == 'GET':
		try: 
			return 200
		except Exception as e:
			return 400


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	# name = "./data" + "/" + "test"
	# convert_pdf_to_docx(name)
	# e = Extraction(name+".docx") 
	# res = e.parseResume()
	# print(res)
	# app.run(host="0.0.0.0", port=port)
	serve(app, host="0.0.0.0", port=port)