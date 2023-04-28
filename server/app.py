from flask import Flask, request, jsonify
import subprocess
from flask_cors import CORS
import os
from flask import send_from_directory

app = Flask(__name__)
CORS(app)

@app.route('/execute', methods=['POST'])
def execute_code():
    # Check if the request body contains valid JSON
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    # Get the JSON data from the request body
    data = request.get_json()

    # Check if the 'code' key is present in the JSON data
    if 'code' not in data:
        return jsonify({"error": "Missing 'code' in request body"}), 400

    code = data['code']
    try:
        output = subprocess.check_output(["python", "-c", code], text=True)
        return jsonify({"output": output})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)})


@app.route('/openapi.yaml')
def serve_openapi_yaml():
    return send_from_directory(".", 'openapi.yaml')

@app.route('/logo.png')
def logo_png():
    return send_from_directory('..', 'logo.png')

@app.route('/.well-known/ai-plugin.json')
def ai_plugin_json():
    return send_from_directory('../.well-known', 'ai-plugin.json')


if __name__ == "__main__":
    app.run(port=3333)
