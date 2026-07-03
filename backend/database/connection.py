from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

print("Database URL found:", DATABASE_URL is not None)

engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    print("✅ Connected to Supabase PostgreSQL")