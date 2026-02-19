from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pickle

from spam_classifier import THRESHOLD

# Load model and vectorizer

model = pickle.load(open("Model/spam_model1.pkl", "rb"))
vectorizer = pickle.load(open("Model/vectorizer1.pkl", "rb"))

app = FastAPI(title="Spam Email Classifier App")

class EmailInput(BaseModel):
    message: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/", response_class=HTMLResponse)
def home():
    html_file = Path("frontend/index.html")
    return html_file.read_text()

@app.post("/predict")
def predict_spam(data: EmailInput):
    message_vector = vectorizer.transform([data.message])

    spam_proba = model.predict_proba(message_vector)[0][1]
    spam_percent = round(spam_proba * 100, 2)

    prediction = "Spam" if spam_proba >= THRESHOLD else "Not Spam"

    return {"prediction": prediction,
            "probability": spam_percent
    }