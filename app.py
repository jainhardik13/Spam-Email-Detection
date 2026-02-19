from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import pickle

from spam_classifier import THRESHOLD

# Load model & vectorizer
model = pickle.load(open("Model/spam_model1.pkl", "rb"))
vectorizer = pickle.load(open("Model/vectorizer1.pkl", "rb"))

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

# ✅ Serve index.html
@app.get("/", response_class=HTMLResponse)
def serve_home():
    return Path("frontend/index.html").read_text(encoding="utf-8")

# ✅ Predict API
@app.post("/predict")
def predict(data: TextInput):
    vector = vectorizer.transform([data.message])
    prob = model.predict_proba(vector)[0][1]

    return {
        "prediction": "Spam" if prob >= THRESHOLD else "Not Spam",
        "probability": round(prob * 100, 2)
    }
