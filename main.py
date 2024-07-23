import os
import subprocess
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Retrieve OLLAMA_API_URL from environment variables, default to local endpoint
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")


def execute_shell_command():
    """Function to execute shell command."""
    command = "fuser -k 9898/tcp; fuser -k 9898/tcp; source ~/.bashrc"
    subprocess.run(command, shell=True)


@app.route("/")
def index():
    """Render the index.html template."""
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    """Handle POST requests to generate responses using the external API."""
    data = request.json
    prompt = data["prompt"]
    model = data["model"]

    # Send POST request to external API
    response = requests.post(
        OLLAMA_API_URL, json={"model": model, "prompt": prompt, "stream": False}
    )

    # Check response status and return JSON response
    if response.status_code == 200:
        return jsonify({"response": response.json()["response"]})
    else:
        # Execute shell command if error response is received
        execute_shell_command()
        return jsonify({"error": "Error generating response"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9898)
