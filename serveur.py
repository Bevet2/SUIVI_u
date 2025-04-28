from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# Le chemin absolu du dossier où est ce script (serveur.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'schema.html')

@app.route('/data_articles.json')
def data():
    return send_from_directory(BASE_DIR, 'data_articles.json')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
