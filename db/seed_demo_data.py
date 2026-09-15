import pandas as pd
import requests
import time

df = pd.read_csv("../data/creditcard.csv")

# Get a mix: 15 normal transactions, 10 fraud transactions
normal_sample = df[df["Class"] == 0].sample(15, random_state=1)
fraud_sample = df[df["Class"] == 1].sample(10, random_state=1)

# Combine and shuffle them so it doesn't look artificially ordered
combined = pd.concat([normal_sample, fraud_sample]).sample(frac=1, random_state=2)

sent = 0
flagged = 0

for _, row in combined.iterrows():
    transaction_data = row.drop("Class").to_dict()
    try:
        response = requests.post(
            "http://127.0.0.1:8000/score-transaction",
            json=transaction_data
        )
        result = response.json()
        sent += 1
        if result.get("is_flagged"):
            flagged += 1
        print(f"Sent transaction -> fraud_score: {result.get('fraud_score'):.2f}, flagged: {result.get('is_flagged')}")
    except Exception as e:
        print(f"Error sending transaction: {e}")
    time.sleep(0.2)  # small delay so it doesn't hammer the API instantly

print(f"\n✅ Done. Sent {sent} transactions, {flagged} were flagged as fraud.")
