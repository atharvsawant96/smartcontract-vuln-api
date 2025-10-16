from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
from scipy.sparse import hstack
import re
import os
from utils.cleaner import clean_code
from utils.feature_extractor import extract_keyword_features

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "best_model.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.pkl")
LABELS_PATH = os.path.join(MODEL_DIR, "labels_map.pkl")

# Load artifacts
def safe_load(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Required file not found: {path}")
    with open(path, "rb") as f:
        return pickle.load(f)

try:
    model = safe_load(MODEL_PATH)
    vectorizer = safe_load(VECTORIZER_PATH)
    labels_map = safe_load(LABELS_PATH)
except Exception as e:
    model = None
    vectorizer = None
    labels_map = None
    LOAD_ERROR = str(e)
else:
    LOAD_ERROR = None

def predict_vulnerability_internal(new_code):
    if LOAD_ERROR:
        raise RuntimeError(f"Model artifacts not loaded: {LOAD_ERROR}")
    cleaned_code = clean_code(new_code)
    code_tfidf = vectorizer.transform([cleaned_code])
    code_keyword_features = extract_keyword_features(cleaned_code).to_frame().T
    code_keyword_features_sparse = code_keyword_features.astype(pd.SparseDtype("int", 0)).sparse.to_coo()
    combined_features = hstack([code_tfidf, code_keyword_features_sparse])
    predicted_label_code = model.predict(combined_features)[0]
    predicted_vulnerability = labels_map.get(predicted_label_code, str(predicted_label_code))
    return predicted_vulnerability

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "*"}})  # Allow all origins; restrict in production

@app.route("/health", methods=["GET"])
def health():
    status = {"status": "ok" if not LOAD_ERROR else "error", "model_loaded": LOAD_ERROR is None}
    if LOAD_ERROR:
        status["load_error"] = LOAD_ERROR
    return jsonify(status), 200 if LOAD_ERROR is None else 503

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)
        code_input = data.get("code", "")
        if not isinstance(code_input, str) or not code_input.strip():
            return jsonify({"error": "No Solidity code provided in 'code' field"}), 400
        prediction = predict_vulnerability_internal(code_input)
        # Convert single prediction to array format
        result = {
            "vulnerabilityPrediction": {
                "predictions": [prediction],  # Wrap in array
                "confidence": 0.95,  # Example confidence
                "message": f"Analyzed code: {code_input[:50]}..."  # Truncate for brevity
            }
        }
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)