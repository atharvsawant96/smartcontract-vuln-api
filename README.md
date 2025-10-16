# Smart Contract Vulnerability API (Production-ready scaffold)

Replace the placeholder `.pkl` files in `models/` with your real artifacts:
- `models/best_model.pkl`    -> Trained sklearn estimator or pipeline
- `models/vectorizer.pkl`    -> Fitted TF-IDF vectorizer
- `models/labels_map.pkl`    -> dict mapping numeric labels to strings

## Run locally (development)
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate    # Windows
pip install -r requirements.txt
python app.py

## Production (example using gunicorn)
gunicorn -w 4 -b 0.0.0.0:$PORT app:app

## Docker
Build and run:
docker build -t sc-vuln-api .
docker run -p 5000:5000 sc-vuln-api