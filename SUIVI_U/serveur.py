from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'schema.html')

@app.route('/data_articles.json')
def data():
    return send_from_directory('.', 'data_articles.json')

if __name__ == '__main__':
    # Par défaut sur http://localhost:5000
    app.run(debug=True)
