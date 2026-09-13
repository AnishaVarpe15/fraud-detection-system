import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()  # reads the .env file

connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

if connection.is_connected():
    print("✅ Successfully connected to MySQL database!")
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES;")
    print("Tables in database:")
    for table in cursor:
        print(table)
    cursor.close()
    connection.close()
else:
    print("❌ Connection failed.")