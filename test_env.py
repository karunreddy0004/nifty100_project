from dotenv import load_dotenv
import os

load_dotenv()

print("Database:", os.getenv("DB_NAME"))
print("Data Path:", os.getenv("DATA_PATH"))
print("Output Path:", os.getenv("OUTPUT_PATH"))