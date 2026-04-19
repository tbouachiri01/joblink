import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
print(f"BASE_DIR: {BASE_DIR}")

env_path = os.path.join(BASE_DIR, '.env')
print(f"Chemin du .env: {env_path}")
print(f"Le fichier .env existe? {os.path.exists(env_path)}")

load_dotenv(env_path)

print(f"\nDB_NAME: {os.getenv('DB_NAME')}")
print(f"DB_USER: {os.getenv('DB_USER')}")
print(f"DB_PASSWORD: {os.getenv('DB_PASSWORD')}")
print(f"DB_HOST: {os.getenv('DB_HOST')}")
print(f"DB_PORT: {os.getenv('DB_PORT')}")