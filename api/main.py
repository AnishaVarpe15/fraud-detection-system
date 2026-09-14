from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import mysql.connector
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

app = FastAPI()

# Load the trained model once, when the server starts
model = joblib.load("../model/fraud_model.pkl")

# Define what a transaction request should look like
class Transaction(BaseModel):
    Time: float
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float
    Amount: float

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

@app.post("/score-transaction")
def score_transaction(transaction: Transaction):
    # Convert incoming data into the format the model expects
    input_data = pd.DataFrame([transaction.dict()])

    # Get prediction: 1 = fraud, 0 = normal
    prediction = model.predict(input_data)[0]
    fraud_score = model.predict_proba(input_data)[0][1]  # probability of fraud

    is_flagged = bool(prediction == 1)

    # Save this transaction to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO transactions (amount, transaction_time, fraud_score, is_flagged) VALUES (%s, %s, %s, %s)",
        (transaction.Amount, "2026-01-01 00:00:00", float(fraud_score), is_flagged)
    )
    transaction_id = cursor.lastrowid

    # If flagged, also create a flagged case
    if is_flagged:
        reason = f"Model flagged this transaction with fraud probability {fraud_score:.2f}"
        cursor.execute(
            "INSERT INTO flagged_cases (transaction_id, reason) VALUES (%s, %s)",
            (transaction_id, reason)
        )

    conn.commit()
    cursor.close()
    conn.close()

    return {
        "transaction_id": transaction_id,
        "fraud_score": fraud_score,
        "is_flagged": is_flagged
    }