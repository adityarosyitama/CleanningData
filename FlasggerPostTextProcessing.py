import re
#import file

from flask import Flask, jsonify
#file akan diolah dengan flask

app = Flask(__name__)
#memanggil flask dengan command

from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
from flask import Response
#memanggil library

app.json_encoder = LazyJSONEncoder
swagger_template = dict (
info = {
        'title': LazyString(lambda: 'API Documentation for Data Processing and Modeling'),
        'version': LazyString(lambda: '1.0.0'),
        'description': LazyString(lambda: 'Dokumentasi API untuk Data Processing and Modeling'),
        },
        host = LazyString(lambda: request.host)
)
#title, version dan description dari dokumentasi API

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger = Swagger(app, template=swagger_template, 
                    config=swagger_config)
#configuration dari swagger

@swag_from('text_processing.yml', methods=['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():

    text = request.form.get('text')
    #masukkan text

    return text
    #memanggil text yang sudah diberikan dari tanda baca

@swag_from('file_processing.yml', methods=['POST'])
@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['file']
    #upload file

    file_text = re.sub(r'[^a-zA-Z,]', ' ', file.read().decode())
    file_text = re.sub(r'[^a-zA-Z,]{5}', ' ', file_text)
    #menghilangkan tanda baca pada file

    return file_text
    #memanggil text yang sudah diberikan dari tanda baca pada kolom response

if __name__ == '__main__':
    app.run()
