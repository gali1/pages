"""
Flask application for handling requests to generate responses using an external API.

This application provides an endpoint '/generate' that accepts POST requests with JSON data
containing 'prompt' and 'model' parameters. It then sends a request to an external API specified
by OLLAMA_API_URL to generate a response based on the provided prompt and model.

Dependencies:
- Flask: Web framework for handling HTTP requests and responses.
- requests: Library for making HTTP requests to the external API.
- python-dotenv: Library for reading environment variables from a .env file.

Usage:
- Ensure Flask and other dependencies are installed (`pip install flask requests python-dotenv`).
- Set the OLLAMA_API_URL environment variable to specify the external API endpoint.

Endpoints:
- '/' (GET): Renders the index.html template.
- '/generate' (POST): Accepts JSON data with 'prompt' and 'model' fields, sends a request to
  OLLAMA_API_URL, and returns the generated response.

Example:
curl -X POST http://localhost:8080/generate -H "Content-Type: application/json" \
-d '{"prompt": "Your prompt text here", "model": "Model name here"}'

"""

import os
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Retrieve OLLAMA_API_URL from environment variables, default to local endpoint
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://localhost:11434/api/generate')

@app.route('/')
def index():
    """Render the index.html template."""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Handle POST requests to generate responses using the external API."""
    try:
        data = request.json
        prompt = data.get('prompt', '')
        model = data.get('model', '')

        if not prompt or not model:
            raise ValueError("Prompt and model fields are required.")

        # Send POST request to external API
        response = requests.post(OLLAMA_API_URL, json={
            'model': model,
            'prompt': prompt,
            'stream': False
        })

        # Check response status and return JSON response
        response.raise_for_status()  # Raise HTTPError for bad responses

        return jsonify({'response': response.json().get('response', '')})

    except (requests.RequestException, ValueError) as e:
        return jsonify({'error': str(e)}), 400  # Return 400 for client errors

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9898)
