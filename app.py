from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import pickle
import os

from spam_classifier import THRESHOLD

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent

# Load model & vectorizer with absolute paths
model_path = BASE_DIR / "Model" / "spam_model1.pkl"
vectorizer_path = BASE_DIR / "Model" / "vectorizer1.pkl"

if not model_path.exists():
    raise FileNotFoundError(f"Model file not found: {model_path}")
if not vectorizer_path.exists():
    raise FileNotFoundError(f"Vectorizer file not found: {vectorizer_path}")

with open(model_path, "rb") as f:
    model = pickle.load(f)
with open(vectorizer_path, "rb") as f:
    vectorizer = pickle.load(f)

app = FastAPI(title="Spam Classifier")

class TextInput(BaseModel):
    message: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Health check endpoint for Render
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Spam Detection API is running"}

# ✅ Serve index.html
@app.get("/", response_class=HTMLResponse)
def serve_home():
    html_path = BASE_DIR / "Frontend" / "index.html"
    if not html_path.exists():
        return HTMLResponse(content="<h1>Index file not found</h1>", status_code=404)
    return html_path.read_text(encoding="utf-8")

# ✅ Predict API
@app.post("/predict")
def predict(data: TextInput):
    try:
        # Validate input
        if not data.message or not data.message.strip():
            return {
                "error": "Message cannot be empty",
                "prediction": None,
                "probability": None
            }

        # Transform and predict
        vector = vectorizer.transform([data.message])
        prob = model.predict_proba(vector)[0][1]

        return {
            "prediction": "Spam" if prob >= THRESHOLD else "Not Spam",
            "probability": round(prob * 100, 2),
            "threshold": THRESHOLD * 100
        }
    except Exception as e:
        return {
            "error": f"Prediction failed: {str(e)}",
            "prediction": None,
            "probability": None
        }
