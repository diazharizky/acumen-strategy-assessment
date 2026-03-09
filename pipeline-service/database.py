import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

db_user = os.getenv('DB_USER', 'postgres')
db_password = os.getenv('DB_PASSWORD', 'password')
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')
db_name = os.getenv('DB_NAME', 'customer_db')

DSN = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=create_engine(DSN),
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
