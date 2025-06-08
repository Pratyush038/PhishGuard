from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from feature_extractor import extract_features_from_url
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Load models
try:
    rf_model = joblib.load("rf_model.pkl")
    xgb_model = joblib.load("xgb_model.pkl")
except Exception as e:
    raise RuntimeError(f"Error loading models: {e}")

# Enable CORS for local dev + deployed frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["phish-guard-ow2mumwfc-pratyush038s-projects.vercel.app",
    "phish-guard-prb.vercel.app",
    "https://phish-guard-pratyush038s-projects.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class URLInput(BaseModel):
    url: str
@app.post("/predict_from_url")
def predict_from_url(data: URLInput):
    print(f"Received URL: {data.url}")  # Debug log

    try:
        features = extract_features_from_url(data.url)
        arr = np.array(features).reshape(1, -1)
        prediction = xgb_model.predict(arr)
        print(f"Prediction: {prediction[0]}")  # Debug log
        return {"prediction": int(prediction[0])}
    except Exception as e:
        print(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/predict_from_url")
def predict_from_url(data: URLInput):
    try:
        features = extract_features_from_url(data.url)
        arr = np.array(features).reshape(1, -1)
        prediction = xgb_model.predict(arr)
        return {"prediction": int(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
