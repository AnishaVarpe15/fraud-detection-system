# Real-Time Transaction Fraud Detection & Risk Scoring System

A full-stack system that scores incoming transactions for fraud risk in real time, flags suspicious ones for human review, and gives investigators a dashboard to approve or reject flagged cases — with a full audit trail.

## Why this project

Fraud detection is a core problem in banking and fintech. Rather than building just a classification model in a notebook, this project wraps a trained ML model in a real system: a database, an API, and a working investigator dashboard — mirroring how fraud-ops tooling actually works in production.

## Tech Stack

- **Model:** Python, scikit-learn (Random Forest)
- **Backend:** FastAPI, MySQL
- **Frontend:** React (Vite), Axios
- **Dataset:** [Kaggle Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)

## Features

- Real-time transaction scoring via `/score-transaction`
- Investigator login (bcrypt password hashing)
- Dashboard showing all flagged cases with fraud scores and plain-language reasons
- Approve/Reject workflow with a full audit trail (`investigator_actions` table)
- Model achieves 92% precision / 74% recall on the fraud class (baseline Random Forest)

## Architecture
React Dashboard → FastAPI Backend → MySQL Database
                        ↓
                Trained ML Model (fraud_model.pkl)

## Database Schema

- `users` — investigators/admins with role-based access
- `transactions` — every transaction scored
- `flagged_cases` — transactions flagged for review, with reason and status
- `investigator_actions` — audit trail of every approve/reject decision

## Running Locally

**Backend:**
```bash
cd model
python train_model.py     # trains and saves the model
cd ../api
uvicorn main:app --reload
```

**Frontend:**
```bash
cd dashboard
npm install
npm run dev
```

Requires a local MySQL instance with the schema set up (see `db/` for connection setup) and a `.env` file with your database credentials.

## What I'd improve next

- JWT-based authentication instead of plain login
- Threshold tuning for better fraud recall
- Interpretability for anonymized (PCA) features using SHAP values