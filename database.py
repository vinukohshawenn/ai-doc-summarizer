import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Replace 'my_password' with your actual Postgres password
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL" , "postgresql://postgres:password@localhost/summary_app")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()