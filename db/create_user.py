from passlib.context import CryptContext
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

name = "Test Investigator"
email = "investigator@test.com"
plain_password = "test1234"
role = "investigator"

hashed_password = pwd_context.hash(plain_password)

conn = get_db_connection()
cursor = conn.cursor()
cursor.execute(
    "INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
    (name, email, hashed_password, role)
)
conn.commit()
cursor.close()
conn.close()

print(f"✅ User created: {email} / password: {plain_password}")