from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import mysql.connector
from dotenv import load_dotenv
import os
import pandas as pd



app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

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
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/login")
def login(credentials: LoginRequest):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email = %s", (credentials.email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return {"success": False, "message": "User not found"}

    if not pwd_context.verify(credentials.password, user["password_hash"]):
        return {"success": False, "message": "Incorrect password"}

    return {
        "success": True,
        "user_id": user["user_id"],
        "name": user["name"],
        "role": user["role"]
    }
@app.get("/flagged-cases")
def get_flagged_cases():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT fc.case_id, fc.transaction_id, fc.reason, fc.status, fc.created_at,
               t.amount, t.fraud_score
        FROM flagged_cases fc
        JOIN transactions t ON fc.transaction_id = t.transaction_id
        ORDER BY fc.created_at DESC
    """)
    cases = cursor.fetchall()

    cursor.close()
    conn.close()

    return cases


class ActionRequest(BaseModel):
    case_id: int
    user_id: int
    decision: str  # "approved" or "rejected"
    notes: str = ""

@app.post("/investigator-action")
def investigator_action(action: ActionRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Log the investigator's decision
    cursor.execute(
        "INSERT INTO investigator_actions (case_id, user_id, decision, notes) VALUES (%s, %s, %s, %s)",
        (action.case_id, action.user_id, action.decision, action.notes)
    )

    # Update the case status too
    cursor.execute(
        "UPDATE flagged_cases SET status = %s WHERE case_id = %s",
        (action.decision, action.case_id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return {"success": True, "message": f"Case {action.case_id} marked as {action.decision}"}