import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from billboard_engine import run_analysis_engine

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        result = run_analysis_engine(filepath)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Server starting... Models may take a moment to load in the background.")
    app.run(debug=True, port=5000)