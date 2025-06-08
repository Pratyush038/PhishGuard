import os
print("Current working directory:", os.getcwd())
print("Files in working directory:", os.listdir('.'))


from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from feature_extractor import extract_features_from_url
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

rf_model = joblib.load("rf_model.pkl")
xgb_model = joblib.load("xgb_model.pkl")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or "*" for all origins (less secure)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLInput(BaseModel):
    url: str

@app.post("/predict_from_url")
def predict_from_url(data: URLInput):
    features = extract_features_from_url(data.url)
    arr = np.array(features).reshape(1, -1)
    prediction = xgb_model.predict(arr)
    return {"prediction": int(prediction[0])}
