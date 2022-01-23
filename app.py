from flask import Flask, request, jsonify
import os
# from waitress import serve


from utils.DataExtract import Extraction
from utils.convert import convert_pdf_to_docx, random_string_generator

ALLOWED_EXTENSIONS = {'docx', 'pdf'}
# os.environ['ENV']= 'production'
app = Flask(__name__)
# app.config['data_dir'] = os.environ.get("DATADIR")
app.config['data_dir'] = "./data"


def allowed_file(filename):
	extention = filename.rsplit('.', 1)[1].lower()
	return {
		"valid":'.' in filename and  extention in ALLOWED_EXTENSIONS,
		"type": extention
		}


@app.route('/summary', methods=['POST'])
def summary():
	if request.method == 'POST':
		try:
			# req = request.get_json()
			if 'file' not in request.files: 
				return 400 
			file = request.files['file'] 
			fileInfo = allowed_file(file.filename)
			if file and fileInfo['valid']: 
				name = app.config["data_dir"] + "/" + random_string_generator()
				if fileInfo['type'] == 'pdf':
					filename = name + '.pdf'
					file.save(filename)
					convert_pdf_to_docx(name)
				else:
					filename = name + ".docx"
					file.save(filename)
				e = Extraction(name+".docx")
				res = e.parseResume()
				return jsonify(res)
		except Exception as e:
			return 400


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
	app.run(host="0.0.0.0", port=port)
	# serve(app, host="0.0.0.0", port=port)