#import file
import re
import pandas as pd
import csv
import flask_swagger
import sqlite3
import string

#file akan diolah dengan flask
from flask import Flask, jsonify

#memanggil flask dengan command
app = Flask(__name__)

#memanggil library
from flask import request, Response, make_response, send_file
from flasgger import Swagger, LazyString, LazyJSONEncoder,swag_from
from flask_swagger import swagger
from pandas import DataFrame

#title, version dan description dari dokumentasi API
app.json_encoder = LazyJSONEncoder
swagger_template = dict (
info = {
        'title': LazyString(lambda: 'API Documentation for Data Processing and Modeling'),
        'version': LazyString(lambda: '1.0.0'),
        'description': LazyString(lambda: 'Dokumentasi API untuk Data Processing and Modeling'),
        },
        host = LazyString(lambda: request.host)
)

#configuration dari swagger
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
@app.route('/Text Processing', methods=['POST'])
def text_processing():

    #masukkan text
    text = request.form.get('text')
    
    #membersihkan text
    text: re.sub(r'[^a-zA-Z]', ' ', text)

    #memanggil text yang sudah diberikan dari tanda baca
    return text

@swag_from('file_processing.yml', methods=['POST'])
@app.route('/File Processing', methods=['POST'])
def upload():
    file = request.files['file']
    df = pd.read_csv(file)
    df = df.dropna()
    df['Tweet'] = df['Tweet'].str.replace(r'[^\w\s]','')
    df['Tweet'] = df['Tweet'].str.replace("\d", ' ')
    df['Tweet'] = df['Tweet'].apply(lambda x: ' '.join([word for word in x.split() if len(word) >= 5]))
    df['Tweet'] = df['Tweet'].str.replace('  ', ' ')  

    csv = df.to_csv(index=False)

    # Create a Flask response object
    response = make_response(csv)

    # Set the content type to CSV
    response.headers['Content-Type'] = 'text/csv'

    # Set the response headers to include the file name
    response.headers['Content-Disposition'] = 'attachment; filename=data.csv'

    return response

@swag_from('upload_sqlite.yml', methods=['POST'])
@app.route('/Upload SQLITE', methods=['POST'])
def uploadsqlite():

    # Connect to the database
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    
    # Get the uploaded file
    file = request.files['file']
    
    # Check if the file is a CSV
    if file.filename.split('.')[-1] != 'csv':
        return 'File is not a CSV'
    
    # Parse the CSV file
    csv_reader = csv.reader(file)
    
    # Insert each row into the database
    for row in csv_reader:
        cursor.execute("INSERT INTO my_table (col1, col2, col3) VALUES (?, ?, ?)", row)
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
    return 'CSV file successfully inserted into the database'
   
if __name__ == '__main__':
    app.run()
