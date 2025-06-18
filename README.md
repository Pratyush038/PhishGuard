# PhishGuard

PhishGuard is a full-stack phishing detection system that leverages machine learning for accurate URL classification. The backend is powered by FastAPI and trained models, while the frontend is built with Next.js and styled using shadcn/ui and Tailwind CSS.

---

## Project Structure

```text
PhishGuard/
├── phishing-backend/           # Machine learning API and utilities
│   ├── app.py                  # Optional Streamlit interface
│   ├── main.ipynb              # Feature exploration and modeling notebook
│   ├── feature_extractor.py   # Functions for extracting URL features
│   ├── test_features.py        # Unit tests for feature extraction
│   ├── rf_model.pkl            # Trained Random Forest model
│   ├── xgb_model.pkl           # Trained XGBoost model
│   ├── phishing.csv            # Dataset for training/testing
│   ├── requirements.txt        # Python dependencies
│   ├── runtime.txt             # Python runtime version (for deployment)
│   └── Procfile                # Deployment entrypoint for backend
│
├── phishing-frontend/          # Frontend built with Next.js + shadcn/ui
│   ├── src/                    # Source directory (components, pages)
│   ├── public/                 # Static assets
│   ├── package.json            # NPM project definition
│   ├── next.config.ts          # Next.js configuration
│   ├── tsconfig.json           # TypeScript config
│   ├── postcss.config.mjs      # Tailwind PostCSS config
│   └── eslint.config.mjs       # ESLint rules
│
└── .gitignore                  # Git ignored files
```
---

## Features

### Backend
- FastAPI-based REST API
- Trained models: Random Forest and XGBoost (stored as `.pkl`)
- Feature extraction module for URL analysis
- Notebook for EDA, model evaluation, and visualization
- Compatible with Heroku deployment (Procfile and runtime.txt included)

### Frontend
- Built using Next.js 14 with TypeScript
- Modern, minimal UI styled with Tailwind CSS and shadcn/ui
- Client-side form for URL input and result display
- Integrated with backend via REST API

---

## Models

Two models are included:

- `rf_model.pkl`: Random Forest classifier trained on URL-based features
- `xgb_model.pkl`: XGBoost classifier trained with tuned hyperparameters

Both are evaluated on the same dataset and exposed via FastAPI endpoints.

---

## Setup Instructions

### Backend

1. Navigate to the backend folder:
cd phishing-backend

2. Create a virtual environment and activate it:
python -m venv venv
#### macOS/Linux:
source venv/bin/activate
#### Windows:
venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

5. Run the API:
uvicorn feature_extractor:app --reload

### Frontend

1. Navigate to the frontend folder:
cd phishing-frontend
2. Install dependencies:
npm install
3. Run the development server:
npm run dev

---

## Dataset

The dataset used is `phishing.csv`, containing labeled URLs with extracted features such as:

- URL length
- Number of dots and special characters
- Presence of HTTPS
- Domain age
- IP address usage

---

## API Endpoints

Sample endpoint for URL classification:

POST /predict
Body: {
"url": "http://example.com/login"
}
Response: {
"prediction": "phishing",
"model": "Random Forest"
}

---

## Future Improvements

- Integration of deep learning model for higher accuracy
- Real-time blacklist and domain reputation checks
- Browser extension to use the model on live websites
- CI/CD pipeline for automated deployment and testing
- Enhanced URL feature set (e.g., WHOIS data, SSL certificate metadata)

---
