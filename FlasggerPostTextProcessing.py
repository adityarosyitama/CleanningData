import re

from flask import Flask, jsonify

app = Flask(__name__)

from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from


app.json_encoder = LazyJSONEncoder
swagger_template = dict (
info = {
        'title': LazyString(lambda: 'API Documentation for Data Processing and Modeling'),
        'version': LazyString(lambda: '1.0.0'),
        'description': LazyString(lambda: 'Dokumentasi API untuk Data Processing and Modeling'),
        },
        host = LazyString(lambda: request.host)
)
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

@swag_from('text_processing.yml', methods=['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():

    text = request.form.get('text')

    json_response = {
        'status_code': 200,
        'description': "Text yang sudah diproses",
        'data': re.sub(r'[^a-zA-Z0-9]', '', text),
    }

    response_data = jsonify(json_response)
    return response_data

@swag_from('file_processing.yml', methods=['POST'])
@app.route('/upload', methods=['POST'])
def upload():

    # Get the uploaded file from the request
    file = request.files['file']
    
    # Read the contents of the file into a string
    file_contents = file.read()
    
    # Remove non-text characters from the string
    file_contents = re.sub(r'[^a-zA-Z0-9]', '', file_contents)
    
    # Create a new file object in write mode
    new_file = open('cleaned_file.txt', 'w')
    
    # Write the modified string to the new file object
    new_file.write(file_contents)
    
    # Close both the original file object and the new file object
    file.close()
    new_file.close()
    
    return 'File successfully uploaded and cleaned!'
    
if __name__ == '__main__':
    app.run()