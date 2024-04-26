from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres.ercglawggazednslkocb:596djmgcg16NjRN4@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

try:
    engine.connect().close()
    print("Database connection successful.")
except Exception as e:
    print("Error connecting to the database:", e)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()