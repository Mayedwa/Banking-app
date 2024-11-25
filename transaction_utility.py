import json
import os

# File paths for storing data
USER_DATABASE = "users.txt"
TRANSACTION_DATABASE = "transactions.txt"

# Utility functions
def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

def load_data(file):
    if not os.path.exists(file):
        return {}
    try:
        with open(file, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

# Load user and transaction data
users = load_data(USER_DATABASE)
transactions = load_data(TRANSACTION_DATABASE)
