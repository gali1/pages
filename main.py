import os
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://localhost:11434/api/generate')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data['prompt']
    model = data['model']

    response = requests.post(OLLAMA_API_URL, json={
        'model': model,
        'prompt': prompt,
        'stream': False
    })

    if response.status_code == 200:
        return jsonify({'response': response.json()['response']})
    else:
        return jsonify({'error': 'Failed to generate response'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
