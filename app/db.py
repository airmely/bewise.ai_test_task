from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    'postgresql://myuser:mypassword@postgres:5432/mydatabase'
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
