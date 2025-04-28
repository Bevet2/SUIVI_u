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
    port = int(os.environ.get('PORT', 5000))  # <- Prendre le port imposé par Railway
    app.run(host='0.0.0.0', port=port, debug=True)  # <- Écouter toutes les adresses (0.0.0.0)
