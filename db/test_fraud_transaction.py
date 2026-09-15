import pandas as pd
import requests

# Load the dataset
df = pd.read_csv("../data/creditcard.csv")

# Get only fraud rows
fraud_rows = df[df["Class"] == 1]

# Pick one fraud row (let's take the 5th one, index 4, so we get variety)
sample = fraud_rows.iloc[4]

# Convert it into the format your API expects (drop the Class column)
transaction_data = sample.drop("Class").to_dict()

print("Sending this transaction:")
print(transaction_data)

# Send it to your running API
response = requests.post(
    "http://127.0.0.1:8000/score-transaction",
    json=transaction_data
)

print("\nAPI Response:")
print(response.json())